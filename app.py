
import streamlit as st
import requests
import json

MODEL = "gemma3:1b"
OLLAMA_URL = "http://localhost:11434/api/chat"

st.set_page_config(
    page_title="Scam Message Investigator",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 Scam Message Investigator")

st.write(
    "Analyze suspicious SMS messages, emails, "
    "job offers and online messages using AI."
)

# Detect cloud API key
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    GROQ_API_KEY = None

if GROQ_API_KEY:
    st.info("Analysis powered by a hosted AI model.")
else:
    st.info("Analysis powered by your locally running Gemma model.")

message = st.text_area(
    "Enter the suspicious message:",
    placeholder="Paste your SMS, email or online message here...",
    height=180,
    key="message_input"
)

SYSTEM_PROMPT = """
You are a Scam Message Investigator.

Analyze the message and return ONLY valid JSON.

Use this exact structure:

{
  "concern_level": "Low Concern, Medium Concern, or High Concern",
  "message_type": "SMS, Email, Job Offer, or Other",
  "summary": "Short summary",
  "warning_signs": ["Warning sign 1"],
  "recommended_actions": ["Safety action 1"],
  "limitations": ["Limitation 1"]
}

Rules:
- Identify urgent threats and suspicious links.
- Identify OTP, password and payment requests.
- Identify requests for personal information.
- Explain warning signs using message evidence.
- Do not assume every message is a scam.
- Never claim a message is definitely safe.
- Return JSON only.
"""

def investigate_message(user_message):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

    if GROQ_API_KEY:

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-oss-20b",
                "messages": messages,
                "response_format": {"type": "json_object"}
            },
            timeout=120
        )

        response.raise_for_status()
        ai_text = response.json()["choices"][0]["message"]["content"]

    else:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": messages,
                "stream": False,
                "format": "json"
            },
            timeout=180
        )

        response.raise_for_status()
        ai_text = response.json()["message"]["content"]

    report = json.loads(ai_text)

    required_fields = [
        "concern_level",
        "message_type",
        "summary",
        "warning_signs",
        "recommended_actions",
        "limitations"
    ]

    for field in required_fields:
        if field not in report:
            raise ValueError("Missing field: " + field)

    if report["concern_level"] not in [
        "Low Concern", "Medium Concern", "High Concern"
    ]:
        raise ValueError("Invalid concern level")

    return report


if st.button("🔍 Investigate Message", type="primary"):

    if not message.strip():
        st.warning("Please enter a message to investigate.")

    else:
        try:
            with st.spinner("AI is analyzing your message..."):
                report = investigate_message(message)

            st.success("Investigation Completed!")

            st.subheader("Investigation Report")

            concern = report["concern_level"]

            if concern == "High Concern":
                st.error("🚨 " + concern)
            elif concern == "Medium Concern":
                st.warning("⚠️ " + concern)
            else:
                st.success("✅ " + concern)

            st.write("**Message Type:**", report["message_type"])

            st.subheader("Summary")
            st.write(report["summary"])

            st.subheader("Warning Signs")
            for sign in report["warning_signs"]:
                st.write("⚠️", sign)

            st.subheader("Recommended Safety Actions")
            for action in report["recommended_actions"]:
                st.write("✔️", action)

            st.subheader("Limitations")
            for limitation in report["limitations"]:
                st.write("•", limitation)

            with st.expander("View JSON Report"):
                st.json(report)

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to the AI service. Check your connection.")

        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")

        except requests.exceptions.HTTPError as error:
            st.error("AI API error: " + str(error))

        except (json.JSONDecodeError, KeyError, ValueError) as error:
            st.error("Invalid AI response: " + str(error))

        except Exception as error:
            st.error("Unexpected error: " + str(error))


st.divider()

st.caption(
    "Scam Message Investigator | Python, Streamlit, "
    "Ollama, Gemma 3 1B and hosted AI API"
)

st.caption(
    "AI results are not definitive scam verdicts. "
    "Verify messages through official channels. "
    "Never share real OTPs, passwords or PINs."
)
