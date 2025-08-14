"""Mock data for news applications"""

from .base_mock_data import BaseMockData


class NewsMockData(BaseMockData):
    """Mock data provider for news applications"""

    def get_data_sources(self):
        return {
            "News Articles": self.get_news_articles(),
            "News Sources": self.get_news_sources(),
            "Categories": self.get_categories(),
            "Breaking News": self.get_breaking_news(),
            "Trending Stories": self.get_trending_stories()
        }

    def get_news_articles(self):
        return [
            {
                "id": "1",
                "title": "Breaking: Major Technology Breakthrough Announced",
                "description": "Scientists reveal groundbreaking discovery that could revolutionize computing",
                "content": "In a stunning announcement today, researchers at leading universities have unveiled a new quantum computing breakthrough...",
                "author": "John Smith",
                "source": "Tech Daily",
                "publishedAt": "2024-01-15T10:30:00Z",
                "urlToImage": "https://picsum.photos/400/200?random=1",
                "category": "technology",
                "readTime": "5 min",
                "likes": 1245,
                "comments": 89
            },
            {
                "id": "2",
                "title": "Global Climate Summit Reaches Historic Agreement",
                "description": "World leaders commit to ambitious new targets for carbon reduction",
                "content": "Representatives from 195 nations have signed a landmark agreement...",
                "author": "Sarah Johnson",
                "source": "World News Network",
                "publishedAt": "2024-01-15T08:45:00Z",
                "urlToImage": "https://picsum.photos/400/200?random=2",
                "category": "general",
                "readTime": "7 min",
                "likes": 3421,
                "comments": 234
            },
            {
                "id": "3",
                "title": "Stock Markets Hit Record Highs",
                "description": "Major indices surge as investors show renewed confidence",
                "content": "The S&P 500 and NASDAQ both reached all-time highs today...",
                "author": "Michael Chen",
                "source": "Financial Times",
                "publishedAt": "2024-01-15T14:20:00Z",
                "urlToImage": "https://picsum.photos/400/200?random=3",
                "category": "business",
                "readTime": "4 min",
                "likes": 567,
                "comments": 45
            },
            # Add more articles...
        ]

    def get_news_sources(self):
        return [
            {
                "id": "tech-daily",
                "name": "Tech Daily",
                "description": "Your source for the latest technology news",
                "category": "technology",
                "language": "en",
                "country": "US",
                "followers": 125000
            },
            {
                "id": "world-news",
                "name": "World News Network",
                "description": "Breaking news from around the globe",
                "category": "general",
                "language": "en",
                "country": "US",
                "followers": 500000
            },
            # Add more sources...
        ]

    def get_categories(self):
        return [
            {"id": "1", "name": "Technology", "icon": "computer", "color": "#2196F3"},
            {"id": "2", "name": "Business", "icon": "business", "color": "#4CAF50"},
            {"id": "3", "name": "Sports", "icon": "sports_soccer", "color": "#FF9800"},
            {"id": "4", "name": "Health", "icon": "health_and_safety", "color": "#E91E63"},
            {"id": "5", "name": "Science", "icon": "science", "color": "#9C27B0"},
            {"id": "6", "name": "Entertainment", "icon": "movie", "color": "#00BCD4"},
        ]

    def get_breaking_news(self):
        return [
            {
                "id": "b1",
                "title": "BREAKING: Emergency Response to Natural Disaster",
                "timestamp": "5 minutes ago",
                "priority": "high",
                "category": "urgent"
            },
            {
                "id": "b2",
                "title": "JUST IN: Major Policy Change Announced",
                "timestamp": "15 minutes ago",
                "priority": "medium",
                "category": "politics"
            }
        ]

    def get_trending_stories(self):
        return [
            {
                "id": "t1",
                "title": "Viral Story Takes Internet by Storm",
                "views": 1500000,
                "trending_rank": 1
            },
            {
                "id": "t2",
                "title": "Celebrity Announcement Breaks Records",
                "views": 980000,
                "trending_rank": 2
            }
        ]

    def get_sample_images(self):
        return {
            "news": [
                "https://picsum.photos/800/400?random=news1",
                "https://picsum.photos/800/400?random=news2",
            ],
            "thumbnails": [
                "https://picsum.photos/200/200?random=thumb1",
                "https://picsum.photos/200/200?random=thumb2",
            ]
        }