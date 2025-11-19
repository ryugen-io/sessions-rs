/// Simple TOML parser for session config
/// Only parses the specific structure we need: [section] and key = "value"
use std::collections::HashMap;

#[derive(Debug, Default)]
pub struct TomlValue {
    pub sections: HashMap<String, HashMap<String, String>>,
}

impl TomlValue {
    pub fn parse(content: &str) -> Result<Self, String> {
        let mut toml = TomlValue::default();
        let mut current_section = String::new();

        for (line_num, line) in content.lines().enumerate() {
            let line = line.trim();

            // Skip empty lines and comments
            if line.is_empty() || line.starts_with('#') {
                continue;
            }

            // Parse section headers [section] or [section.subsection]
            if line.starts_with('[') && line.ends_with(']') {
                current_section = line[1..line.len() - 1].to_string();
                toml.sections
                    .entry(current_section.clone())
                    .or_insert_with(HashMap::new);
                continue;
            }

            // Parse key-value pairs
            if let Some((key, value)) = line.split_once('=') {
                let key = key.trim().to_string();
                let value = value.trim();

                // Remove quotes from value if present
                let value = if (value.starts_with('"') && value.ends_with('"'))
                    || (value.starts_with('\'') && value.ends_with('\''))
                {
                    &value[1..value.len() - 1]
                } else {
                    value
                }
                .to_string();

                if current_section.is_empty() {
                    return Err(format!(
                        "Key-value pair outside of section at line {}",
                        line_num + 1
                    ));
                }

                toml.sections
                    .get_mut(&current_section)
                    .unwrap()
                    .insert(key, value);
            }
        }

        Ok(toml)
    }

    pub fn get_section(&self, section: &str) -> Option<&HashMap<String, String>> {
        self.sections.get(section)
    }

    pub fn get(&self, section: &str, key: &str) -> Option<&String> {
        self.sections.get(section)?.get(key)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_toml() {
        let content = r##"
# Comment
[colors]
blue = "#3B82F6"
red = "#EF4444"

[hosts.ryujin]
icon = ""
color = "blue"
        "##;

        let toml = TomlValue::parse(content).unwrap();

        assert_eq!(toml.get("colors", "blue"), Some(&"#3B82F6".to_string()));
        assert_eq!(toml.get("hosts.ryujin", "icon"), Some(&"".to_string()));
    }
}
