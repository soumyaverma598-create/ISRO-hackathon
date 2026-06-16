#!/usr/bin/env python3
"""
Solar Sentinel AI - Startup Guide
Run this script to start the application or use: streamlit run app.py
"""

import subprocess
import sys
import os
import platform

def main():
    """Main startup function"""
    
    print("\n" + "="*60)
    print("  ☀️  SOLAR SENTINEL AI - STARTUP")
    print("="*60 + "\n")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ ERROR: Python 3.8+ required")
        print(f"   Current version: {sys.version}")
        return 1
    
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    # Check if running in virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✓ Virtual environment detected")
    else:
        print("⚠ Warning: Not running in virtual environment")
        print("  Recommended: python -m venv venv && venv\\Scripts\\activate (Windows)")
        print("  Recommended: python3 -m venv venv && source venv/bin/activate (Mac/Linux)")
    
    # Check required packages
    print("\n" + "-"*60)
    print("Checking dependencies...")
    print("-"*60 + "\n")
    
    required_packages = ['streamlit', 'pandas', 'numpy', 'plotly']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("\nInstall missing packages with:")
        print("  pip install -r requirements.txt")
        return 1
    
    print("\n" + "="*60)
    print("  🚀 All checks passed! Starting application...")
    print("="*60 + "\n")
    
    # Start Streamlit
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "app.py"],
            check=False
        )
    except KeyboardInterrupt:
        print("\n\n✓ Application stopped")
        return 0
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
