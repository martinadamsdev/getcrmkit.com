import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.auth.entities import User
from app.domain.customer.entities import Contact
from app.domain.customer.exceptions import ContactNotFoundError, CustomerNotFoundError
from app.domain.customer.services import ContactService
from app.interfaces.api.deps import get_contact_service, get_current_user, get_db
from app.interfaces.schemas.customer import (
    ContactResponse,
    CreateContactRequest,
    UpdateContactRequest,
)

router = APIRouter(prefix="/api/v1", tags=["contacts"])


def _contact_response(contact: Contact) -> ContactResponse:
    return ContactResponse(
        id=contact.id,
        customer_id=contact.customer_id,
        name=contact.name,
        title=contact.title,
        email=contact.email,
        phone=contact.phone,
        whatsapp=contact.whatsapp,
        skype=contact.skype,
        linkedin=contact.linkedin,
        wechat=contact.wechat,
        is_primary=contact.is_primary,
        notes=contact.notes,
        custom_fields=contact.custom_fields,
        created_at=contact.created_at,
        updated_at=contact.updated_at,
    )


@router.get("/customers/{customer_id}/contacts", response_model=list[ContactResponse])
async def list_contacts(
    customer_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: ContactService = Depends(get_contact_service),
) -> list[ContactResponse]:
    contacts = await service.list_contacts(current_user.tenant_id, customer_id)
    return [_contact_response(c) for c in contacts]


@router.post("/customers/{customer_id}/contacts", response_model=ContactResponse, status_code=201)
async def create_contact(
    customer_id: uuid.UUID,
    body: CreateContactRequest,
    current_user: User = Depends(get_current_user),
    service: ContactService = Depends(get_contact_service),
    session: AsyncSession = Depends(get_db),
) -> ContactResponse:
    try:
        contact = await service.create_contact(
            customer_id=customer_id,
            name=body.name,
            tenant_id=current_user.tenant_id,
            created_by=current_user.id,
            title=body.title,
            email=body.email,
            phone=body.phone,
            whatsapp=body.whatsapp,
            skype=body.skype,
            linkedin=body.linkedin,
            wechat=body.wechat,
            notes=body.notes,
            custom_fields=body.custom_fields,
        )
        await session.commit()
        return _contact_response(contact)
    except CustomerNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e


@router.put("/contacts/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: uuid.UUID,
    body: UpdateContactRequest,
    current_user: User = Depends(get_current_user),
    service: ContactService = Depends(get_contact_service),
    session: AsyncSession = Depends(get_db),
) -> ContactResponse:
    try:
        updates = body.model_dump(exclude_unset=True)
        contact = await service.update_contact(
            tenant_id=current_user.tenant_id,
            contact_id=contact_id,
            **updates,
        )
        await session.commit()
        return _contact_response(contact)
    except ContactNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e


@router.delete("/contacts/{contact_id}", status_code=204)
async def delete_contact(
    contact_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: ContactService = Depends(get_contact_service),
    session: AsyncSession = Depends(get_db),
) -> None:
    try:
        await service.soft_delete_contact(tenant_id=current_user.tenant_id, contact_id=contact_id)
        await session.commit()
    except ContactNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e


@router.put("/contacts/{contact_id}/primary", response_model=ContactResponse)
async def set_primary_contact(
    contact_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: ContactService = Depends(get_contact_service),
    session: AsyncSession = Depends(get_db),
) -> ContactResponse:
    try:
        contact = await service.set_primary(tenant_id=current_user.tenant_id, contact_id=contact_id)
        await session.commit()
        return _contact_response(contact)
    except ContactNotFoundError as e:
        raise HTTPException(status_code=404, detail={"code": e.code, "message": e.message}) from e
