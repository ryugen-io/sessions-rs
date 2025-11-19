# sessions-rs - codebase

```
sessions-rs/
├── .github/
│   ├── logs/
│   │   ├── 20251119-201955-workflow.log
│   │   ├── 20251119-202004-workflow.log
│   │   ├── 20251119-202005-workflow.log
│   │   ├── 20251119-202007-workflow.log
│   │   ├── 20251119-202253-workflow.log
│   │   ├── 20251119-202303-workflow.log
│   │   ├── 20251119-202305-workflow.log
│   │   ├── 20251119-202501-workflow.log
│   │   ├── 20251119-202509-workflow.log
│   │   ├── 20251119-202511-workflow.log
│   │   └── 20251119-203114-workflow.log
│   ├── skips/
│   │   └── SKIP_SYSTEM.md
│   └── workflows/
│       ├── scripts/
│       │   ├── ci-lines.sh
│       │   ├── ci-logger.sh
│       │   ├── cleanup_logs.py
│       │   └── update_readme.py
│       ├── check-skip.yml
│       ├── cleanup-logs.yml
│       └── update-readme.yml
├── src/
│   ├── color.rs
│   ├── config.rs
│   ├── main.rs
│   └── toml_parser.rs
├── sys/
│   ├── rust/
│   │   ├── audit.py
│   │   ├── check.py
│   │   ├── clean.py
│   │   ├── clippy.py
│   │   ├── rustfmt.py
│   │   └── test_rust.py
│   ├── theme/
│   │   ├── theme.py
│   │   └── theme.toml
│   └── utils/
│       ├── cleanup_backups.py
│       ├── fix_nerdfonts.py
│       ├── lines.py
│       ├── precommit.py
│       ├── pyclean.py
│       ├── pycompile.py
│       ├── pylint.py
│       ├── remove_emojis.py
│       ├── venv.py
│       └── xdg_paths.py
├── build.py
├── Cargo.toml
├── install.py
├── justfile
├── README.md
└── sessions.toml.example
```
