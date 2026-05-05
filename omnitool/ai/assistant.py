"""AI Assistant module for OmniTool Pro"""

import json
from typing import Optional


class AIAssistant:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.client = None
        self._init_client()

    def _init_client(self):
        if not self.api_key:
            return
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            self.client = None

    def set_key(self, key: str):
        self.api_key = key
        self._init_client()

    def ask(self, question: str) -> str:
        if not self.client:
            return "AI not configured. Please set your OpenAI API key in Settings."

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are OmniAI, an assistant specialized in Android device management, ADB commands, FRP bypass procedures, and mobile device tools. Provide concise, step-by-step guidance. Only describe legitimate procedures for devices the user owns."
                    },
                    {"role": "user", "content": question}
                ],
                max_tokens=500,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"AI error: {str(e)}"
