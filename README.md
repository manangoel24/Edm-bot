# EDM Festival Chatbot 🎧🔥

A Streamlit application that helps users explore upcoming EDM festivals, check lineups, find tickets, get travel tips, and much more — powered by OpenAI GPT and the EDMTrain API.

---

## 🌐 Overview

This project combines the power of large language models with real-time event data to deliver an interactive chatbot experience tailored to EDM fans. Users can ask about upcoming festivals, ticket availability, packing tips, or even how to travel to events — and the bot responds in a fun, raver-friendly tone using real-time data.

---

## ⚙️ Technical Implementation

- **Frontend**: Streamlit web interface
- **AI Model**: OpenAI GPT-3.5 for natural language understanding and generation
- **Intent Classification**: GPT-based intent detection using few-shot prompts
- **Data Source**: EDMTrain API for real-time festival data
- **Prompting Technique**: Few-shot prompting with curated example questions and answers

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.8+
- OpenAI API Key
- EDMTrain API Key
- Internet connection

### 🔧 Installation

# Clone the repository
git clone https://github.com/yourusername/edm-festival-chatbot.git
cd edm-festival-chatbot

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run main.py
