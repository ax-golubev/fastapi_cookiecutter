from core.config import settings
from database.session import Database

db = Database(settings.database_uri)
