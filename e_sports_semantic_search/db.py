from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker

from .config import settings

# PostgresQL 연결 정보
DB_USER = settings.POSTGRES_USER
DB_PASS = settings.POSTGRES_PASSWORD
DB_HOST = settings.POSTGRES_HOST
DB_PORT = settings.POSTGRES_PORT
DB_NAME = settings.POSTGRES_DB

# Database URL
POSTGRES_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

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
