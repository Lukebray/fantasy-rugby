# Import Base from one place
from .User import Base

# Import all models to register them with Base
from .User import User
from .League import League
from .LeagueMembership import LeagueMembership

# This ensures all models are registered with Base
__all__ = ["Base", "User", "League", "LeagueMembership"]