from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey
from sqlalchemy import create_engine, MetaData
from config import test_settings


engine = create_engine(test_settings.db_url_test_ddl)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user_account'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    addresses: Mapped[list["Address"]] = relationship(back_populates="user")


class Address(Base):
    __tablename__ = 'address'

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(String(40))
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")


# print(Base.metadata)
Address.metadata.create_all(engine)
