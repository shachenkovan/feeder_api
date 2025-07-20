from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from api.schemas.filial_enterprises_schema import FilialEnterprisesSchemaGet, FilialEnterprisesSchemaPost, \
    FilialEnterprisesSchemaUpdate
from database.crud.filial_enterprises_crud import get_all_filial_enterprises, get_filial_enterprise_by_id, \
    create_filial_enterprise, update_filial_enterprise, delete_filial_enterprise
from database.db import get_db
from database.models import FilialEnterprises

filial_enterprise_router = APIRouter(prefix='/filial_enterprise', tags=['Филиалы предприятий'])


@filial_enterprise_router.get('/all_filial_enterprises')
def all_filial_enterprises(db: Session = Depends(get_db)):
    try:
        orm_models = get_all_filial_enterprises(db)
        result = [FilialEnterprisesSchemaGet.model_validate(m) for m in orm_models]
        return result
    except Exception as e:
        return {"error": str(e)}


@filial_enterprise_router.get('/get_filial_enterprise/{filial_enterprise_id}')
def filial_enterprise_by_id(filial_enterprise_id: int, db: Session = Depends(get_db)):
    try:
        orm_model = get_filial_enterprise_by_id(db, filial_enterprise_id)
        result = FilialEnterprisesSchemaGet.model_validate(orm_model)
        return result
    except Exception as e:
        return {"error": str(e)}


@filial_enterprise_router.post('/create_filial_enterprise')
def add_filial_enterprise(filial_enterprise: FilialEnterprisesSchemaPost, db: Session = Depends(get_db)):
    try:
        db_filial_enterprise = FilialEnterprises(inn=filial_enterprise.inn,
                                    adres=filial_enterprise.adres)
        result = create_filial_enterprise(db, db_filial_enterprise)
        return result
    except Exception as e:
        return {"error": str(e)}


@filial_enterprise_router.patch('/update_filial_enterprise/{filial_enterprise_id}')
def update_filial_enterprise_by_id(filial_enterprise_id: int, filial_enterprise: FilialEnterprisesSchemaUpdate, db: Session = Depends(get_db)):
    try:
        data_to_update = filial_enterprise.model_dump(exclude_unset=True)
        return update_filial_enterprise(db, filial_enterprise_id, changes=data_to_update)
    except Exception as e:
        return {"error": str(e)}


@filial_enterprise_router.delete('/delete_filial_enterprise/{filial_enterprise_id}')
def delete_filial_enterprise_by_id(filial_enterprise_id: int, db: Session = Depends(get_db)):
    try:
        return delete_filial_enterprise(db, filial_enterprise_id)
    except Exception as e:
        return {"error": str(e)}


