from paths import Paths
from core.config.config_singleton import ConfigSingleton

# Hosts, users credentials, and other config.
CONFIG = ConfigSingleton(config_file_path=Paths.CONFIG_FILE_PATH).get_config()
CONFIG.hosts = CONFIG[CONFIG.env].hosts
CONFIG.users = CONFIG[CONFIG.env].users
