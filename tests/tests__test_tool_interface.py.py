import pytest
from agents.tool_interface import AIAgentToolInterface


@pytest.fixture
def ti():
    return AIAgentToolInterface()


def test_list_all_tools(ti):
    tools = ti.list_all_tools()
    assert "filesystem" in tools
    assert "device" in tools


def test_list_device_tools(ti):
    dt = ti.list_device_tools()
    assert "android_frp_bypass" in dt
    assert "icloud_bypass" in dt
    assert "imei" in dt