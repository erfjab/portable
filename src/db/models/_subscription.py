from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, Session, relationship

from src.config import SUBCRIPTION_DOMAIN_PREFIX
from ._server import Server
from ..core import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(64), nullable=False)
    key: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    server_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("servers.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now())

    server: Mapped["Server"] = relationship(
        "Server",
        backref=None,
        primaryjoin="Subscription.server_id == Server.id",
        lazy="joined",
    )

    @property
    def kb_remark(self) -> str:
        return f"{self.username} [{self.key}]"

    @property
    def link(self) -> str:
        return f"{SUBCRIPTION_DOMAIN_PREFIX}/sub/{self.key}"

    def format(self) -> dict:
        return {"username": self.username, "key": self.key, "link": self.link}

    @classmethod
    def get_by_id(cls, db: Session, id: int) -> Optional["Subscription"]:
        return db.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_by_key(cls, db: Session, key: int) -> Optional["Subscription"]:
        return db.query(cls).filter(cls.key == key).first()

    @classmethod
    def get_by_username(cls, db: Session, username: int) -> Optional["Subscription"]:
        return db.query(cls).filter(cls.username == username).first()

    @classmethod
    def get_all(cls, db: Session) -> Optional["Subscription"]:
        query = db.query(cls)
        return query.all()

    @classmethod
    def update(
        cls,
        db: Session,
        *,
        key: str,
        username: Optional[str] = None,
        server_id: Optional[int] = None,
    ) -> Optional["Subscription"]:
        subscription = cls.get_by_key(db, key=key)
        if not subscription:
            return None
        if username:
            subscription.username = username
        if server_id:
            subscription.server_id = server_id
        db.flush()
        return subscription

    @classmethod
    def create(
        cls, db: Session, *, key: str, username: str, server_id: int
    ) -> "Subscription":
        subscription = cls(key=key, username=username, server_id=server_id)
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
