import streamlit as st
import requests
from openai import OpenAI  # ✅ New OpenAI SDK import
from prompt import generate_system_prompt, generate_user_prompt
from intent import classify_intent  # OpenAI-based intent classifier

# 🎧 EDMTrain API Key and Base URL
EDMTRAIN_API_KEY = "6912aa7e-135d-4d78-afc5-3cf9b9dd0be9"
EDMTRAIN_BASE_URL = "https://edmtrain.com/api/events"

# Function to fetch upcoming EDM festivals from EDMTrain API
def get_upcoming_edmtrain_festivals():
    url = EDMTRAIN_BASE_URL 
    params = {"client": EDMTRAIN_API_KEY}

    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return f"⚠️ EDMTrain API error: {response.status_code}"

        data = response.json()
        events = data.get("data", [])

        if not events:
            return "🎵 No upcoming EDM festivals found at the moment!"

        festival_list = []
        for event in events[:5]:
            name = event.get("name", "Unknown Event")
            date = event.get("dates", {}).get("start", "Unknown Date")
            venue = event.get("venue", {}).get("name", "Unknown Venue")
            location = event.get("venue", {}).get("location", "Unknown Location")
            festival_list.append(f"🎧 **{name}** - 📅 {date} - 📍 {venue}, {location}")

        return "\n".join(festival_list)

    except Exception as e:
        return f"⚠️ Error fetching from EDMTrain: {e}"

# Sidebar
with st.sidebar:
    st.header("🎧 EDM Festival Chatbot Settings")
    openai_api_key = st.text_input("Enter OpenAI API Key", type="password")
    st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
    st.markdown("[Get an EDMTrain API Key](https://edmtrain.com/api)")

# Title & Welcome
st.title("🎶 EDM Festival Chatbot 🎤🔥")
st.caption("🧠 Powered by: OpenAI GPT-3.5 + EDMTrain")
st.markdown("🔗 Data Source: [edmtrain.com](https://edmtrain.com)")

st.markdown("""
Welcome to your **EDM Festival Chatbot**! Ask me about:
- 🏟 **Upcoming Festivals**
- 🎵 **Lineups & Set Times**
- 🎟 **Ticket Prices & Availability**
- ✈️ **Travel & Accommodation**
- 🎒 **Festival Tips**
- 🤝 **Meetups & Community Chats**
""")

# Chat History
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hey raver! 🎶 What festival details do you need?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# EDM relevance check
def is_edm_related(user_input):
    edm_keywords = [
        "edm", "festival", "rave", "ultra", "tomorrowland", "edc", "dreamstate",
        "hardstyle", "trance", "house music", "techno", "dj", "lineup", "set times",
        "tickets", "vip passes", "camping", "main stage", "afterparty"
    ]
    return any(keyword in user_input.lower() for keyword in edm_keywords)

# Chat input interface
if prompt := st.chat_input("Ask about EDM festivals... 🎧"):
    if not openai_api_key:
        st.warning("⚠️ Please enter your OpenAI API key to continue.")
        st.stop()

    edm_check = is_edm_related(prompt)
    if not edm_check:
        st.warning("⚠️ That doesn't seem EDM-related, but I’ll try answering it anyway...")

    # 🧠 Use OpenAI to classify intent
    intent = classify_intent(prompt, openai_api_key)
    st.write(f"📌 Intent classified as: {intent}")  # Optional debug

    # Step 1: Fetch real event data if needed
    scraped_data = ""
    if intent == "Upcoming Festivals":
        scraped_data = get_upcoming_edmtrain_festivals()
        st.chat_message("assistant").write(scraped_data)

    # Step 2: Build full prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(f"🗣 {prompt} \n\n(Category: {intent})")

    full_prompt = prompt
    if scraped_data:
        full_prompt += f"\n\nHere are some real upcoming EDM events:\n{scraped_data}"

    # Step 3: Generate GPT response using OpenAI SDK v1.x
    try:
        client = OpenAI(api_key=openai_api_key)  # ✅ New SDK pattern
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": generate_system_prompt()},
                {"role": "user", "content": generate_user_prompt(intent, full_prompt)}
            ]
        )
        msg = response.choices[0].message.content
    except Exception as e:
        msg = f"⚠️ Error: {e}"

    # Step 4: Save & show message
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

