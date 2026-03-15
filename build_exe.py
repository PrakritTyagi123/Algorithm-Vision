"""
AlgoVision - Build to EXE

    python build_exe.py

Creates dist/AlgoVision.exe - standalone, double-click to run.
Requires: pip install pyinstaller
"""

import subprocess
import sys
import os
import shutil

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")
SHARED_DIR = os.path.join(ROOT_DIR, "shared")
SEP = os.pathsep  # ; on Windows, : on Linux


def main():
    print()
    print("=" * 50)
    print("  AlgoVision - Building EXE")
    print("=" * 50)
    print()

    # Step 1: Install deps
    print("[1/4] Installing PyInstaller + deps...")
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "pyinstaller", "fastapi", "uvicorn", "pydantic", "-q"])
    print("      Done.")

    # Step 2: Write launcher script (pure ASCII, no unicode)
    print("[2/4] Creating launcher...")
    launcher = os.path.join(ROOT_DIR, "_launcher.py")
    with open(launcher, "w", encoding="utf-8") as f:
        f.write(
            'import os, sys, threading, time, webbrowser\n'
            'def main():\n'
            '    PORT = 8000\n'
            '    if getattr(sys, "frozen", False):\n'
            '        base = sys._MEIPASS\n'
            '    else:\n'
            '        base = os.path.dirname(os.path.abspath(__file__))\n'
            '    backend = os.path.join(base, "backend")\n'
            '    os.chdir(backend)\n'
            '    sys.path.insert(0, backend)\n'
            '    print()\n'
            '    print("  AlgoVision - Algorithm Visualizer")\n'
            '    print(f"  Server: http://localhost:{PORT}")\n'
            '    print("  Press Ctrl+C to stop")\n'
            '    print()\n'
            '    def _open():\n'
            '        time.sleep(1.5)\n'
            '        webbrowser.open(f"http://localhost:{PORT}")\n'
            '    threading.Thread(target=_open, daemon=True).start()\n'
            '    import uvicorn\n'
            '    from app import app\n'
            '    try:\n'
            '        uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")\n'
            '    except KeyboardInterrupt:\n'
            '        print("\\n  Goodbye!")\n'
            'if __name__ == "__main__":\n'
            '    main()\n'
        )
    print("      Done.")

    # Step 3: Build
    print("[3/4] Building EXE (this takes 1-3 minutes)...")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name=AlgoVision",
        "--console",
        f"--add-data={BACKEND_DIR}{SEP}backend",
        f"--add-data={FRONTEND_DIR}{SEP}frontend",
        f"--add-data={SHARED_DIR}{SEP}shared",
        "--hidden-import=uvicorn",
        "--hidden-import=uvicorn.logging",
        "--hidden-import=uvicorn.loops",
        "--hidden-import=uvicorn.loops.auto",
        "--hidden-import=uvicorn.protocols",
        "--hidden-import=uvicorn.protocols.http",
        "--hidden-import=uvicorn.protocols.http.auto",
        "--hidden-import=uvicorn.protocols.http.h11_impl",
        "--hidden-import=uvicorn.protocols.http.httptools_impl",
        "--hidden-import=uvicorn.protocols.websockets",
        "--hidden-import=uvicorn.protocols.websockets.auto",
        "--hidden-import=uvicorn.protocols.websockets.wsproto_impl",
        "--hidden-import=uvicorn.protocols.websockets.websockets_impl",
        "--hidden-import=uvicorn.lifespan",
        "--hidden-import=uvicorn.lifespan.on",
        "--hidden-import=uvicorn.lifespan.off",
        "--hidden-import=fastapi",
        "--hidden-import=pydantic",
        "--hidden-import=starlette",
        "--hidden-import=starlette.routing",
        "--hidden-import=starlette.responses",
        "--hidden-import=starlette.middleware",
        "--hidden-import=starlette.middleware.cors",
        "--hidden-import=starlette.staticfiles",
        "--hidden-import=anyio",
        "--hidden-import=anyio._backends",
        "--hidden-import=anyio._backends._asyncio",
        "--hidden-import=h11",
        "--collect-submodules=uvicorn",
        "--collect-submodules=starlette",
        "--noconfirm",
        "--clean",
        launcher,
    ]

    result = subprocess.run(cmd, cwd=ROOT_DIR)

    # Cleanup
    if os.path.exists(launcher):
        os.remove(launcher)
    spec = os.path.join(ROOT_DIR, "AlgoVision.spec")
    if os.path.exists(spec):
        os.remove(spec)
    build_dir = os.path.join(ROOT_DIR, "build")
    if os.path.isdir(build_dir):
        shutil.rmtree(build_dir, ignore_errors=True)

    # Step 4: Report
    print()
    if result.returncode == 0:
        dist = os.path.join(ROOT_DIR, "dist")
        exe = None
        for name in ["AlgoVision.exe", "AlgoVision"]:
            p = os.path.join(dist, name)
            if os.path.exists(p):
                exe = p
                break

        if exe:
            size_mb = os.path.getsize(exe) / (1024 * 1024)
            print("[4/4] BUILD SUCCESS!")
            print()
            print(f"  EXE:  {exe}")
            print(f"  Size: {size_mb:.1f} MB")
            print()
            print("  Double-click AlgoVision.exe to run!")
        else:
            print("  Build completed but EXE not found in dist/")
    else:
        print("  BUILD FAILED. Common fixes:")
        print("    pip install pyinstaller --upgrade")
        print("    pip install fastapi uvicorn pydantic h11")
    print()


if __name__ == "__main__":
    main()
