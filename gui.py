"""
gui.py
======
Graphical User Interface — ResearchOps Multi-Agent Pipeline

Dark-mode desktop GUI built with tkinter.

Features:
- First-run API key setup screen (saved locally to config.json)
- API key is never hardcoded or shared — each user provides their own
- Mock Mode / Live Mode toggle
- Live console output streamed in real time
- Open output folder button
- Settings screen to update API key at any time

Usage:
    python gui.py
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import sys
import os
import json

# ---------------------------------------------------------------------------
# Colour Palette — dark mode
# ---------------------------------------------------------------------------

BG_DARK      = "#1e1e2e"
BG_PANEL     = "#2a2a3e"
BG_INPUT     = "#313147"
ACCENT       = "#7c6af7"
ACCENT_HOVER = "#6a58e0"
TEXT_PRIMARY = "#cdd6f4"
TEXT_DIM     = "#6c7086"
SUCCESS      = "#a6e3a1"
WARNING      = "#f9e2af"
ERROR        = "#f38ba8"
MOCK_COLOUR  = "#89dceb"

# ---------------------------------------------------------------------------
# Config — local storage for API key
# ---------------------------------------------------------------------------
# The API key is saved to config.json in the same folder as the app.
# It never leaves the user's machine.
# ---------------------------------------------------------------------------

CONFIG_FILE = "config.json"


def load_config() -> dict:
    """Load config from disk. Returns empty dict if file doesn't exist."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def save_config(data: dict):
    """Save config dict to disk as JSON."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ---------------------------------------------------------------------------
# Setup Screen — shown on first run or when user wants to change key
# ---------------------------------------------------------------------------

class SetupScreen:
    """
    First-run screen that collects the user's Anthropic API key.

    Shown automatically when no key is found in config.json.
    Can also be triggered from the main screen via the Settings button.
    Once saved, the key is stored locally and loaded automatically on future runs.
    """

    def __init__(self, root, on_complete):
        """
        Args:
            root: The tkinter root window.
            on_complete: Callback function called after key is saved successfully.
        """
        self.root = root
        self.on_complete = on_complete
        self.root.title("ResearchOps — Setup")
        self.root.geometry("620x580")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)
        self._build_ui()

    def _build_ui(self):
        """Build the setup screen UI."""

        # Header
        header = tk.Frame(self.root, bg=BG_DARK, pady=30)
        header.pack(fill="x", padx=40)

        tk.Label(
            header,
            text="ResearchOps",
            font=("Helvetica", 26, "bold"),
            fg=ACCENT,
            bg=BG_DARK
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Multi-Agent AI Research Pipeline",
            font=("Helvetica", 11),
            fg=TEXT_DIM,
            bg=BG_DARK
        ).pack(anchor="w")

        # Divider
        tk.Frame(self.root, bg=BG_PANEL, height=1).pack(fill="x", padx=40)

        # Main panel
        panel = tk.Frame(self.root, bg=BG_PANEL, padx=24, pady=24)
        panel.pack(fill="x", padx=40, pady=24)

        tk.Label(
            panel,
            text="Welcome! To use Live Mode, enter your Anthropic API key below.",
            font=("Helvetica", 11),
            fg=TEXT_PRIMARY,
            bg=BG_PANEL,
            wraplength=520,
            justify="left"
        ).pack(anchor="w", pady=(0, 4))

        tk.Label(
            panel,
            text="Your key is stored locally on your machine only and never shared.",
            font=("Helvetica", 10),
            fg=TEXT_DIM,
            bg=BG_PANEL,
            wraplength=520,
            justify="left"
        ).pack(anchor="w", pady=(0, 16))

        # API key label
        tk.Label(
            panel,
            text="Anthropic API Key",
            font=("Helvetica", 11, "bold"),
            fg=TEXT_PRIMARY,
            bg=BG_PANEL
        ).pack(anchor="w", pady=(0, 6))

        # API key input
        self.key_entry = tk.Entry(
            panel,
            font=("Helvetica", 11),
            bg=BG_INPUT,
            fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY,
            relief="flat",
            show="*"  # Mask the key like a password field
        )
        self.key_entry.pack(fill="x", ipady=10, padx=2, pady=(0, 8))

        # Show/hide toggle
        self.show_key = tk.BooleanVar(value=False)
        tk.Checkbutton(
            panel,
            text="Show key",
            variable=self.show_key,
            font=("Helvetica", 10),
            fg=TEXT_DIM,
            bg=BG_PANEL,
            selectcolor=BG_INPUT,
            activebackground=BG_PANEL,
            activeforeground=TEXT_DIM,
            command=self._toggle_key_visibility
        ).pack(anchor="w", pady=(0, 16))

        # Get a key link
        tk.Label(
            panel,
            text="Don't have a key? Get one free at console.anthropic.com",
            font=("Helvetica", 10),
            fg=ACCENT,
            bg=BG_PANEL,
            cursor="hand2"
        ).pack(anchor="w", pady=(0, 4))

        # Note about mock mode
        tk.Label(
            panel,
            text="You can also skip this and use Mock Mode for free — no key needed.",
            font=("Helvetica", 10),
            fg=TEXT_DIM,
            bg=BG_PANEL,
            wraplength=520,
            justify="left"
        ).pack(anchor="w")

        # Buttons
        btn_frame = tk.Frame(self.root, bg=BG_DARK)
        btn_frame.pack(fill="x", padx=40, pady=(0, 20))

        tk.Button(
            btn_frame,
            text="Save Key & Continue",
            font=("Helvetica", 11, "bold"),
            fg="white",
            bg=ACCENT,
            activebackground=ACCENT_HOVER,
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self._save_key
        ).pack(side="left")

        tk.Button(
            btn_frame,
            text="Skip — Use Mock Mode Only",
            font=("Helvetica", 11),
            fg=TEXT_DIM,
            bg=BG_PANEL,
            activebackground=BG_INPUT,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self._skip
        ).pack(side="left", padx=(12, 0))

        # Load existing key if present
        config = load_config()
        if config.get("api_key"):
            self.key_entry.insert(0, config["api_key"])

    def _toggle_key_visibility(self):
        """Show or hide the API key characters."""
        self.key_entry.config(show="" if self.show_key.get() else "*")

    def _save_key(self):
        """Validate and save the API key to config.json."""
        key = self.key_entry.get().strip()

        if not key.startswith("sk-ant-"):
            messagebox.showerror(
                "Invalid Key",
                "That doesn't look like a valid Anthropic API key.\n\n"
                "Keys start with: sk-ant-"
            )
            return

        # Save to config and set as environment variable for this session
        save_config({"api_key": key})
        os.environ["ANTHROPIC_API_KEY"] = key

        self.on_complete()

    def _skip(self):
        """Skip key entry and continue in mock-mode-only mode."""
        save_config({"api_key": ""})
        self.on_complete()


# ---------------------------------------------------------------------------
# Main Application Screen
# ---------------------------------------------------------------------------

class ResearchOpsGUI:
    """
    Main GUI screen for ResearchOps.

    Shown after setup is complete. Allows the user to enter a topic,
    choose mock or live mode, and run the full agent pipeline.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("ResearchOps — Multi-Agent Research Pipeline")
        self.root.geometry("900x700")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(True, True)
        self.mock_mode = tk.BooleanVar(value=True)

        # Check if a key is available — if not, lock live mode
        config = load_config()
        self.has_key = bool(config.get("api_key"))
        if self.has_key:
            os.environ["ANTHROPIC_API_KEY"] = config["api_key"]

        self._build_ui()
        self._check_live_mode_availability()

    def _build_ui(self):
        self._build_header()
        self._build_input_panel()
        self._build_controls()
        self._build_console()
        self._build_footer()

    # ---------------------------------------------------------------------------
    # UI Construction
    # ---------------------------------------------------------------------------

    def _build_header(self):
        header = tk.Frame(self.root, bg=BG_DARK, pady=20)
        header.pack(fill="x", padx=30)

        tk.Label(
            header,
            text="ResearchOps",
            font=("Helvetica", 28, "bold"),
            fg=ACCENT,
            bg=BG_DARK
        ).pack(side="left")

        # Settings button — top right
        tk.Button(
            header,
            text="⚙  Settings",
            font=("Helvetica", 10),
            fg=TEXT_DIM,
            bg=BG_DARK,
            activebackground=BG_PANEL,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            command=self._open_settings
        ).pack(side="right", pady=8)

        tk.Frame(self.root, bg=BG_PANEL, height=1).pack(fill="x", padx=30)

    def _build_input_panel(self):
        panel = tk.Frame(self.root, bg=BG_PANEL, padx=20, pady=20)
        panel.pack(fill="x", padx=30, pady=20)

        tk.Label(
            panel,
            text="Research Topic",
            font=("Helvetica", 11, "bold"),
            fg=TEXT_PRIMARY,
            bg=BG_PANEL
        ).pack(anchor="w", pady=(0, 6))

        self.topic_entry = tk.Text(
            panel,
            height=3,
            font=("Helvetica", 12),
            bg=BG_INPUT,
            fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY,
            relief="flat",
            padx=12,
            pady=10,
            wrap="word"
        )
        self.topic_entry.pack(fill="x", pady=(0, 16))
        self.topic_entry.insert("1.0", "artificial intelligence in healthcare 2025")
        self.topic_entry.bind("<FocusIn>", self._clear_placeholder)

        # Mode toggle
        mode_frame = tk.Frame(panel, bg=BG_PANEL)
        mode_frame.pack(fill="x")

        tk.Label(
            mode_frame,
            text="Mode",
            font=("Helvetica", 11, "bold"),
            fg=TEXT_PRIMARY,
            bg=BG_PANEL
        ).pack(side="left", padx=(0, 16))

        tk.Radiobutton(
            mode_frame,
            text="Mock Mode  (free — no API calls)",
            variable=self.mock_mode,
            value=True,
            font=("Helvetica", 11),
            fg=MOCK_COLOUR,
            bg=BG_PANEL,
            selectcolor=BG_INPUT,
            activebackground=BG_PANEL,
            activeforeground=MOCK_COLOUR,
            command=self._update_mode_label
        ).pack(side="left", padx=(0, 24))

        self.live_radio = tk.Radiobutton(
            mode_frame,
            text="Live Mode  (uses API credits)",
            variable=self.mock_mode,
            value=False,
            font=("Helvetica", 11),
            fg=WARNING,
            bg=BG_PANEL,
            selectcolor=BG_INPUT,
            activebackground=BG_PANEL,
            activeforeground=WARNING,
            command=self._update_mode_label
        )
        self.live_radio.pack(side="left")

    def _build_controls(self):
        controls = tk.Frame(self.root, bg=BG_DARK, pady=4)
        controls.pack(fill="x", padx=30)

        self.run_button = tk.Button(
            controls,
            text="▶  Run Pipeline",
            font=("Helvetica", 12, "bold"),
            fg="white",
            bg=ACCENT,
            activebackground=ACCENT_HOVER,
            activeforeground="white",
            relief="flat",
            padx=24,
            pady=10,
            cursor="hand2",
            command=self._run_pipeline
        )
        self.run_button.pack(side="left")

        tk.Button(
            controls,
            text="📁  Open Output Folder",
            font=("Helvetica", 11),
            fg=TEXT_DIM,
            bg=BG_PANEL,
            activebackground=BG_INPUT,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            padx=16,
            pady=10,
            cursor="hand2",
            command=self._open_output_folder
        ).pack(side="left", padx=(12, 0))

        self.mode_label = tk.Label(
            controls,
            text="● Mock Mode",
            font=("Helvetica", 11),
            fg=MOCK_COLOUR,
            bg=BG_DARK
        )
        self.mode_label.pack(side="right")

    def _build_console(self):
        console_frame = tk.Frame(self.root, bg=BG_DARK, padx=30, pady=8)
        console_frame.pack(fill="both", expand=True)

        tk.Label(
            console_frame,
            text="Console Output",
            font=("Helvetica", 10, "bold"),
            fg=TEXT_DIM,
            bg=BG_DARK
        ).pack(anchor="w", pady=(0, 6))

        self.console = scrolledtext.ScrolledText(
            console_frame,
            font=("Courier", 10),
            bg=BG_PANEL,
            fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY,
            relief="flat",
            padx=12,
            pady=10,
            state="disabled",
            wrap="word"
        )
        self.console.pack(fill="both", expand=True)

        self.console.tag_config("info",    foreground=TEXT_PRIMARY)
        self.console.tag_config("success", foreground=SUCCESS)
        self.console.tag_config("warning", foreground=WARNING)
        self.console.tag_config("error",   foreground=ERROR)
        self.console.tag_config("mock",    foreground=MOCK_COLOUR)
        self.console.tag_config("stage",   foreground=ACCENT)
        self.console.tag_config("dim",     foreground=TEXT_DIM)

    def _build_footer(self):
        footer = tk.Frame(self.root, bg=BG_DARK, pady=10)
        footer.pack(fill="x", padx=30)

        tk.Label(
            footer,
            text="Built by Ciaran Brennan  •  ResearchOps v1.0  •  Powered by Claude",
            font=("Helvetica", 9),
            fg=TEXT_DIM,
            bg=BG_DARK
        ).pack(side="left")

        # Key status indicator
        self.key_status = tk.Label(
            footer,
            text="🔑 API Key Saved" if self.has_key else "⚠ No API Key — Mock Mode Only",
            font=("Helvetica", 9),
            fg=SUCCESS if self.has_key else WARNING,
            bg=BG_DARK
        )
        self.key_status.pack(side="right")

    # ---------------------------------------------------------------------------
    # Event Handlers
    # ---------------------------------------------------------------------------

    def _check_live_mode_availability(self):
        """Disable live mode radio if no API key is configured."""
        if not self.has_key:
            self.live_radio.config(state="disabled")
            self._log("No API key found. Running in Mock Mode only.", "warning")
            self._log("Click ⚙ Settings to add your Anthropic API key.", "dim")

    def _clear_placeholder(self, event):
        current = self.topic_entry.get("1.0", "end-1c").strip()
        if current == "artificial intelligence in healthcare 2025":
            self.topic_entry.delete("1.0", tk.END)

    def _update_mode_label(self):
        if self.mock_mode.get():
            self.mode_label.config(text="● Mock Mode", fg=MOCK_COLOUR)
        else:
            self.mode_label.config(text="● Live Mode", fg=WARNING)

    def _open_output_folder(self):
        output_path = os.path.abspath("output")
        os.makedirs(output_path, exist_ok=True)
        os.startfile(output_path)

    def _open_settings(self):
        """Open the setup screen as a settings window."""
        settings_win = tk.Toplevel(self.root)
        SetupScreen(settings_win, on_complete=lambda: self._on_settings_saved(settings_win))

    def _on_settings_saved(self, window):
        """Called after user saves a new key in settings."""
        window.destroy()
        config = load_config()
        self.has_key = bool(config.get("api_key"))
        if self.has_key:
            os.environ["ANTHROPIC_API_KEY"] = config["api_key"]
            self.live_radio.config(state="normal")
            self.key_status.config(text="🔑 API Key Saved", fg=SUCCESS)
            self._log("API key updated. Live Mode is now available.", "success")
        else:
            self.live_radio.config(state="disabled")
            self.key_status.config(text="⚠ No API Key — Mock Mode Only", fg=WARNING)

    # ---------------------------------------------------------------------------
    # Pipeline Execution
    # ---------------------------------------------------------------------------

    def _run_pipeline(self):
        topic = self.topic_entry.get("1.0", "end-1c").strip()

        if not topic:
            self._log("Please enter a research topic.", "error")
            return

        if not self.mock_mode.get() and not self.has_key:
            self._log("No API key found. Please add one in Settings.", "error")
            return

        self.run_button.config(state="disabled", text="⏳  Running...")
        self.console.config(state="normal")
        self.console.delete("1.0", tk.END)
        self.console.config(state="disabled")

        thread = threading.Thread(
            target=self._pipeline_thread,
            args=(topic, self.mock_mode.get()),
            daemon=True
        )
        thread.start()

    def _pipeline_thread(self, topic: str, mock: bool):
        try:
            sys.stdout = ConsoleRedirector(self._log)

            import agents.researcher as researcher_module
            import agents.analyst   as analyst_module
            import agents.critic    as critic_module
            import agents.writer    as writer_module

            researcher_module.MOCK_MODE = mock
            analyst_module.MOCK_MODE    = mock
            critic_module.MOCK_MODE     = mock
            writer_module.MOCK_MODE     = mock

            from orchestrator import run_pipeline
            run_pipeline(topic)

            self._log("\n✓ Pipeline complete! Check the output/ folder.", "success")

        except Exception as e:
            self._log(f"\n✗ Error: {str(e)}", "error")

        finally:
            sys.stdout = sys.__stdout__
            self.root.after(0, self._reset_button)

    def _reset_button(self):
        self.run_button.config(state="normal", text="▶  Run Pipeline")

    # ---------------------------------------------------------------------------
    # Console Logging
    # ---------------------------------------------------------------------------

    def _log(self, message: str, tag: str = "info"):
        if tag == "info":
            if "MOCK" in message:
                tag = "mock"
            elif "Stage" in message or "Orchestrator" in message:
                tag = "stage"
            elif "complete" in message.lower() or "saved" in message.lower():
                tag = "success"
            elif "error" in message.lower():
                tag = "error"

        def append():
            self.console.config(state="normal")
            self.console.insert(tk.END, message + "\n", tag)
            self.console.see(tk.END)
            self.console.config(state="disabled")

        self.root.after(0, append)


# ---------------------------------------------------------------------------
# Console Redirector
# ---------------------------------------------------------------------------

class ConsoleRedirector:
    def __init__(self, log_func):
        self.log_func = log_func

    def write(self, message: str):
        if message.strip():
            self.log_func(message.strip())

    def flush(self):
        pass


# ---------------------------------------------------------------------------
# Entry Point — checks for API key and shows correct screen first
# ---------------------------------------------------------------------------

def main():
    root = tk.Tk()
    config = load_config()

    # First run — no config file exists yet
    if "api_key" not in config:
        def launch_main():
            # Clear setup screen widgets and launch main app
            for widget in root.winfo_children():
                widget.destroy()
            ResearchOpsGUI(root)

        SetupScreen(root, on_complete=launch_main)
    else:
        ResearchOpsGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()