"""Comprehensive mock data for news application"""

from .base_mock_data import BaseMockData
import random
from datetime import datetime, timedelta
import uuid


class ComprehensiveNewsMockData(BaseMockData):
    """Comprehensive mock data provider for news application"""

    def __init__(self):
        self.categories = self._generate_categories()
        self.sources = self._generate_sources()
        self.authors = self._generate_authors()
        self.articles = self._generate_articles()

    def get_data_sources(self):
        """Return dictionary of data source names and their mock data - Required by BaseMockData"""
        return {
            "News Feed": self.articles,
            "Categories": self.categories,
            "Sources": self.sources,
            "Authors": self.authors,
            "Breaking News": self.get_breaking(),
            "Trending Stories": self.get_trending(),
            "Video News": self.get_videos(),
            "Podcasts": self.get_podcasts(),
            "Premium Content": self.get_premium(),
            "Bookmarks": self.get_bookmarks(None),
            "Notifications": self.get_notifications(None)
        }

    def get_sample_images(self):
        """Return dictionary of image categories and URLs - Required by BaseMockData"""
        return {
            "articles": [f"https://picsum.photos/800/400?random=article{i}" for i in range(1, 21)],
            "thumbnails": [f"https://picsum.photos/300/200?random=thumb{i}" for i in range(1, 21)],
            "authors": [f"https://picsum.photos/200/200?random=author{i}" for i in range(1, 11)],
            "sources": [f"https://picsum.photos/100/100?random=source{i}" for i in range(1, 11)],
            "categories": [f"https://picsum.photos/400/200?random=cat{i}" for i in range(1, 26)],
            "banners": [f"https://picsum.photos/1200/400?random=banner{i}" for i in range(1, 6)]
        }

    def _generate_categories(self):
        """Generate 25+ news categories"""
        categories = [
            {"id": "breaking", "name": "Breaking News", "icon": "warning", "color": "#FF0000", "priority": 1},
            {"id": "world", "name": "World News", "icon": "public", "color": "#2196F3", "priority": 2},
            {"id": "politics", "name": "Politics", "icon": "how_to_vote", "color": "#9C27B0", "priority": 3},
            {"id": "business", "name": "Business", "icon": "business", "color": "#4CAF50", "priority": 4},
            {"id": "technology", "name": "Technology", "icon": "computer", "color": "#00BCD4", "priority": 5},
            {"id": "science", "name": "Science", "icon": "science", "color": "#FF9800", "priority": 6},
            {"id": "health", "name": "Health", "icon": "health_and_safety", "color": "#E91E63", "priority": 7},
            {"id": "sports", "name": "Sports", "icon": "sports", "color": "#795548", "priority": 8},
            {"id": "entertainment", "name": "Entertainment", "icon": "movie", "color": "#FF5722", "priority": 9},
            {"id": "lifestyle", "name": "Lifestyle", "icon": "style", "color": "#607D8B", "priority": 10},
            {"id": "education", "name": "Education", "icon": "school", "color": "#3F51B5", "priority": 11},
            {"id": "environment", "name": "Environment", "icon": "eco", "color": "#8BC34A", "priority": 12},
            {"id": "crime", "name": "Crime", "icon": "gavel", "color": "#F44336", "priority": 13},
            {"id": "weather", "name": "Weather", "icon": "wb_sunny", "color": "#FFEB3B", "priority": 14},
            {"id": "opinion", "name": "Opinion", "icon": "forum", "color": "#673AB7", "priority": 15},
            {"id": "local", "name": "Local News", "icon": "location_on", "color": "#009688", "priority": 16},
            {"id": "culture", "name": "Arts & Culture", "icon": "palette", "color": "#E91E63", "priority": 17},
            {"id": "automotive", "name": "Automotive", "icon": "directions_car", "color": "#424242", "priority": 18},
            {"id": "realestate", "name": "Real Estate", "icon": "home", "color": "#6D4C41", "priority": 19},
            {"id": "crypto", "name": "Cryptocurrency", "icon": "currency_bitcoin", "color": "#FFC107", "priority": 20},
            {"id": "gaming", "name": "Gaming", "icon": "sports_esports", "color": "#7C4DFF", "priority": 21},
            {"id": "photography", "name": "Photography", "icon": "photo_camera", "color": "#00ACC1", "priority": 22},
            {"id": "food", "name": "Food & Dining", "icon": "restaurant", "color": "#FF7043", "priority": 23},
            {"id": "travel", "name": "Travel", "icon": "flight", "color": "#26A69A", "priority": 24},
            {"id": "fashion", "name": "Fashion", "icon": "checkroom", "color": "#AB47BC", "priority": 25},
        ]
        return categories

    def _generate_sources(self):
        """Generate news sources"""
        sources = [
            {
                "id": str(uuid.uuid4()),
                "name": "Global News Network",
                "logo": "https://picsum.photos/100/100?random=1",
                "website": "https://gnn.example.com",
                "description": "24/7 Global News Coverage",
                "category": "general",
                "language": "en",
                "country": "US",
                "followers": 5000000,
                "verified": True,
                "trustScore": 95
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Tech Today",
                "logo": "https://picsum.photos/100/100?random=2",
                "website": "https://techtoday.example.com",
                "description": "Latest Technology News and Reviews",
                "category": "technology",
                "language": "en",
                "country": "US",
                "followers": 2500000,
                "verified": True,
                "trustScore": 92
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Business Weekly",
                "logo": "https://picsum.photos/100/100?random=3",
                "website": "https://businessweekly.example.com",
                "description": "Financial News and Market Analysis",
                "category": "business",
                "language": "en",
                "country": "US",
                "followers": 1800000,
                "verified": True,
                "trustScore": 90
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Sports Central",
                "logo": "https://picsum.photos/100/100?random=4",
                "website": "https://sportscentral.example.com",
                "description": "Complete Sports Coverage",
                "category": "sports",
                "language": "en",
                "country": "US",
                "followers": 3200000,
                "verified": True,
                "trustScore": 88
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Entertainment Daily",
                "logo": "https://picsum.photos/100/100?random=5",
                "website": "https://entertainmentdaily.example.com",
                "description": "Celebrity News and Entertainment",
                "category": "entertainment",
                "language": "en",
                "country": "US",
                "followers": 4100000,
                "verified": True,
                "trustScore": 85
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Science Journal",
                "logo": "https://picsum.photos/100/100?random=6",
                "website": "https://sciencejournal.example.com",
                "description": "Scientific Discoveries and Research",
                "category": "science",
                "language": "en",
                "country": "US",
                "followers": 950000,
                "verified": True,
                "trustScore": 94
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Health Monitor",
                "logo": "https://picsum.photos/100/100?random=7",
                "website": "https://healthmonitor.example.com",
                "description": "Medical News and Health Tips",
                "category": "health",
                "language": "en",
                "country": "US",
                "followers": 1200000,
                "verified": True,
                "trustScore": 91
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Local Voice",
                "logo": "https://picsum.photos/100/100?random=8",
                "website": "https://localvoice.example.com",
                "description": "Your Local News Source",
                "category": "local",
                "language": "en",
                "country": "US",
                "followers": 450000,
                "verified": True,
                "trustScore": 87
            },
            {
                "id": str(uuid.uuid4()),
                "name": "World Report",
                "logo": "https://picsum.photos/100/100?random=9",
                "website": "https://worldreport.example.com",
                "description": "International News Coverage",
                "category": "world",
                "language": "en",
                "country": "UK",
                "followers": 3800000,
                "verified": True,
                "trustScore": 93
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Political Insider",
                "logo": "https://picsum.photos/100/100?random=10",
                "website": "https://politicalinsider.example.com",
                "description": "Politics and Government News",
                "category": "politics",
                "language": "en",
                "country": "US",
                "followers": 2100000,
                "verified": True,
                "trustScore": 86
            }
        ]
        return sources

    def _generate_authors(self):
        """Generate journalist/author profiles"""
        first_names = ["John", "Sarah", "Michael", "Emma", "David", "Lisa", "Robert", "Maria", "James", "Anna",
                      "William", "Jennifer", "Charles", "Patricia", "Thomas", "Linda", "Christopher", "Barbara",
                      "Daniel", "Elizabeth", "Matthew", "Susan", "Joseph", "Jessica", "Mark", "Karen"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Wilson", "Martinez",
                     "Anderson", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White", "Harris", "Clark"]
        specialties = ["Politics", "Technology", "Business", "Sports", "Health", "Science", "Entertainment",
                      "World Affairs", "Environment", "Education", "Crime", "Culture", "Fashion", "Food", "Travel"]

        authors = []
        for i in range(50):
            authors.append({
                "id": str(uuid.uuid4()),
                "name": f"{random.choice(first_names)} {random.choice(last_names)}",
                "avatar": f"https://picsum.photos/200/200?random=author{i}",
                "bio": f"Award-winning journalist specializing in {random.choice(specialties)}. {random.randint(5, 25)} years of experience.",
                "specialty": random.choice(specialties),
                "verified": random.choice([True, False]),
                "followers": random.randint(1000, 100000),
                "articles_count": random.randint(50, 500),
                "awards": random.randint(0, 10),
                "twitter": f"@journalist{i}",
                "email": f"journalist{i}@news.com"
            })
        return authors

    def _generate_articles(self):
        """Generate comprehensive article data"""
        articles = []

        # Headlines templates for different categories
        headline_templates = {
            "breaking": [
                "BREAKING: Major Development in {} Situation",
                "URGENT: {} Announces Immediate Action",
                "LIVE UPDATE: {} Crisis Unfolds",
                "BREAKING NEWS: Historic {} Agreement Reached",
                "ALERT: Emergency Response to {} Incident"
            ],
            "technology": [
                "{} Unveils Revolutionary New Technology",
                "How {} is Changing the Future of Tech",
                "{} Breakthrough Could Transform Industry",
                "Exclusive: Inside {}'s Secret Project",
                "{} Stock Soars After Tech Announcement"
            ],
            "business": [
                "{} Stock Surges After Earnings Beat",
                "{} CEO Announces Major Restructuring",
                "Market Analysis: Why {} is Trending",
                "{} Merger Creates Industry Giant",
                "Economic Impact: {} Decision Affects Millions"
            ],
            "sports": [
                "{} Wins Championship in Dramatic Fashion",
                "Breaking: {} Star Player Traded",
                "{} Sets New World Record",
                "Exclusive Interview with {} Coach",
                "{} Season Preview: What to Expect"
            ],
            "entertainment": [
                "{} Wins Major Award at Ceremony",
                "Exclusive: {} Announces New Project",
                "{} Box Office Breaks Records",
                "Behind the Scenes of {}'s Latest",
                "{} Controversy Sparks Debate"
            ],
            "health": [
                "New Study: {} Shows Promising Results",
                "Medical Breakthrough in {} Treatment",
                "Health Alert: {} Cases Rising",
                "Expert Tips for {} Prevention",
                "Research Reveals {} Connection"
            ],
            "politics": [
                "{} Announces Presidential Bid",
                "Congress Passes {} Legislation",
                "{} Policy Sparks National Debate",
                "Election Update: {} Takes Lead",
                "Analysis: Impact of {} Decision"
            ],
            "science": [
                "Scientists Discover {} in Space",
                "Breakthrough: {} Could Change Everything",
                "Research Team Uncovers {} Mystery",
                "Climate Study Reveals {} Trend",
                "Nobel Prize Awarded for {} Discovery"
            ]
        }

        subjects = ["Global Leaders", "Tech Giants", "Market Analysts", "Scientists", "Government Officials",
                   "Healthcare Workers", "Athletes", "Celebrities", "Researchers", "Industry Experts"]

        # Generate 200+ articles with rich content
        for i in range(200):
            category = random.choice(self.categories)
            author = random.choice(self.authors)
            source = random.choice(self.sources)

            # Random publication time within last 30 days
            pub_date = datetime.now() - timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )

            # Get appropriate headline template for category
            templates = headline_templates.get(category["id"], ["Latest Update on {}"])
            headline_template = random.choice(templates)
            headline = headline_template.format(random.choice(subjects))

            article = {
                "id": str(uuid.uuid4()),
                "title": headline,
                "summary": self._generate_summary(),
                "content": self._generate_content(),
                "author": author,
                "source": source,
                "category": category,
                "subcategory": self._get_subcategory(category),
                "tags": self._generate_tags(category),
                "featuredImage": f"https://picsum.photos/800/400?random={i}",
                "images": [
                    f"https://picsum.photos/600/400?random={i}1",
                    f"https://picsum.photos/600/400?random={i}2",
                    f"https://picsum.photos/600/400?random={i}3"
                ],
                "videoUrl": f"https://example.com/video{i}.mp4" if random.random() > 0.7 else None,
                "audioUrl": f"https://example.com/audio{i}.mp3" if random.random() > 0.8 else None,
                "publishedAt": pub_date.isoformat(),
                "updatedAt": (pub_date + timedelta(hours=random.randint(0, 24))).isoformat(),
                "readingTime": random.randint(1, 15),
                "wordCount": random.randint(200, 2000),
                "viewsCount": random.randint(100, 1000000),
                "likesCount": random.randint(10, 50000),
                "commentsCount": random.randint(0, 1000),
                "sharesCount": random.randint(0, 10000),
                "bookmarksCount": random.randint(0, 5000),
                "isPremium": random.random() > 0.8,
                "isBreaking": random.random() > 0.95,
                "isTrending": random.random() > 0.85,
                "isExclusive": random.random() > 0.9,
                "isFactChecked": random.random() > 0.7,
                "factCheckScore": random.randint(70, 100) if random.random() > 0.7 else None,
                "sentiment": random.choice(["positive", "negative", "neutral"]),
                "importance": random.choice(["high", "medium", "low"]),
                "location": self._generate_location(),
                "relatedArticles": [],  # Will be filled with IDs
                "comments": self._generate_comments(random.randint(0, 20))
            }
            articles.append(article)

        # Link related articles
        for article in articles:
            article["relatedArticles"] = random.sample(
                [a["id"] for a in articles if a["id"] != article["id"]],
                min(5, len(articles) - 1)
            )

        return articles

    def _generate_summary(self):
        """Generate article summary"""
        summaries = [
            "In a groundbreaking development that has captured global attention, experts are calling this the most significant advancement in recent years.",
            "New data reveals surprising trends that could reshape our understanding of this critical issue.",
            "Industry leaders gather to discuss the implications of recent events and chart a path forward.",
            "Exclusive investigation uncovers details that challenge conventional wisdom on this important topic.",
            "Analysis shows unprecedented patterns emerging in data that could signal major changes ahead.",
            "Breaking developments continue to unfold in this rapidly evolving situation that affects millions.",
            "Expert analysis provides new insights into complex challenges facing society today.",
            "Revolutionary approach promises to transform how we think about this fundamental issue.",
            "Latest research findings offer hope for breakthrough solutions to long-standing problems.",
            "Comprehensive report examines the far-reaching implications of recent policy decisions."
        ]
        return random.choice(summaries)

    def _generate_content(self):
        """Generate rich article content"""
        paragraphs = []
        num_paragraphs = random.randint(5, 15)

        for i in range(num_paragraphs):
            paragraph = f"""Paragraph {i+1}: In today's rapidly evolving landscape, stakeholders are closely monitoring 
            developments that could have far-reaching implications. Recent data suggests that trends observed over 
            the past quarter are accelerating, prompting experts to reassess their projections. Industry analysts 
            point to several key factors driving these changes, including technological advancement, shifting consumer 
            preferences, and regulatory updates. The convergence of these elements creates both opportunities and 
            challenges for organizations navigating this complex environment."""
            paragraphs.append(paragraph)

        return "\n\n".join(paragraphs)

    def _generate_tags(self, category):
        """Generate relevant tags"""
        all_tags = [
            "trending", "exclusive", "analysis", "opinion", "investigation",
            "update", "feature", "profile", "review", "guide", "tutorial",
            "announcement", "report", "study", "research", "data",
            "interview", "documentary", "live", "developing", "verified"
        ]
        return random.sample(all_tags, random.randint(3, 7))

    def _get_subcategory(self, category):
        """Get subcategory based on main category"""
        subcategories = {
            "technology": ["AI", "Smartphones", "Software", "Hardware", "Internet", "Cybersecurity", "Startups"],
            "business": ["Markets", "Startups", "Finance", "Economy", "Corporate", "Real Estate", "Banking"],
            "sports": ["Football", "Basketball", "Tennis", "Cricket", "Olympics", "Baseball", "Soccer"],
            "entertainment": ["Movies", "Music", "Television", "Streaming", "Gaming", "Books", "Theater"],
            "politics": ["Elections", "Policy", "International", "Congress", "White House", "Courts", "Local"],
            "health": ["Medicine", "Fitness", "Nutrition", "Mental Health", "Research", "Hospitals", "Vaccines"],
            "science": ["Space", "Physics", "Biology", "Chemistry", "Earth Science", "Technology", "Research"]
        }
        return random.choice(subcategories.get(category["id"], ["General"]))

    def _generate_location(self):
        """Generate location data"""
        locations = [
            {"city": "New York", "state": "NY", "country": "USA", "lat": 40.7128, "lng": -74.0060},
            {"city": "London", "state": None, "country": "UK", "lat": 51.5074, "lng": -0.1278},
            {"city": "Tokyo", "state": None, "country": "Japan", "lat": 35.6762, "lng": 139.6503},
            {"city": "Paris", "state": None, "country": "France", "lat": 48.8566, "lng": 2.3522},
            {"city": "Sydney", "state": "NSW", "country": "Australia", "lat": -33.8688, "lng": 151.2093},
            {"city": "Dubai", "state": None, "country": "UAE", "lat": 25.2048, "lng": 55.2708},
            {"city": "Singapore", "state": None, "country": "Singapore", "lat": 1.3521, "lng": 103.8198},
            {"city": "Mumbai", "state": "Maharashtra", "country": "India", "lat": 19.0760, "lng": 72.8777},
            {"city": "Toronto", "state": "Ontario", "country": "Canada", "lat": 43.6532, "lng": -79.3832},
            {"city": "Berlin", "state": None, "country": "Germany", "lat": 52.5200, "lng": 13.4050}
        ]
        return random.choice(locations) if random.random() > 0.3 else None

    def _generate_comments(self, count):
        """Generate comment threads"""
        comments = []
        usernames = ["NewsReader", "InfoSeeker", "TruthHunter", "FactChecker", "Observer",
                    "Analyst", "Commenter", "Viewer", "Reader", "Subscriber"]

        for i in range(count):
            comment = {
                "id": str(uuid.uuid4()),
                "userId": str(uuid.uuid4()),
                "userName": f"{random.choice(usernames)}{random.randint(100, 999)}",
                "userAvatar": f"https://picsum.photos/50/50?random=user{i}",
                "content": self._generate_comment_content(),
                "timestamp": (datetime.now() - timedelta(hours=random.randint(1, 72))).isoformat(),
                "likes": random.randint(0, 100),
                "dislikes": random.randint(0, 20),
                "replies": self._generate_replies(random.randint(0, 3))
            }
            comments.append(comment)
        return comments

    def _generate_comment_content(self):
        """Generate comment content"""
        comments = [
            "This is a very insightful article. Thanks for sharing!",
            "I disagree with some points, but overall well researched.",
            "Can you provide more sources for these claims?",
            "This confirms what I've been observing in my field.",
            "Interesting perspective, hadn't thought about it this way.",
            "The data presented here is compelling.",
            "Would love to see a follow-up article on this topic.",
            "How does this compare to the situation in other countries?",
            "Great journalism! Keep up the excellent work.",
            "This needs more fact-checking before drawing conclusions."
        ]
        return random.choice(comments)

    def _generate_replies(self, count):
        """Generate reply threads"""
        replies = []
        for i in range(count):
            replies.append({
                "id": str(uuid.uuid4()),
                "userId": str(uuid.uuid4()),
                "userName": f"User{random.randint(1000, 9999)}",
                "content": "I agree with your point.",
                "timestamp": datetime.now().isoformat(),
                "likes": random.randint(0, 20)
            })
        return replies

    # API Methods for different endpoints
    def get_feed(self, user_id=None, page=1, limit=20):
        """Get personalized feed"""
        start = (page - 1) * limit
        end = start + limit
        return {
            "articles": self.articles[start:end],
            "page": page,
            "total": len(self.articles),
            "hasMore": end < len(self.articles)
        }

    def get_trending(self):
        """Get trending articles"""
        trending = [a for a in self.articles if a.get("isTrending")]
        return sorted(trending, key=lambda x: x["viewsCount"], reverse=True)[:20]

    def get_breaking(self):
        """Get breaking news"""
        return [a for a in self.articles if a.get("isBreaking")][:10]

    def get_by_category(self, category_id):
        """Get articles by category"""
        return [a for a in self.articles if a["category"]["id"] == category_id]

    def search(self, query, filters=None):
        """Search articles"""
        results = []
        query_lower = query.lower()
        for article in self.articles:
            if (query_lower in article["title"].lower() or
                query_lower in article["summary"].lower()):
                results.append(article)
        return results[:50]

    def get_article_details(self, article_id):
        """Get full article with all details"""
        for article in self.articles:
            if article["id"] == article_id:
                return article
        return None

    def get_recommendations(self, user_id):
        """Get AI-powered recommendations"""
        return random.sample(self.articles, min(20, len(self.articles)))

    def get_categories(self):
        """Get all categories"""
        return self.categories

    def get_sources(self):
        """Get all news sources"""
        return self.sources

    def get_authors(self):
        """Get all authors"""
        return self.authors

    def get_videos(self):
        """Get video news"""
        return [a for a in self.articles if a.get("videoUrl")][:20]

    def get_podcasts(self):
        """Get podcast episodes"""
        return [a for a in self.articles if a.get("audioUrl")][:20]

    def get_premium(self):
        """Get premium content"""
        return [a for a in self.articles if a.get("isPremium")][:20]

    def get_local_news(self, location=None):
        """Get local news based on location"""
        if location:
            return [a for a in self.articles if a.get("location") and a["location"]["city"] == location]
        return [a for a in self.articles if a["category"]["id"] == "local"][:20]

    def get_notifications(self, user_id):
        """Get user notifications"""
        notifications = []
        for i in range(10):
            notifications.append({
                "id": str(uuid.uuid4()),
                "type": random.choice(["breaking", "trending", "comment", "follow", "like"]),
                "title": "New notification",
                "message": "You have a new update",
                "timestamp": (datetime.now() - timedelta(hours=random.randint(1, 24))).isoformat(),
                "read": random.choice([True, False]),
                "articleId": random.choice(self.articles)["id"] if self.articles else None
            })
        return notifications

    def get_bookmarks(self, user_id):
        """Get user bookmarks"""
        return random.sample(self.articles, min(10, len(self.articles)))

    def get_history(self, user_id):
        """Get reading history"""
        return random.sample(self.articles, min(15, len(self.articles)))

    def get_stats(self):
        """Get platform statistics"""
        return {
            "totalArticles": len(self.articles),
            "totalCategories": len(self.categories),
            "totalSources": len(self.sources),
            "totalAuthors": len(self.authors),
            "totalViews": sum(a["viewsCount"] for a in self.articles),
            "totalLikes": sum(a["likesCount"] for a in self.articles),
            "totalComments": sum(a["commentsCount"] for a in self.articles),
            "totalShares": sum(a["sharesCount"] for a in self.articles),
            "trendingTopics": self._get_trending_topics(),
            "topAuthors": self._get_top_authors(),
            "topSources": self._get_top_sources()
        }

    def _get_trending_topics(self):
        """Get trending topics"""
        topics = ["Climate Change", "AI Technology", "Economic Recovery", "Space Exploration",
                 "Healthcare Reform", "Cybersecurity", "Remote Work", "Electric Vehicles",
                 "Social Media", "Cryptocurrency"]
        return random.sample(topics, 5)

    def _get_top_authors(self):
        """Get top authors by followers"""
        return sorted(self.authors, key=lambda x: x["followers"], reverse=True)[:5]

    def _get_top_sources(self):
        """Get top sources by trust score"""
        return sorted(self.sources, key=lambda x: x["trustScore"], reverse=True)[:5]