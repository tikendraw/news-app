
# Exceptions for database operations
class AddArticleError(Exception):
    """Raised when adding an article to the database fails."""

    pass


class UpdateArticleError(Exception):
    """Raised when updating an article in the database fails."""

    pass

class DeleteArticleError(Exception):
    """Raised when deleting an article in the database fails."""

    pass


class DatabaseError(Exception):
    """Raised for database-related errors."""

    pass


