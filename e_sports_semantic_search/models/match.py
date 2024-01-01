from sqlalchemy import (
    TIMESTAMP,
    BigInteger,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    SmallInteger,
)
from sqlalchemy.sql import func

from ..db import Base


class Match(Base):
    # pylint:disable=not-callable
    id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    tournamentId = Column(BigInteger, ForeignKey("tournament.id"), nullable=False)
    startTime = Column(DateTime, nullable=False)
    state = Column(
        Enum("unStarted", "finished", "inProgress", name="state_enum"),
        nullable=False,
        default="unStarted",
    )  # type: Column
    team1Id = Column(BigInteger, ForeignKey("team.id"), nullable=False)
    team2Id = Column(BigInteger, ForeignKey("team.id"), nullable=False)
    team1Score = Column(SmallInteger, nullable=False, default=0)
    team2Score = Column(SmallInteger, nullable=False, default=0)
    winnerId = Column(BigInteger, ForeignKey("team.id"), nullable=True)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updatedAt = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())
