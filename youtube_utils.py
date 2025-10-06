import os
from googleapiclient.discovery import build

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_youtube_client():
    return build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def extract_channel_id(url: str) -> str:
    youtube = get_youtube_client()
    if "channel/" in url:
        return url.split("channel/")[1].split("/")[0]
    elif "youtube.com/@" in url:
        username = url.split("@")[1].split("/")[0]
        request = youtube.search().list(part="snippet", q=username, type="channel", maxResults=1)
        response = request.execute()
        return response["items"][0]["snippet"]["channelId"]
    elif "/user/" in url or "/c/" in url:
        request = youtube.search().list(part="snippet", q=url, type="channel", maxResults=1)
        response = request.execute()
        return response["items"][0]["snippet"]["channelId"]
    else:
        raise ValueError("Invalid YouTube channel URL format.")

def get_channel_data(channel_url):
    youtube = get_youtube_client()
    channel_id = extract_channel_id(channel_url)
    request = youtube.channels().list(part="snippet,statistics", id=channel_id)
    response = request.execute()
    data = response["items"][0]
    channel_info = {
        "channel_name": data["snippet"]["title"],
        "subscribers": data["statistics"].get("subscriberCount", "Hidden"),
        "views": data["statistics"]["viewCount"],
    }
    videos = []
    req = youtube.search().list(part="snippet", channelId=channel_id, maxResults=50, order="date")
    res = req.execute()
    for item in res["items"]:
        if item["id"]["kind"] == "youtube#video":
            videos.append({
                "id": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "description": item["snippet"].get("description", "")
            })
    return channel_info, videos

def search_videos(videos, query):
    if not query:
        return videos
    q = query.lower()
    return [v for v in videos if q in v["title"].lower() or q in v["description"].lower()]
