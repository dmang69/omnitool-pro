#!/usr/bin/env python3
"""
AI Developer Toolkit - Main Entry Point

A comprehensive toolkit for AI-assisted development and device management.
"""
import argparse
import json
import sys
from pathlib import Path

from agents.tool_interface import AIAgentToolInterface
from agents.chat_agent import ChatAgent
from utils.logging_config import setup_logging

logger = setup_logging()


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="AI Developer Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --chat
  python main.py --tool list_devices
  python main.py --tool read_file --file example.py
  python main.py --tool search_codebase --file . --query "def main"
  python main.py --tool adb_list_devices
  python main.py --tool audit_android --device-id ABC123
        """,
    )
    
    # Mode selection
    parser.add_argument(
        "--chat", action="store_true", help="Start interactive chat"
    )
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument(
        "--config", type=str, default="config/default.yaml",
        help="Config file path"
    )
    
    # Tool execution
    parser.add_argument("--tool", type=str, help="Tool to execute")
    parser.add_argument("--file", type=str, help="File path")
    parser.add_argument("--content", type=str, help="Content for writes")
    parser.add_argument("--query", type=str, help="Search query")
    parser.add_argument("--device-id", type=str, help="Device ID")
    parser.add_argument("--mode", type=str, help="Mode parameter")
    parser.add_argument("--package", type=str, help="Package name")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--command", type=str, help="Shell command")
    
    return parser


def main() -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args()
    
    # Chat mode
    if args.chat:
        chat = ChatAgent(args.config)
        chat.start_interactive()
        return 0
    
    # Tool execution mode
    if args.tool:
        interface = AIAgentToolInterface(args.config)
        
        # Build kwargs based on tool name
        kwargs = {}
        if args.file:
            kwargs["filepath"] = args.file
            kwargs["dir_path"] = args.file
            kwargs["root_path"] = args.file
        if args.content:
            kwargs["content"] = args.content
            kwargs["output_path"] = args.content
        if args.query:
            kwargs["query"] = args.query
        if args.device_id:
            kwargs["device_id"] = args.device_id
        if args.mode:
            kwargs["mode"] = args.mode
        if args.package:
            kwargs["package_name"] = args.package
        if args.overwrite:
            kwargs["overwrite"] = True
        if args.command:
            kwargs["command"] = args.command
        
        result = interface.execute_tool(args.tool, **kwargs)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result.get("success", False):
                print(f"Success: {result.get('message', 'Done')}")
                for key, value in result.items():
                    if key not in ("success", "message"):
                        print(f"  {key}: {json.dumps(value, indent=2) if isinstance(value, (dict, list)) else value}")
            else:
                print(f"Error: {result.get('error', 'Unknown error')}")
        
        return 0 if result.get("success", False) else 1
    
    # Default: show help
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())