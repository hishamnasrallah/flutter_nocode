"""Base class for mock data providers"""

import json
from abc import ABC, abstractmethod


class BaseMockData(ABC):
    """Base class for all mock data providers"""

    @abstractmethod
    def get_data_sources(self):
        """Return dictionary of data source names and their mock data"""
        pass

    @abstractmethod
    def get_sample_images(self):
        """Return dictionary of image categories and URLs"""
        pass

    def to_json(self, data):
        """Convert Python data to JSON string"""
        return json.dumps(data, indent=2, ensure_ascii=False)