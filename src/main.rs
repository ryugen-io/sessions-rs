mod color;
mod config;
mod toml_parser;

use config::Config;
use std::env;
use std::io::{self, Write};
use std::process;

/// Get current username
fn get_username() -> String {
    env::var("USER")
        .or_else(|_| env::var("USERNAME"))
        .unwrap_or_else(|_| "user".to_string())
}

/// Get hostname
fn get_hostname() -> String {
    if let Ok(hostname) = std::fs::read_to_string("/etc/hostname") {
        return hostname.trim().to_string();
    }

    // Fallback: try hostname command
    if let Ok(output) = process::Command::new("hostname").arg("-s").output()
        && let Ok(hostname) = String::from_utf8(output.stdout)
    {
        return hostname.trim().to_string();
    }

    // Last fallback
    "host".to_string()
}

fn main() {
    // Load config
    let config = match Config::load() {
        Ok(cfg) => cfg,
        Err(e) => {
            eprintln!("Error loading config: {}", e);
            process::exit(1);
        }
    };

    let user = get_username();
    let host = get_hostname();

    // Get host config (with wildcard matching)
    let host_config = config.get_host(&host);

    // Resolve color name to hex, or use color name directly if it starts with #
    let color_code = if host_config.color.starts_with('#') {
        // Direct hex color
        color::hex_to_ansi(&host_config.color)
    } else {
        // Named color - resolve from config
        config
            .resolve_color(&host_config.color)
            .and_then(|hex| color::hex_to_ansi(hex))
    };

    // Build output
    let mut output = String::new();

    // Add colored icon if we have a color code
    if let Some(ansi_color) = color_code {
        output.push_str(&format!(
            "{}@{} {}{}{}",
            user,
            host,
            ansi_color,
            host_config.icon,
            color::RESET
        ));
    } else {
        // Fallback: no color
        output.push_str(&format!("{}@{} {}", user, host, host_config.icon));
    }

    // Print to stdout
    print!("{}", output);
    io::stdout().flush().unwrap();
}
