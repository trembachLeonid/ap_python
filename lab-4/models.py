from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Date,
    DateTime,
    ForeignKey,
    PrimaryKeyConstraint,
    Table,
    MetaData,
    create_engine,
    insert,
)

Base = declarative_base()
engine = create_engine("mysql://root:password@localhost/family_budget_db", echo=False)
session = sessionmaker(bind=engine)
s = session()


class FamilyMemberRelation(Base):
    __tablename__ = "family_members"
    user = Column(Integer, ForeignKey("users.id"), primary_key=True)
    family = Column(Integer, ForeignKey("families.id"), primary_key=True)
    users = relationship("User")
    families = relationship("Family")
    __table_args__ = (
        PrimaryKeyConstraint(user, family),
        {},
    )


class Operation(Base):
    __tablename__ = "operations"
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey("users.id"))
    familyId = Column(Integer, ForeignKey("families.id"))
    moneyChange = Column(Float)
    date = Column(DateTime)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    email = Column(String(30), unique=True)
    password = Column(String(15))
    phone = Column(String(20), unique=True)
    currentMoney = Column(Float)

    def __str__(self):
        return (
            f"fName = {self.first_name}\n"
            f"lName = {self.last_name}\n"
            f"email = {self.email}\n "
            f"phone = {self.phone}\n"
            f"money = {self.currentMoney}\n"
        )


class Family(Base):
    __tablename__ = "families"
    id = Column(Integer, primary_key=True)
    familyname = Column(String(30))

    currentMoney = Column(Float)

    def __str__(self):
        return (
            f"fName = {self.first_name}\n"
            f"lName = {self.last_name}\n"
            f"email = {self.email}\n "
            f"phone = {self.phone}\n"
            f"money = {self.currentMoney}\n"
        )


if __name__ == "__main__":
    user1 = User(
        id=1,
        username="ba1nan",
        first_name="Ivan",
        last_name="Franko",
        email="banan@ex.com",
        password="7548Rfd8f3",
        phone="+380682314564",
        currentMoney=100.5,
    )
    user2 = User(
        id=2,
        username="yabanan",
        first_name="Oleg",
        last_name="Franko",
        email="ban@ex.com",
        password="7548Rfd8f3",
        phone="+380542312364",
        currentMoney=1000,
    )
    user3 = User(
        id=3,
        username="banan",
        first_name="Olena",
        last_name="Franko",
        email="plfdfde@ex.com",
        password="7548Rfd8f3",
        phone="+380682312364",
        currentMoney=0,
    )

    family = Family(id=1, familyname="Brawl Stars", currentMoney=50)
    member1 = FamilyMemberRelation(user=1, family=1)
    member2 = FamilyMemberRelation(user=2, family=1)
    member3 = FamilyMemberRelation(user=3, family=1)

    operation = Operation(id=1, userId=1, familyId=1, moneyChange=50, date=datetime.now())

    s.add(user1)
    s.add(user2)
    s.add(user3)
    s.add(family)
    s.add(member1)
    s.add(member2)
    s.add(member3)
    s.commit()
    s.add(operation)

    s.commit()

    # print(s.query(User).all()[0])
