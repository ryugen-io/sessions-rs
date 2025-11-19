/// Configuration management for session display
use crate::toml_parser::TomlValue;
use std::collections::HashMap;
use std::env;
use std::fs;
use std::path::PathBuf;

#[derive(Debug)]
pub struct HostConfig {
    pub icon: String,
    pub color: String,
}

#[derive(Debug)]
pub struct Config {
    pub colors: HashMap<String, String>,
    pub hosts: HashMap<String, HostConfig>,
    pub default: HostConfig,
}

impl Config {
    /// Load config from default path or XDG_CONFIG_HOME
    pub fn load() -> Result<Self, String> {
        let config_path = Self::get_config_path();

        if !config_path.exists() {
            return Err(format!(
                "Config file not found: {}\nRun install.py to set up",
                config_path.display()
            ));
        }

        let content = fs::read_to_string(&config_path)
            .map_err(|e| format!("Failed to read config: {}", e))?;

        Self::parse(&content)
    }

    /// Get config file path
    fn get_config_path() -> PathBuf {
        if let Ok(xdg_config) = env::var("XDG_CONFIG_HOME") {
            PathBuf::from(xdg_config).join("starship/sessions.toml")
        } else if let Ok(home) = env::var("HOME") {
            PathBuf::from(home).join(".config/starship/sessions.toml")
        } else {
            PathBuf::from("sessions.toml")
        }
    }

    /// Parse TOML config
    fn parse(content: &str) -> Result<Self, String> {
        let toml = TomlValue::parse(content)?;

        // Parse color mappings
        let mut colors = HashMap::new();
        if let Some(color_section) = toml.get_section("colors") {
            for (name, hex) in color_section {
                colors.insert(name.clone(), hex.clone());
            }
        }

        // Parse default config
        let default = HostConfig {
            icon: toml
                .get("default", "icon")
                .cloned()
                .unwrap_or_else(|| "".to_string()),
            color: toml
                .get("default", "color")
                .cloned()
                .unwrap_or_else(|| "blue".to_string()),
        };

        // Parse host configs
        let mut hosts = HashMap::new();
        for (section_name, section) in &toml.sections {
            if section_name.starts_with("hosts.") {
                let hostname = section_name.strip_prefix("hosts.").unwrap().to_string();

                let host_config = HostConfig {
                    icon: section
                        .get("icon")
                        .cloned()
                        .unwrap_or_else(|| default.icon.clone()),
                    color: section
                        .get("color")
                        .cloned()
                        .unwrap_or_else(|| default.color.clone()),
                };

                hosts.insert(hostname, host_config);
            }
        }

        Ok(Config {
            colors,
            hosts,
            default,
        })
    }

    /// Get host config by hostname, with wildcard matching
    pub fn get_host(&self, hostname: &str) -> &HostConfig {
        // Exact match first
        if let Some(config) = self.hosts.get(hostname) {
            return config;
        }

        // Wildcard matching (e.g., "oni*" matches "oni1", "oni2", etc.)
        for (pattern, config) in &self.hosts {
            if pattern.ends_with('*') {
                let prefix = &pattern[..pattern.len() - 1];
                if hostname.starts_with(prefix) {
                    return config;
                }
            }
        }

        // Fallback to default
        &self.default
    }

    /// Resolve color name to hex value
    pub fn resolve_color(&self, color_name: &str) -> Option<&String> {
        self.colors.get(color_name)
    }
}
