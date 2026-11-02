"""Standard error response models."""

from typing import Optional
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Consistent error response structure across the entire API."""

    error: str
    message: str
    field: Optional[str] = None
    detail: Optional[str] = None

    def to_dict(self) -> dict:
        """Serialize error response omitting detail when None."""
        data = {
            "error": self.error,
            "message": self.message,
            "field": self.field,
        }
        if self.detail is not None:
            data["detail"] = self.detail
        return data
