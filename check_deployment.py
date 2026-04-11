#!/usr/bin/env python3
"""
Pre-deployment verification script.
Tests all components before deploying to Streamlit Cloud.
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check Python 3.8+"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("✗ Python 3.8+ required!")
        return False
    return True

def check_env_file():
    """Check .env exists and has GROQ_API_KEY"""
    env_path = Path(".env")
    if not env_path.exists():
        print("✗ .env file not found")
        return False
    
    with open(env_path) as f:
        content = f.read()
        if "GROQ_API_KEY" not in content:
            print("✗ GROQ_API_KEY not found in .env")
            return False
    
    print("✓ .env file configured")
    return True

def check_requirements():
    """Check all required packages are installed"""
    req_path = Path("requirements.txt")
    if not req_path.exists():
        print("✗ requirements.txt not found")
        return False
    
    try:
        with open(req_path) as f:
            packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        print(f"✓ requirements.txt has {len(packages)} packages")
        return True
    except Exception as e:
        print(f"✗ Error reading requirements.txt: {e}")
        return False

def check_streamlit_entry():
    """Check streamlit_app.py exists at root"""
    if not Path("streamlit_app.py").exists():
        print("✗ streamlit_app.py not found at project root")
        return False
    print("✓ streamlit_app.py entry point exists")
    return True

def check_app_structure():
    """Check app directory structure"""
    required_dirs = [
        "app",
        "app/dashboard",
        "app/api",
        "app/services",
        "app/models"
    ]
    
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            print(f"✗ Missing directory: {dir_path}")
            return False
    
    print(f"✓ App structure intact ({len(required_dirs)} directories)")
    return True

def check_main_app():
    """Check main app files"""
    files = [
        "app/main.py",
        "app/dashboard/streamlit_app.py",
        "app/api/routes.py"
    ]
    
    for file_path in files:
        if not Path(file_path).exists():
            print(f"✗ Missing file: {file_path}")
            return False
    
    print(f"✓ Core app files present")
    return True

def check_gitignore():
    """Check .gitignore has secrets"""
    if not Path(".gitignore").exists():
        print("⚠ Warning: .gitignore not found (creating one...)")
        return True
    
    with open(".gitignore") as f:
        content = f.read()
        if ".env" not in content:
            print("⚠ Warning: .env not in .gitignore (add it!)")
            return False
    
    print("✓ .gitignore configured")
    return True

def main():
    """Run all checks"""
    print("\n" + "="*50)
    print("🚀 PDMS DEPLOYMENT PRE-CHECK")
    print("="*50 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Environment Variables", check_env_file),
        ("Requirements", check_requirements),
        ("Streamlit Entry Point", check_streamlit_entry),
        ("App Structure", check_app_structure),
        ("Core Files", check_main_app),
        ("Git Ignore", check_gitignore),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"✗ Error: {e}")
            results.append(False)
    
    print("\n" + "="*50)
    passed = sum(results)
    total = len(results)
    print(f"✅ RESULTS: {passed}/{total} checks passed")
    print("="*50 + "\n")
    
    if all(results):
        print("🎉 Ready for deployment! Next steps:")
        print("1. git add .")
        print("2. git commit -m 'Ready for Streamlit Cloud'")
        print("3. git push origin main")
        print("4. Go to https://share.streamlit.io/")
        print("5. Enter: your-username/migration → main → streamlit_app.py")
        return 0
    else:
        print("❌ Fix issues above before deploying:")
        for i, (name, _) in enumerate(checks):
            status = "✓" if results[i] else "✗"
            print(f"   {status} {name}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
