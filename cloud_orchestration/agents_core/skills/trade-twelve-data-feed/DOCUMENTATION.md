# ═══════════════════════════════════════════════════════════════════
#
#    SKILL MODULE: TWELVE DATA LIVE MARKET FEED
#    ANTIGRAVITY REAL-TIME DATA ACQUISITION ENGINE (v4.1)
#
# ═══════════════════════════════════════════════════════════════════

## PURPOSE:
Enable Antigravity to access LIVE market data — real-time prices,
multi-timeframe OHLCV candles, 100+ technical indicators, and
cross-asset feeds — through the Twelve Data API, transforming
the agent from an analyst that works on static snapshots into
one that sees the market BREATHING in real-time.

## AUTHENTICATION

Base URL (REST):   https://api.twelvedata.com
Base URL (WebSocket): wss://ws.twelvedata.com
API Key:           Stored in environment variable TWELVEDATA_API_KEY
Auth Method:       Query parameter (&apikey=YOUR_API_KEY) or
                   Header (Authorization: apikey YOUR_API_KEY)

## PLAN AWARENESS & CREDIT MANAGEMENT

The API operates on a CREDIT SYSTEM that resets every minute.
Antigravity must track credit consumption to avoid 429 errors.

| Plan     | API Credits/Min | WS Credits | Daily Limit | Cost    |
|----------|----------------|------------|-------------|---------|
| Basic    | 8              | 8 trial    | 800/day     | Free    |
| Grow     | 55+            | 8          | Unlimited   | $29/mo  |
| Pro      | 610+           | 500+       | Unlimited   | $99/mo  |
| Ultra    | 2,584+         | 2,500+     | Unlimited   | $329/mo |

**CURRENT PLAN**: Basic (Free) — 8 credits/minute, 800/day.
**CRITICAL RULE**: Antigravity must NEVER exceed 8 API calls per
minute. Every request must be strategically prioritized.

**CREDIT COST PER ENDPOINT:**
| Endpoint                | Credits | Use Case                       |
|-------------------------|---------|--------------------------------|
| /price                  | 1       | Latest price (single number)   |
| /quote                  | 1       | Full quote (OHLCV + change)    |
| /time_series            | 1       | Historical OHLCV candles       |
| /technical_indicators   | 1       | RSI, ATR, EMA, SMA, etc.      |
| /forex_pairs            | 1       | List available forex pairs     |
| /exchange_rate          | 1       | Current exchange rate          |
| /price (batch 3 symbols)| 3       | 3 prices in one call           |

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1: CORE API ENDPOINTS FOR ANTIGRAVITY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 1.1 — REAL-TIME PRICE (The Heartbeat)

Returns the LATEST price for XAU/USD. Costs 1 credit.

**Request:**
GET https://api.twelvedata.com/price?symbol=XAU/USD&dp=2&apikey=YOUR_API_KEY

**Response:**
{
    "price": "4455.20"
}

**Multi-Symbol Request (1 credit per symbol):**
GET https://api.twelvedata.com/price?symbol=XAU/USD,XAG/USD,EUR/USD&dp=2&apikey=YOUR_API_KEY

**Response:**
{
    "XAU/USD": {"price": "4455.20"},
    "XAG/USD": {"price": "32.45"},
    "EUR/USD": {"price": "1.08320"}
}

**Antigravity Use**: Call this every analysis cycle to get the
current price for gold and SMT correlation pairs (silver, EUR/USD).


## 1.2 — FULL QUOTE (The Snapshot)

Returns comprehensive real-time data including OHLCV, change,
52-week range, and volume. Costs 1 credit.

**Request:**
GET https://api.twelvedata.com/quote?symbol=XAU/USD&interval=1day&dp=2&apikey=YOUR_API_KEY

**Response (key fields):**
{
    "symbol": "XAU/USD",
    "name": "Gold Spot / US Dollar",
    "exchange": "FOREX",
    "currency": "USD",
    "datetime": "2026-03-23",
    "open": "4491.00",
    "high": "4498.50",
    "low": "4128.00",
    "close": "4455.20",
    "previous_close": "4491.15",
    "change": "-35.95",
    "percent_change": "-0.80",
    "is_market_open": true,
    "fifty_two_week": {
        "low": "3280.00",
        "high": "5420.00",
        "range": "3280.00 - 5420.00"
    }
}

**Antigravity Use**: Run at SESSION START to get the daily OHLC,
previous close (for gap detection — Layer 11), and 52-week
range context.


## 1.3 — TIME SERIES (The Backbone)

Returns historical OHLCV candles at any interval. This is the
PRIMARY data feed for all structural and liquidity analysis.
Costs 1 credit per symbol.

