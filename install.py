#!/usr/bin/env python3
"""
Installation script for session binary
Installs binary to ~/.config/starship/scripts/ and config to ~/.config/starship/
"""

import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR
sys.path.insert(0, str(REPO_ROOT / 'sys' / 'theme'))

from theme import Colors, Icons, log_success, log_error, log_warn, log_info


def get_install_paths():
    """Get installation paths"""
    config_home = Path.home() / '.config' / 'starship'
    scripts_dir = config_home / 'scripts'

    return {
        'binary_src': REPO_ROOT / 'target' / 'release' / 'sessions',
        'binary_dst': scripts_dir / 'sessions',
        'config_example': REPO_ROOT / 'sessions.toml.example',
        'config_dst': config_home / 'sessions.toml',
        'old_script': scripts_dir / 'session.sh',
    }


def backup_old_script(old_script: Path) -> bool:
    """Backup old session.sh if it exists"""
    if not old_script.exists():
        return True

    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_path = old_script.with_suffix(f'.sh.backup-{timestamp}')

    try:
        shutil.copy2(old_script, backup_path)
        log_info(f"backed up old script to {backup_path.name}")
        return True
    except Exception as e:
        log_error(f"failed to backup old script: {e}")
        return False


def build_release() -> bool:
    """Build release version"""
    log_info("building release version...")
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


def install_binary(src: Path, dst: Path) -> bool:
    """Install binary to destination"""
    if not src.exists():
        log_error(f"binary not found: {src}")
        log_info("run build.py first")
        return False

    # Create destination directory if needed
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.copy2(src, dst)
        dst.chmod(0o755)  # Make executable
        log_success(f"installed binary to {dst}")
        return True
    except Exception as e:
        log_error(f"failed to install binary: {e}")
        return False


def install_config(example: Path, dst: Path) -> bool:
    """Install config file if it doesn't exist"""
    if dst.exists():
        log_warn(f"config already exists: {dst}")
        log_info("skipping config installation (not overwriting)")
        return True

    if not example.exists():
        log_error(f"example config not found: {example}")
        return False

    # Create destination directory if needed
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.copy2(example, dst)
        log_success(f"installed config to {dst}")
        return True
    except Exception as e:
        log_error(f"failed to install config: {e}")
        return False


def main():
    """Main installation process"""
    import argparse

    parser = argparse.ArgumentParser(description='Install session binary')
    parser.add_argument(
        '--rebuild',
        action='store_true',
        help='Rebuild before installing'
    )
    args = parser.parse_args()

    print()
    print(f"{Colors.MAUVE}[install]{Colors.NC} {Icons.ROCKET}  installing session...")
    print()

    paths = get_install_paths()

    # Build if needed
    if args.rebuild or not paths['binary_src'].exists():
        if not build_release():
            return 1
        print()

    # Backup old script
    if not backup_old_script(paths['old_script']):
        return 1

    # Install binary
    if not install_binary(paths['binary_src'], paths['binary_dst']):
        return 1

    print()

    # Install config
    if not install_config(paths['config_example'], paths['config_dst']):
        return 1

    print()
    log_success("installation complete")
    print()

    # Show info
    print(f"{Colors.TEXT}Binary:{Colors.NC}")
    print(f"  {Colors.SAPPHIRE}{paths['binary_dst']}{Colors.NC}")
    print()
    print(f"{Colors.TEXT}Config:{Colors.NC}")
    print(f"  {Colors.SAPPHIRE}{paths['config_dst']}{Colors.NC}")
    print()
    print(f"{Colors.TEXT}Edit config to customize hosts and colors{Colors.NC}")
    print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
