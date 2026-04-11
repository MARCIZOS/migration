"""
Streamlit Cloud entry point - imports and runs the main dashboard.
"""
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent / "app" / "dashboard"))

# Import and run the main dashboard
from streamlit_app import main

if __name__ == "__main__":
    main()
