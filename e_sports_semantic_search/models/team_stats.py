from sqlalchemy import (
    ARRAY,
    TIMESTAMP,
    BigInteger,
    Boolean,
    Column,
    Enum,
    ForeignKey,
    Integer,
    SmallInteger,
)
from sqlalchemy.sql import func

from ..db import Base


class TeamStats(Base):
    # pylint:disable=not-callable
    id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    gameId = Column(BigInteger, ForeignKey("game.id"), nullable=False)
    teamId = Column(BigInteger, ForeignKey("team.id"), nullable=False)

    # Ban & Pick
    ban1 = Column(Integer, ForeignKey("champion.id"), nullable=True)
    ban2 = Column(Integer, ForeignKey("champion.id"), nullable=True)
    ban3 = Column(Integer, ForeignKey("champion.id"), nullable=True)
    ban4 = Column(Integer, ForeignKey("champion.id"), nullable=True)
    ban5 = Column(Integer, ForeignKey("champion.id"), nullable=True)
    pick1 = Column(Integer, ForeignKey("champion.id"), nullable=False)
    pick2 = Column(Integer, ForeignKey("champion.id"), nullable=False)
    pick3 = Column(Integer, ForeignKey("champion.id"), nullable=False)
    pick4 = Column(Integer, ForeignKey("champion.id"), nullable=False)
    pick5 = Column(Integer, ForeignKey("champion.id"), nullable=False)

    # Game Stats
    kills = Column(SmallInteger, nullable=False)
    deaths = Column(SmallInteger, nullable=False)
    assists = Column(SmallInteger, nullable=False)
    golds = Column(Integer, nullable=False)
    towers = Column(SmallInteger, nullable=False)
    heralds = Column(SmallInteger, nullable=True)
    drakes = Column(
        ARRAY(
            Enum(
                "normal",
                "chemtech",
                "cloud",
                "hextech",
                "infernal",
                "mountain",
                "ocean",
                "elder",
                name="drake_type",
            )
        ),
        nullable=True,
        default="normal",
    )  # type: Column
    barons = Column(SmallInteger, nullable=True)
    win = Column(Boolean, nullable=False)

    createdAt = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updatedAt = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())
