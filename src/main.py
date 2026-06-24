import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cli import run


def main() -> None:
    """Entry point for the Weather-Aware Assistant."""
    run()


if __name__ == "__main__":
    main()
