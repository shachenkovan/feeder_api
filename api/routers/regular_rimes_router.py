from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from api.schemas.regular_times_schema import RegularTimesSchemaGet, RegularTimesSchemaPost, RegularTimesSchemaUpdate
from database.crud.regular_times_crud import get_all_regular_times, get_regular_time_by_id, \
    create_regular_time, update_regular_time, delete_regular_time
from database.db import get_db
from database.models import TaskLists, RegularTimes

regular_time_router = APIRouter(prefix='/regular_time', tags=['Временные периоды'])


@regular_time_router.get('/all_regular_times')
def all_regular_times(db: Session = Depends(get_db)):
    try:
        orm_models = get_all_regular_times(db)
        result = [RegularTimesSchemaGet.model_validate(m) for m in orm_models]
        return result
    except Exception as e:
        return {"error": str(e)}


@regular_time_router.get('/get_regular_time/{regular_time_id}')
def regular_time_by_id(regular_time_id: int, db: Session = Depends(get_db)):
    try:
        orm_model = get_regular_time_by_id(db, regular_time_id)
        result = RegularTimesSchemaGet.model_validate(orm_model)
        return result
    except Exception as e:
        return {"error": str(e)}


@regular_time_router.post('/create_regular_time')
def add_regular_time(regular_time: RegularTimesSchemaPost, db: Session = Depends(get_db)):
    try:
        db_regular_time = RegularTimes(period=regular_time.period,
                                 days=regular_time.days,
                                 timing=regular_time.timing)
        result = create_regular_time(db, db_regular_time)
        return result
    except Exception as e:
        return {"error": str(e)}


@regular_time_router.patch('/update_regular_time/{regular_time_id}')
def update_regular_time_by_id(regular_time_id: int, regular_time: RegularTimesSchemaUpdate, db: Session = Depends(get_db)):
    try:
        data_to_update = regular_time.model_dump(exclude_unset=True)
        return update_regular_time(db, regular_time_id, changes=data_to_update)
    except Exception as e:
        return {"error": str(e)}


@regular_time_router.delete('/delete_regular_time/{regular_time_id}')
def delete_regular_time_by_id(regular_time_id: int, db: Session = Depends(get_db)):
    try:
        return delete_regular_time(db, regular_time_id)
    except Exception as e:
        return {"error": str(e)}


