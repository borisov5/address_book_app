from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


"""
Configure database
"""
SQLALCHEMY_DATABASE_URL = "sqlite:///./database/addresses.db"

# creating engine
# By default, check_same_thread is True and only the creating thread may use the connection. If set False,
# the returned connection may be shared across multiple threads
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# bind – An optional Connectable, will be assigned the bind attribute on the MetaData instance.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# A simple constructor that allows initialization from kwargs.
Base = declarative_base()