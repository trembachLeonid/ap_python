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
engine = create_engine("mysql://root:12345@localhost/family_budget_db", echo=False)
Session = sessionmaker(bind=engine)
s = Session()

class FamilyMemberRelation(Base):
    __tablename__ = "family_members"
    userId = Column(Integer, ForeignKey("users.id"), primary_key=True)
    familyId = Column(Integer, ForeignKey("families.id"), primary_key=True)
    users = relationship("User")
    families = relationship("Family")


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
    firstName = Column(String(30))
    lastName = Column(String(30))
    email = Column(String(30), unique=True)
    password = Column(String(100))
    phone = Column(String(20), unique=True)
    currentMoney = Column(Float)

class Family(Base):
    __tablename__ = "families"
    id = Column(Integer, primary_key=True)
    familyName = Column(String(30))
    currentMoney = Column(Float)

if __name__ == "__main__":
    user1 = User(
        id=1,
        username="ba1nan",
        firstName="Ivan",
        lastName="Franko",
        email="banan@ex.com",
        password="7548Rfd8f3",
        phone="+380682314564",
        currentMoney=100.5,
    )
    user2 = User(
        id=2,
        username="yabanan",
        firstName="Oleg",
        lastName="Franko",
        email="ban@ex.com",
        password="7548Rfd8f3",
        phone="+380542312364",
        currentMoney=1000,
    )
    user3 = User(
        id=3,
        username="banan",
        firstName="Olena",
        lastName="Franko",
        email="plfdfde@ex.com",
        password="7548Rfd8f3",
        phone="+380682312364",
        currentMoney=0,
    )

    family = Family(id=1, familyName="Brawl Stars", currentMoney=50)
    member1 = FamilyMemberRelation(userId=1, familyId=1)
    member2 = FamilyMemberRelation(userId=2, familyId=1)
    member3 = FamilyMemberRelation(userId=3, familyId=1)

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
