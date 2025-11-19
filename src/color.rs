/// Color utilities for converting hex colors to ANSI escape codes
///
/// Converts a hex color string (#RRGGBB) to an ANSI true color escape sequence
pub fn hex_to_ansi(hex: &str) -> Option<String> {
    let hex = hex.trim_start_matches('#');

    if hex.len() != 6 {
        return None;
    }

    let r = u8::from_str_radix(&hex[0..2], 16).ok()?;
    let g = u8::from_str_radix(&hex[2..4], 16).ok()?;
    let b = u8::from_str_radix(&hex[4..6], 16).ok()?;

    Some(format!("\x1b[38;2;{};{};{}m", r, g, b))
}

/// Reset ANSI color to default
pub const RESET: &str = "\x1b[0m";

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hex_to_ansi() {
        assert_eq!(
            hex_to_ansi("#3B82F6"),
            Some("\x1b[38;2;59;130;246m".to_string())
        );

        assert_eq!(
            hex_to_ansi("3B82F6"),
            Some("\x1b[38;2;59;130;246m".to_string())
        );

        assert_eq!(hex_to_ansi("#FFF"), None);
        assert_eq!(hex_to_ansi("invalid"), None);
    }
}
