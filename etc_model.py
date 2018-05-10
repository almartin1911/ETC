from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy import create_engine

from datetime import datetime

maker = sessionmaker(autoflush=True, autocommit=False)
DBSession = scoped_session(maker)

Base = declarative_base()


def init_model(engine):
    DBSession.configure(bind=engine)


def setup_database(engine):
    Base.metadata.create_all(engine)
    print("Database sucessfully loaded/created")


def connect_to_database(echo):
    db_path = "sqlite:///etc_database.db?check_same_thread=False"
    # echo=True for debugging purposes
    engine = create_engine(db_path, encoding="utf-8", echo=echo)
    init_model(engine)
    db_session = DBSession()
    setup_database(engine)

    return db_session


def add_record(session, raw_data, command, user_exec):
    record = Record()
    record.raw_data = raw_data
    record.datetime = datetime.now()

    record.command = command
    record.user_exec = user_exec

    session.add(record)
    session.commit()

    return record


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    fullname = Column(String)
    email = Column(String, nullable=False)
    phone = Column(String)
    password = Column(String, nullable=False)

    # Relationship with Command
    commands = relationship("Command", back_populates="user")
    # Relationship with Record
    records = relationship("Record", back_populates="user_exec")

    def __repr__(self):
        result = f"<User(username='{self.username}', "
        result += f"fullname='{self.fullname}', "
        result += f"email='{self.email}', "
        result += f"phone='{self.phone}', "
        result += f"password='{self.password}')>"
        return result


class Parameter(Base):
    __tablename__ = 'parameter'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    symbol = Column(String, nullable=False)
    unit = Column(String)
    description = Column(String)

    # Relationship with Parameter_record
    parameter_records = relationship("Parameter_record",
                                     back_populates="parameter")

    def __repr__(self):
        result = f"<Parameter(name='{self.name}', "
        result += f"symbol='{self.symbol}', "
        result += f"unit='{self.unit}', "
        result += f"description='{self.description}')>"
        return result


class Command(Base):
    __tablename__ = 'command'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    command = Column(String, nullable=False, unique=True)
    date_creation = Column(DateTime, nullable=False)
    date_modification = Column(DateTime)

    # Relationship with User
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="commands")
    # Relationship with Record
    records = relationship("Record", back_populates="command")

    def __repr__(self):
        result = f"<Command(name='{self.name}', "
        result += f"description='{self.description}', "
        result += f"command='{self.command}', "
        result += f"date_creation='{self.date_creation}', "
        result += f"date_modification='{self.date_modification}')>"
        return result


class Record(Base):
    __tablename__ = "record"

    id = Column(Integer, primary_key=True)
    raw_data = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)

    # Relationship with Command
    command_id = Column(Integer, ForeignKey('command.id'), nullable=False)
    command = relationship("Command", back_populates="records")
    # Relationship with User
    user_exec_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_exec = relationship("User", back_populates="records")
    # Relationship with Parameter_record
    parameter_records = relationship("Parameter_record",
                                     back_populates="record")

    def __repr__(self):
        result = f"<Record(raw_data='{self.raw_data}', "
        result += f"datetime='{self.datetime}')>"
        return result


class Parameter_record(Base):
    __tablename__ = 'parameter_record'

    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=False)
    datetime = Column(DateTime, nullable=False)

    # Relationship with Parameter
    parameter_id = Column(Integer, ForeignKey('parameter.id'), nullable=False)
    parameter = relationship("Parameter", back_populates="parameter_records")
    # Relationship with Record
    record_id = Column(Integer, ForeignKey('record.id'), nullable=False)
    record = relationship("Record", back_populates="parameter_records")

    def __repr__(self):
        result = f"<Parameter_record(value='{self.value}', "
        result += f"datetime='{self.datetime}')>"
        return result
