import requests
from collections import Counter
import re
import random
from typing import List, Tuple, Optional, Dict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.util import ngrams
from textblob import TextBlob
import spacy

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

API_KEY = "Enter Your Youtube Data API Key"  # Replace with your actual YouTube Data API key

EMOTIONAL_TRIGGERS = [
    "Amazing", "Incredible", "Unbelievable", "Mind-blowing", "Secrets", "Revealed",
    "Untold", "Discover", "Now", "Instant", "Hurry", "Quick", "Insider", "Exclusive",
    "Limited", "VIP", "Proven", "Guaranteed", "Reliable", "Authentic"
]

def get_top_videos(api_key: str, query: str, max_results: int = 50) -> Optional[List[dict]]:
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults={max_results}&key={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('items', [])
    except requests.RequestException as e:
        print(f"Error fetching videos: {e}")
        return None

def preprocess_text(text: str) -> str:
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return ' '.join(text.lower().split())

def generate_title(keyword: str) -> str:
    title_structure = [
        random.choice(EMOTIONAL_TRIGGERS),
        keyword.title(),
        random.choice(["Secrets", "Adventures", "Discoveries", "Explorations"]),
        f"({random.choice(EMOTIONAL_TRIGGERS)} Tips)"
    ]
    
    new_title = ' '.join(title_structure)
    return new_title[:70].strip()

def generate_description(keyword: str) -> str:
    intro = f"{random.choice(EMOTIONAL_TRIGGERS)}! {random.choice(EMOTIONAL_TRIGGERS)} guide to {keyword}! 🚀"
    content_details = f"Embark on an extraordinary journey into the world of {keyword}. Discover hidden gems, expert insights, and breathtaking experiences that will leave you in awe."
    cta = f"🔔 {random.choice(EMOTIONAL_TRIGGERS)}! SUBSCRIBE now for {random.choice(EMOTIONAL_TRIGGERS)} {keyword} content!"
    engagement = f"👇 Share your {random.choice(EMOTIONAL_TRIGGERS)} thoughts! What's your experience with {keyword}?"
    outro = f"Don't miss out on our upcoming videos about {keyword} and related topics. Stay tuned for more {random.choice(EMOTIONAL_TRIGGERS)} content!"
    
    description = f"{intro}\n\n{content_details}\n\n{cta}\n\n{engagement}\n\n{outro}"
    
    return description[:2000].strip()

def generate_tags(keyword: str) -> List[str]:
    base_tags = keyword.split()
    related_terms = [
        "adventure", "exploration", "discovery", "travel", "experience",
        "guide", "tips", "secrets", "hidden", "amazing", "breathtaking",
        "unforgettable", "journey", "expedition", "ultimate"
    ]
    
    tags = [keyword] + base_tags + related_terms
    tags += [f"{keyword} {term}" for term in related_terms]
    tags += [f"{term} {keyword}" for term in related_terms]
    
    # Remove duplicates and limit to 30 tags
    return list(dict.fromkeys(tags))[:30]

def generate_hashtags(tags: List[str], keyword: str) -> List[str]:
    hashtags = [f"#{tag.replace(' ', '')}" for tag in tags[:14] if len(tag) > 2]
    keyword_hashtag = f"#{keyword.replace(' ', '')}"
    if keyword_hashtag not in hashtags:
        hashtags.insert(0, keyword_hashtag)
    return list(dict.fromkeys(hashtags))[:15]

def calculate_seo_score(title: str, description: str, tags: List[str], hashtags: List[str]) -> int:
    score = 0
    if len(title) <= 70:
        score += 20
    if 500 <= len(description) <= 2000:
        score += 30
    score += min(len(tags), 30)
    score += min(len(hashtags) * 2, 20)
    return min(score, 100)

def get_mock_analytics() -> Dict[str, int]:
    return {
        "views": random.randint(10000, 1000000),
        "likes": random.randint(1000, 100000),
        "comments": random.randint(100, 10000),
        "shares": random.randint(50, 5000)
    }

def generate_seo_content(query: str) -> Tuple[str, str, List[str], List[str], int, Dict[str, int]]:
    new_title = generate_title(query)
    new_description = generate_description(query)
    new_tags = generate_tags(query)
    new_hashtags = generate_hashtags(new_tags, query)
    
    seo_score = calculate_seo_score(new_title, new_description, new_tags, new_hashtags)
    mock_analytics = get_mock_analytics()

    return new_title, new_description, new_tags, new_hashtags, seo_score, mock_analytics

def process_keyword(keyword: str) -> None:
    print(f"\nGenerating SEO Content for '{keyword}'...")
    
    for i in range(2):
        title, description, tags, hashtags, seo_score, analytics = generate_seo_content(keyword)

        print(f"\n{'='*80}\nSEO Content (Option {i+1})\n{'='*80}")
        print(f"\nTitle:\n{title}")
        print(f"\nDescription:\n{description}")
        print(f"\nTags:\n{', '.join(tags)}")
        print(f"\nHashtags:\n{' '.join(hashtags)}")
        print(f"\nSEO Score: {seo_score}/100")
        print("\nEstimated Analytics:")
        for key, value in analytics.items():
            print(f"  {key.capitalize()}: {value:,}")

def main():
    print("Welcome to the Advanced YouTube SEO Generator!")
    while True:
        print("\n1. Generate SEO Content")
        print("2. Exit")
        choice = input("Enter your choice (1-2): ")
        
        if choice == '1':
            keyword = input("Enter a keyword to generate SEO content: ")
            process_keyword(keyword)
        elif choice == '2':
            print("Thank you for using the Advanced YouTube SEO Generator. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()