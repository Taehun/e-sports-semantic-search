from urllib.parse import quote

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker

from .config import settings

# PostgresQL 연결 정보
DB_USER = settings.DB_USER
DB_PASS = settings.DB_PASS
DB_HOST = settings.DB_HOST
DB_PORT = settings.DB_PORT
DB_NAME = settings.DB_NAME

# Database URL
POSTGRES_URL = f"postgresql://{DB_USER}:{quote(DB_PASS)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the SQLAlchemy engine
engine = create_engine(POSTGRES_URL, echo=True)

# Create a sessionmaker instance
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:
    """
    Base class for SQLAlchemy models.
    """

    __name__: str

    @declared_attr.directive
    # pylint: disable=E0213
    def __tablename__(cls) -> str:
        """
        Automatically generate __tablename__ using the class name.
        """
        return cls.__name__.lower()
