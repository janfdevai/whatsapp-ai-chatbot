# Simple WhatsApp AI Chatbot

A simple AI-powered WhatsApp chatbot built with FastAPI and LangChain. This project demonstrates how to integrate a Large Language Model (LLM) with the WhatsApp Business API using a webhook.

## Features

-   **WhatsApp Webhook Integration**: Handles verification challenges and processes incoming messages.
-   **AI Agent**: Uses LangChain to create an agent (currently a Weather Agent) that can respond to user queries.
-   **Weather Tool**: A simple tool that fetches real-time weather data using the OpenWeatherMap API.
-   **FastAPI**: High-performance web framework for the backend.

## Prerequisites

-   Python 3.12+
-   [uv](https://docs.astral.sh/uv/) (Fast Python package installer and resolver)
-   A Meta (Facebook) Developer Account and a configured WhatsApp App.
-   `ngrok` (or similar) to expose your local server to the internet.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd simple-whatsapp-ai-chatbot
    ```

2.  **Install dependencies:**

    This project uses `uv` for dependency management.

    ```bash
    uv sync
    ```

3.  **Environment Configuration:**

    Create a `.env` file in the root directory (you can copy `.env.example` if it exists, or use the following template):

    ```env
    # Meta / WhatsApp Configuration
    VERIFY_TOKEN=your_verify_token
    WHATSAPP_ACCESS_TOKEN=your_access_token
    PHONE_NUMBER_ID=your_phone_number_id
    GRAPH_API_VERSION=v22.0
    OPEN_WEATHER_API_KEY=your_open_weather_api_key

    # OpenAI API Key (if using OpenAI models)
    OPENAI_API_KEY=your_openai_api_key
    ```

    *   **VERIFY_TOKEN**: A random string you define (used for webhook verification).
    *   **WHATSAPP_ACCESS_TOKEN**: Your temporary or permanent access token from the Meta Developer Dashboard.
    *   **PHONE_NUMBER_ID**: The Phone Number ID from the WhatsApp API Setup page.
    *   **GRAPH_API_VERSION**: The version of the Graph API you are using (e.g., v21.0).
    *   **OPEN_WEATHER_API_KEY**: Your API key from [OpenWeatherMap](https://openweathermap.org/api) to fetch weather data.
    *   **OPENAI_API_KEY**: Your API key from [OpenAI](https://platform.openai.com/) (required for the AI agent).

## Running the Application

1.  **Start the server:**

    ```bash
    uv run fastapi dev app/main.py
    ```

    The server will start at `http://127.0.0.1:8000`.

2.  **Expose your server:**

    Use `ngrok` to tunnel your local server to the public internet.

    *   [ngrok Setup Guide](https://dashboard.ngrok.com/get-started/setup)

    ```bash
    ngrok http 8000
    ```

3.  **Configure Webhook:**

    Follow the official guide to set up your webhook in the Meta Developer Portal.

    *   [Meta Webhook Configuration Guide](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started#configure-webhooks)
    *   [Meta Webhook Configuration Guide (Video)](https://www.youtube.com/watch?v=8hKEbOHWyQk)

    Use the HTTPS URL provided by ngrok (e.g., `https://<your-id>.ngrok-free.app/webhook`) and the `VERIFY_TOKEN` from your `.env` file.

## Usage

Send a message to the test WhatsApp number associated with your app. The bot should reply!

Currently, it tries to answer using a Weather Agent. For example:
"What is the weather in London?"