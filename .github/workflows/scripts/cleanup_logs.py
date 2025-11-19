#!/usr/bin/env python3
"""
Log Cleanup Script - Keeps only logs from the last N workflow runs
"""

import sys
import re
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / 'sys' / 'theme'))

from theme import Colors, Icons, log_success, log_info, log_error

# Configuration
LOG_DIR = REPO_ROOT / '.github' / 'logs'
KEEP_RUNS = 2  # Keep logs from the last 2 workflow runs


def group_logs_by_run():
    """Group log files by run timestamp prefix (5-minute windows)"""
    if not LOG_DIR.exists():
        return {}

    log_files = list(LOG_DIR.glob('*.log'))

    # Group by 5-minute timestamp windows
    runs = defaultdict(list)

    for log_file in log_files:
        # Extract timestamp from filename: 20251119-201452-workflow.log
        match = re.match(r'^(\d{8})-(\d{2})(\d{2})', log_file.name)
        if match:
            date = match.group(1)  # YYYYMMDD
            hour = match.group(2)  # HH
            minute = int(match.group(3))  # MM

            # Round minute down to nearest 5-minute block
            rounded_minute = (minute // 5) * 5

            # Create timestamp key: YYYYMMDD-HHMM
            timestamp = f"{date}-{hour}{rounded_minute:02d}"
            runs[timestamp].append(log_file)

    # Sort runs by timestamp (newest first)
    sorted_runs = sorted(runs.items(), key=lambda x: x[0], reverse=True)

    return sorted_runs


def cleanup_logs():
    """Remove old log files, keeping only the last N runs"""
    print()
    print(f"{Colors.MAUVE}[cleanup]{Colors.NC} {Icons.CLEAN}  checking logs...")
    print()

    runs = group_logs_by_run()

    if not runs:
        log_info("no logs found")
        return 0

    run_count = len(runs)
    total_files = sum(len(files) for _, files in runs)

    log_info(f"found {total_files} log(s) from {run_count} run(s)")

    if run_count <= KEEP_RUNS:
        log_info(f"keeping all {run_count} run(s)")
        return 0

    # Keep the N most recent runs
    keep_runs = runs[:KEEP_RUNS]
    delete_runs = runs[KEEP_RUNS:]

    keep_count = sum(len(files) for _, files in keep_runs)
    delete_count = sum(len(files) for _, files in delete_runs)

    log_info(f"keeping {keep_count} log(s) from newest {KEEP_RUNS} run(s)")
    log_info(f"deleting {delete_count} log(s) from {len(delete_runs)} old run(s)")

    # Delete files from old runs
    deleted = 0
    for timestamp, files in delete_runs:
        for log_file in files:
            try:
                log_file.unlink()
                deleted += 1
            except OSError as e:
                log_error(f"failed to delete {log_file.name}: {e}")
                return 1

    log_success(f"deleted {deleted} old log(s)")
    return 0


def main():
    """Main function"""
    try:
        return cleanup_logs()
    except Exception as e:
        log_error(f"cleanup failed: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
