"""
Version and Migration Management for Encrypt-D
Handles version tracking and data migrations between versions
"""

import json
from pathlib import Path
from typing import Optional, Tuple
import shutil
from datetime import datetime

from .config import APP_VERSION, APP_DATA_DIR


class VersionManager:
    """Manages application versioning and data migrations"""

    def __init__(self):
        self.version_file = APP_DATA_DIR / "version.json"
        self.backup_dir = APP_DATA_DIR / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def get_current_app_version(self) -> str:
        """Returns the current application version"""
        return APP_VERSION

    def get_installed_version(self) -> Optional[str]:
        """Returns the version of installed data, or None if first install"""
        if not self.version_file.exists():
            return None

        try:
            with open(self.version_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("version")
        except Exception as e:
            print(f"Warning: Could not read version file: {e}")
            return None

    def save_version(self, version: str = None) -> bool:
        """Saves the current version to version file"""
        if version is None:
            version = APP_VERSION

        try:
            version_data = {
                "version": version,
                "updated_at": datetime.now().isoformat(),
                "platform": "windows",
            }

            with open(self.version_file, "w", encoding="utf-8") as f:
                json.dump(version_data, f, indent=2)

            return True
        except Exception as e:
            print(f"Error saving version: {e}")
            return False

    def needs_migration(self) -> Tuple[bool, Optional[str], str]:
        """
        Check if migration is needed

        Returns:
            Tuple[bool, Optional[str], str]: (needs_migration, from_version, to_version)
        """
        installed_version = self.get_installed_version()
        current_version = APP_VERSION

        if installed_version is None:
            # First install, no migration needed
            return False, None, current_version

        if installed_version != current_version:
            return True, installed_version, current_version

        return False, installed_version, current_version

    def create_backup(self) -> Tuple[bool, str]:
        """
        Creates a backup of all user data before migration

        Returns:
            Tuple[bool, str]: (success, backup_path or error_message)
        """
        try:
            # Create timestamped backup folder
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            installed_version = self.get_installed_version() or "unknown"
            backup_name = f"backup_v{installed_version}_{timestamp}"
            backup_path = self.backup_dir / backup_name

            backup_path.mkdir(parents=True, exist_ok=True)

            # Files to backup
            files_to_backup = [
                "auth.dat",
                "config.json",
                "version.json",
            ]

            # Backup files
            for filename in files_to_backup:
                source = APP_DATA_DIR / filename
                if source.exists():
                    dest = backup_path / filename
                    shutil.copy2(source, dest)

            # Backup vault directory if exists
            vault_dir = APP_DATA_DIR / "vault"
            if vault_dir.exists():
                vault_backup = backup_path / "vault"
                shutil.copytree(vault_dir, vault_backup)

            return True, str(backup_path)

        except Exception as e:
            return False, f"Backup failed: {e}"

    def migrate(self, from_version: str, to_version: str) -> Tuple[bool, str]:
        """
        Performs migration from one version to another

        Returns:
            Tuple[bool, str]: (success, message)
        """
        print(f"Migrating from v{from_version} to v{to_version}")

        # Create backup before migration
        backup_success, backup_info = self.create_backup()
        if not backup_success:
            return False, f"Migration aborted: {backup_info}"

        print(f"Backup created: {backup_info}")

        # Perform version-specific migrations
        try:
            migration_success = self._run_migrations(from_version, to_version)

            if migration_success:
                # Update version file
                self.save_version(to_version)
                return True, f"Migration successful! Backup: {backup_info}"
            else:
                return False, "Migration failed. Your data backup is safe."

        except Exception as e:
            return False, f"Migration error: {e}. Backup: {backup_info}"

    def _run_migrations(self, from_version: str, to_version: str) -> bool:
        """
        Runs specific migrations based on version changes

        Returns:
            bool: Success status
        """
        # Parse version numbers
        from_major, from_minor, from_patch = self._parse_version(from_version)
        to_major, to_minor, to_patch = self._parse_version(to_version)

        # Define migrations
        migrations = []

        # Migration from 1.0.x to 1.1.0
        if from_major == 1 and from_minor == 0 and to_minor >= 1:
            migrations.append(self._migrate_1_0_to_1_1)

        # Add future migrations here
        # if from_version < "1.2.0" and to_version >= "1.2.0":
        #     migrations.append(self._migrate_1_1_to_1_2)

        # Execute migrations in order
        for migration_func in migrations:
            try:
                print(f"Running migration: {migration_func.__name__}")
                if not migration_func():
                    return False
            except Exception as e:
                print(f"Migration {migration_func.__name__} failed: {e}")
                return False

        # If no specific migrations, just update version
        if not migrations:
            print("No specific migrations needed, updating version only")

        return True

    def _migrate_1_0_to_1_1(self) -> bool:
        """
        Migration from version 1.0.x to 1.1.0

        Changes in 1.1.0:
        - Added configurable auto-destruction
        - Added configurable max attempts
        - Strong password requirements

        Note: auth.dat format is backward compatible
        """
        print("Migrating 1.0.x → 1.1.0")

        # Check if auth.dat exists and needs migration
        auth_file = APP_DATA_DIR / "auth.dat"
        if not auth_file.exists():
            print("No auth.dat found, skipping migration")
            return True

        # In v1.1.0, auth.dat will automatically add new fields
        # when loaded by AuthManager, so no manual migration needed
        print("auth.dat will be automatically updated on first load")

        return True

    def _parse_version(self, version: str) -> Tuple[int, int, int]:
        """
        Parse version string into major, minor, patch

        Args:
            version: Version string like "1.2.3"

        Returns:
            Tuple[int, int, int]: (major, minor, patch)
        """
        try:
            parts = version.split(".")
            major = int(parts[0]) if len(parts) > 0 else 0
            minor = int(parts[1]) if len(parts) > 1 else 0
            patch = int(parts[2]) if len(parts) > 2 else 0
            return major, minor, patch
        except Exception:
            return 0, 0, 0

    def get_migration_info(self) -> dict:
        """
        Get information about current version state

        Returns:
            dict: Version information
        """
        installed = self.get_installed_version()
        current = self.get_current_app_version()
        needs_mig, from_v, to_v = self.needs_migration()

        return {
            "installed_version": installed,
            "current_version": current,
            "needs_migration": needs_mig,
            "from_version": from_v,
            "to_version": to_v,
            "is_first_install": installed is None,
        }

    def list_backups(self) -> list:
        """
        List all available backups

        Returns:
            list: List of backup directories with metadata
        """
        backups = []

        if not self.backup_dir.exists():
            return backups

        for backup_path in sorted(self.backup_dir.iterdir(), reverse=True):
            if backup_path.is_dir():
                backups.append(
                    {
                        "name": backup_path.name,
                        "path": str(backup_path),
                        "created": datetime.fromtimestamp(
                            backup_path.stat().st_ctime
                        ).isoformat(),
                    }
                )

        return backups

    def cleanup_old_backups(self, keep_last: int = 5) -> int:
        """
        Remove old backups, keeping only the most recent ones

        Args:
            keep_last: Number of recent backups to keep

        Returns:
            int: Number of backups deleted
        """
        backups = self.list_backups()

        if len(backups) <= keep_last:
            return 0

        deleted = 0
        for backup in backups[keep_last:]:
            try:
                backup_path = Path(backup["path"])
                shutil.rmtree(backup_path)
                deleted += 1
            except Exception as e:
                print(f"Could not delete backup {backup['name']}: {e}")

        return deleted

