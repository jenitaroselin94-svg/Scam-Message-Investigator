
import streamlit as st
import requests
import json

# Model Configuration
MODEL = "gemma3:1b"
OLLAMA_URL = "http://localhost:11434/api/chat"

# Page Configuration
st.set_page_config(
    page_title="Scam Message Investigator",
    page_icon="🔍",
    layout="centered"
)

# Application Title
st.title("🔍 Scam Message Investigator")

st.write(
    "Analyze suspicious SMS messages, emails, "
    "job offers and online messages using AI."
)

st.info(
    "Your message is analyzed using a locally running Gemma model."
)

# User Input - Only ONE text area
message = st.text_area(
    "Enter the suspicious message:",
    placeholder="Paste your SMS, email or online message here...",
    height=180,
    key="message_input"
)


# Investigation Function
def investigate_message(user_message):

    system_prompt = """
    You are a Scam Message Investigator.

    Analyze the given message and return ONLY valid JSON.

    Use this exact structure:

    {
        "concern_level": "Low Concern, Medium Concern, or High Concern",
        "message_type": "SMS, Email, Job Offer, or Other",
        "summary": "Short summary of the message",
        "warning_signs": [
            "Warning sign 1",
            "Warning sign 2"
        ],
        "recommended_actions": [
            "Safety action 1",
            "Safety action 2"
        ],
        "limitations": [
            "Limitation 1"
        ]
    }

    Rules:
    - Identify suspicious links and urgent threats.
    - Identify OTP, password and payment requests.
    - Identify requests for personal information.
    - Explain warning signs using message evidence.
    - Do not assume every message is a scam.
    - Use Low Concern if there are no obvious warning signs.
    - Never claim that a message is definitely safe.
    - Return JSON only.
    """

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "stream": False,
        "format": "json"
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=180
    )

    response.raise_for_status()

    result = response.json()

    ai_response = result["message"]["content"]

    report = json.loads(ai_response)

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
        "Low Concern",
        "Medium Concern",
        "High Concern"
    ]:
        raise ValueError("Invalid concern level")

    return report


# Investigate Button
if st.button("🔍 Investigate Message", type="primary"):

    if not message.strip():

        st.warning("Please enter a message to investigate.")

    else:

        try:

            with st.spinner("Gemma AI is analyzing your message..."):

                report = investigate_message(message)

            st.success("Investigation Completed!")

            st.subheader("Investigation Report")

            # Concern Level
            concern = report["concern_level"]

            if concern == "High Concern":

                st.error("🚨 " + concern)

            elif concern == "Medium Concern":

                st.warning("⚠️ " + concern)

            else:

                st.success("✅ " + concern)

            # Message Type
            st.write("**Message Type:**", report["message_type"])

            # Summary
            st.subheader("Summary")

            st.write(report["summary"])

            # Warning Signs
            st.subheader("Warning Signs")

            if report["warning_signs"]:

                for sign in report["warning_signs"]:

                    st.write("⚠️", sign)

            else:

                st.write("No obvious warning signs identified.")

            # Recommended Actions
            st.subheader("Recommended Safety Actions")

            for action in report["recommended_actions"]:

                st.write("✔️", action)

            # Limitations
            st.subheader("Limitations")

            for limitation in report["limitations"]:

                st.write("•", limitation)

            # JSON Report
            with st.expander("View JSON Report"):

                st.json(report)

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to Ollama. "
                "Please make sure Ollama is running."
            )

        except requests.exceptions.Timeout:

            st.error(
                "Request timed out. Please try again."
            )

        except json.JSONDecodeError:

            st.error(
                "Invalid JSON response from Gemma. "
                "Please try again."
            )

        except (KeyError, ValueError) as error:

            st.error("Invalid investigation report: " + str(error))

        except requests.exceptions.RequestException as error:

            st.error("Ollama API Error: " + str(error))

        except Exception as error:

            st.error("Unexpected Error: " + str(error))


# Footer
st.divider()

st.caption(
    "Scam Message Investigator | Powered by Python, "
    "Streamlit, Ollama and Gemma 3 1B"
)

st.caption(
    "AI-generated results are not definitive scam verdicts. "
    "Always verify messages through official channels. "
    "Never share real OTPs, passwords or PINs."
)
