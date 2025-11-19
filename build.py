#!/usr/bin/env python3
"""
Build script for session binary
Performs: format, clippy, build (dev + release) with cargo auditable
"""

import sys
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR
sys.path.insert(0, str(REPO_ROOT / 'sys' / 'theme'))

from theme import Colors, Icons, log_success, log_error, log_info


def check_cargo() -> bool:
    """Check if cargo is installed"""
    try:
        subprocess.run(['cargo', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        log_error("cargo is not installed")
        print()
        print(f"{Colors.TEXT}Install Rust and cargo:{Colors.NC}")
        print(f"{Colors.BLUE}  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh{Colors.NC}")
        print()
        return False


def check_auditable() -> bool:
    """Check if cargo-auditable is installed"""
    try:
        subprocess.run(['cargo', 'auditable', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        log_error("cargo-auditable is not installed")
        print()
        print(f"{Colors.TEXT}Install cargo-auditable:{Colors.NC}")
        print(f"{Colors.BLUE}  cargo install cargo-auditable{Colors.NC}")
        print()
        return False


def run_format() -> bool:
    """Run cargo fmt"""
    log_info("formatting code...")
    try:
        subprocess.run(['cargo', 'fmt', '--all'], cwd=REPO_ROOT, check=True)
        log_success("code formatted")
        return True
    except subprocess.CalledProcessError:
        log_error("formatting failed")
        return False


def run_clippy() -> bool:
    """Run cargo clippy"""
    log_info("running clippy...")
    try:
        subprocess.run(
            ['cargo', 'clippy', '--all-targets', '--', '-D', 'warnings'],
            cwd=REPO_ROOT,
            check=True
        )
        log_success("clippy passed")
        return True
    except subprocess.CalledProcessError:
        log_error("clippy found issues")
        return False


def build_dev() -> bool:
    """Build dev version with cargo auditable"""
    log_info("building dev...")
    try:
        subprocess.run(
            ['cargo', 'auditable', 'build'],
            cwd=REPO_ROOT,
            check=True
        )
        log_success("dev build complete")
        return True
    except subprocess.CalledProcessError:
        log_error("dev build failed")
        return False


def build_release() -> bool:
    """Build release version with cargo auditable"""
    log_info("building release...")
    try:
        subprocess.run(
            ['cargo', 'auditable', 'build', '--release'],
            cwd=REPO_ROOT,
            check=True
        )
        log_success("release build complete")
        return True
    except subprocess.CalledProcessError:
        log_error("release build failed")
        return False


def main():
    """Main build process"""
    print()
    print(f"{Colors.MAUVE}[build]{Colors.NC} {Icons.HAMMER}  building session binary...")
    print()

    if not check_cargo():
        return 1

    if not check_auditable():
        return 1

    print()

    # Format
    if not run_format():
        return 1

    print()

    # Clippy
    if not run_clippy():
        return 1

    print()

    # Build dev
    if not build_dev():
        return 1

    print()

    # Build release
    if not build_release():
        return 1

    print()
    log_success("build complete")
    print()

    # Show binary info
    release_bin = REPO_ROOT / 'target' / 'release' / 'session'
    if release_bin.exists():
        size = release_bin.stat().st_size
        size_kb = size / 1024
        print(f"{Colors.TEXT}Release binary:{Colors.NC}")
        print(f"  {Colors.SAPPHIRE}{release_bin}{Colors.NC}")
        print(f"  {Colors.TEXT}Size: {Colors.SAPPHIRE}{size_kb:.1f} KB{Colors.NC}")
        print()
        print(f"{Colors.TEXT}Run install.py to install to starship{Colors.NC}")
        print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
