import os
import logging.config
import yaml


def setup_logging(
    default_path: str = 'garmin_fit_eda/logging.yaml',
    default_level: int = logging.INFO,
    env_key: str = 'LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
