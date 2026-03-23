import uuid
from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.application.customer.export_service import CustomerExportService
from app.application.customer.import_service import CustomerImportService
from app.application.customer.queries import Customer360QueryService
from app.application.follow_up.commands import CreateFollowUpHandler
from app.application.shared.task_queue import AbstractTaskQueue
from app.application.shared.unit_of_work import AbstractUnitOfWork
from app.config.settings import Settings, get_settings
from app.domain.auth.entities import User
from app.domain.auth.services import AuthConfig, AuthService
from app.domain.auth.value_objects import Token
from app.domain.customer.services import (
    ContactService,
    CustomerGradeService,
    CustomerService,
    DuplicateChecker,
    SavedViewService,
    TagService,
)
from app.domain.follow_up.services import FollowUpService, ScriptTemplateService
from app.domain.product.services import (
    CustomizationOptionService,
    PricingService,
    PricingTierService,
    ProductCategoryService,
    ProductService,
    ProductVariantService,
)
from app.infra.auth.token_blacklist import TokenBlacklist
from app.infra.cache.redis_client import redis_client
from app.infra.database.connection import async_session_factory, engine
from app.infra.database.repositories.customer_repository import (
    ContactRepository,
    CustomerGradeRepository,
    CustomerRepository,
    TagRepository,
)
from app.infra.database.repositories.customization_option_repository import CustomizationOptionRepository
from app.infra.database.repositories.data_job_repository import DataJobRepository
from app.infra.database.repositories.follow_up_repository import FollowUpRepository, ScriptTemplateRepository
from app.infra.database.repositories.pricing_tier_repository import PricingTierRepository
from app.infra.database.repositories.product_category_repository import ProductCategoryRepository
from app.infra.database.repositories.product_repository import ProductRepository
from app.infra.database.repositories.product_variant_repository import ProductVariantRepository
from app.infra.database.repositories.saved_view_repository import SavedViewRepository
from app.infra.database.repositories.user_repository import UserRepository
from app.infra.database.unit_of_work import SqlAlchemyUnitOfWork
from app.infra.queue import task_queue

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with async_session_factory() as session:
        yield session


async def get_uow() -> AsyncGenerator[AbstractUnitOfWork]:
    async with SqlAlchemyUnitOfWork() as uow:
        yield uow


def get_engine() -> AsyncEngine:
    return engine


def get_redis() -> Redis:
    return redis_client


def get_task_queue() -> AbstractTaskQueue:
    return task_queue


def get_token_blacklist(redis: Redis = Depends(get_redis)) -> TokenBlacklist:
    return TokenBlacklist(redis)


def get_auth_config(settings: Settings = Depends(get_settings)) -> AuthConfig:
    return AuthConfig(
        jwt_secret_key=settings.jwt_secret_key,
        jwt_algorithm=settings.jwt_algorithm,
        access_token_expire_minutes=settings.jwt_access_token_expire_minutes,
        refresh_token_expire_days=settings.jwt_refresh_token_expire_days,
        refresh_token_short_expire_hours=settings.jwt_refresh_token_short_expire_hours,
        password_min_length=settings.password_min_length,
    )


def get_auth_service(
    session: AsyncSession = Depends(get_db),
    blacklist: TokenBlacklist = Depends(get_token_blacklist),
    config: AuthConfig = Depends(get_auth_config),
) -> AuthService:
    repo = UserRepository(session)
    return AuthService(user_repo=repo, token_blacklist=blacklist, config=config)


async def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
    settings: Settings = Depends(get_settings),
) -> User:
    if token is None:
        raise HTTPException(status_code=401, detail={"code": "INVALID_TOKEN", "message": "Not authenticated"})

    from app.domain.auth.exceptions import AuthenticationError

    try:
        payload = Token.decode(token, settings.jwt_secret_key, settings.jwt_algorithm)
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail={"code": "INVALID_TOKEN", "message": e.message}) from e

    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail={"code": "INVALID_TOKEN", "message": "Invalid token type"})

    blacklist = TokenBlacklist(redis)
    jti = payload.get("jti", "")
    if await blacklist.is_blacklisted(jti):
        raise HTTPException(status_code=401, detail={"code": "INVALID_TOKEN", "message": "Token has been revoked"})

    repo = UserRepository(session)
    user = await repo.get_by_id(uuid.UUID(payload["sub"]))
    if user is None:
        raise HTTPException(status_code=401, detail={"code": "INVALID_TOKEN", "message": "User not found"})
    if not user.is_active:
        raise HTTPException(status_code=403, detail={"code": "USER_INACTIVE", "message": "Account is inactive"})

    return user


