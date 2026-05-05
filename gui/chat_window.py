import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import threading
import queue
from agents.tool_interface import AIAgentToolInterface
from agents.chat_agent import ChatAgent

class ChatWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🛠️ Legitimate Device Repair Toolkit")
        self.geometry("1100x800")
        self.configure(bg="#0a0a0a")

        self.interface = AIAgentToolInterface()
        self.agent = ChatAgent(self.interface)
        self.queue = queue.Queue()

        self._build_ui()
        self.after(100, self._poll_queue)

    def _build_ui(self):
        tk.Label(self, text="AI Device Repair Toolkit - Authorized Mode", 
                 font=("Consolas", 18, "bold"), fg="#00ffaa", bg="#0a0a0a").pack(pady=15)

        self.chat = scrolledtext.ScrolledText(self, wrap=tk.WORD, state=tk.DISABLED, bg="#1a1a1a", fg="#e0e0e0", font=("Consolas", 11))
        self.chat.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)

        input_frame = tk.Frame(self, bg="#0a0a0a")
        input_frame.pack(fill=tk.X, padx=25, pady=10)

        self.entry = tk.Entry(input_frame, font=("Consolas", 12), bg="#2a2a2a", fg="#fff")
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=12)
        self.entry.bind("<Return>", lambda e: self.send())

        tk.Button(input_frame, text="SEND", command=self.send, bg="#00cc66", fg="black", font=("Arial", 11, "bold")).pack(side=tk.RIGHT, padx=5)

        # Quick buttons
        btn_frame = tk.Frame(self, bg="#0a0a0a")
        btn_frame.pack(fill=tk.X, padx=25, pady=5)
        for text, cmd in [("List Devices", "list_devices"), ("Android Reset Plan", "android_factory_reset_plan"), ("Create New Toolkit", "create_new_diagnostic_toolkit")]:
            tk.Button(btn_frame, text=text, command=lambda c=cmd: self.quick(c), bg="#333", fg="#ccc").pack(side=tk.LEFT, padx=5)

    def _append(self, text: str, tag: str = "ai"):
        self.chat.configure(state=tk.NORMAL)
        self.chat.insert(tk.END, text + "\n\n", tag)
        self.chat.configure(state=tk.DISABLED)
        self.chat.see(tk.END)

    def quick(self, cmd: str):
        self.entry.delete(0, tk.END)
        self.send_text(cmd)

    def send_text(self, text: str):
        self._append(f"You: {text}", "user")
        threading.Thread(target=self._process, args=(text,), daemon=True).start()

    def send(self, event=None):
        text = self.entry.get().strip()
        if text:
            self.send_text(text)
            self.entry.delete(0, tk.END)

    def _process(self, msg: str):
        try:
            resp = self.agent.respond(msg)
            self.queue.put(resp)
        except Exception as e:
            self.queue.put(f"Error: {e}")

    def _poll_queue(self):
        try:
            while True:
                resp = self.queue.get_nowait()
                self._append(f"AI: {resp}", "ai")
        except queue.Empty:
            pass
        self.after(100, self._poll_queue)

    def run(self):
        self.mainloop()