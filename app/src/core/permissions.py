"""
File permissions management for sensitive data
Ensures only the current user can access encrypted files and authentication data
"""

import os
import sys
from pathlib import Path


def set_restricted_permissions(file_path: Path) -> bool:
    """
    Sets restrictive permissions on a file/directory
    Only the current user should be able to read/write

    Args:
        file_path: Path to file or directory

    Returns:
        bool: Success status
    """
    try:
        if sys.platform == "win32":
            return _set_windows_permissions(file_path)
        else:
            return _set_unix_permissions(file_path)
    except Exception as e:
        print(f"Warning: Could not set permissions on {file_path}: {e}")
        return False


def _set_windows_permissions(file_path: Path) -> bool:
    """Sets Windows-specific permissions (ACLs)"""
    try:
        import win32security
        import ntsecuritycon as con

        # Get current user SID
        user, domain, type = win32security.LookupAccountName(
            "", win32security.GetUserName()
        )

        # Create a security descriptor
        sd = win32security.SECURITY_DESCRIPTOR()

        # Create a DACL (Discretionary Access Control List)
        dacl = win32security.ACL()

        # Add ACE (Access Control Entry) for current user with full control
        dacl.AddAccessAllowedAce(win32security.ACL_REVISION, con.FILE_ALL_ACCESS, user)

        # Set the DACL in the security descriptor
        sd.SetSecurityDescriptorDacl(1, dacl, 0)

        # Apply the security descriptor to the file
        win32security.SetFileSecurity(
            str(file_path), win32security.DACL_SECURITY_INFORMATION, sd
        )

        return True

    except ImportError:
        # pywin32 not available, fall back to basic permissions
        print("Warning: pywin32 not installed, using basic permissions")
        return _set_basic_permissions(file_path)
    except Exception as e:
        print(f"Error setting Windows permissions: {e}")
        return False


def _set_unix_permissions(file_path: Path) -> bool:
    """Sets Unix-specific permissions (chmod)"""
    try:
        # 0o600 = Read/write for owner only
        # 0o700 = Read/write/execute for owner only (directories)
        if file_path.is_dir():
            os.chmod(file_path, 0o700)
        else:
            os.chmod(file_path, 0o600)
        return True
    except Exception as e:
        print(f"Error setting Unix permissions: {e}")
        return False


def _set_basic_permissions(file_path: Path) -> bool:
    """
    Fallback method using basic Python os module
    Less secure than native ACLs but better than nothing
    """
    try:
        if file_path.is_dir():
            os.chmod(file_path, 0o700)
        else:
            os.chmod(file_path, 0o600)
        return True
    except Exception as e:
        print(f"Error setting basic permissions: {e}")
        return False


def set_restricted_permissions_recursive(dir_path: Path) -> bool:
    """
    Recursively sets restricted permissions on directory and all contents

    Args:
        dir_path: Path to directory

    Returns:
        bool: Success status (True if all succeeded)
    """
    try:
        if not dir_path.exists():
            return False

        success = True

        # Set permissions on root directory
        if not set_restricted_permissions(dir_path):
            success = False

        # Set permissions on all files and subdirectories
        for root, dirs, files in os.walk(dir_path):
            root_path = Path(root)

            # Set permissions on directories
            for dir_name in dirs:
                dir_full_path = root_path / dir_name
                if not set_restricted_permissions(dir_full_path):
                    success = False

            # Set permissions on files
            for file_name in files:
                file_path = root_path / file_name
                if not set_restricted_permissions(file_path):
                    success = False

        return success

    except Exception as e:
        print(f"Error setting recursive permissions: {e}")
        return False
