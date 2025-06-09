
import subprocess
import sys
import os

def install_requirements():
    """Install Python requirements"""
    print("Installing Python requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/simple-auth/requirements.txt"])

def start_backend():
    """Start the Flask backend"""
    print("Starting FinFlow backend...")
    os.chdir("backend/simple-auth")
    subprocess.run([sys.executable, "app.py"])

if __name__ == "__main__":
    install_requirements()
    start_backend()
