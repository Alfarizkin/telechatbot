class ChatServiceError(Exception):
    """Base class untuk semua error di ChatService."""
    pass

class DatabaseError(ChatServiceError):
    """Error terkait operasi database."""
    pass

class AIServiceError(ChatServiceError):
    """Error terkait AI client (http request, timeout, dll)."""
    pass