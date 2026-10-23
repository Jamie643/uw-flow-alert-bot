import httpx
import asyncio
from config import settings
from utils.logger import logger

class UnusualWhalesClient:
    def __init__(self):
        self.base_url = "https://api.unusualwhales.com/api"
        self.headers = {"Authorization": f"Bearer {settings.UW_API_TOKEN}"}

    async def fetch_flow_alerts(self) -> list[dict]:
        url = f"{self.base_url}/option-trades/flow-alerts"
        params = {
            "min_premium": settings.MIN_PREMIUM_THRESHOLD,
            "is_otm": True,
            "limit": 50
        }

        for attempt in range(1, settings.MAX_RETRIES + 1):
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.get(url, headers=self.headers, params=params)

                    if response.status_code == 200:
                        data = response.json().get("data", [])
                        logger.info("uw_api_fetch_success", records_retrieved=len(data))
                        return data
                    elif response.status_code == 429:
                        logger.warning("uw_api_rate_limit", attempt=attempt, delay=2**attempt)
                        await asyncio.sleep(2**attempt)
                    else:
                        logger.error("uw_api_error", status_code=response.status_code, text=response.text)

            except Exception as e:
                logger.error("uw_api_exception", attempt=attempt, error=str(e))
                await asyncio.sleep(2**attempt)

        logger.critical("uw_api_fallback_triggered", msg="All fetch attempts failed.")
        return []
