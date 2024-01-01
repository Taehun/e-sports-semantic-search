from sqlalchemy import TIMESTAMP, BigInteger, Column, Date, ForeignKey, String
from sqlalchemy.sql import func

from ..db import Base


class Tournament(Base):
    # pylint:disable=not-callable
    id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    leagueId = Column(BigInteger, ForeignKey("league.id"), nullable=False)
    name = Column(String, nullable=False)
    startDate = Column(Date, nullable=False)
    endDate = Column(Date, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updatedAt = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())
