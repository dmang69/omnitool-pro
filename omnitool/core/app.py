"""Main application entry point for OmniTool Pro"""

import sys
import json
import os
from pathlib import Path

try:
    import customtkinter as ctk
    from tkinter import messagebox, ttk
except ImportError:
    print("Missing dependencies. Install with: pip install -r requirements.txt")
    sys.exit(1)

from ..ai.assistant import AIAssistant
from ..tools.base import ToolManager
from ..core.device import DeviceManager


class OmniToolApp:
    def __init__(self):
        self.version = "1.0.0"
        self.config = self.load_config()
        self.device_manager = DeviceManager()
        self.tool_manager = ToolManager()
        self.ai_assistant = AIAssistant(self.config.get("openai_api_key"))
        self.root = None

    def load_config(self):
        config_path = Path("config.json")
        if config_path.exists():
            with open(config_path) as f:
                return json.load(f)
        return {"theme": "dark", "openai_api_key": "", "adb_path": "adb"}

    def run(self):
        ctk.set_appearance_mode(self.config.get("theme", "dark"))
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title(f"OmniTool Pro v{self.version}")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)

        self.setup_ui()
        self.root.mainloop()

    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self.root, height=60)
        header.pack(fill="x", padx=10, pady=(10, 0))
        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header, text=f"OmniTool Pro v{self.version}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(side="left", padx=20, pady=15)

        self.status_label = ctk.CTkLabel(header, text="Ready", text_color="gray")
        self.status_label.pack(side="right", padx=20)

        # Main container
        main = ctk.CTkFrame(self.root)
        main.pack(fill="both", expand=True, padx=10, pady=10)

        # Sidebar
        sidebar = ctk.CTkFrame(main, width=200)
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)

        ctk.CTkLabel(sidebar, text="Tools", font=ctk.CTkFont(weight="bold")).pack(pady=10)

        tools = [
            ("Dashboard", self.show_dashboard),
            ("FRP Tools", self.show_frp_tools),
            ("Android Tools", self.show_android_tools),
            ("IMEI Tools", self.show_imei_tools),
            ("Diagnostics", self.show_diagnostics),
            ("AI Assistant", self.show_ai_assistant),
            ("Settings", self.show_settings),
        ]

        for name, cmd in tools:
            ctk.CTkButton(sidebar, text=name, command=cmd, height=36).pack(fill="x", padx=10, pady=3)

        # Content area
        self.content = ctk.CTkFrame(main)
        self.content.pack(side="left", fill="both", expand=True)

        self.show_dashboard()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()
        ctk.CTkLabel(
            self.content, text="Dashboard",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)

        # Stats
        stats = ctk.CTkFrame(self.content)
        stats.pack(fill="x", padx=20, pady=10)

        stats_data = [
            ("Tools", "52+"),
            ("Scripts", "8"),
            ("AI Queries", "0"),
            ("Plan", "Pro"),
        ]

        for label, value in stats_data:
            frame = ctk.CTkFrame(stats)
            frame.pack(side="left", expand=True, fill="both", padx=5, pady=10)
            ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(10, 0))
            ctk.CTkLabel(frame, text=label).pack(pady=(0, 10))

        # Device list
        ctk.CTkLabel(self.content, text="Connected Devices", font=ctk.CTkFont(weight="bold")).pack(pady=(20, 10))

        devices = self.device_manager.get_devices()
        if devices:
            for dev in devices:
                ctk.CTkLabel(self.content, text=f"  {dev}").pack(anchor="w", padx=40)
        else:
            ctk.CTkLabel(self.content, text="  No devices connected", text_color="gray").pack(anchor="w", padx=40)

    def show_frp_tools(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="FRP Bypass Tools", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        ctk.CTkLabel(self.content, text="8 tools available", text_color="gray").pack()
        tools = ["Samsung TalkBack Method", "ADB Bypass", "QR Code Method", "Google Account Bypass"]
        for t in tools:
            ctk.CTkButton(self.content, text=t, height=36).pack(fill="x", padx=40, pady=5)

    def show_android_tools(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Android Tools", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        tools = ["ADB Shell", "Fastboot Commands", "Device Info", "APK Installer", "Screen Mirroring", "File Manager", "Logcat Viewer"]
        for t in tools:
            ctk.CTkButton(self.content, text=t, height=36).pack(fill="x", padx=40, pady=5)

    def show_imei_tools(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="IMEI Tools", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        tools = ["IMEI Lookup", "Device Info by IMEI", "TAC Database", "Blacklist Check", "Warranty Check"]
        for t in tools:
            ctk.CTkButton(self.content, text=t, height=36).pack(fill="x", padx=40, pady=5)

    def show_diagnostics(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Diagnostics", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        ctk.CTkButton(self.content, text="Run Full Diagnostics", height=36).pack(fill="x", padx=40, pady=5)

    def show_ai_assistant(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="AI Assistant", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        self.chat_frame = ctk.CTkScrollableFrame(self.content, height=400)
        self.chat_frame.pack(fill="both", expand=True, padx=20, pady=10)

        input_frame = ctk.CTkFrame(self.content)
        input_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.chat_entry = ctk.CTkEntry(input_frame, placeholder_text="Ask the AI assistant...")
        self.chat_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.chat_entry.bind("<Return>", lambda e: self.send_chat())

        ctk.CTkButton(input_frame, text="Send", width=80, command=self.send_chat).pack(side="right")

    def send_chat(self):
        msg = self.chat_entry.get().strip()
        if not msg:
            return
        self.chat_entry.delete(0, "end")

        ctk.CTkLabel(self.chat_frame, text=f"You: {msg}", anchor="w").pack(fill="x", pady=2)
        response = self.ai_assistant.ask(msg)
        ctk.CTkLabel(self.chat_frame, text=f"AI: {response}", anchor="w", text_color="lightblue").pack(fill="x", pady=2)

    def show_settings(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Settings", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        ctk.CTkLabel(self.content, text="OpenAI API Key:").pack(anchor="w", padx=40, pady=(10, 0))
        key_entry = ctk.CTkEntry(self.content, placeholder_text="sk-...", show="*", width=400)
        key_entry.insert(0, self.config.get("openai_api_key", ""))
        key_entry.pack(padx=40, pady=5, anchor="w")

        def save():
            self.config["openai_api_key"] = key_entry.get()
            with open("config.json", "w") as f:
                json.dump(self.config, f, indent=2)
            self.ai_assistant.set_key(key_entry.get())
            messagebox.showinfo("Saved", "Settings saved successfully")

        ctk.CTkButton(self.content, text="Save Settings", command=save).pack(padx=40, pady=20, anchor="w")
