"""
Graphical User Interface for Encrypt-D
Modern application for encrypted folder management
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import shutil
from typing import Optional

from core.config import *
from encryption import CryptoManager
from authentication import AuthManager
from i18n import Translator


class EncryptDGUI:
    """Main graphical interface"""

    def __init__(self):
        self.root = tk.Tk()

        # Initialize translator
        self.translator = Translator()

        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)

        # Managers
        self.crypto_manager = CryptoManager(VAULT_DIR)
        self.auth_manager = AuthManager(AUTH_FILE, MAX_LOGIN_ATTEMPTS)

        # State
        self.authenticated = False
        self.current_password = None

        # Configure modern style
        self._setup_modern_style()

        # Check initial state
        if self.auth_manager.is_locked():
            self._show_locked_screen()
        elif not self.auth_manager.has_password():
            self._show_setup_screen()
        else:
            self._show_login_screen()

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

        frame = ttk.Frame(self.root, padding=50)
        frame.place(relx=0.5, rely=0.5, anchor="center")

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
        password_entry = ttk.Entry(frame, show="*", font=("Segoe UI", 12), width=35)
        password_entry.pack(pady=5, ipady=8)

        ttk.Label(frame, text=self._translate("setup.confirm_label")).pack(pady=(10, 5))
        confirm_entry = ttk.Entry(frame, show="*", font=("Segoe UI", 12), width=35)
        confirm_entry.pack(pady=5, ipady=8)

        # Security information
        info_text = (
            self._translate("setup.warning_title")
            + "\n\n"
            + self._translate("setup.warning_text", max_attempts=MAX_LOGIN_ATTEMPTS)
        )

        ttk.Label(
            frame, text=info_text, justify="left", foreground=self.colors["warning"]
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

            success, message = self.auth_manager.set_password(password)

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

        # Remaining attempts
        attempts_remaining = self.auth_manager.get_attempts_remaining()
        color = (
            self.colors["error"] if attempts_remaining <= 2 else self.colors["warning"]
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
                self.current_password = password
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

        # Encrypt
        success, message = self.crypto_manager.encrypt_folder(
            folder_path, self.current_password, result["name"] or None
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
                    shutil.rmtree(folder_path)
                    messagebox.showinfo(
                        self._translate("success.title"),
                        self._translate("locked.success"),
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

        # Decrypt
        success, message = self.crypto_manager.decrypt_folder(
            full_id, self.current_password, output_path
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
                self.current_password = new_pass
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
            self.current_password = None
            self._show_login_screen()

    def run(self):
        """Starts the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = EncryptDGUI()
    app.run()
