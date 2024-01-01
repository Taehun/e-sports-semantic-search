from sqlalchemy import TIMESTAMP, BigInteger, Column, ForeignKey, SmallInteger, Time
from sqlalchemy.sql import func

from ..db import Base


class Game(Base):
    # pylint:disable=not-callable
    id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    matchId = Column(BigInteger, ForeignKey("match.id"), nullable=False)
    team1Id = Column(BigInteger, ForeignKey("team.id"), nullable=False)
    team2Id = Column(BigInteger, ForeignKey("team.id"), nullable=False)
    gameNumber = Column(SmallInteger, nullable=False)
    winnerId = Column(BigInteger, ForeignKey("team.id"), nullable=True)
    gameTime = Column(Time, nullable=False)

    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updatedAt = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())