**Supported Intervals:**
1min, 5min, 15min, 30min, 45min, 1h, 2h, 4h, 1day, 1week, 1month

**Request — M15 Candles (Last 100 bars):**
GET https://api.twelvedata.com/time_series?symbol=XAU/USD&interval=15min&outputsize=100&dp=2&timezone=UTC&apikey=YOUR_API_KEY

**Request — Daily Candles (Last 60 bars for IPDA):**
GET https://api.twelvedata.com/time_series?symbol=XAU/USD&interval=1day&outputsize=60&dp=2&timezone=UTC&apikey=YOUR_API_KEY

**Request — H4 Candles (Last 50 bars):**
GET https://api.twelvedata.com/time_series?symbol=XAU/USD&interval=4h&outputsize=50&dp=2&timezone=UTC&apikey=YOUR_API_KEY

**Response Format:**
{
    "meta": {
        "symbol": "XAU/USD",
        "interval": "15min",
        "currency": "USD",
        "exchange_timezone": "UTC",
        "type": "Physical Currency"
    },
    "values": [
        {
            "datetime": "2026-03-23 14:45:00",
            "open": "4450.30",
            "high": "4458.10",
            "low": "4448.50",
            "close": "4455.20",
            "volume": "0"
        },
        // ... more candles
    ],
    "status": "ok"
}

**Antigravity Use**:
- Daily (60 bars) → IPDA 20/40/60-day range computation (Module I)
- H4 (50 bars) → HTF structural analysis, OB/FVG identification
  (Module II & III)
- H1 (100 bars) → Intermediate structure, PO3 phase ID
- M15 (100 bars) → Active scalping range, zone identification
- M5 (100 bars) → Entry refinement, CISD detection
- M1 (100 bars) → Surgical entry execution


## 1.4 — TECHNICAL INDICATORS (The Analytical Arsenal)

Twelve Data provides 100+ pre-computed technical indicators.
Each costs 1 credit. Key indicators for Antigravity:

### ATR (Average True Range) — Volatility Regime Classification

GET https://api.twelvedata.com/atr?symbol=XAU/USD&interval=5min&time_period=14&dp=2&timezone=UTC&apikey=YOUR_API_KEY

**Response:**
{
    "meta": {"symbol": "XAU/USD", "interval": "5min", "indicator": {"name": "ATR", "time_period": 14}},
    "values": [
        {"datetime": "2026-03-23 14:45:00", "atr": "3.85"},
        // ...
    ]
}

→ Feed ATR value into Layer 7/13 for volatility regime classification.


### RSI (Relative Strength Index) — Momentum & Oversold/Overbought

GET https://api.twelvedata.com/rsi?symbol=XAU/USD&interval=1h&time_period=14&dp=2&timezone=UTC&apikey=YOUR_API_KEY

→ Feed into Module II for divergence detection and regime
  transition early warning (Layer 10.4).


### EMA (Exponential Moving Average) — Trend & Dynamic S/R

GET https://api.twelvedata.com/ema?symbol=XAU/USD&interval=1day&time_period=200&dp=2&timezone=UTC&apikey=YOUR_API_KEY

→ 200-day EMA = institutional trend filter.
→ 50-day EMA = medium-term momentum.
→ Feed into Module II for structural bias confirmation.


### BBANDS (Bollinger Bands) — Volatility Squeeze Detection

GET https://api.twelvedata.com/bbands?symbol=XAU/USD&interval=1h&time_period=20&sd=2&dp=2&timezone=UTC&apikey=YOUR_API_KEY

→ Feed into Layer 10.4: When bands squeeze to tightest in 20+
  candles = BREAKOUT IMMINENT regime warning.


### ADX (Average Directional Index) — Trend Strength

GET https://api.twelvedata.com/adx?symbol=XAU/USD&interval=1h&time_period=14&dp=2&timezone=UTC&apikey=YOUR_API_KEY

→ ADX > 25 = Trending regime. ADX < 20 = Ranging regime.
  Feed directly into Layer 10.1 regime classification.


### STOCH (Stochastic Oscillator) — OTE Zone Confirmation

GET https://api.twelvedata.com/stoch?symbol=XAU/USD&interval=15min&fast_k_period=14&slow_k_period=3&slow_d_period=3&dp=2&timezone=UTC&apikey=YOUR_API_KEY

→ Use at OTE zones: Stochastic in oversold (<20) at a bullish OTE
  zone = additional entry confirmation.


