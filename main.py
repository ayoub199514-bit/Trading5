"""
main.py — نقطة انطلاق البوت

طريقة التشغيل:
    python3 main.py

باش يخدم فعلا (بيانات حقيقية)، خاصك تثبت ccxt:
    pip install ccxt pandas numpy scikit-learn
"""

import time
import sys

import config
from core.indicators import add_indicators
from core.risk_manager import RiskManager
from core.paper_broker import PaperBroker
from strategies.adaptive_ml_strategy import AdaptiveMLStrategy


def get_data_feed():
    """يرجع DataFeed حقيقي (ccxt) إذا PAPER_TRADING=False، وإلا يرجع mock feed."""
    if config.PAPER_TRADING:
        from core.mock_data_feed import MockDataFeed
        return MockDataFeed()
    else:
        from core.data_feed import DataFeed
        return DataFeed(
            exchange_name=config.EXCHANGE_NAME,
            api_key=config.API_KEY,
            api_secret=config.API_SECRET,
            testnet=config.USE_TESTNET,
        )


def run():
    print("=" * 60)
    print("🤖 Crypto AI Trading Bot — بوت تداول مفتوح المصدر")
    print(f"وضعية: {'Paper Trading (وهمي)' if config.PAPER_TRADING else 'تداول حقيقي'}")
    print("=" * 60)

    feed = get_data_feed()
    risk_manager = RiskManager(
        risk_per_trade=config.RISK_PER_TRADE,
        stop_loss_pct=config.STOP_LOSS_PCT,
        take_profit_pct=config.TAKE_PROFIT_PCT,
        max_open_positions=config.MAX_OPEN_POSITIONS,
    )
    broker = PaperBroker(starting_balance=config.PAPER_STARTING_BALANCE)

    # نموذج/استراتيجية واحدة لكل عملة
    strategies = {symbol: AdaptiveMLStrategy() for symbol in config.SYMBOLS}

    cycle = 0
    try:
        while True:
            cycle += 1
            print(f"\n--- الدورة {cycle} ---")

            for symbol in config.SYMBOLS:
                df = feed.fetch_ohlcv(symbol, timeframe=config.TIMEFRAME, limit=config.LOOKBACK_CANDLES)
                df = add_indicators(df)

                if len(df) < 50:
                    print(f"[{symbol}] بيانات ماكافيش باش نحلل، تخطينا.")
                    continue

                strategy = strategies[symbol]

                # يتعلم/يعيد التدريب كل RETRAIN_EVERY_N_CYCLES دورة
                if not strategy.is_trained or cycle % config.RETRAIN_EVERY_N_CYCLES == 0:
                    acc = strategy.train(df)
                    print(f"[{symbol}] 🧠 تدرب/تحسن من جديد — دقة التوقع: {acc:.1%}")

                current_price = df.iloc[-1]["close"]

                # نتفقد الصفقات المفتوحة (stop-loss/take-profit)
                closed = broker.check_and_close_positions(symbol, current_price)
                if closed:
                    print(f"[{symbol}] 🔒 صفقة سكرات: {closed['reason']} | PnL: {closed['pnl']}$")

                # نطلب إشارة جديدة إذا معندناش صفقة مفتوحة فهاد العملة
                if symbol not in broker.open_positions and risk_manager.can_open_new_position(broker.get_open_positions_count()):
                    signal = strategy.predict_signal(df.iloc[-1])
                    print(f"[{symbol}] السعر: {current_price:.2f} | إشارة: {signal['action']} (ثقة: {signal['confidence']:.0%})")

                    if signal["action"] in ("BUY", "SELL"):
                        size = risk_manager.calc_position_size(broker.balance, current_price)
                        sl = risk_manager.get_stop_loss(current_price, signal["action"])
                        tp = risk_manager.get_take_profit(current_price, signal["action"])
                        broker.open_position(symbol, signal["action"], size, current_price, sl, tp)
                        print(f"[{symbol}] ✅ صفقة جديدة: {signal['action']} حجم {size} @ {current_price:.2f}")

            summary = broker.get_summary()
            print(f"\n💰 الرصيد: {summary['balance']}$ | الربح/الخسارة: {summary['total_pnl']}$ "
                  f"({summary['total_pnl_pct']}%) | صفقات: {summary['total_trades']} | نسبة الربح: {summary['win_rate']}%")

            time.sleep(5)  # فالواقع، خليها تنتظر مدة تناسب الـ timeframe (مثلا 3600 لـ 1h)

    except KeyboardInterrupt:
        print("\n\n⏹️  توقف البوت.")
        print(broker.get_summary())
        sys.exit(0)


if __name__ == "__main__":
    run()
