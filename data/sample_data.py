import sys
import os
from pathlib import Path

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

SAMPLE_ASSET_DATA = [
    {
        "name": "Gold",
        "type": "asset_class",
        "description": "Precious metal commodity",
        "sub_classes": ["Physical Gold", "Gold ETFs", "Gold Mining Stocks"],
    },
    {
        "name": "Apple Inc",
        "type": "security_name",
        "sector": "Technology",
        "sub_sector": "Consumer Electronics",
    },
    {
        "name": "US Equities",
        "type": "asset_class",
        "description": "United States listed stocks",
        "sub_classes": ["Large Cap", "Mid Cap", "Small Cap"],
    }
]