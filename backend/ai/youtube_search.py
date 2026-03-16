"""
YouTube Video Search Module
Searches for educational videos based on keywords using YouTube Data API v3
"""

import requests
from typing import List, Dict


class YouTubeSearcher:
    """Search for educational videos on YouTube based on keywords."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3/search"
    
    def search_video(self, keyword: str, max_results: int = 1) -> List[Dict]:
        """
        Search for videos based on a keyword.
        
        Args:
            keyword: The search term
            max_results: Number of videos to return (default: 1)
        
        Returns:
            List of video dictionaries with title, url, description, and channel
        """
        params = {
            'part': 'snippet',
            'q': keyword,
            'key': self.api_key,
            'type': 'video',
            'maxResults': max_results,
            'order': 'relevance',
            'videoDefinition': 'high',
            'videoDuration': 'medium',  # Prefer medium-length educational content
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            videos = []
            for item in data.get('items', []):
                video_id = item['id']['videoId']
                snippet = item['snippet']
                
                video_info = {
                    'title': snippet['title'],
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'description': snippet['description'],
                    'channel': snippet['channelTitle'],
                    'thumbnail': snippet['thumbnails']['medium']['url'],
                    'published_at': snippet['publishedAt']
                }
                videos.append(video_info)
            
            return videos
        
        except requests.RequestException as e:
            print(f"Error searching for '{keyword}': {e}")
            return []
    
    def search_multiple_keywords(self, keywords: List[str]) -> Dict[str, List[Dict]]:
        """
        Search for videos for multiple keywords.
        
        Args:
            keywords: List of search keywords
        
        Returns:
            Dictionary mapping each keyword to its video results
        """
        results = {}
        for keyword in keywords:
            print(f"🔍 Searching for: {keyword}")
            videos = self.search_video(keyword, max_results=1)
            results[keyword] = videos
            if videos:
                print(f" Found video: {videos[0]['title']}\n")
            else:
                print(f" No videos found\n")
        
        return results
    
    def format_results(self, results: Dict[str, List[Dict]]) -> str:
        """
        Format search results into a readable string.
        
        Args:
            results: Dictionary of keyword -> videos
        
        Returns:
            Formatted string with video information
        """
        output = "\n📹 YouTube Video Suggestions\n" + "="*60 + "\n\n"
        
        for keyword, videos in results.items():
            output += f" Keyword: {keyword}\n"
            output += "-" * 60 + "\n"
            
            if not videos:
                output += "   No videos found for this keyword.\n\n"
                continue
            
            for i, video in enumerate(videos, 1):
                output += f"   {i}. {video['title']}\n"
                output += f"      Channel: {video['channel']}\n"
                output += f"      URL: {video['url']}\n"
                output += f"      Description: {video['description'][:150]}...\n"
                output += "\n"
        
        return output


def main():
    """Main function to demonstrate YouTube video search."""
    
    # YouTube API Key
    YOUTUBE_API_KEY = "AIzaSyBs1MR63pOlXOOvu0Zbw23B0b7NZh4E5Lg"
    
    # Initialize searcher
    searcher = YouTubeSearcher(YOUTUBE_API_KEY)
    
    print("🎥 YouTube Video Suggestion Tool\n")
    
    # Get keyword from user
    keyword = input("Enter a keyword: ").strip()
    
    if not keyword:
        print(" No keyword provided. Exiting.")
        return
    
    print(f"\n Searching for '{keyword}'...\n")
    
    # Search for video
    videos = searcher.search_video(keyword, max_results=1)
    
    if not videos:
        print(" No videos found for this keyword.")
        return
    
    # Display the best fit video
    video = videos[0]
    print(" Best Fit Video")
    print("=" * 60)
    print(f"\n Title: {video['title']}")
    print(f" Channel: {video['channel']}")
    print(f" URL: {video['url']}")
    print(f" Description: {video['description'][:200]}...")
    print(f" Published: {video['published_at'][:10]}")
    print(f" Thumbnail: {video['thumbnail']}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
