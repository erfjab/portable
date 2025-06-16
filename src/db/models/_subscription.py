from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import mapped_column, Mapped, Session, relationship

from src.config import SUBCRIPTION_DOMAIN_PREFIX
from ._server import Server
from ._user import User
from ..core import Base


class MarzneshinTag(Base):
    __tablename__ = "marzneshin_tags"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    key: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    subscription_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("subscriptions.id", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now())

    subscription: Mapped["Subscription"] = relationship(
        "Subscription", back_populates="marzneshin_tags", lazy="joined"
    )

    @classmethod
    def get(cls, db: Session, *, key: str, username: str) -> Optional["MarzneshinTag"]:
        return (
            db.query(cls)
            .filter(cls.username == username)
            .filter(cls.key == key)
            .first()
        )

    @classmethod
    def create(
        cls, db: Session, *, key: str, username: str, subscription_id: int
    ) -> Optional["MarzneshinTag"]:
        tag = cls(username=username, key=key, subscription_id=subscription_id)
        db.add(tag)
        db.flush()
        return tag

    @classmethod
    def remove_by_subscription(cls, db: Session, *, subscription_id: int) -> bool:
        db.query(cls).filter(cls.subscription_id == subscription_id).delete()
        db.flush()
        return True


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(64), nullable=False)
    key: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    owner: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.chat_id"), nullable=True
    )
    server_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("servers.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now())

    user: Mapped["User"] = relationship(
        "User",
        backref=None,
        primaryjoin="Subscription.owner == User.chat_id",
        lazy="joined",
    )
    server: Mapped["Server"] = relationship(
        "Server",
        backref=None,
        primaryjoin="Subscription.server_id == Server.id",
        lazy="selectin",
    )
    marzneshin_tags: Mapped[list["MarzneshinTag"]] = relationship(
        "MarzneshinTag",
        back_populates="subscription",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @property
    def kb_remark(self) -> str:
        return f"{self.username} [{self.key}]"

    @property
    def link(self) -> str:
        return f"{SUBCRIPTION_DOMAIN_PREFIX}/sub/{self.key}"

    def format(self) -> dict:
        return {
            "username": self.username,
            "key": self.key,
            "link": self.link,
            "owner": self.owner,
        }

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
    def get_all(cls, db: Session) -> Optional[list["Subscription"]]:
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
        owner: Optional[int] = None,
    ) -> Optional["Subscription"]:
        subscription = cls.get_by_key(db, key=key)
        if not subscription:
            return None
        if username:
            subscription.username = username
        if server_id:
            subscription.server_id = server_id
        if owner:
            subscription.owner = owner
        db.flush()
        return subscription

    @classmethod
    def create(
        cls, db: Session, *, key: str, username: str, server_id: int, owner: int
    ) -> "Subscription":
        subscription = cls(key=key, username=username, server_id=server_id, owner=owner)
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
