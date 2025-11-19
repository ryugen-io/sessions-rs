# sessions-rs

Starship session info binary with customizable icons and colors.

## Features

- Custom host icons and colors via TOML config
- Pattern matching for wildcards (e.g., `oni*` matches `oni1`, `oni2`, etc.)
- Hex color to ANSI true color conversion
- Zero dependencies (custom TOML parser)
- Built with cargo-auditable for supply chain security
- Fast and lightweight

## Requirements

- Rust 1.91.1 or later (Edition 2024)
- cargo-auditable: `cargo install cargo-auditable`

## Installation

1. Build and install:
```bash
./install.py --rebuild
```

This will:
- Build release binary with cargo-auditable
- Install to `~/.config/starship/scripts/sessions`
- Copy example config to `~/.config/starship/sessions.toml`
- Backup old `session.sh` if present

2. Configure Starship to use the binary in `~/.config/starship/starship.toml`:
```toml
[custom.session]
command = "~/.config/starship/scripts/sessions"
when = true
```

3. Edit `~/.config/starship/sessions.toml` to customize hosts and colors

## Configuration

Example config (`~/.config/starship/sessions.toml`):

```toml
# Color definitions
[colors]
blue = "#3B82F6"
red = "#EF4444"
green = "#10B981"

# Default fallback
[default]
icon = ""
color = "blue"

# Host-specific configs
[hosts.ryujin]
icon = ""
color = "purple"

# Wildcard patterns
["hosts.oni*"]
icon = "󰒋"
color = "orange"
```

## Development

### Build

```bash
./build.py
```

Runs:
- `cargo fmt` - Format code
- `cargo clippy` - Lint
- `cargo auditable build` - Dev build
- `cargo auditable build --release` - Release build

### Dev Scripts

Located in `sys/rust/`:
- `check.py` - Run cargo check
- `clippy.py` - Run clippy linter
- `rustfmt.py` - Format code
- `test_rust.py` - Run tests
- `audit.py` - Security audit
- `clean.py` - Clean build artifacts

### Run Individual Scripts

```bash
python3 sys/rust/check.py
python3 sys/rust/clippy.py
python3 sys/rust/rustfmt.py
```

## Project Structure

```
sessions-rs/
├── src/
│   ├── main.rs           # Main entry point
│   ├── config.rs         # Config loading and management
│   ├── toml_parser.rs    # Custom TOML parser
│   └── color.rs          # Hex to ANSI conversion
├── sys/
│   ├── rust/             # Rust dev scripts
│   ├── utils/            # Utility scripts
│   ├── theme/            # Theme system (Catppuccin Mocha)
│   └── env/              # Environment config
├── build.py              # Build script
├── install.py            # Installation script
├── session.toml.example  # Example config
└── Cargo.toml            # Rust project config
```

## License

MIT