### COMPLETE INDICATOR LIST (All available at 1 credit each):
SMA, EMA, WMA, DEMA, TEMA, TRIMA, KAMA, T3MA, RSI, STOCH,
STOCHRSI, MACD, ADX, CCI, ATR, BBANDS, SAR, OBV, AD, ADOSC,
TRIX, WILLR, ROC, MOM, PPO, ULTOSC, DX, MINUS_DI, PLUS_DI,
MINUS_DM, PLUS_DM, ICHIMOKU, AROON, SUPERTREND, PIVOT_POINTS_HL,
PERCENT_B, HT_TRENDLINE, HT_SINE, VWAP, and 60+ more.


## 1.5 — CROSS-ASSET DATA (For SMT Divergence — Module V)

**Silver (XAG/USD) — Primary SMT Pair:**
GET https://api.twelvedata.com/time_series?symbol=XAG/USD&interval=15min&outputsize=50&dp=4&timezone=UTC&apikey=YOUR_API_KEY

**EUR/USD — Dollar Weakness Proxy:**
GET https://api.twelvedata.com/time_series?symbol=EUR/USD&interval=15min&outputsize=50&dp=5&timezone=UTC&apikey=YOUR_API_KEY

**GBP/USD — Secondary Dollar Proxy:**
GET https://api.twelvedata.com/time_series?symbol=GBP/USD&interval=15min&outputsize=50&dp=5&timezone=UTC&apikey=YOUR_API_KEY

**DXY (US Dollar Index):**
Note: DXY may require symbol "DXY" or may not be available on
the free plan. Alternative: Use EUR/USD as inverse proxy.


## 1.6 — EXCHANGE RATE (Quick Cross-Asset Check)

GET https://api.twelvedata.com/exchange_rate?symbol=XAU/USD&dp=2&apikey=YOUR_API_KEY

