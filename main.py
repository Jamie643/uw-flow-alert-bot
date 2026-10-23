import asyncio
from services.uw_client import UnusualWhalesClient
from services.risk_engine import RiskEngine
from services.notifier import Notifier # <-- Import the new tool
from utils.logger import logger
from config import settings

async def main():
    logger.info("service_started", poll_interval=settings.POLL_INTERVAL_SECONDS)
    client = UnusualWhalesClient()
    risk_engine = RiskEngine()
    seen_trade_ids = set()

    for i in range(3): # Running 3 times for the demo
        print(f"\n--- Polling attempt {i+1} ---")
        raw_trades = await client.fetch_flow_alerts()

        new_trades = [t for t in raw_trades if t.get("id") not in seen_trade_ids]
        for t in new_trades:
            if t.get("id"):
                seen_trade_ids.add(t.get("id"))

        if new_trades:
            signals = risk_engine.process_and_score(new_trades)
            for sig in signals:
                print(f"🚨 [WHALE ALERT] {sig['ticker']} | {sig['type']} {sig['strike']} Exp:{sig['expiry']} | Premium: {sig['premium']} | Vol/OI: {sig['vol_oi']}")
                # Send to Discord!
                await Notifier.send_discord_alert(sig)
        else:
            print("No new trades found in this batch.")
            
        await asyncio.sleep(settings.POLL_INTERVAL_SECONDS)

    logger.info("demo_complete", msg="Stopping after 3 polls.")

if __name__ == "__main__":
    await main()
