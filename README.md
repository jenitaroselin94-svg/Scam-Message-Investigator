
# Scam Message Investigator

## Project Description

Scam Message Investigator is an AI-powered application that analyzes suspicious SMS messages, emails, job offers, and online messages using a locally running Gemma 3 1B language model through Ollama.

The application identifies possible scam indicators, assesses the concern level, explains warning signs, and provides recommended safety actions.

## Features

- Analyzes suspicious SMS messages and emails
- Identifies possible scam indicators
- Classifies messages into Low, Medium, and High Concern
- Explains warning signs with evidence
- Provides recommended safety actions
- Generates structured JSON investigation reports
- Displays investigation results using Streamlit
- Runs AI locally using Ollama

## Technologies Used

- Python
- Streamlit
- Requests
- Ollama
- Gemma 3 1B

## Project Structure

    Scam-Message-Investigator/
    │
    ├── app.py
    ├── requirements.txt
    └── README.md

## Installation and Setup

### 1. Clone the Repository

    git clone YOUR_GITHUB_REPOSITORY_URL

### 2. Open the Project Folder

    cd Scam-Message-Investigator

### 3. Install Required Packages

    py -m pip install -r requirements.txt

### 4. Install Ollama

Download Ollama from:

https://ollama.com/download

### 5. Download Gemma Model

    ollama pull gemma3:1b

### 6. Verify the Model

    ollama list

### 7. Run the Application

    py -m streamlit run app.py

The application will open in your browser at:

    http://localhost:8501

## How It Works

1. The user enters a suspicious message into the application.
2. Streamlit collects the message.
3. Python sends the message to the Ollama API.
4. Gemma 3 1B analyzes the message.
5. The model generates a structured JSON report.
6. Streamlit displays the concern level, warning signs, summary, and recommended safety actions.

## Concern Levels

- Low Concern – No obvious warning signs identified.
- Medium Concern – Some suspicious indicators are identified.
- High Concern – Multiple serious scam indicators are identified.

## Sample Test Message

    URGENT! Your bank account will be blocked
    in 2 hours. Click this link to update your KYC
    immediately and enter your OTP.

Expected Concern Level: High Concern

## Requirements

Python 3.10 or newer

Ollama installed and running

Gemma 3 1B model downloaded

Required Python packages installed using requirements.txt.

## Limitations

- AI-generated results are not definitive scam verdicts.
- The application analyzes message text only.
- It does not independently verify URLs or sender identities.
- A Low Concern result does not guarantee that a message is safe.
- Users should verify suspicious requests through official channels.

## Safety Note

Never share real OTPs, passwords, PINs, or confidential banking information. Use sample messages for testing.
