from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import youtube_utils
import ai_utils
import pandas as pd

st.set_page_config(page_title="YouTube AI Analyzer", layout="wide")
st.title("YouTube AI Analyzer")

channel_url = st.text_input("Enter YouTube Channel URL:")

if channel_url:
    try:
        channel_info, videos = youtube_utils.get_channel_data(channel_url)
        st.session_state["videos"] = videos

        st.subheader("Channel Information")
        st.write(f"Name: {channel_info['channel_name']}")
        st.write(f"Subscribers: {channel_info['subscribers']}")
        st.write(f"Total Views: {channel_info['views']}")
        st.write(f"Videos Fetched: {len(videos)}")
        st.markdown("---")
        search_query = st.text_input("Search videos by title or description:")
        filtered_videos = youtube_utils.search_videos(videos, search_query) if search_query else videos
        if st.session_state.get("run_analysis") and "selected_video" in st.session_state:
            video = st.session_state["selected_video"]
            st.subheader(f"Analysis for: {video['title']}")
            with st.spinner("Analyzing video..."):
                try:
                    transcript = ai_utils.get_video_transcript(video["id"])
                    analysis = ai_utils.analyze_video(video["title"], transcript)
                    sentiment = ai_utils.analyze_comments(video["id"])
                    st.markdown("AI Summary & Insights")
                    st.write(analysis)
                    st.markdown("Comment Sentiment")
                    df = pd.DataFrame([sentiment])
                    st.table(df)
                    st.session_state["run_analysis"] = False
                except Exception as e:
                    st.error(f"Error analyzing video: {e}")
        st.subheader("Select a Video")
        clicked_video = None
        for idx, v in enumerate(filtered_videos):
            st.write(f"**{v['title']}**")
            if st.button("Analyze", key=f"analyze_{idx}"):
                st.session_state["selected_video"] = v
                st.session_state["run_analysis"] = True
                st.rerun()
    except Exception as e:
        st.error(f"Error fetching channel data: {e}")
