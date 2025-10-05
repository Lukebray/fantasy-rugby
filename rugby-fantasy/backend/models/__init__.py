# Import Base from one place
from .User import Base

# Import all models to register them with Base
from .User import User
from .League import League
from .LeagueMember import LeagueMember
from .Competition import Competition
from .CompetitionRound import CompetitionRound
from .Player import Player
from .Squad import Squad
from .SquadPlayer import SquadPlayer
from .Transfer import Transfer
from .RoundStats import RoundStats

# This ensures all models are registered with Base
__all__ = ["Base", "User", "League", "LeagueMember", "Competition", "CompetitionRound", "Player", "Squad", "SquadPlayer", "Transfer", "RoundStats"]