from sqlalchemy import TIMESTAMP, Column, Integer, String
from sqlalchemy.sql import func

from ..db import Base


# https://darkintaqt.com/blog/champ-ids
class Champion(Base):
    # pylint:disable=not-callable
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    key = Column(String, nullable=False)
    name = Column(String, nullable=False)
    image = Column(String, nullable=False)

    createdAt = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updatedAt = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())
