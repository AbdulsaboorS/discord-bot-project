"""
Discord Feedback Bot — sentiment analysis and key phrase extraction for user feedback.

Uses Azure Text Analytics for sentiment and spaCy for key phrase extraction.
"""

import json
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import discord
import requests
import spacy

# Load the spaCy English model (run: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

# Configuration from environment
DISCORD_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
AZURE_API_KEY = os.environ["AZURE_TEXT_ANALYTICS_KEY"]
AZURE_ENDPOINT = os.environ.get(
    "AZURE_TEXT_ANALYTICS_ENDPOINT",
    "https://discordfeedbackanalysis.cognitiveservices.azure.com/"
).rstrip("/")

# Bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.presences = False
intents.members = False

client = discord.Client(intents=intents)
collected_key_phrases: list[str] = []


def analyze_sentiment(text: str) -> dict:
    """Analyze sentiment of text using Azure Text Analytics API."""
    url = f"{AZURE_ENDPOINT}/text/analytics/v3.0/sentiment"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "documents": [{"language": "en", "id": "1", "text": text}]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
    response.raise_for_status()
    return response.json()


def extract_key_phrases(text: str) -> list[str]:
    """Extract key phrases (noun chunks) using spaCy."""
    doc = nlp(text)
    return [chunk.text.strip() for chunk in doc.noun_chunks if len(chunk.text.strip()) > 1]


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    content = message.content.strip()

    if content.startswith("!feedback"):
        feedback = content[len("!feedback"):].strip()
        if not feedback:
            await message.channel.send("Usage: `!feedback <your feedback text>`")
            return

        try:
            sentiment_result = analyze_sentiment(feedback)
            sentiment = sentiment_result["documents"][0]["sentiment"]
            await message.channel.send(f"**Sentiment:** {sentiment}")

            key_phrases = extract_key_phrases(feedback)
            if key_phrases:
                await message.channel.send(
                    f"**Key phrases:** {', '.join(key_phrases)}"
                )
                collected_key_phrases.extend(key_phrases)
            else:
                await message.channel.send("No key phrases extracted.")
        except requests.RequestException as e:
            await message.channel.send(f"Sentiment API error: {e}")
        except (KeyError, IndexError) as e:
            await message.channel.send(f"Could not parse sentiment response: {e}")

    elif content == "!summary":
        if collected_key_phrases:
            unique = list(dict.fromkeys(collected_key_phrases))  # preserve order, unique
            await message.channel.send(
                f"**Summary of key phrases:** {', '.join(unique)}"
            )
        else:
            await message.channel.send("No key phrases collected yet. Use `!feedback <text>` first.")


def main():
    if not DISCORD_TOKEN:
        raise SystemExit("Set DISCORD_BOT_TOKEN in your environment or .env file.")
    if not AZURE_API_KEY:
        raise SystemExit("Set AZURE_TEXT_ANALYTICS_KEY in your environment or .env file.")
    client.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
