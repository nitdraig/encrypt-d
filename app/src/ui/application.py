"""
Graphical User Interface for Encrypt-D
Modern application for encrypted folder management
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import shutil
import time
from typing import Optional

from core.config import (
    APP_NAME,
    APP_VERSION,
    AUTH_FILE,
    VAULT_DIR,
    MAX_LOGIN_ATTEMPTS,
    MIN_LOGIN_ATTEMPTS,
    MAX_LOGIN_ATTEMPTS_LIMIT,
)
from core import VersionManager
from core.security_logger import init_security_logger, get_logger
from core.secure_string import SecurePassword
from encryption import CryptoManager
from authentication import AuthManager
from i18n import Translator


class EncryptDGUI:
    """Main graphical interface"""

    def __init__(self):
        self.root = tk.Tk()

        # Initialize translator
        self.translator = Translator()

        # Initialize security logger
        log_dir = VAULT_DIR / "logs"
        init_security_logger(log_dir)
        logger = get_logger()
        if logger:
            logger.log_app_started()

        self.root.title(f"{APP_NAME} v{APP_VERSION}")

        # Set window icon
        self._set_window_icon()

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set minimum window size
        self.root.minsize(800, 600)

        # Calculate optimal window size (80% of screen, max 1400x900)
        window_width = min(int(screen_width * 0.8), 1400)
        window_height = min(int(screen_height * 0.8), 900)

        # Calculate position to center window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(True, True)

        # Version Manager - check for migrations BEFORE initializing other managers
        self.version_manager = VersionManager()
        self._handle_version_migration()

        # Managers
        self.crypto_manager = CryptoManager(VAULT_DIR)
        self.auth_manager = AuthManager(AUTH_FILE, MAX_LOGIN_ATTEMPTS)

        # State
        self.authenticated = False
        self.secure_password = (
            SecurePassword()
        )  # Secure password storage (CRIT-002 fix)

        # Session timeout (15 minutes of inactivity)
        self.session_timeout = 15 * 60 * 1000  # milliseconds
        self.last_activity = None
        self.timeout_check_id = None

        # Configure modern style
        self._setup_modern_style()

        # Configure window close handler
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # Bind activity events for session timeout
        self.root.bind_all("<Key>", lambda e: self._reset_activity_timer())
        self.root.bind_all("<Button>", lambda e: self._reset_activity_timer())

        # Check initial state
        if self.auth_manager.is_locked():
            self._show_locked_screen()
        elif not self.auth_manager.has_password():
            self._show_setup_screen()
        else:
            self._show_login_screen()

    def _set_window_icon(self):
        """Sets the window icon for the application"""
        try:
            # Try to find icon.ico in multiple locations
            import os
            import sys

            # Get base path (works for both dev and PyInstaller)
            if getattr(sys, "frozen", False):
                # Running as compiled executable
                base_path = sys._MEIPASS
            else:
                # Running in development
                base_path = Path(__file__).parent.parent.parent

            # Possible icon locations
            icon_paths = [
                Path(base_path) / "icon.ico",  # Root of app
                Path(base_path) / "app" / "icon.ico",  # In app folder
                Path(__file__).parent.parent.parent
                / "icon.ico",  # Relative to this file
            ]

            # Try each path
            for icon_path in icon_paths:
                if icon_path.exists():
                    self.root.iconbitmap(str(icon_path))
                    return

            # If no icon found, log but don't crash
            print("Warning: icon.ico not found, using default icon")

        except Exception as e:
            # If anything fails, just use default icon
            print(f"Warning: Could not set window icon: {e}")

    def _handle_version_migration(self):
        """Handles version detection and migration if needed"""
        try:
            # Check if migration is needed
            needs_migration, from_version, to_version = (
                self.version_manager.needs_migration()
            )

            if needs_migration:
                # Show migration dialog
                self._show_migration_dialog(from_version, to_version)
            else:
                # First install or same version
                info = self.version_manager.get_migration_info()
                if info["is_first_install"]:
                    # Save version on first install
                    self.version_manager.save_version()
                    print(f"First install: v{to_version}")
                else:
                    print(f"Version up to date: v{to_version}")

        except Exception as e:
            print(f"Warning: Version check failed: {e}")
            # Continue anyway, don't block the app

    def _show_migration_dialog(self, from_version: str, to_version: str):
        """Shows migration dialog and performs migration"""
        # Hide main window during migration
        self.root.withdraw()

        # Create migration dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Required")
        dialog.geometry("600x400")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 600) // 2
        y = (dialog.winfo_screenheight() - 400) // 2
        dialog.geometry(f"600x400+{x}+{y}")

        # Content
        main_frame = ttk.Frame(dialog, padding=30)
        main_frame.pack(fill="both", expand=True)

        # Title
        ttk.Label(
            main_frame,
            text="🔄 Update Detected",
            font=("Segoe UI", 18, "bold"),
        ).pack(pady=(0, 20))

        # Message
        message = f"""Encrypt-D is being updated from version {from_version} to {to_version}.

Your data will be automatically migrated to the new version.

