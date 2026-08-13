"""
Nepali NLP Library - Dataloader Package (`nepalinlplibrary.dataloader`)
"""

from .spec import DatasetSpec
from .loader import DatasetLoader
from .catalog import CatalogManager

__all__ = ["DatasetSpec", "DatasetLoader", "CatalogManager"]
