# -*- coding: utf-8 -*-
"""
Unit tests for nepalinlplibrary.config (DataConfig)
"""

import os
import pytest
from nepalinlplibrary.config import DataConfig, ENV_DATA_PATH

def test_data_config_env_override(tmp_path, monkeypatch):
    test_data_dir = tmp_path / "data_override"
    test_data_dir.mkdir()

    monkeypatch.setenv(ENV_DATA_PATH, str(test_data_dir))
    config = DataConfig()
    
    assert config.data_path is not None
    assert os.path.abspath(config.data_path) == os.path.abspath(str(test_data_dir))

def test_data_config_fallback(monkeypatch):
    monkeypatch.delenv(ENV_DATA_PATH, raising=False)
    config = DataConfig()
    # When env var is absent and no config.yaml exists, data_path is None or file path
    assert config.data_path is None or os.path.exists(config.data_path)
