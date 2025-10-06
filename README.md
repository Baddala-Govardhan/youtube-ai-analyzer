# youtube-ai-analyzer

Live Url - https://web-production-11386.up.railway.app/


**a. Challenges faced and how you solved them**

I didn't face any big challenges because i used streamlit the main thing is API keys exceed everytime i need to change the API keys 

**b. Trade-offs made during development**

I choose simplicity over scalability. Instead of a full backend (eg,flask,React.js,Angular) so everything runs within streamlit to keep it lightweight for demo purpose so this reduces flexibility for handling large scale video analysis and it gives quick response  and easy deployment

**c. What you would improve with more time**

- Improve UI/UX with a modern React or Next.js frontend that communicates with a Python backend API.
- Implement caching and asynchronous processing to handle multiple video analyses faster and reduce repeated API calls
- Add data visualizations to show trends in sentiment, views, and engagement across all channel videos
- Experiment with fine-tuned summarization models and include topic classification to improve content insights
- set up automatic report generation that summarizes a channel performance and tone over time
- OAuth login so users can analyze their private playlists


**Architecture Workflow**

User enters a YouTube channel -> Videos are fetched -> User selects -> Transcript & comments are analyzed -> AI summary + sentiment report displayed

**Tech Stack Choices**

- Streamlit –  front-end + back-end integration for rapid prototyping.

- Python –  support for APIs and data handling.

- Google API Client + YouTube Transcript API – For channel & transcript retrieval.

- OpenRouter – For AI summarization and insights.

- TextBlob – For lightweight comment sentiment analysis.

- Railway – For fast cloud deployment with secret management

**Setup**

**Clone repository**

- git clone https://github.com/Baddala-Govardhan/youtube-ai-analyzer.git

- cd youtube-ai-analyzer

**Create virtual environment**

- python3 -m venv venv

- source venv/bin/activate

**Install dependencies**

- pip install -r requirements.txt

**Run locally**

- streamlit run app.py


**API Keys**

- YOUTUBE_API_KEY - AIzaSyBRE--fxmY8yu-f2SSCYe4DrCkQerEzCYk

- LLM_API_KEY - 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

- create .env file and the API keys or in railway -> variables 


**Deployment Process**

- Project Push to Github -> got railway.app -> create a new project and deploy from github repo and add the variables -> railway will deploy and give the public url 


**Output Screenshot**

<img width="1229" height="569" alt="image" src="https://github.com/user-attachments/assets/43e2dd63-71cc-464f-8a5e-10c34ba44cf1" />

<img width="1420" height="784" alt="image" src="https://github.com/user-attachments/assets/b82a7a7d-00c3-4c35-9646-d73f1b0f8227" />






