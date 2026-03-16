"""
AlgoVision - Secure EXE Builder

    python build_exe.py              # Full: Cython + PyArmor + PyInstaller
    python build_exe.py --no-cython  # Skip Cython (PyArmor + PyInstaller only)
    python build_exe.py --no-armor   # Skip PyArmor (Cython + PyInstaller only)
    python build_exe.py --basic      # PyInstaller only (no protection)

Pipeline:
  1. Cython   - compiles .py -> .pyd/.so (C-level obfuscation)
  2. PyArmor  - encrypts remaining .pyc (runtime decryption)
  3. PyInstaller - packs into single .exe
"""

import subprocess
import sys
import os
import shutil
import glob
import argparse

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")
SHARED_DIR = os.path.join(ROOT_DIR, "shared")
STAGE_DIR = os.path.join(ROOT_DIR, "_build_stage")
SEP = os.pathsep


def run_cmd(cmd, label, cwd=None):
    """Run a command, print label, return success bool."""
    print(f"      Running: {' '.join(cmd[:5])}...")
    result = subprocess.run(cmd, cwd=cwd or ROOT_DIR, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"      FAILED: {result.stderr[:300]}")
        return False
    return True


def install_deps(use_cython, use_armor):
    """Install all required build tools."""
    print("[1/5] Installing build tools...")
    pkgs = ["pyinstaller", "fastapi", "uvicorn", "pydantic", "h11"]
    if use_cython:
        pkgs.append("cython")
    if use_armor:
        pkgs.append("pyarmor")
    subprocess.run([sys.executable, "-m", "pip", "install"] + pkgs + ["-q"],
                   capture_output=True)
    print("      Done.")


def prepare_stage():
    """Copy backend to a staging directory for compilation."""
    print("[2/5] Preparing build stage...")
    if os.path.isdir(STAGE_DIR):
        shutil.rmtree(STAGE_DIR)
    shutil.copytree(BACKEND_DIR, os.path.join(STAGE_DIR, "backend"))
    shutil.copytree(FRONTEND_DIR, os.path.join(STAGE_DIR, "frontend"))
    shutil.copytree(SHARED_DIR, os.path.join(STAGE_DIR, "shared"))

    # Clean pycache from stage
    for root, dirs, files in os.walk(STAGE_DIR):
        for d in dirs:
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root, d))
    print("      Done.")


def step_cython():
    """Compile .py files to .pyd/.so using Cython one by one."""
    print("[3/5] Cython: compiling Python -> C extensions...")

    backend_stage = os.path.join(STAGE_DIR, "backend")

    # Find all algorithm .py files (skip __init__.py, app.py, routes)
    py_files = []
    for root, dirs, files in os.walk(backend_stage):
        # Skip routes/ and models/ — only compile algorithm implementations
        rel = os.path.relpath(root, backend_stage)
        if rel.startswith("routes") or rel.startswith("models"):
            continue
        for f in files:
            if f.endswith(".py") and f != "__init__.py":
                py_files.append(os.path.join(root, f))

    if not py_files:
        print("      No .py files to compile.")
        return True

    compiled = 0
    failed = 0

    for py_file in py_files:
        py_dir = os.path.dirname(py_file)
        py_name = os.path.splitext(os.path.basename(py_file))[0]

        # Create a mini setup.py in the file's directory
        setup_content = (
            "from setuptools import setup, Extension\n"
            "from Cython.Build import cythonize\n"
            f"setup(ext_modules=cythonize('{os.path.basename(py_file)}', language_level='3', quiet=True))\n"
        )
        setup_path = os.path.join(py_dir, "_setup.py")
        with open(setup_path, "w", encoding="utf-8") as f:
            f.write(setup_content)

        result = subprocess.run(
            [sys.executable, "_setup.py", "build_ext", "--inplace"],
            cwd=py_dir, capture_output=True, text=True,
        )

        # Clean setup file
        if os.path.exists(setup_path):
            os.remove(setup_path)

        # Check if .pyd/.so was created
        pyd_files = glob.glob(os.path.join(py_dir, py_name + "*.pyd")) + \
                    glob.glob(os.path.join(py_dir, py_name + "*.so"))

        if pyd_files and result.returncode == 0:
            # Remove source .py and .c
            os.remove(py_file)
            c_file = os.path.join(py_dir, py_name + ".c")
            if os.path.exists(c_file):
                os.remove(c_file)
            compiled += 1
        else:
            failed += 1

        # Clean build dir in each folder
        build_dir = os.path.join(py_dir, "build")
        if os.path.isdir(build_dir):
            shutil.rmtree(build_dir)

    print(f"      Compiled {compiled}/{compiled + failed} files to native code. ({failed} skipped)")
    return True


