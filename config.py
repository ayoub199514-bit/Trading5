"""
إعدادات البوت — عدّل هذا الملف حسب حاجتك.
"""

# ==== إعدادات المنصة (Exchange) ====
EXCHANGE_NAME = "binance"          # اسم المنصة (binance, kucoin, bybit...) — ccxt يدعم أكثر من 100 منصة
API_KEY = ""                       # حط API Key ديالك هنا (خليه فارغ للـ Paper Trading)
API_SECRET = ""                    # حط API Secret ديالك هنا
USE_TESTNET = True                 # True = تستعمل شبكة تجريبية (بلا فلوس حقيقية)

# ==== وضعية التشغيل ====
PAPER_TRADING = True               # True = تداول وهمي (بلا API حتى)، False = تداول حقيقي
PAPER_STARTING_BALANCE = 1000.0    # رأس المال الوهمي بالدولار (لـ Paper Trading)

# ==== أزواج التداول ====
SYMBOLS = ["BTC/USDT", "ETH/USDT"] # الأزواج يلي البوت يتداول فيها
TIMEFRAME = "1h"                   # الإطار الزمني للشموع: 1m, 5m, 15m, 1h, 4h, 1d

# ==== إدارة المخاطر ====
RISK_PER_TRADE = 0.02              # نسبة رأس المال المخاطر بها في كل صفقة (2%)
STOP_LOSS_PCT = 0.03               # وقف الخسارة (3%)
TAKE_PROFIT_PCT = 0.06             # جني الأرباح (6%)
MAX_OPEN_POSITIONS = 3             # أقصى عدد صفقات مفتوحة فنفس الوقت

# ==== إعدادات التعلم/التحسين ====
LOOKBACK_CANDLES = 500             # عدد الشموع التاريخية المستعملة للتحليل
RETRAIN_EVERY_N_CYCLES = 24        # البوت يعيد تدريب/تحسين استراتيجيته كل كم دورة
