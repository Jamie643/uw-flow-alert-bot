import asyncio
from services.uw_client import UnusualWhalesClient
from services.risk_engine import RiskEngine
from utils.logger import logger
from config import settings

async def main():
    logger.info("service_started", poll_interval=settings.POLL_INTERVAL_SECONDS)
    client = UnusualWhalesClient()
    risk_engine = RiskEngine()
    seen_trade_ids = set()

    while True:
        raw_trades = await client.fetch_flow_alerts()

        new_trades = [t for t in raw_trades if t.get("id") not in seen_trade_ids]
        for t in new_trades:
            if t.get("id"):
                seen_trade_ids.add(t.get("id"))

        if new_trades:
            signals = risk_engine.process_and_score(new_trades)
            for sig in signals:
                print(f"🚨 [WHALE ALERT] {sig['ticker']} | {sig['type']} {sig['strike']} Exp:{sig['expiry']} | Premium: {sig['premium']} | Vol/OI: {sig['vol_oi']}")

        await asyncio.sleep(settings.POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("service_stopped_by_user")