def step_pyarmor():
    """Encrypt remaining .py files with PyArmor."""
    print("[3/5] PyArmor: encrypting Python files...")

    backend_stage = os.path.join(STAGE_DIR, "backend")

    # Detect working pyarmor base command
    pyarmor_base = None
    for base_try in [
        ["pyarmor"],
        [sys.executable, "-m", "pyarmor.cli"],
        [sys.executable, "-m", "pyarmor"],
    ]:
        try:
            r = subprocess.run(base_try + ["--version"],
                               capture_output=True, text=True, timeout=10)
            if r.returncode == 0 or "pyarmor" in (r.stdout + r.stderr).lower():
                pyarmor_base = base_try
                break
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue

    if pyarmor_base is None:
        print("      PyArmor not found — skipping encryption.")
        print("      Install with: pip install pyarmor")
        return True

    # Encrypt backend — use quoted paths for spaces
    output_dir = os.path.join(STAGE_DIR, "_armored")
    cmd = pyarmor_base + ["gen", "--output", output_dir, backend_stage]

    print(f"      Command: {' '.join(cmd[:4])}...")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=STAGE_DIR)

    if result.returncode == 0:
        # Find the armored output
        armored_backend = None
        for candidate in [
            os.path.join(output_dir, "backend"),
            output_dir,
        ]:
            if os.path.isdir(candidate) and any(
                f.endswith(".py") for r, d, files in os.walk(candidate) for f in files
            ):
                armored_backend = candidate
                break

        if armored_backend:
            shutil.rmtree(backend_stage)
            if armored_backend == output_dir:
                shutil.copytree(armored_backend, backend_stage)
            else:
                shutil.move(armored_backend, backend_stage)

            # Copy PyArmor runtime
            if os.path.isdir(output_dir):
                for item in os.listdir(output_dir):
                    if item.startswith("pyarmor_runtime"):
                        src = os.path.join(output_dir, item)
                        dst = os.path.join(backend_stage, item)
                        if os.path.isdir(src) and not os.path.exists(dst):
                            shutil.copytree(src, dst)

            print("      Encrypted backend files.")
        else:
            print("      PyArmor output empty — continuing unencrypted.")
    else:
        err = (result.stderr or result.stdout or "unknown error")[:200]
        print(f"      PyArmor failed: {err}")
        print("      Continuing unencrypted.")

    # Cleanup
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir, ignore_errors=True)

    return True


