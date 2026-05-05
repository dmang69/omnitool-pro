from utils.config import Config
from agents.tool_interface import AIAgentToolInterface
from agents.chatbot import SyntheticChatBot

def make_interface(tmp_path):
    cfg = Config()
    cfg.set("security.allowed_paths", [str(tmp_path)])
    return AIAgentToolInterface(config=cfg)

def test_list_tools(tmp_path):
    interface = make_interface(tmp_path)
    tools = interface.list_tools()
    names = [t["name"] for t in tools]
    assert "read_file" in names
    assert "create_tool_scaffold" in names

def test_chatbot_tools_command(tmp_path):
    interface = make_interface(tmp_path)
    bot = SyntheticChatBot(interface)
    response = bot.respond("/tools")
    assert "read_file" in response