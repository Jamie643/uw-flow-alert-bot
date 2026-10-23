from utils.logger import logger

class RiskEngine:
    @staticmethod
    def process_and_score(trades: list[dict]) -> list[dict]:
        actionable_trades = []

        for trade in trades:
            ticker = trade.get("ticker", "UNKNOWN")
            total_premium = float(trade.get("total_premium", 0))
            trade_type = trade.get("type", "call")
            vol_oi_ratio = float(trade.get("volume_oi_ratio", 0))

            if total_premium >= 100_000 and vol_oi_ratio >= 1.5:
                signal = {
                    "ticker": ticker,
                    "type": trade_type.upper(),
                    "premium": f"${total_premium:,.0f}",
                    "vol_oi": f"{vol_oi_ratio:.2f}x",
                    "strike": trade.get("strike"),
                    "expiry": trade.get("expiry"),
                    "conviction_score": "HIGH_WHALE_SWEEP" if vol_oi_ratio > 3.0 else "MEDIUM"
                }
                actionable_trades.append(signal)
                logger.info("high_conviction_flow_detected", ticker=ticker, premium=total_premium, vol_oi=vol_oi_ratio)

        return actionable_trades
