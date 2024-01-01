from sqlalchemy import TIMESTAMP, BigInteger, Column, Enum, ForeignKey, String
from sqlalchemy.sql import func

from ..db import Base


class Player(Base):
    # pylint:disable=not-callable
    id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    summonerName = Column(String, nullable=False)
    name = Column(String, nullable=False)
    teamId = Column(BigInteger, ForeignKey("team.id"), nullable=False)
    position = Column(
        Enum("top", "jungle", "mid", "bot", "support", name="position_type"),
        nullable=False,
    )  # type: Column
    image = Column(String, nullable=False)
    createdAt = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updatedAt = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())
