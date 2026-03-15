"""
AlgoVision — One-Click Launcher

    python run.py

Starts the backend API + serves the frontend.
Press Ctrl+C to stop cleanly.
"""

import subprocess
import sys
import os
import signal
import threading
import time
import webbrowser

PORT = 8000
HOST = "0.0.0.0"
URL = f"http://localhost:{PORT}"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")


def install_dependencies():
    print("[1/3] Installing dependencies...")
    packages = ["fastapi", "uvicorn", "pydantic"]
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install"] + packages + ["-q"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install"] + packages + ["-q", "--break-system-packages"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            print("      Warning: pip install had issues, continuing...")
    print("      Done.")


def open_browser():
    time.sleep(2)
    print(f"[3/3] Opening browser at {URL}")
    webbrowser.open(URL)


def start_server():
    print(f"[2/3] Starting server on {URL}")
    print()
    print("  ┌─────────────────────────────────────────┐")
    print(f"  │   App:      {URL}/          │")
    print(f"  │   API Docs: {URL}/docs      │")
    print(f"  │   Press Ctrl+C to stop                  │")
    print("  └─────────────────────────────────────────┘")
    print()

    threading.Thread(target=open_browser, daemon=True).start()

    os.chdir(BACKEND_DIR)
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app:app",
         "--host", HOST, "--port", str(PORT), "--reload"],
    )
    try:
        process.wait()
    except KeyboardInterrupt:
        pass
    finally:
        print("\n\n  Shutting down AlgoVision...")
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
        print("  Goodbye!\n")


def main():
    print()
    print("╔═══════════════════════════════════════════════╗")
    print("║         ◈  AlgoVision — Starting              ║")
    print("║         Algorithm Visualizer Platform          ║")
    print("╚═══════════════════════════════════════════════╝")
    print()

    if not os.path.isdir(BACKEND_DIR):
        print(f"ERROR: backend/ not found at {BACKEND_DIR}")
        sys.exit(1)
    if not os.path.isfile(os.path.join(FRONTEND_DIR, "index.html")):
        print(f"ERROR: frontend/index.html not found at {FRONTEND_DIR}")
        sys.exit(1)

    print(f"[OK] Python {sys.version.split()[0]}")
    print(f"[OK] Project: {ROOT_DIR}")

    install_dependencies()
    start_server()


if __name__ == "__main__":
    main()