def step_pyinstaller():
    """Bundle everything into a single EXE."""
    print("[4/5] PyInstaller: building EXE...")

    backend_stage = os.path.join(STAGE_DIR, "backend")
    frontend_stage = os.path.join(STAGE_DIR, "frontend")
    shared_stage = os.path.join(STAGE_DIR, "shared")

    # Write launcher
    launcher = os.path.join(STAGE_DIR, "_launcher.py")
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

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name=AlgoVision",
        "--console",
        f"--add-data={backend_stage}{SEP}backend",
        f"--add-data={frontend_stage}{SEP}frontend",
        f"--add-data={shared_stage}{SEP}shared",
        "--collect-submodules=uvicorn",
        "--collect-submodules=fastapi",
        "--collect-submodules=starlette",
        "--collect-submodules=pydantic",
        "--collect-submodules=anyio",
        "--collect-submodules=h11",
        "--collect-submodules=sniffio",
        "--collect-submodules=httptools",
        "--hidden-import=email.mime.multipart",
        "--hidden-import=email.mime.text",
        "--hidden-import=multipart",
        "--noconfirm",
        "--clean",
        launcher,
    ]

    # If PyArmor runtime exists, collect it too
    for item in os.listdir(backend_stage):
        if item.startswith("pyarmor_runtime"):
            cmd.insert(-3, f"--collect-submodules={item}")
            cmd.insert(-3, f"--hidden-import={item}")

    result = subprocess.run(cmd, cwd=ROOT_DIR)
    return result.returncode == 0


def cleanup():
    """Remove build artifacts."""
    print("[5/5] Cleaning up...")
    for path in [STAGE_DIR,
                 os.path.join(ROOT_DIR, "build"),
                 os.path.join(ROOT_DIR, "AlgoVision.spec"),
                 os.path.join(ROOT_DIR, "_launcher.py")]:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)
    print("      Done.")


def main():
    parser = argparse.ArgumentParser(description="AlgoVision Secure EXE Builder")
    parser.add_argument("--no-cython", action="store_true", help="Skip Cython compilation")
    parser.add_argument("--no-armor", action="store_true", help="Skip PyArmor encryption")
    parser.add_argument("--basic", action="store_true", help="PyInstaller only, no protection")
    args = parser.parse_args()

    use_cython = not args.no_cython and not args.basic
    use_armor = not args.no_armor and not args.basic

    print()
    print("=" * 55)
    print("  AlgoVision - Secure EXE Builder")
    print("=" * 55)

    mode_parts = []
    if use_cython:
        mode_parts.append("Cython")
    if use_armor:
        mode_parts.append("PyArmor")
    mode_parts.append("PyInstaller")
    print(f"  Mode: {' + '.join(mode_parts)}")
    print()

    # Step 1: Install
    install_deps(use_cython, use_armor)

    # Step 2: Stage
    prepare_stage()

    # Step 3a: Cython
    if use_cython:
        step_cython()

    # Step 3b: PyArmor
    if use_armor:
        step_pyarmor()

    # Step 4: PyInstaller
    success = step_pyinstaller()

    # Step 5: Cleanup
    cleanup()

    # Report
    print()
    if success:
        dist = os.path.join(ROOT_DIR, "dist")
        exe = None
        for name in ["AlgoVision.exe", "AlgoVision"]:
            p = os.path.join(dist, name)
            if os.path.exists(p):
                exe = p
                break

        if exe:
            size_mb = os.path.getsize(exe) / (1024 * 1024)
            print("=" * 55)
            print("  BUILD SUCCESS!")
            print("=" * 55)
            print(f"  EXE:  {exe}")
            print(f"  Size: {size_mb:.1f} MB")
            print()
            protection = []
            if use_cython:
                protection.append("Cython (native code)")
            if use_armor:
                protection.append("PyArmor (encrypted)")
            if protection:
                print(f"  Protection: {' + '.join(protection)}")
            else:
                print("  Protection: None (basic build)")
            print()
            print("  Double-click AlgoVision.exe to run!")
            print()
        else:
            print("  Build completed but EXE not found in dist/")
    else:
        print("=" * 55)
        print("  BUILD FAILED")
        print("=" * 55)
        print()
        print("  Try these fixes:")
        print("    python build_exe.py --no-cython    # skip Cython")
        print("    python build_exe.py --no-armor     # skip PyArmor")
        print("    python build_exe.py --basic        # no protection")
        print()
        print("  Or install missing tools:")
        print("    pip install pyinstaller cython pyarmor")
        print("    pip install fastapi uvicorn pydantic h11")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()