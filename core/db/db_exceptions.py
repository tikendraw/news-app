
# Exceptions for database operations
class AddError(Exception):
    """Raised when adding an object to the database fails."""
    pass

class UpdateError(Exception):
    """Raised when updating an object in the database fails."""
    pass

class DeleteError(Exception):
    """Raised when deleting an object in the database fails."""
    pass

class DatabaseError(Exception):
    """Raised for database-related errors."""
    pass