"""Settings repository for settings data access."""

from typing import Optional
from sqlalchemy.orm import Session

from app.models.settings import Settings
from app.repositories.base_repository import BaseRepository


class SettingsRepository(BaseRepository[Settings]):
    """Repository for Settings model."""

    def __init__(self, session: Session):
        """Initialize settings repository."""
        super().__init__(Settings, session)

    def get_by_key(self, key: str) -> Optional[Settings]:
        """Get setting by key.

        Args:
            key: Setting key

        Returns:
            Settings instance or None
        """
        return self.session.query(Settings).filter(Settings.key == key).first()

    def get_global_settings(self):
        """Get all global settings.

        Returns:
            List of global settings
        """
        return self.session.query(Settings).filter(Settings.is_global == True).all()

    def get_user_settings(self, user_id: int):
        """Get all settings for a user.

        Args:
            user_id: User ID

        Returns:
            List of user settings
        """
        return self.session.query(Settings).filter(Settings.user_id == user_id).all()

    def set_global_setting(self, key: str, value: str, data_type: str = "string") -> Settings:
        """Set a global setting.

        Args:
            key: Setting key
            value: Setting value
            data_type: Data type

        Returns:
            Settings instance
        """
        setting = self.get_by_key(key)
        if setting:
            setting.value = value
            setting.data_type = data_type
            self.session.commit()
            self.session.refresh(setting)
            return setting
        
        setting = Settings(key=key, value=value, data_type=data_type, is_global=True)
        return self.create(setting)

    def set_user_setting(self, user_id: int, key: str, value: str, data_type: str = "string") -> Settings:
        """Set a user setting.

        Args:
            user_id: User ID
            key: Setting key
            value: Setting value
            data_type: Data type

        Returns:
            Settings instance
        """
        setting = self.session.query(Settings).filter(
            Settings.key == key,
            Settings.user_id == user_id
        ).first()
        
        if setting:
            setting.value = value
            setting.data_type = data_type
            self.session.commit()
            self.session.refresh(setting)
            return setting
        
        setting = Settings(key=key, value=value, data_type=data_type, is_global=False, user_id=user_id)
        return self.create(setting)
