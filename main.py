import streamlit as st
import requests
from openai import OpenAI
from prompt import generate_system_prompt, generate_user_prompt  # 👈 imported prompt logic

# 🎧 Songkick API Key (Hardcoded) ⚠️
SONGKICK_API_KEY = "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"
SONGKICK_BASE_URL = "https://api.songkick.com/api/3.0/"

# Sidebar for API Key and Settings
with st.sidebar:
    st.header("🎧 EDM Festival Chatbot Settings")
    openai_api_key = st.text_input("Enter OpenAI API Key", type="password")
    st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
    st.markdown("[Get a Songkick API Key](https://www.songkick.com/developer/)")

# Title and Welcome Message
st.title("🎶 EDM Festival Chatbot 🎤🔥")

st.markdown("""
Welcome to your **EDM Festival Chatbot**! Ask me about:
- 🏟 **Upcoming Festivals**
- 🎵 **Lineups & Set Times**
- 🎟 **Ticket Prices & Availability**
- ✈️ **Travel & Accommodation**
- 🎒 **Festival Tips**
- 🤝 **Meetups & Community Chats**
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hey raver! 🎶 What festival details do you need?"}]

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Function to check if the query is EDM-related
def is_edm_related(user_input):
    edm_keywords = [
        "edm", "festival", "rave", "ultra", "tomorrowland", "edc", "dreamstate",
        "hardstyle", "trance", "house music", "techno", "dj", "lineup", "set times",
        "tickets", "vip passes", "camping", "main stage", "afterparty"
    ]
    return any(keyword in user_input.lower() for keyword in edm_keywords)

# Function to fetch upcoming EDM festivals from Songkick API
def get_upcoming_edm_festivals():
    url = f"{SONGKICK_BASE_URL}metro_areas/24426/calendar.json?apikey={SONGKICK_API_KEY}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return "⚠️ Error fetching festival data. Please try again later."
    
    data = response.json()
    events = data.get("resultsPage", {}).get("results", {}).get("event", [])
    
    if not events:
        return "🎵 No upcoming EDM festivals found at the moment!"
    
    festival_list = []
    for event in events[:5]:  # Show only the top 5 festivals
        event_name = event.get("displayName", "Unknown Festival")
        event_date = event.get("start", {}).get("date", "Unknown Date")
        location = event.get("venue", {}).get("displayName", "Unknown Location")
        
        festival_list.append(f"🎧 **{event_name}** - 📅 {event_date} - 📍 {location}")

    return "\n\n".join(festival_list)

# Function to categorize user intent
def classify_intent(user_input):
    keywords = {
        "upcoming": "Upcoming Festivals",
        "festival": "Upcoming Festivals",
        "lineup": "Lineups & Set Times",
        "set time": "Lineups & Set Times",
        "tickets": "Ticket Prices & Availability",
        "price": "Ticket Prices & Availability",
        "travel": "Travel & Accommodation",
        "hotel": "Travel & Accommodation",
        "tips": "Festival Tips",
        "packing": "Festival Tips",
        "meet": "Meetups & Community Chats",
        "friends": "Meetups & Community Chats"
    }
    for keyword, category in keywords.items():
        if keyword in user_input.lower():
            return category
    return "General Inquiry"

# User Input Processing
if prompt := st.chat_input("Ask about EDM festivals... 🎧"):
    if not openai_api_key:
        st.warning("⚠️ Please enter your OpenAI API key to continue.")
        st.stop()

    # Step 1: Scope Check (Reject Non-EDM Queries)
    if not is_edm_related(prompt):
        response_message = "🚨 Sorry! I can only help with EDM festivals, tickets, lineups, and travel. Try asking about an event like 'Tomorrowland' or 'Ultra Music Festival'! 🎶"
        st.session_state.messages.append({"role": "assistant", "content": response_message})
        st.chat_message("assistant").write(response_message)
        st.stop()

    # Step 2: Categorize intent
    intent = classify_intent(prompt)

    # Step 3: Fetch festival data if query is about upcoming festivals
    if intent == "Upcoming Festivals":
        festival_data = get_upcoming_edm_festivals()
        st.session_state.messages.append({"role": "assistant", "content": festival_data})
        st.chat_message("assistant").write(festival_data)
        st.stop()

    # Step 4: Send request to OpenAI for other queries
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(f"🗣 {prompt} \n\n(Category: {intent})")

    try:
        client = OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": generate_system_prompt()},
                {"role": "user", "content": generate_user_prompt(intent, prompt)}
            ]
        )
        msg = response.choices[0].message.content
    except Exception as e:
        msg = f"⚠️ Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
