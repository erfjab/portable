from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import mapped_column, Mapped, Session

from src.config import SUBCRIPTION_DOMAIN_PREFIX
from ..core import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    remark: Mapped[str] = mapped_column(String(64), nullable=False)
    key: Mapped[str] = mapped_column(String(8), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now())

    @property
    def kb_remark(self) -> str:
        return f"{self.remark} [{self.key}]"

    @property
    def link(self) -> str:
        return f"{SUBCRIPTION_DOMAIN_PREFIX}/sub/{self.key}"

    def format(self) -> dict:
        return {"remark": self.remark, "key": self.key, "link": self.link}

    @classmethod
    def get_by_id(cls, db: Session, id: int) -> Optional["Subscription"]:
        return db.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_by_key(cls, db: Session, key: int) -> Optional["Subscription"]:
        return db.query(cls).filter(cls.key == key).first()

    @classmethod
    def get_by_remark(cls, db: Session, remark: int) -> Optional["Subscription"]:
        return db.query(cls).filter(cls.remark == remark).first()

    @classmethod
    def get_all(cls, db: Session) -> Optional["Subscription"]:
        query = db.query(cls)
        return query.all()

    @classmethod
    def update(
        cls, db: Session, *, key: str, remark: Optional[str] = None
    ) -> Optional["Subscription"]:
        subscription = cls.get_by_key(db, key=key)
        if not subscription:
            return None
        if remark:
            subscription.remark = remark
        db.flush()
        return subscription

    @classmethod
    def create(cls, db: Session, *, key: str, remark: str) -> "Subscription":
        subscription = cls(key=key, remark=remark)
        db.add(subscription)
        db.flush()
        return subscription

    @classmethod
    def remove(cls, db: Session, *, key: str) -> bool:
        subscription = cls.get_by_key(db, key=key)
        if not subscription:
            return True
        db.delete(subscription)
        db.flush()
        return True
