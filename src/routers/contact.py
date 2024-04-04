from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database.fu_db import get_db
from models.model import User, Role
from repository import contact as ContactService
from services.roles import RoleAccess
from services.auth import current_active_user
from dto.contact import ContactResponse, ContactSchema
from dto import contact 

router = APIRouter()

access_to_route_all = RoleAccess([Role.admin, Role.moderator])

@router.post('/',  response_model=ContactResponse, status_code=status.HTTP_201_CREATED, tags=['Contact'])
async def create_contact(data: ContactSchema, db: AsyncSession = Depends(get_db),
                      user: User = Depends(current_active_user)):
    man = await ContactService.create_contact(data, db, user)
    return man

@router.get('/{id}', tags=['Contact'])
async def get_contact(id: int = None, db: AsyncSession = Depends(get_db)):
    return await ContactService.get_contact(id, db)

@router.get('/name/{name}', tags=['Contact'])
async def get_contact_by_name(name: str, db: AsyncSession = Depends(get_db)):
    return await ContactService.get_contact_by_name(name, db)

@router.get('/last_name/{last_name}', tags=['Contact'])
async def get_contact_by_last_name(last_name: str, db: AsyncSession = Depends(get_db)):
    return await ContactService.get_contact_by_last_name(last_name, db)

@router.get('/email/{email}', tags=['Contact'])
async def get_contact_by_email(email: str, db: AsyncSession = Depends(get_db)):
    return await ContactService.get_contact_by_email(email, db)

@router.get('/all', response_model=list[ContactResponse], tags=['Contact'])
async def get_contacts(db: AsyncSession = Depends(get_db), user: User = Depends(current_active_user)):
    man = await ContactService.get_contacts(db, user)
    return man

@router.put('/{id}', tags=['Contact'])
async def update_contact(id: int = Path(ge=1), data: contact.ContactSchema = None, db: AsyncSession = Depends(get_db),  user: User = Depends(current_active_user)):
    man = await ContactService.update_contact(data, id, db, user)
    if man is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return man

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Contact'])
async def delete_contact(id: int = Path(ge=1), db: AsyncSession = Depends(get_db),user: User = Depends(current_active_user)):
    man = await ContactService.delete_contact(id, db, user)
    return man

@router.get('/user/{birthday}', tags=['Contact'])
async def birthday_seven(db: AsyncSession = Depends(get_db)):
    return await ContactService.birthday_seven(db)