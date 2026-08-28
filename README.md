# 🤖 Crypto AI Trading Bot — بوت تداول عملات رقمية مفتوح المصدر

بوت تداول للعملات الرقمية، مفتوح المصدر بالكامل (رخصة MIT)، فيه:

- 🧠 **استراتيجية تتعلم**: نموذج Machine Learning (Random Forest) يحلل مؤشرات تقنية (RSI, MACD, Bollinger Bands...) ويتوقع اتجاه السعر، ويعيد تدريب نفسه بشكل دوري.
- 📝 **Paper Trading**: تداول وهمي بلا فلوس حقيقية وبلا حتى API — تقدر تجرب البوت مباشرة.
- 🔌 **يدعم منصات حقيقية**: عبر مكتبة `ccxt` (Binance, KuCoin, Bybit وأكثر من 100 منصة).
- 🛡️ **إدارة مخاطر**: حجم الصفقة، وقف الخسارة (Stop-Loss)، جني الأرباح (Take-Profit)، أقصى عدد صفقات مفتوحة.

## ⚠️ تحذير مهم

هاد البوت **مثال تعليمي/نقطة انطلاق**، ماشي نصيحة مالية. التداول بالعملات الرقمية فيه مخاطر عالية وممكن تخسر فلوسك. **جرب دائما فـ Paper Trading بزاف قبل ما تستعمل فلوس حقيقية**، وابدا بمبالغ صغيرة جدا.

## 📁 هيكلة المشروع

```
crypto-ai-bot/
├── config.py                       # الإعدادات (عدّل هنا)
├── main.py                         # نقطة انطلاق البوت
├── core/
│   ├── data_feed.py                # اتصال حقيقي بالمنصة (ccxt)
│   ├── mock_data_feed.py           # بيانات وهمية (للتجربة بلا API)
│   ├── indicators.py               # المؤشرات التقنية
│   ├── risk_manager.py             # إدارة المخاطر
│   └── paper_broker.py             # محاكي التداول الوهمي
├── strategies/
│   └── adaptive_ml_strategy.py     # الاستراتيجية يلي تتعلم
├── logs/                           # سجلات الصفقات
└── requirements.txt
```

## 🚀 التشغيل

### 1. ثبت المتطلبات
```bash
pip install -r requirements.txt
```

### 2. شغل البوت (Paper Trading — بلا API)
البوت مضبوط افتراضيا على `PAPER_TRADING = True` فـ `config.py`، يعني تقدر تشغله مباشرة:
```bash
python3 main.py
```
غادي يستعمل بيانات وهمية (mock) ويحاكي التداول بـ 1000$ وهميين.

### 3. الانتقال للتداول الحقيقي
فـ `config.py`:
```python
PAPER_TRADING = False
USE_TESTNET = True          # ابدا بالـ testnet ديال المنصة (بلا فلوس حقيقية)
API_KEY = "المفتاح_ديالك"
API_SECRET = "السر_ديالك"
```
باش تجيب API Key من Binance مثلا: `Binance → Account → API Management`. استعمل صلاحيات **Trade only** (بلا Withdraw) لأمانك.

## 🧠 كيفاش يتعلم البوت؟

كل `RETRAIN_EVERY_N_CYCLES` دورة، البوت:
1. يجيب آخر البيانات التاريخية
2. يحسب مؤشرات تقنية (features)
3. يدرب نموذج Random Forest يتوقع: واش السعر غادي يطلع فالشمعة الجاية؟
4. يستعمل التوقع (مع نسبة الثقة) باش يقرر BUY / SELL / HOLD

تقدر تبدل النموذج بأي حاجة أعقد (XGBoost, LSTM, Reinforcement Learning...) فـ `strategies/adaptive_ml_strategy.py`.

## 🛠️ تطوير المشروع

أفكار للتحسين:
- [ ] Backtesting engine كامل على بيانات تاريخية طويلة
- [ ] Dashboard (Streamlit/Flask) لمتابعة الأداء
- [ ] دعم إشعارات Telegram
- [ ] نماذج ML أعقد (LSTM, XGBoost)
- [ ] تحسين المعايير آليا (hyperparameter tuning)

## 📄 الرخصة

MIT License — استعملو، عدّلو، وزعو بحرية.
