import os
import requests
from textblob import TextBlob
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
LLM_API_KEY = os.getenv("LLM_API_KEY")

def get_youtube_client():
    return build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([t["text"] for t in transcript])
        return text
    except Exception:
        return None

def analyze_video(title, transcript):
    if not transcript:
        transcript = "Transcript unavailable."
    prompt = f"""
    Analyze this YouTube video titled "{title}".
    Provide:
    1. 5-bullet summary
    2. Key takeaways
    3. Creator's style
    4. Content quality
    Transcript: {transcript[:3000]}
    """
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {LLM_API_KEY}"},
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=60
    )
    data = response.json()
    return data["choices"][0]["message"]["content"]

def analyze_comments(video_id):
    youtube = get_youtube_client()
    comments = []
    request = youtube.commentThreads().list(
        part="snippet", videoId=video_id, maxResults=20, textFormat="plainText"
    )
    response = request.execute()
    for item in response["items"]:
        text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(text)
    pos = neu = neg = 0
    for c in comments:
        polarity = TextBlob(c).sentiment.polarity
        if polarity > 0.1:
            pos += 1
        elif polarity < -0.1:
            neg += 1
        else:
            neu += 1
    total = max(len(comments), 1)
    return {
        "positive": round(pos / total * 100, 1),
        "neutral": round(neu / total * 100, 1),
        "negative": round(neg / total * 100, 1),
    }
