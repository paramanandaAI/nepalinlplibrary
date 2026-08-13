# -*- coding: utf-8 -*-
"""
Layered Configuration Resolver (`nepalinlplibrary.config`)
Resolves data directory paths dynamically from environment variables, configuration files, or local workspace paths.
"""

import os
import yaml
from pathlib import Path
from typing import Optional

CONFIG_FILE_PATH = Path.home() / ".paramananda" / "config.yaml"
ENV_DATA_PATH = "PARAMANANDA_DATA_PATH"
ENV_SAMPLES_PATH = "PARAMANANDA_SAMPLES_PATH"

class DataConfig:
    def __init__(self):
        self._file_config = self._load_file_config()

    def _load_file_config(self) -> dict:
        if CONFIG_FILE_PATH.exists():
            try:
                with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                print(f"Warning: Could not parse {CONFIG_FILE_PATH}: {e}")
                return {}
        return {}

    @property
    def data_path(self) -> Optional[str]:
        """
        Resolution order:
        1. Environment variable PARAMANANDA_DATA_PATH
        2. Config file ~/.paramananda/config.yaml -> data_path
        """
        env_val = os.environ.get(ENV_DATA_PATH)
        if env_val and os.path.exists(env_val):
            return os.path.abspath(env_val)
        
        file_val = self._file_config.get("data_path")
        if file_val and os.path.exists(file_val):
            return os.path.abspath(file_val)

        return None

    @property
    def samples_path(self) -> Optional[str]:
        env_val = os.environ.get(ENV_SAMPLES_PATH)
        if env_val and os.path.exists(env_val):
            return os.path.abspath(env_val)
        
        file_val = self._file_config.get("samples_path")
        if file_val and os.path.exists(file_val):
            return os.path.abspath(file_val)

        return None

_config = DataConfig()
