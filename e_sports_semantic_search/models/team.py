from sqlalchemy import TIMESTAMP, BigInteger, Column, String
from sqlalchemy.sql import func

from ..db import Base


class Team(Base):
    # pylint:disable=not-callable
    id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    region = Column(String, nullable=False)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    image = Column(String, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updatedAt = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())
