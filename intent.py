import openai

# List of intent categories
INTENT_CATEGORIES = [
    "Upcoming Festivals",
    "Lineups & Set Times",
    "Ticket Prices & Availability",
    "Travel & Accommodation",
    "Festival Tips",
    "Meetups & Community Chats"
]

def classify_intent(user_input, openai_api_key):
    openai.api_key = openai_api_key

    categories = ", ".join(INTENT_CATEGORIES)

    system_msg = (
        "You are an assistant that classifies user messages about EDM festivals into one of the following categories: "
        f"{categories}. If none apply, say 'General Inquiry'. Respond only with the category name."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_input}
            ]
        )

        intent = response.choices[0].message.content.strip()
        print(f"[DEBUG] GPT classified intent as: {intent}")
        return intent if intent in INTENT_CATEGORIES else "General Inquiry"

    except Exception as e:
        print(f"[ERROR] Intent classification failed: {e}")
        return "General Inquiry"
