from sqlalchemy import (
    TIMESTAMP,
    BigInteger,
    Column,
    Enum,
    ForeignKey,
    Integer,
    SmallInteger,
)
from sqlalchemy.sql import func

from ..db import Base


class PlayerStats(Base):
    # pylint:disable=not-callable
    id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    gameId = Column(BigInteger, ForeignKey("game.id"), nullable=False)
    playerId = Column(BigInteger, ForeignKey("player.id"), nullable=False)
    position = Column(
        Enum("top", "jungle", "mid", "bot", "support", name="position_type"),
        nullable=False,
    )  # type: Column
    champion = Column(Integer, ForeignKey("champion.key"), nullable=True)
    kills = Column(SmallInteger, nullable=False)
    deaths = Column(SmallInteger, nullable=False)
    assists = Column(SmallInteger, nullable=False)
    golds = Column(Integer, nullable=True)
    cs = Column(SmallInteger, nullable=True)
    level = Column(SmallInteger, nullable=True)
    damageDealt = Column(Integer, nullable=True)
    damageTaken = Column(Integer, nullable=True)

    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updatedAt = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())