A backup of your current data will be created before the update.

This process is safe and automatic."""

        ttk.Label(
            main_frame,
            text=message,
            wraplength=500,
            justify="left",
            font=("Segoe UI", 10),
        ).pack(pady=(0, 20))

        # Progress label
        progress_label = ttk.Label(
            main_frame,
            text="Click 'Update Now' to continue",
            font=("Segoe UI", 10, "italic"),
        )
        progress_label.pack(pady=(0, 20))

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(20, 0))

        def perform_migration():
            # Update progress
            progress_label.config(text="Creating backup...")
            dialog.update()

            # Perform migration
            success, message = self.version_manager.migrate(from_version, to_version)

            if success:
                progress_label.config(text="✅ " + message)
                dialog.update()
                # Close dialog and show main window after 2 seconds
                dialog.after(2000, lambda: (dialog.destroy(), self.root.deiconify()))
            else:
                progress_label.config(text="❌ " + message)
                messagebox.showerror("Migration Failed", message, parent=dialog)
                # Close app on migration failure
                dialog.destroy()
                self.root.destroy()

        ttk.Button(
            button_frame,
            text="Update Now",
            command=perform_migration,
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Exit",
            command=lambda: (dialog.destroy(), self.root.destroy()),
        ).pack(side="left", padx=5)

    def _setup_modern_style(self):
        """Configures modern visual style for the application"""
        style = ttk.Style()
        style.theme_use("clam")

        # Modern color palette
        self.colors = {
            "bg_primary": "#1a1a2e",
            "bg_secondary": "#16213e",
            "bg_tertiary": "#0f3460",
            "accent": "#00adb5",
            "accent_hover": "#00d9e6",
            "text_primary": "#eeeeee",
            "text_secondary": "#aaaaaa",
            "error": "#ff4757",
            "success": "#2ed573",
            "warning": "#ffa502",
        }

        self.root.configure(bg=self.colors["bg_primary"])

        # Custom styles
        style.configure("TFrame", background=self.colors["bg_primary"])
        style.configure("Secondary.TFrame", background=self.colors["bg_secondary"])
        style.configure(
            "Card.TFrame", background=self.colors["bg_secondary"], relief="flat"
        )

        style.configure(
            "TLabel",
            background=self.colors["bg_primary"],
            foreground=self.colors["text_primary"],
            font=("Segoe UI", 10),
        )
        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 28, "bold"),
            foreground=self.colors["accent"],
        )
        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 12),
            foreground=self.colors["text_secondary"],
        )
        style.configure(
            "Header.TLabel",
            font=("Segoe UI", 18, "bold"),
            foreground=self.colors["accent"],
        )

        # Button styles
        style.configure(
            "Accent.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=12,
            background=self.colors["accent"],
            foreground=self.colors["text_primary"],
            borderwidth=0,
            focuscolor="none",
        )
        style.map(
            "Accent.TButton",
            background=[("active", self.colors["accent_hover"])],
            foreground=[("active", self.colors["text_primary"])],
        )

        # Entry style
        style.configure(
            "Modern.TEntry",
            fieldbackground=self.colors["bg_tertiary"],
            foreground=self.colors["text_primary"],
            borderwidth=2,
            relief="flat",
        )

        # Combobox style for language selector
        style.configure(
            "Modern.TCombobox",
            fieldbackground=self.colors["bg_tertiary"],
            background=self.colors["bg_secondary"],
            foreground=self.colors["text_primary"],
            arrowcolor=self.colors["accent"],
            borderwidth=1,
        )

        # Treeview style
        style.configure(
            "Modern.Treeview",
            background=self.colors["bg_secondary"],
            foreground=self.colors["text_primary"],
            fieldbackground=self.colors["bg_secondary"],
            borderwidth=0,
        )
        style.configure(
            "Modern.Treeview.Heading",
            background=self.colors["bg_tertiary"],
            foreground=self.colors["text_primary"],
            relief="flat",
        )
        style.map(
            "Modern.Treeview",
            background=[("selected", self.colors["accent"])],
            foreground=[("selected", self.colors["text_primary"])],
        )

        # Checkbutton style
        style.configure(
            "TCheckbutton",
            background=self.colors["bg_secondary"],
            foreground=self.colors["text_primary"],
            font=("Segoe UI", 11),
        )
        style.map(
            "TCheckbutton",
            foreground=[("active", self.colors["accent"])],
        )

    def _translate(self, key: str, **kwargs) -> str:
        """Helper to get translated text"""
        return self.translator.get(key, **kwargs)

    def _change_language(self, lang_code: str):
        """Changes the application language"""
        self.translator.set_language(lang_code)
        # Reload current screen
        if self.authenticated:
            self._show_main_screen()
        elif self.auth_manager.is_locked():
            self._show_locked_screen()
        elif not self.auth_manager.has_password():
            self._show_setup_screen()
        else:
            self._show_login_screen()

    def _clear_window(self):
        """Clears all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def _create_language_selector(self, parent):
        """Creates a modern language selector"""
        lang_frame = ttk.Frame(parent)

        languages = [
            ("en", self._translate("language.en")),
            ("es", self._translate("language.es")),
        ]

        current_lang_name = dict(languages).get(
            self.translator.current_language, "English"
        )

        lang_var = tk.StringVar(value=current_lang_name)
        lang_combo = ttk.Combobox(
            lang_frame,
            textvariable=lang_var,
            values=[name for _, name in languages],
            state="readonly",
            width=12,
            style="Modern.TCombobox",
            font=("Segoe UI", 9),
        )

        def on_language_change(event):
            selected_name = lang_var.get()
            lang_code = next(
                (code for code, name in languages if name == selected_name), "en"
            )
            self._change_language(lang_code)

        lang_combo.bind("<<ComboboxSelected>>", on_language_change)
        lang_combo.pack(side="right", padx=5)

        ttk.Label(lang_frame, text="🌐", font=("Segoe UI", 12)).pack(
            side="right", padx=(0, 5)
        )

        return lang_frame

    def _show_locked_screen(self):
        """Displays permanent lock screen"""
        self._clear_window()

        # Language selector at top
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill="x")
        lang_selector = self._create_language_selector(top_frame)
        lang_selector.pack(side="right")

        frame = ttk.Frame(self.root, padding=50)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Alert icon
        ttk.Label(
            frame, text="⚠️", font=("Segoe UI", 72), foreground=self.colors["error"]
        ).pack(pady=20)

        # Message
        ttk.Label(
            frame,
            text=self._translate("locked.title"),
            style="Title.TLabel",
            foreground=self.colors["error"],
        ).pack(pady=10)

        ttk.Label(
            frame,
            text=self._translate("locked.message"),
            style="Subtitle.TLabel",
            justify="center",
        ).pack(pady=20)

        ttk.Button(
            frame,
            text=self._translate("locked.button_reset"),
            command=self._reset_application,
            style="Accent.TButton",
        ).pack(pady=10)

    def _reset_application(self):
        """Resets the application completely"""
        response = messagebox.askyesno(
            self._translate("locked.confirm_title"),
            self._translate("locked.confirm_message"),
            icon="warning",
        )

        if response:
            # Destroy all data
            self.crypto_manager.destroy_all_data()
            self.auth_manager.reset_auth_data()

            # Reload application
            self.__init__()

    def _show_setup_screen(self):
        """Displays initial setup screen"""
        self._clear_window()

        # Language selector at top
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill="x")
        lang_selector = self._create_language_selector(top_frame)
        lang_selector.pack(side="right")

        # Main container with scrollbar capability
        main_container = ttk.Frame(self.root)
        main_container.pack(fill="both", expand=True)

        # Canvas for scrolling
        canvas = tk.Canvas(
            main_container, bg=self.colors["bg_primary"], highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            main_container, orient="vertical", command=canvas.yview
        )
        scrollable_frame = ttk.Frame(canvas)

        def _on_canvas_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Center content: canvas window full width and horizontally centered
            cw = event.width
            canvas.itemconfig(canvas_window_id, width=cw)
            canvas.coords(canvas_window_id, (cw // 2, 0))

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas_window_id = canvas.create_window(
            (0, 0), window=scrollable_frame, anchor="n"
        )
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", _on_canvas_configure)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Form frame centered within the scroll area
        frame = ttk.Frame(scrollable_frame, padding=30)
        frame.pack(pady=20, anchor="center")

        # Title
        ttk.Label(
            frame, text=self._translate("setup.welcome_title"), style="Title.TLabel"
        ).pack(pady=20)

        ttk.Label(
            frame,
            text=self._translate("setup.welcome_subtitle"),
            style="Subtitle.TLabel",
        ).pack(pady=10)

        # Password fields
        ttk.Label(frame, text=self._translate("setup.password_label")).pack(
            pady=(30, 5)
        )
        password_entry = ttk.Entry(frame, show="*", font=("Segoe UI", 12), width=45)
        password_entry.pack(pady=5, ipady=8)

        ttk.Label(frame, text=self._translate("setup.confirm_label")).pack(pady=(10, 5))
        confirm_entry = ttk.Entry(frame, show="*", font=("Segoe UI", 12), width=45)
        confirm_entry.pack(pady=5, ipady=8)

        # Password requirements info
        requirements_frame = ttk.Frame(frame, style="Card.TFrame", padding=15)
        requirements_frame.pack(pady=15, fill="x")

        ttk.Label(
            requirements_frame,
            text=self._translate("password.requirements"),
            justify="left",
            font=("Segoe UI", 10),
            foreground=self.colors["text_primary"],  # Lighter text for better contrast
            background=self.colors["bg_secondary"],
            wraplength=550,
        ).pack(anchor="w", padx=5, pady=5)

        # Security Options Section
        security_frame = ttk.Frame(frame, style="Card.TFrame", padding=15)
        security_frame.pack(pady=20, fill="x")

        ttk.Label(
            security_frame,
            text=self._translate("setup.security_options_title"),
            font=("Segoe UI", 14, "bold"),
            foreground=self.colors["accent"],
            background=self.colors["bg_secondary"],
        ).pack(anchor="w", pady=(0, 15))

        # Auto-destroy checkbox
        auto_destroy_var = tk.BooleanVar(value=True)
        auto_destroy_check = ttk.Checkbutton(
            security_frame,
            text=self._translate("setup.auto_destroy_label"),
            variable=auto_destroy_var,
        )
        auto_destroy_check.pack(anchor="w", pady=5)

        # Max attempts frame (shown/hidden based on checkbox)
        attempts_frame = ttk.Frame(security_frame, style="Card.TFrame")
        attempts_frame.pack(fill="x", pady=10)

        ttk.Label(
            attempts_frame,
            text=self._translate("setup.max_attempts_label"),
            background=self.colors["bg_secondary"],
            foreground=self.colors["text_primary"],  # Lighter text for better contrast
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=5, padx=5)

        attempts_var = tk.IntVar(value=MAX_LOGIN_ATTEMPTS)
        attempts_spinbox = ttk.Spinbox(
            attempts_frame,
            from_=MIN_LOGIN_ATTEMPTS,
            to=MAX_LOGIN_ATTEMPTS_LIMIT,
            textvariable=attempts_var,
            width=10,
            font=("Segoe UI", 11),
        )
        attempts_spinbox.pack(anchor="w", pady=5)

        # Info label
        info_label = ttk.Label(
            attempts_frame,
            text=self._translate("setup.attempts_note"),
            font=("Segoe UI", 10),
            foreground="#ffb84d",  # Lighter orange for better contrast
            background=self.colors["bg_secondary"],
            wraplength=500,
            justify="left",
        )
        info_label.pack(anchor="w", pady=5, padx=5)

        # Toggle visibility of attempts options
        def toggle_attempts_options():
            if auto_destroy_var.get():
                for widget in attempts_frame.winfo_children():
                    widget.configure(state="normal")
                info_label.configure(text=self._translate("setup.attempts_note"))
            else:
                for widget in attempts_frame.winfo_children():
                    if isinstance(widget, ttk.Spinbox):
                        widget.configure(state="disabled")
                info_label.configure(text=self._translate("setup.no_limit_note"))

        auto_destroy_check.configure(command=toggle_attempts_options)

        # Security information
        info_text = (
            self._translate("setup.warning_title")
            + "\n\n"
            + self._translate("setup.warning_text")
        )

        ttk.Label(
            frame,
            text=info_text,
            justify="left",
            foreground="#ffb84d",  # Lighter orange for better contrast
            font=("Segoe UI", 10),
            wraplength=600,
        ).pack(pady=20)

        # Setup button
        def setup_password():
            password = password_entry.get()
            confirm = confirm_entry.get()

            if not password:
                messagebox.showerror(
                    self._translate("error.title"), self._translate("setup.error_empty")
                )
                return

            if password != confirm:
                messagebox.showerror(
                    self._translate("error.title"),
                    self._translate("setup.error_mismatch"),
                )
                return

            auto_destroy = auto_destroy_var.get()
            max_attempts = attempts_var.get()

            success, message = self.auth_manager.set_password(
                password, auto_destroy, max_attempts
            )

            if success:
                messagebox.showinfo(
                    self._translate("success.title"), self._translate("setup.success")
                )
                self._show_login_screen()
            else:
                messagebox.showerror(self._translate("error.title"), message)

        ttk.Button(
            frame,
            text=self._translate("setup.button_continue"),
            command=setup_password,
            style="Accent.TButton",
        ).pack(pady=20)

        # Bind Enter key
        confirm_entry.bind("<Return>", lambda e: setup_password())

        # Bind mouse wheel to scroll
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _show_login_screen(self):
        """Displays login screen"""
        self._clear_window()

        # Language selector at top
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill="x")
        lang_selector = self._create_language_selector(top_frame)
        lang_selector.pack(side="right")

        frame = ttk.Frame(self.root, padding=50)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        ttk.Label(
            frame, text=self._translate("login.title"), style="Title.TLabel"
        ).pack(pady=20)

        ttk.Label(
            frame, text=self._translate("login.subtitle"), style="Subtitle.TLabel"
        ).pack(pady=10)

        # Remaining attempts (only if auto-destroy is enabled)
        if self.auth_manager.is_auto_destroy_enabled():
            attempts_remaining = self.auth_manager.get_attempts_remaining()
            color = (
                self.colors["error"]
                if attempts_remaining <= 2
                else self.colors["warning"]
            )
            ttk.Label(
                frame,
                text=self._translate(
                    "login.attempts_remaining", attempts=attempts_remaining
                ),
                foreground=color,
                font=("Segoe UI", 10, "bold"),
            ).pack(pady=10)

        # Password field
        ttk.Label(frame, text=self._translate("login.password_label")).pack(
            pady=(30, 5)
        )
        password_entry = ttk.Entry(frame, show="*", font=("Segoe UI", 12), width=35)
        password_entry.pack(pady=5, ipady=8)
        password_entry.focus()

        # Login button
        def attempt_login():
            password = password_entry.get()

            if not password:
                messagebox.showerror(
                    self._translate("error.title"), self._translate("login.error_empty")
                )
                return

            success, message = self.auth_manager.verify_password(password)

            if success:
                self.authenticated = True
                self.secure_password.set(password)
                self._start_session_timer()
                self._show_main_screen()
            else:
                messagebox.showerror(self._translate("login.access_denied"), message)

                # Check if locked
                if self.auth_manager.is_locked():
                    # Destroy all data
                    self.crypto_manager.destroy_all_data()
                    self._show_locked_screen()
                else:
                    # Update counter and reload screen
                    self._show_login_screen()

        ttk.Button(
            frame,
            text=self._translate("login.button_login"),
            command=attempt_login,
            style="Accent.TButton",
        ).pack(pady=20)

        # Bind Enter key
        password_entry.bind("<Return>", lambda e: attempt_login())

    def _show_main_screen(self):
        """Displays main application screen"""
        self._clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # Modern header
        header = ttk.Frame(main_frame, padding=15, style="Secondary.TFrame")
        header.pack(fill="x")

        # App title
        title_frame = ttk.Frame(header, style="Secondary.TFrame")
        title_frame.pack(side="left")

        ttk.Label(
            title_frame,
            text=self._translate("main.header_title"),
            font=("Segoe UI", 20, "bold"),
            foreground=self.colors["accent"],
            background=self.colors["bg_secondary"],
        ).pack(side="left")

        # Right side buttons
        button_frame = ttk.Frame(header, style="Secondary.TFrame")
        button_frame.pack(side="right")

        # Language selector
        lang_selector = self._create_language_selector(button_frame)
        lang_selector.pack(side="right", padx=5)

        # About button
        ttk.Button(
            button_frame,
            text=self._translate("about.menu_item"),
            command=self._show_about_dialog,
            style="Accent.TButton",
        ).pack(side="right", padx=5)

        # Change password button
        ttk.Button(
            button_frame,
            text=self._translate("main.button_change_password"),
            command=self._change_password,
            style="Accent.TButton",
        ).pack(side="right", padx=5)

        # Logout button
        ttk.Button(
            button_frame,
            text=self._translate("main.button_logout"),
            command=self._logout,
            style="Accent.TButton",
        ).pack(side="right", padx=5)

        # Content area
        content = ttk.Frame(main_frame, padding=20)
        content.pack(fill="both", expand=True)

        # Action panel with modern cards
        action_panel = ttk.Frame(content)
        action_panel.pack(fill="x", pady=(0, 20))

        # Modern action buttons
        action_buttons = [
            (
                self._translate("main.button_add_folder"),
                self._add_folder,
                self.colors["success"],
            ),
            (
                self._translate("main.button_decrypt"),
                self._decrypt_folder,
                self.colors["accent"],
            ),
            (
                self._translate("main.button_delete"),
                self._delete_folder,
                self.colors["error"],
            ),
            (
                self._translate("main.button_refresh"),
                self._refresh_list,
                self.colors["text_secondary"],
            ),
        ]

        for text, command, color in action_buttons:
            btn = tk.Button(
                action_panel,
                text=text,
                command=command,
                font=("Segoe UI", 10, "bold"),
                bg=color,
                fg=self.colors["text_primary"],
                activebackground=color,
                activeforeground=self.colors["text_primary"],
                relief="flat",
                padx=20,
                pady=12,
                cursor="hand2",
                borderwidth=0,
            )
            btn.pack(side="left", padx=5)

        # Folders list with modern styling
        list_frame = ttk.Frame(content, style="Card.TFrame", padding=10)
        list_frame.pack(fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        # Treeview
        columns = ("name", "original_path", "status")
        self.folder_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="tree headings",
            yscrollcommand=scrollbar.set,
            height=18,
            style="Modern.Treeview",
        )

        self.folder_tree.heading("#0", text=self._translate("main.column_id"))
        self.folder_tree.heading("name", text=self._translate("main.column_name"))
        self.folder_tree.heading(
            "original_path", text=self._translate("main.column_path")
        )
        self.folder_tree.heading("status", text=self._translate("main.column_status"))

        self.folder_tree.column("#0", width=180)
        self.folder_tree.column("name", width=220)
        self.folder_tree.column("original_path", width=400)
        self.folder_tree.column("status", width=120)

        self.folder_tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.folder_tree.yview)

        # Load folders
        self._refresh_list()

        # Excelso footer
        self._add_excelso_footer(main_frame)

    def _add_excelso_footer(self, parent):
        """Adds Excelso branding footer"""
        from core.config import EXCELSO_COMPANY, EXCELSO_SLOGAN, EXCELSO_URL

        footer = ttk.Frame(parent, style="Secondary.TFrame", padding=10)
        footer.pack(fill="x", side="bottom")

        # Centered footer content
        footer_content = ttk.Frame(footer, style="Secondary.TFrame")
        footer_content.pack(anchor="center")

        # "Supported by Excelso" text
        supported_text = tk.Label(
            footer_content,
            text=f"Supported by {EXCELSO_COMPANY}",
            font=("Segoe UI", 9),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_secondary"],
            cursor="hand2",
        )
        supported_text.pack(side="left", padx=(0, 5))
        supported_text.bind("<Button-1>", lambda e: self._open_url(EXCELSO_URL))

        # Separator
        tk.Label(
            footer_content,
            text="•",
            font=("Segoe UI", 9),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_secondary"],
        ).pack(side="left", padx=5)

        # Slogan
        tk.Label(
            footer_content,
            text=EXCELSO_SLOGAN,
            font=("Segoe UI", 9, "italic"),
            fg=self.colors["accent"],
            bg=self.colors["bg_secondary"],
        ).pack(side="left", padx=(5, 0))

    def _open_url(self, url):
        """Opens URL in default browser"""
        import webbrowser

        webbrowser.open(url)

    def _show_about_dialog(self):
        """Displays about dialog with app information"""
        dialog = tk.Toplevel(self.root)
        dialog.title(self._translate("about.title"))
        dialog.geometry("700x650")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.colors["bg_primary"])

        # Make dialog non-resizable
        dialog.resizable(False, False)

        # Main frame with scrollbar
        main_frame = ttk.Frame(dialog, padding=30)
        main_frame.pack(fill="both", expand=True)

        # Title
        ttk.Label(
            main_frame, text=self._translate("about.title"), style="Header.TLabel"
        ).pack(pady=(0, 10))

        # Version
        ttk.Label(
            main_frame,
            text=f"{self._translate('about.version_label')} {APP_VERSION}",
            font=("Segoe UI", 10),
            foreground=self.colors["text_secondary"],
        ).pack(pady=(0, 20))

        # Description
        desc_frame = ttk.Frame(main_frame, style="Card.TFrame", padding=15)
        desc_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(
            desc_frame,
            text=self._translate("about.description"),
            wraplength=600,
            justify="left",
            font=("Segoe UI", 10),
            background=self.colors["bg_secondary"],
        ).pack()

        # Features
        features_frame = ttk.Frame(main_frame, style="Card.TFrame", padding=15)
        features_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(
            features_frame,
            text=self._translate("about.features_title"),
            font=("Segoe UI", 12, "bold"),
            foreground=self.colors["accent"],
            background=self.colors["bg_secondary"],
        ).pack(anchor="w", pady=(0, 10))

        for feature in self._translate("about.features"):
            ttk.Label(
                features_frame,
                text=feature,
                font=("Segoe UI", 9),
                background=self.colors["bg_secondary"],
            ).pack(anchor="w", pady=2)

        # How it works
        how_frame = ttk.Frame(main_frame, style="Card.TFrame", padding=15)
        how_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(
            how_frame,
            text=self._translate("about.how_it_works_title"),
            font=("Segoe UI", 12, "bold"),
            foreground=self.colors["accent"],
            background=self.colors["bg_secondary"],
        ).pack(anchor="w", pady=(0, 10))

        for step in self._translate("about.how_it_works"):
            ttk.Label(
                how_frame,
                text=step,
                font=("Segoe UI", 9),
                wraplength=600,
                background=self.colors["bg_secondary"],
            ).pack(anchor="w", pady=2)

        # Security info
        security_frame = ttk.Frame(main_frame, style="Card.TFrame", padding=15)
        security_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(
            security_frame,
            text=self._translate("about.security_title"),
            font=("Segoe UI", 12, "bold"),
            foreground=self.colors["warning"],
            background=self.colors["bg_secondary"],
        ).pack(anchor="w", pady=(0, 10))

        ttk.Label(
            security_frame,
            text=self._translate(
                "about.security_info", max_attempts=MAX_LOGIN_ATTEMPTS
            ),
            font=("Segoe UI", 9),
            wraplength=600,
            justify="left",
            background=self.colors["bg_secondary"],
        ).pack(anchor="w")

        # Excelso branding section
        excelso_frame = ttk.Frame(main_frame, style="Card.TFrame", padding=15)
        excelso_frame.pack(fill="x", pady=(0, 20))

        from core.config import (
            EXCELSO_COMPANY,
            EXCELSO_SLOGAN,
            EXCELSO_URL,
            EXCELSO_DOMAIN,
        )

        ttk.Label(
            excelso_frame,
            text=f"Supported by {EXCELSO_COMPANY}",
            font=("Segoe UI", 12, "bold"),
            foreground=self.colors["accent"],
            background=self.colors["bg_secondary"],
        ).pack(anchor="w", pady=(0, 5))

        ttk.Label(
            excelso_frame,
            text=EXCELSO_SLOGAN,
            font=("Segoe UI", 10, "italic"),
            foreground=self.colors["text_secondary"],
            background=self.colors["bg_secondary"],
        ).pack(anchor="w", pady=(0, 10))

        # Website link
        website_label = tk.Label(
            excelso_frame,
            text=EXCELSO_DOMAIN,
            font=("Segoe UI", 10, "underline"),
            foreground=self.colors["accent"],
            background=self.colors["bg_secondary"],
            cursor="hand2",
        )
        website_label.pack(anchor="w")
        website_label.bind("<Button-1>", lambda e: self._open_url(EXCELSO_URL))

        # Close button
        ttk.Button(
            main_frame,
            text=self._translate("about.button_close"),
            command=dialog.destroy,
            style="Accent.TButton",
        ).pack(pady=(10, 0))

    def _refresh_list(self):
        """Updates the list of encrypted folders"""
        # Clear list
        for item in self.folder_tree.get_children():
            self.folder_tree.delete(item)

        # Load folders
        folders = self.crypto_manager.get_encrypted_folders()

        for folder in folders:
            status_text = (
                self._translate("main.status_encrypted")
                if folder.get("encrypted", True)
                else self._translate("main.status_decrypted")
            )
            self.folder_tree.insert(
                "",
                "end",
                text=folder["id"][:16] + "...",
                values=(
                    folder["name"],
                    folder["original_path"],
                    status_text,
                ),
            )

    def _add_folder(self):
        """Adds and encrypts a new folder"""
        folder_path = filedialog.askdirectory(
            title=self._translate("folder.select_encrypt")
        )

        if not folder_path:
            return

        # Ask for custom name
        dialog = tk.Toplevel(self.root)
        dialog.title(self._translate("folder.name_dialog_title"))
        dialog.geometry("500x180")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.colors["bg_primary"])

        frame = ttk.Frame(dialog, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text=self._translate("folder.name_dialog_label")).pack(pady=10)

        name_entry = ttk.Entry(frame, font=("Segoe UI", 11), width=45)
        name_entry.pack(pady=10, ipady=5)
        name_entry.insert(0, Path(folder_path).name)

        result = {"confirmed": False, "name": ""}

        def confirm():
            result["confirmed"] = True
            result["name"] = name_entry.get()
            dialog.destroy()

        ttk.Button(
            frame,
            text=self._translate("folder.button_encrypt"),
            command=confirm,
            style="Accent.TButton",
        ).pack(pady=10)

        dialog.wait_window()

        if not result["confirmed"]:
            return

        # Confirm encryption
        response = messagebox.askyesno(
            self._translate("folder.confirm_encrypt_title"),
            self._translate(
                "folder.confirm_encrypt_message", name=Path(folder_path).name
            ),
        )

        if not response:
            return

        # Encrypt (using secure password method)
        success, message = self.crypto_manager.encrypt_folder_secure(
            folder_path, self.secure_password, result["name"] or None
        )

        if success:
            messagebox.showinfo(
                self._translate("success.title"),
                self._translate("success.folder_encrypted", id=message.split(": ")[-1]),
            )

            # Ask to delete original
            delete_original = messagebox.askyesno(
                self._translate("folder.delete_original_title"),
                self._translate("folder.delete_original_message"),
            )

            if delete_original:
                try:
                    # Import secure delete function
                    from encryption.crypto_manager import secure_delete_directory

                    # Securely delete original folder
                    if secure_delete_directory(Path(folder_path), passes=3):
                        messagebox.showinfo(
                            self._translate("success.title"),
                            self._translate("locked.success"),
                        )
                    else:
                        messagebox.showerror(
                            self._translate("error.title"),
                            "Could not securely delete folder",
                        )
                except Exception as e:
                    messagebox.showerror(
                        self._translate("error.title"),
                        self._translate("error.cannot_delete_original", error=str(e)),
                    )

            self._refresh_list()
        else:
            messagebox.showerror(self._translate("error.title"), message)

    def _decrypt_folder(self):
        """Decrypts a selected folder"""
        selection = self.folder_tree.selection()

        if not selection:
            messagebox.showwarning(
                self._translate("warning.title"),
                self._translate("folder.select_warning"),
            )
            return

        item = selection[0]
        folder_id = self.folder_tree.item(item, "text").replace("...", "")

        # Find full ID
        folders = self.crypto_manager.get_encrypted_folders()
        full_id = None
        folder_name = None

        for folder in folders:
            if folder["id"].startswith(folder_id):
                full_id = folder["id"]
                folder_name = folder["name"]
                break

        if not full_id:
            messagebox.showerror(
                self._translate("error.title"), self._translate("folder.not_found")
            )
            return

        # Ask for output location
        output_path = filedialog.askdirectory(
            title=self._translate("folder.select_decrypt")
        )

        if not output_path:
            return

        # Decrypt (using secure password method)
        success, message = self.crypto_manager.decrypt_folder_secure(
            full_id, self.secure_password, output_path
        )

        if success:
            messagebox.showinfo(
                self._translate("success.title"),
                self._translate(
                    "success.folder_decrypted", path=message.split(": ")[-1]
                ),
            )
        else:
            messagebox.showerror(self._translate("error.title"), message)

    def _delete_folder(self):
        """Permanently deletes an encrypted folder"""
        selection = self.folder_tree.selection()

        if not selection:
            messagebox.showwarning(
                self._translate("warning.title"),
                self._translate("folder.select_warning"),
            )
            return

        item = selection[0]
        folder_id = self.folder_tree.item(item, "text").replace("...", "")
        folder_name = self.folder_tree.item(item, "values")[0]

        # Find full ID
        folders = self.crypto_manager.get_encrypted_folders()
        full_id = None

        for folder in folders:
            if folder["id"].startswith(folder_id):
                full_id = folder["id"]
                break

        if not full_id:
            messagebox.showerror(
                self._translate("error.title"), self._translate("folder.not_found")
            )
            return

        # Confirm deletion
        response = messagebox.askyesno(
            self._translate("folder.confirm_delete_title"),
            self._translate("folder.confirm_delete_message", name=folder_name),
            icon="warning",
        )

        if not response:
            return

        # Delete
        success, message = self.crypto_manager.delete_encrypted_folder(full_id)

        if success:
            messagebox.showinfo(
                self._translate("success.title"),
                self._translate("success.folder_deleted"),
            )
            self._refresh_list()
        else:
            messagebox.showerror(self._translate("error.title"), message)

    def _change_password(self):
        """Changes the master password"""
        dialog = tk.Toplevel(self.root)
        dialog.title(self._translate("password.change_title"))
        dialog.geometry("500x350")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.colors["bg_primary"])

        frame = ttk.Frame(dialog, padding=30)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text=self._translate("password.current_label")).pack(
            pady=(10, 5)
        )
        old_pass_entry = ttk.Entry(frame, show="*", font=("Segoe UI", 11), width=40)
        old_pass_entry.pack(pady=5, ipady=5)

        ttk.Label(frame, text=self._translate("password.new_label")).pack(pady=(10, 5))
        new_pass_entry = ttk.Entry(frame, show="*", font=("Segoe UI", 11), width=40)
        new_pass_entry.pack(pady=5, ipady=5)

        ttk.Label(frame, text=self._translate("password.confirm_label")).pack(
            pady=(10, 5)
        )
        confirm_pass_entry = ttk.Entry(frame, show="*", font=("Segoe UI", 11), width=40)
        confirm_pass_entry.pack(pady=5, ipady=5)

        def change():
            old_pass = old_pass_entry.get()
            new_pass = new_pass_entry.get()
            confirm_pass = confirm_pass_entry.get()

            if not all([old_pass, new_pass, confirm_pass]):
                messagebox.showerror(
                    self._translate("error.title"),
                    self._translate("password.error_empty"),
                )
                return

            if new_pass != confirm_pass:
                messagebox.showerror(
                    self._translate("error.title"),
                    self._translate("password.error_mismatch"),
                )
                return

            success, message = self.auth_manager.change_password(old_pass, new_pass)

            if success:
                self.secure_password.set(new_pass)
                messagebox.showinfo(
                    self._translate("success.title"),
                    self._translate("password.success"),
                )
                dialog.destroy()
            else:
                messagebox.showerror(self._translate("error.title"), message)

        ttk.Button(
            frame,
            text=self._translate("password.button_change"),
            command=change,
            style="Accent.TButton",
        ).pack(pady=30)

    def _logout(self):
        """Logs out the current session"""
        response = messagebox.askyesno(
            self._translate("main.button_logout"),
            self._translate("main.logout_confirm"),
        )

        if response:
            self.authenticated = False
            self.secure_password.clear()
            self._stop_session_timer()
            self._show_login_screen()

    def _reset_activity_timer(self):
        """Resets the inactivity timer"""
        if self.authenticated:
            self.last_activity = time.time()

    def _check_session_timeout(self):
        """Checks if session has timed out due to inactivity"""
        if not self.authenticated:
            return

        if self.last_activity is not None:
            elapsed = time.time() - self.last_activity
            if elapsed * 1000 >= self.session_timeout:
                self._handle_timeout()
                return

        # Schedule next check (every 30 seconds)
        self.timeout_check_id = self.root.after(30000, self._check_session_timeout)

    def _handle_timeout(self):
        """Handles session timeout"""
        if self.authenticated:
            self.authenticated = False
            self.secure_password.clear()
            self._stop_session_timer()
            messagebox.showwarning(
                self._translate("warning.title"),
                "Session expired due to inactivity. Please log in again.",
            )
            self._show_login_screen()

    def _start_session_timer(self):
        """Starts the session timeout monitoring"""
        self.last_activity = time.time()
        if self.timeout_check_id:
            self.root.after_cancel(self.timeout_check_id)
        self.timeout_check_id = self.root.after(30000, self._check_session_timeout)

    def _stop_session_timer(self):
        """Stops the session timeout monitoring"""
        if self.timeout_check_id:
            self.root.after_cancel(self.timeout_check_id)
            self.timeout_check_id = None
        self.last_activity = None

    def _on_close(self):
        """Handles application close event"""
        # Clear password from memory before closing
        self.secure_password.clear()

        logger = get_logger()
        if logger:
            logger.log_app_closed()
        self.root.destroy()

    def run(self):
        """Starts the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = EncryptDGUI()
    app.run()
