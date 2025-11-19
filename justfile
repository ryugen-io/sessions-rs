# sessions-rs - Just commands

# Build project (format, clippy, build dev + release with cargo-auditable)
build:
    ./build.py

# Install binary to starship scripts directory
install:
    ./install.py

# Install and rebuild
install-rebuild:
    ./install.py --rebuild

# Format all code
fmt:
    python3 sys/rust/rustfmt.py

# Run clippy on all targets
clippy:
    python3 sys/rust/clippy.py

# Run cargo check
check:
    python3 sys/rust/check.py

# Run tests
test:
    python3 sys/rust/test_rust.py

# Run security audit
audit:
    python3 sys/rust/audit.py

# Clean build artifacts
clean:
    python3 sys/rust/clean.py

# Count lines of code
lines:
    python3 sys/utils/lines.py

# Alias for lines
loc: lines

# Python linting
pylint:
    python3 sys/utils/pylint.py --recursive

# Python syntax check (compile all .py files)
pycompile:
    python3 sys/utils/pycompile.py --recursive

# Clean Python cache files
pyclean:
    python3 sys/utils/pyclean.py --recursive

# Fix Nerd Font icons in files
fix-nerdfonts:
    python3 sys/utils/fix_nerdfonts.py

# Remove emojis from files
remove-emojis:
    python3 sys/utils/remove_emojis.py

# Run all Rust checks (fmt, clippy, check, test)
rust-checks:
    @python3 sys/rust/rustfmt.py
    @echo -e "\033[38;2;186;194;222m────────────────────────────────────────\033[0m"
    @python3 sys/rust/clippy.py
    @echo -e "\033[38;2;186;194;222m────────────────────────────────────────\033[0m"
    @python3 sys/rust/check.py
    @echo -e "\033[38;2;186;194;222m────────────────────────────────────────\033[0m"
    @python3 sys/rust/test_rust.py

# Run all Python checks (pylint, pycompile)
python-checks:
    @python3 sys/utils/pylint.py --recursive
    @echo -e "\033[38;2;186;194;222m────────────────────────────────────────\033[0m"
    @python3 sys/utils/pycompile.py --recursive

# Run all checks (Rust + Python)
all-checks: rust-checks python-checks

# Pre-commit checks
pc:
    python3 sys/utils/precommit.py --verbose
    python3 sys/utils/pyclean.py

# Pre-commit checks (summary only)
pc-summary:
    python3 sys/utils/precommit.py --summary
    python3 sys/utils/pyclean.py

# Alias for backward compatibility
pre-commit: pc

# Test binary directly
run:
    ./target/release/sessions

# Build and test
bt: build run

# Build, install, and test
full: build install
    @echo -e "\033[38;2;166;227;161m✓\033[0m Testing installed binary:"
    @~/.config/starship/scripts/sessions