def get_grade_service(session: AsyncSession = Depends(get_db)) -> CustomerGradeService:
    grade_repo = CustomerGradeRepository(session)
    customer_repo = CustomerRepository(session)
    return CustomerGradeService(grade_repo=grade_repo, customer_repo=customer_repo)


def get_customer_service(session: AsyncSession = Depends(get_db)) -> CustomerService:
    return CustomerService(customer_repo=CustomerRepository(session))


def get_contact_service(session: AsyncSession = Depends(get_db)) -> ContactService:
    return ContactService(
        contact_repo=ContactRepository(session),
        customer_repo=CustomerRepository(session),
    )


def get_tag_service(session: AsyncSession = Depends(get_db)) -> TagService:
    return TagService(tag_repo=TagRepository(session))


def get_duplicate_checker(session: AsyncSession = Depends(get_db)) -> DuplicateChecker:
    return DuplicateChecker(customer_repo=CustomerRepository(session))


def get_360_query_service(session: AsyncSession = Depends(get_db)) -> Customer360QueryService:
    return Customer360QueryService(
        customer_repo=CustomerRepository(session),
        contact_repo=ContactRepository(session),
        grade_repo=CustomerGradeRepository(session),
        tag_repo=TagRepository(session),
    )


def get_saved_view_service(session: AsyncSession = Depends(get_db)) -> SavedViewService:
    return SavedViewService(repo=SavedViewRepository(session))


def get_data_job_repo(session: AsyncSession = Depends(get_db)) -> DataJobRepository:
    return DataJobRepository(session)


def get_import_service(
    session: AsyncSession = Depends(get_db),
    task_queue_dep: AbstractTaskQueue = Depends(get_task_queue),
) -> CustomerImportService:
    return CustomerImportService(
        job_repo=DataJobRepository(session),
        customer_repo=CustomerRepository(session),
        contact_repo=ContactRepository(session),
        duplicate_checker=DuplicateChecker(customer_repo=CustomerRepository(session)),
        task_queue=task_queue_dep,
    )


def get_export_service(
    session: AsyncSession = Depends(get_db),
    task_queue_dep: AbstractTaskQueue = Depends(get_task_queue),
) -> CustomerExportService:
    return CustomerExportService(
        job_repo=DataJobRepository(session),
        customer_repo=CustomerRepository(session),
        contact_repo=ContactRepository(session),
        grade_repo=CustomerGradeRepository(session),
        task_queue=task_queue_dep,
    )


def get_follow_up_service(session: AsyncSession = Depends(get_db)) -> FollowUpService:
    return FollowUpService(follow_up_repo=FollowUpRepository(session))


def get_follow_up_handler(session: AsyncSession = Depends(get_db)) -> CreateFollowUpHandler:
    return CreateFollowUpHandler(
        follow_up_service=FollowUpService(follow_up_repo=FollowUpRepository(session)),
        customer_repo=CustomerRepository(session),
    )


def get_script_template_service(session: AsyncSession = Depends(get_db)) -> ScriptTemplateService:
    return ScriptTemplateService(template_repo=ScriptTemplateRepository(session))


# --- Product ---


def get_product_service(session: AsyncSession = Depends(get_db)) -> ProductService:
    return ProductService(product_repo=ProductRepository(session))


def get_product_variant_service(session: AsyncSession = Depends(get_db)) -> ProductVariantService:
    return ProductVariantService(
        variant_repo=ProductVariantRepository(session),
        product_repo=ProductRepository(session),
    )


def get_product_category_service(session: AsyncSession = Depends(get_db)) -> ProductCategoryService:
    return ProductCategoryService(category_repo=ProductCategoryRepository(session))


def get_pricing_tier_service(session: AsyncSession = Depends(get_db)) -> PricingTierService:
    return PricingTierService(pricing_tier_repo=PricingTierRepository(session))


def get_pricing_service(session: AsyncSession = Depends(get_db)) -> PricingService:
    return PricingService(pricing_tier_repo=PricingTierRepository(session))


def get_customization_option_service(session: AsyncSession = Depends(get_db)) -> CustomizationOptionService:
    return CustomizationOptionService(option_repo=CustomizationOptionRepository(session))
