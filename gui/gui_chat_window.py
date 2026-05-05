import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
from typing import Optional

from agents.chatbot import SyntheticChatBot
from agents.tool_interface import AIAgentToolInterface
from utils.logging_config import setup_logging

logger = setup_logging()

class ChatWindow:
    def __init__(self, config_path: Optional[str] = None):
        self.interface = AIAgentToolInterface(config_path=config_path)
        self.bot = SyntheticChatBot(self.interface)
        
        self.root = tk.Tk()
        self.root.title("AI Toolkit - Authorized Device Service")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")

        self.setup_ui()
        self.setup_styles()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Chat bubble styles
        style.configure("User.TFrame", background="#e1f5fe")
        style.configure("Bot.TFrame", background="#ffffff")
        
        style.configure("User.TLabel", background="#e1f5fe", foreground="black", font=("Arial", 10))
        style.configure("Bot.TLabel", background="#ffffff", foreground="black", font=("Arial", 10))
        
        style.configure("Response.TText", background="#ffffff", font=("Consolas", 9), wraplength=800)

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=50)
        header.pack(fill=tk.X)
        
        title_label = tk.Label(header, text="AI Toolkit", bg="#2c3e50", fg="white", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        status_label = tk.Label(header, text="Authorized Mode: ON", bg="#2c3e50", fg="#2ecc71", font=("Arial", 8))
        status_label.pack()

        # Chat Area
        self.chat_area = scrolledtext.ScrolledText(
            self.root, 
            wrap=tk.WORD, 
            state=tk.DISABLED, 
            bg="#ffffff", 
            font=("Arial", 10)
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.chat_area.tag_config("user_msg", background="#e1f5fe", foreground="black", justify=tk.LEFT)
        self.chat_area.tag_config("bot_msg", background="#ffffff", foreground="#333333", justify=tk.LEFT)
        self.chat_area.tag_config("json_output", background="#f8f9fa", foreground="#555555", justify=tk.LEFT, font=("Consolas", 9))
        self.chat_area.tag_config("error_msg", background="#ffebee", foreground="#c62828", justify=tk.LEFT)

       