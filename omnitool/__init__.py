"""OmniTool Pro v1.0.0 - Professional Device Management Platform"""

__version__ = "1.0.0"
__author__ = "OmniTool Pro Contributors"

from .core.app import OmniToolApp

def main():
    app = OmniToolApp()
    app.run()

if __name__ == "__main__":
    main()
