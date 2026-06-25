# 🚀 AI Career & Resume Toolkit  
**Powered by Grok-4 (xAI) + Streamlit**

A powerful, all-in-one AI-powered career assistant that helps you write better cover letters, score & optimize your resume, get quick feedback, and talk to a personalized career coach — **all in one beautiful Streamlit app**.
 
<!-- ↑ Replace with real screenshot(s) later -->

<p align="center">
  <a href="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">
    <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  </a>
  <a href="https://img.shields.io/badge/xAI-Grok-4-black?style=for-the-badge">
    <img src="https://img.shields.io/badge/xAI-Grok--4-black?style=for-the-badge" alt="Grok-4">
  </a>
  <a href="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white">
    <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  </a>
  <a href="https://img.shields.io/badge/License-MIT-green?style=for-the-badge">
    <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License">
  </a>
</p>

## ✨ Features

| Tool                            | What it does                                                                 | Best for                              |
|---------------------------------|------------------------------------------------------------------------------|----------------------------------------|
| ✉️ Cover Letter Generator       | Creates tailored, professional cover letters (300–450 words)                 | Job applications                      |
| 📊 Resume Matcher & Scorer      | Deep ATS + keyword + skill-gap + industry-specific analysis                  | Serious job hunters, career switchers |
| 🔍 Quick Resume Checker         | Fast score + strengths/weaknesses + next roles in seconds                    | Quick reality check                   |
| 🗣️ Career Coach Chatbot        | Conversational AI mentor that **knows your resume** — interview prep, strategy, gaps | Long-term career planning             |

## 🖥️ Live Demo (optional — coming soon)

<!-- 
[![Open in Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)
-->

(Deploy it yourself in < 5 minutes — see instructions below)

## 🚀 Quick Start (Local)

```bash
# 1. Clone the repo
git clone 
cd ai-career-resume-toolkit

# 2. Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate    # Linux / macOS
# or
.venv\Scripts\activate       # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Important) Add your xAI API key
# Option A: Create .streamlit/secrets.toml
echo 'XAI_API_KEY = "xai-YourRealKeyHere"' > .streamlit/secrets.toml

# Option B: Set environment variable
export XAI_API_KEY="xai-YourRealKeyHere"

# 5. Run the app
streamlit run app_hub.py