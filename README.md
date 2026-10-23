# 🐋 Unusual Whales Flow Alert Bot

A zero-UI, asynchronous Python engine that monitors live options flow from the Unusual Whales API, filters for high-conviction "whale" sweeps (premium > $100k, Vol/OI > 1.5), and dispatches real-time telemetry.

## 🚀 Live Demo (Google Colab)
Because this bot uses an infinite asynchronous polling loop, we have packaged it as a 1-click Google Colab notebook for easy, dependency-free execution and judging.

**[Click here to open the Live Demo Notebook in Colab](PASTE_YOUR_COLAB_LINK_HERE)**

*(Note: You will need to paste your own Unusual Whales API key into the `os.environ` cell before running).*

## ✨ Features
* **Resilient Ingestor:** Async HTTP client (`httpx`) with exponential backoff for HTTP 429 rate limits.
* **Anomaly Risk Engine:** Filters out noise; only flags options with high premium and extreme Vol/OI ratios.
* **Deduplication:** In-memory tracking prevents alert fatigue on the same trade ID.
* **Structured Telemetry:** JSON formatted logs using `structlog` for CloudWatch/Datadog readiness.

## 🏗️ Architecture
1. **Ingestor:** Polls `/api/option-trades/flow-alerts` every 15 seconds.
2. **Risk Engine:** Calculates conviction scores (MEDIUM vs HIGH_WHALE_SWEEP).
3. **Dispatcher:** Outputs formatted CLI alerts.

## 🛠️ Local Installation (Optional)
1. `pip install -r requirements.txt`
2. Rename `.env.example` to `.env` and add your `UW_API_TOKEN`
3. `python main.py`
