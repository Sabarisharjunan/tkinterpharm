"""Data validation utilities using Pydantic."""

import re
from typing import Optional

from pydantic import BaseModel, field_validator, EmailStr

from app.utils.constants import AppConstants


class BaseValidator(BaseModel):
    """Base validator with common configuration."""

    class Config:
        """Pydantic config."""
        from_attributes = True
        populate_by_name = True


class UserValidator(BaseValidator):
    """User data validator."""
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: str = "USER"
    is_active: bool = True

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Validate username."""
        if not (AppConstants.USERNAME_MIN_LENGTH <= len(v) <= AppConstants.USERNAME_MAX_LENGTH):
            raise ValueError(
                f"Username must be between {AppConstants.USERNAME_MIN_LENGTH} "
                f"and {AppConstants.USERNAME_MAX_LENGTH} characters"
            )
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError("Username can only contain letters, numbers, hyphens, and underscores")
        return v

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_names(cls, v: str) -> str:
        """Validate first and last names."""
        if not v or len(v) < 2:
            raise ValueError("Name must be at least 2 characters")
        return v.strip()

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate user role."""
        valid_roles = ["ADMIN", "MANAGER", "USER"]
        if v not in valid_roles:
            raise ValueError(f"Role must be one of {valid_roles}")
        return v
