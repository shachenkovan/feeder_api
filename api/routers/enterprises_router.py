from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from database.crud.enterprices_crud import get_enterprise_by_inn, get_all_enterprises, create_enterprise, \
    update_enterprise, delete_enterprise
from api.schemas.enterprices_schema import EnterprisesSchema, EnterprisesSchemaUpdate
from database.db import get_db
from database.models import Enterprises

enterprise_router = APIRouter(prefix='/enterprise', tags=['Предприятия'])


@enterprise_router.get('/all_enterprises')
def all_enterprises(db: Session = Depends(get_db)):
    try:
        orm_models = get_all_enterprises(db)
        result = [EnterprisesSchema.model_validate(m) for m in orm_models]
        return result
    except Exception as e:
        return {"error": str(e)}


@enterprise_router.get('/get_enterprise/{enterprise_inn}')
def enterprise_by_inn(enterprise_inn: str, db: Session = Depends(get_db)):
    try:
        orm_model = get_enterprise_by_inn(db, enterprise_inn)
        result = EnterprisesSchema.model_validate(orm_model)
        return result
    except Exception as e:
        return {"error": str(e)}


@enterprise_router.post('/create_enterprise')
def add_enterprise(enterprise: EnterprisesSchema, db: Session = Depends(get_db)):
    try:
        db_enterprise = Enterprises(inn=enterprise.inn,
                                    ogrn=enterprise.ogrn,
                                    kpp=enterprise.kpp,
                                    name=enterprise.name,
                                    adres=enterprise.adres)
        result = create_enterprise(db, db_enterprise)
        return result
    except Exception as e:
        return {"error": str(e)}


@enterprise_router.patch('/update_enterprise/{enterprise_inn}')
def update_enterprise_by_inn(enterprise_inn: str, enterprise: EnterprisesSchemaUpdate, db: Session = Depends(get_db)):
    try:
        data_to_update = enterprise.model_dump(exclude_unset=True)
        return update_enterprise(db, enterprise_inn, changes=data_to_update)
    except Exception as e:
        return {"error": str(e)}


@enterprise_router.delete('/delete_enterprise/{enterprise_inn}')
def delete_enterprise_by_inn(enterprise_inn: str, db: Session = Depends(get_db)):
    try:
        return delete_enterprise(db, enterprise_inn)
    except Exception as e:
        return {"error": str(e)}


