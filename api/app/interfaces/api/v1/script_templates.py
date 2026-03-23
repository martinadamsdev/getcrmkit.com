import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.auth.entities import User
from app.domain.follow_up.entities import ScriptTemplate
from app.domain.follow_up.enums import ScriptScene
from app.domain.follow_up.exceptions import (
    ScriptTemplateNotFoundError,
    ScriptTemplateTitleRequiredError,
    SystemTemplateCannotBeDeletedError,
)
from app.domain.follow_up.services import ScriptTemplateService
from app.interfaces.api.deps import get_current_user, get_db, get_script_template_service
from app.interfaces.schemas.script_template import (
    CreateScriptTemplateRequest,
    ScriptTemplateResponse,
    UpdateScriptTemplateRequest,
)

router = APIRouter(prefix="/api/v1/script-templates", tags=["script-templates"])


def _template_response(t: ScriptTemplate) -> ScriptTemplateResponse:
    return ScriptTemplateResponse(
        id=t.id,
        scene=t.scene.value,
        title=t.title,
        content=t.content,
        language=t.language,
        position=t.position,
        is_system=t.is_system,
        created_at=t.created_at,
        updated_at=t.updated_at,
    )


@router.get("", response_model=list[ScriptTemplateResponse])
async def list_templates(
    scene: str | None = None,
    current_user: User = Depends(get_current_user),
    service: ScriptTemplateService = Depends(get_script_template_service),
) -> list[ScriptTemplateResponse]:
    templates = await service.get_all(current_user.tenant_id, scene=scene)
    return [_template_response(t) for t in templates]


@router.post("", response_model=ScriptTemplateResponse, status_code=201)
async def create_template(
    body: CreateScriptTemplateRequest,
    current_user: User = Depends(get_current_user),
    service: ScriptTemplateService = Depends(get_script_template_service),
    session: AsyncSession = Depends(get_db),
) -> ScriptTemplateResponse:
    try:
        template = await service.create_template(
            scene=ScriptScene(body.scene),
            title=body.title,
            content=body.content,
            tenant_id=current_user.tenant_id,
            created_by=current_user.id,
            language=body.language,
            position=body.position,
        )
        await session.commit()
        return _template_response(template)
    except ScriptTemplateTitleRequiredError as e:
        raise HTTPException(status_code=422, detail={"code": e.code, "message": e.message}) from e


@router.put("/{template_id}", response_model=ScriptTemplateResponse)
async def update_template(
    template_id: uuid.UUID,
    body: UpdateScriptTemplateRequest,
    current_user: User = Depends(get_current_user),
    service: ScriptTemplateService = Depends(get_script_template_service),
    session: AsyncSession = Depends(get_db),
) -> ScriptTemplateResponse:
    try:
        updates = body.model_dump(exclude_unset=True)
        template = await service.update_template(
            tenant_id=current_user.tenant_id,
            template_id=template_id,
            **updates,
        )
        await session.commit()
        return _template_response(template)
    except ScriptTemplateNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e


@router.delete("/{template_id}", status_code=204)
async def delete_template(
    template_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: ScriptTemplateService = Depends(get_script_template_service),
    session: AsyncSession = Depends(get_db),
) -> None:
    try:
        await service.delete_template(
            tenant_id=current_user.tenant_id,
            template_id=template_id,
        )
        await session.commit()
    except ScriptTemplateNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e
    except SystemTemplateCannotBeDeletedError as e:
        raise HTTPException(status_code=403, detail={"code": e.code, "message": e.message}) from e
