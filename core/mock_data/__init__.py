"""Mock data module for different application types"""
from .ecommerce_mock_data import EcommerceMockData
from .complete_news_mock_data import ComprehensiveNewsMockData
from .news_mock_data import NewsMockData
from .restaurant_mock_data import RestaurantMockData

MOCK_DATA_REGISTRY = {
    'news': NewsMockData,
    'ecommerce': EcommerceMockData,
    'restaurant': RestaurantMockData,
    'comp_news': ComprehensiveNewsMockData,
}

def get_mock_data_for_app_type(app_type):
    """Get mock data class for a specific app type"""
    return MOCK_DATA_REGISTRY.get(app_type.lower())