**Response:**
{
    "symbol": "XAU/USD",
    "rate": 4455.20,
    "timestamp": 1711152000
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2: STRATEGIC CREDIT BUDGET — THE 8-CREDIT PROTOCOL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

On the Basic (Free) plan, Antigravity has exactly 8 credits per
minute and 800 credits per day. Every credit must be spent with
SURGICAL PRECISION. Here is the optimized budget:

## 2.1 — FULL ANALYSIS CYCLE (8 credits — runs once per minute max)

| Priority | API Call                                      | Credits | Data Acquired                          |
|----------|-----------------------------------------------|---------|----------------------------------------|
| 1        | /time_series XAU/USD 15min (100 bars)         | 1       | Primary scalping structure              |
| 2        | /time_series XAU/USD 1day (60 bars)           | 1       | IPDA 20/40/60-day ranges               |
| 3        | /time_series XAU/USD 4h (50 bars)             | 1       | HTF structure, OB/FVG mapping          |
| 4        | /time_series XAU/USD 1h (100 bars)            | 1       | PO3 phase, intermediate structure      |
| 5        | /atr XAU/USD 5min (14 period)                 | 1       | Volatility regime (Layer 7/13)         |
| 6        | /rsi XAU/USD 1h (14 period)                   | 1       | Momentum, divergence detection         |
| 7        | /price XAU/USD,XAG/USD (batch)                | 2       | Current prices + SMT comparison        |
| **TOTAL**|                                               | **8**   | Complete analytical dataset             |

## 2.2 — QUICK UPDATE CYCLE (3 credits — for between-cycle checks)

| Priority | API Call                                      | Credits | Data Acquired                          |
|----------|-----------------------------------------------|---------|----------------------------------------|
| 1        | /price XAU/USD                                | 1       | Current gold price                     |
| 2        | /time_series XAU/USD 5min (30 bars)           | 1       | Recent M5 structure for entry          |
| 3        | /price XAG/USD                                | 1       | Silver for SMT check                   |
| **TOTAL**|                                               | **3**   | Entry-critical data refresh            |

## 2.3 — DAILY CREDIT BUDGET (800 credits/day)

| Activity                          | Frequency              | Credits/Cycle | Total/Day |
|-----------------------------------|------------------------|---------------|-----------|
| Full Analysis Cycle               | Every 5 min × 4 hrs   | 8             | 384       |
|                                   | (London + NY AM only)  |               |           |
| Quick Update Cycle                | Every 2 min × 4 hrs   | 3             | 360       |
| Session Start Deep Scan           | 1× per session         | 8             | 16        |
| Emergency News Re-scan            | ~3× per day            | 8             | 24        |
| **DAILY TOTAL**                   |                        |               | **784**   |
| **BUFFER REMAINING**              |                        |               | **16**    |

This budget provides FULL COVERAGE of London + NY AM sessions
(the highest-probability windows) while staying within the 800
daily limit with a safety buffer.


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3: DATA PROCESSING PIPELINE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 3.1 — FROM RAW API DATA TO ANTIGRAVITY INTELLIGENCE

When Antigravity receives time_series data, it must process it
through the following pipeline:

**STEP 1: IPDA Range Computation (from Daily data)**

From the 60 daily candles:
- 20-Day Range: Highest High & Lowest Low of candles [0–19]
- 40-Day Range: Highest High & Lowest Low of candles [0–39]
- 60-Day Range: Highest High & Lowest Low of candles [0–59]
- Equilibrium for each = (High + Low) / 2

**STEP 2: Structural Analysis (from H4 + H1 data)**

From H4/H1 candles, identify:
- Swing Highs: A candle high that is higher than the high of
  the candle before AND after it
- Swing Lows: A candle low that is lower than the low of the
  candle before AND after it
- BOS: When a candle CLOSES beyond a previous swing in the
  trend direction
- CHoCH: When a candle CLOSES beyond a swing AGAINST the
  current trend direction

**STEP 3: FVG Identification (from all timeframes)**

Scan every 3-candle sequence:
- Bullish FVG: candle[i-2].high < candle[i].low
  (gap between candle 1's high and candle 3's low)
- Bearish FVG: candle[i-2].low > candle[i].high
  (gap between candle 1's low and candle 3's high)

**STEP 4: Order Block Identification**

- Bullish OB: The last bearish (close < open) candle before a
  bullish displacement that creates BOS
- Bearish OB: The last bullish (close > open) candle before a
  bearish displacement that creates BOS

**STEP 5: Session Extreme Extraction**

From M15/H1 data with UTC timestamps:
- Asian Session: Highest High & Lowest Low between 00:00–07:00 UTC
- London Session: Highest High & Lowest Low between 07:00–12:00 UTC
- NY AM Session: Highest High & Lowest Low between 12:00–16:00 UTC
- Previous Day High/Low: From the daily candle [1]
- Previous Week High/Low: From the weekly candle or last 5 daily candles

**STEP 6: ATR Regime Classification (from /atr response)**

Read the latest ATR value and classify per Layer 13:
- ATR < 1.50: DEAD ZONE
- ATR 1.50–3.50: NORMAL
- ATR 3.50–5.00: ELEVATED
- ATR 5.00–8.00: HIGH (Adaptive Mode)
- ATR 8.00–15.00: EXTREME (Survival Mode)
- ATR > 15.00: CRISIS (No Trade)

**STEP 7: SMT Divergence Check (from XAG/USD comparison)**

Compare the last swing low/high on XAU/USD with the corresponding
swing low/high on XAG/USD at the same timestamp. Flag divergence
per Module V rules.


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 4: INTEGRATION WITH ANTIGRAVITY MODULES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## How Each Module Consumes Twelve Data:

| Antigravity Module                      | Twelve Data Feed                   | Endpoint           |
|-----------------------------------------|------------------------------------|--------------------|
| Module I (IPDA Liquidity)               | Daily candles (60 bars)            | /time_series 1day  |
| Module I (Session Extremes)             | M15/H1 candles                     | /time_series 15min |
| Module II (Fractal Structure)           | H4, H1, M15 candles               | /time_series multi |
| Module II (PO3 Phase)                   | H1 candles + Daily candle OHLC     | /time_series + /quote |
| Module III (FVG/OB Detection)           | All TF candles                     | /time_series multi |
| Module III (OTE Fibonacci)              | Computed from swing points in data | (calculated locally)|
| Module IV (Macro Context)               | Daily candles for trend, /quote    | /quote + /time_series|
| Module V (SMT Divergence)               | XAG/USD candles + current prices   | /time_series + /price|
| Layer 7/13 (Volatility)                 | ATR(14) on M5                      | /atr               |
| Layer 10 (Regime)                       | ADX on H1 + BBands on H1          | /adx + /bbands     |
| Layer 10.4 (Divergence Detection)       | RSI(14) on H1                      | /rsi               |


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 5: ERROR HANDLING & RESILIENCE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Antigravity must handle API failures gracefully:

| Error Code | Meaning              | Antigravity Response                     |
|------------|----------------------|------------------------------------------|
| 429        | Rate limit hit       | Wait 60s. Use cached data. Flag warning. |
| 400        | Bad parameter        | Log error. Skip this call. Use fallback. |
| 401        | Bad API key          | HALT. Alert user. Cannot proceed.        |
| 500        | Server error         | Retry once after 5s. Then use cache.     |
| No response| Network timeout      | Use last cached data. Flag STALE DATA.   |

**STALE DATA PROTOCOL**: If API data is older than 5 minutes,
flag all analysis outputs with:
⚠️ WARNING: Market data is STALE (last update: [timestamp]).
Analysis may not reflect current prices. Confidence reduced.
