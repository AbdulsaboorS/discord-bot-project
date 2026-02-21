# Discord Feedback Bot

A Discord bot that analyzes user feedback with **sentiment analysis** (Azure Text Analytics) and **key phrase extraction** (spaCy). Collect feedback in your server and get instant sentiment plus a running summary of key topics.

## Features

- **`!feedback <text>`** — Submits feedback for analysis:
  - **Sentiment** (positive / negative / neutral) via Azure Text Analytics
  - **Key phrases** extracted with spaCy (noun chunks)
  - Phrases are stored for the session and included in `!summary`
- **`!summary`** — Replies with all unique key phrases collected so far

## Tech Stack

| Component        | Technology              |
|-----------------|-------------------------|
| Bot framework   | [discord.py](https://github.com/Rapptz/discord.py) |
| Sentiment API   | [Azure Text Analytics](https://learn.microsoft.com/en-us/azure/cognitive-services/language-service/sentiment-opinion-mining/overview) (v3) |
| Key phrase NLP  | [spaCy](https://spacy.io/) `en_core_web_sm` |

## Setup

### 1. Clone and create a virtual environment

```bash
git clone https://github.com/YOUR_USERNAME/discord-feedback-bot.git
cd discord-feedback-bot
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Configure environment variables

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:

| Variable | Description |
|----------|-------------|
| `DISCORD_BOT_TOKEN` | Bot token from [Discord Developer Portal](https://discord.com/developers/applications) → Your App → Bot |
| `AZURE_TEXT_ANALYTICS_KEY` | Key from Azure Portal → your Language resource → Keys and Endpoint |
| `AZURE_TEXT_ANALYTICS_ENDPOINT` | Endpoint URL of the same Language resource (optional if using default) |

**Discord:** Enable **Message Content Intent** for your bot in the Developer Portal (Bot → Privileged Gateway Intents).

**Azure:** Create a **Language** (Cognitive Services) resource in [Azure Portal](https://portal.azure.com) and use its key and endpoint.

### 4. Run the bot

```bash
python discordbotproject/discord_bot.py
```

Or from the project root with the module path:

```bash
python -m discordbotproject.discord_bot
```

## Usage

In any channel where the bot can read and send messages:

- `!feedback The new dashboard is great but loading is slow.`  
  → Bot replies with sentiment and key phrases, and adds phrases to the summary.
- `!summary`  
  → Bot lists all unique key phrases collected in this run.

## Project Structure

```
discord_bot_project/
├── discordbotproject/
│   └── discord_bot.py    # Bot entry point and logic
├── .env.example          # Template for environment variables
├── requirements.txt      # Python dependencies
├── README.md
└── LICENSE
```

## License

MIT — see [LICENSE](LICENSE).
