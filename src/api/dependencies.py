from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from src.db import Subscription, GetDB


def get_db():
    with GetDB() as db:
        yield db


def get_subscription_user(key: str, db: Annotated[Session, Depends(get_db)]):
    dbsub = Subscription.get_by_key(db, key)
    if not dbsub:
        raise HTTPException(status_code=404)
    return dbsub


SubDep = Annotated[Subscription, Depends(get_subscription_user)]
DBDep = Annotated[Session, Depends(get_db)]
