from email.policy import default
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import date


Base = declarative_base()

class LegExercise(Base):

    __tablename__ ="LegExercise"
    id =Column(Integer, primary_key=True)
    counter= Column(Integer)
    user_id = Column(Integer,default=1)
    date=Column(Date, index=True, default=date.today)

class ArmExercise(Base):
    
    __tablename__ ="ArmExercise"
    id =Column(Integer, primary_key=True)
    counter= Column(Integer)
    user_id = Column(Integer,default=1)
    date=Column(Date, index=True, default=date.today)

class KneeExercise(Base):
    
    __tablename__ ="KneeExercise"
    id =Column(Integer, primary_key=True)
    counter= Column(Integer)
    user_id = Column(Integer,default=1)
    date=Column(Date, index=True, default=date.today)

if __name__ == "__main__":
    engine = create_engine('sqlite:///db.sqlite3')
    Base.metadata.create_all(engine)
