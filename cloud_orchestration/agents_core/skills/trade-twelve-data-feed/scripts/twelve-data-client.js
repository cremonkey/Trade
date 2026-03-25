// ── Twelve Data API Client for Antigravity Dashboard ──

const TD_BASE = 'https://api.twelvedata.com';
const TD_KEY = process.env.TWELVEDATA_API_KEY; // NEVER expose client-side

// ── Core Fetch Function with Error Handling ──
async function tdFetch(endpoint, params = {}) {
  const url = new URL(`${TD_BASE}/${endpoint}`);
  Object.entries({ ...params, apikey: TD_KEY }).forEach(
    ([k, v]) => url.searchParams.set(k, v)
  );
  const res = await fetch(url.toString());
  const data = await res.json();
  if (data.code === 429) throw new Error('RATE_LIMIT: Wait 60 seconds');
  if (data.status === 'error') throw new Error(`TD_ERROR: ${data.message}`);
  return data;
}

// ── 1. Get Current Price ──
async function getPrice(symbol = 'XAU/USD') {
  return tdFetch('price', { symbol, dp: 2 });
}

// ── 2. Get Multi-Symbol Prices (SMT + Gold) ──
async function getSMTPrices() {
  return tdFetch('price', {
    symbol: 'XAU/USD,XAG/USD',
    dp: 4
  });
}

// ── 3. Get Full Quote ──
async function getQuote(symbol = 'XAU/USD') {
  return tdFetch('quote', {
    symbol,
    interval: '1day',
    dp: 2,
    timezone: 'UTC'
  });
}

// ── 4. Get Time Series (Any TF) ──
async function getTimeSeries(symbol, interval, outputsize = 100) {
  return tdFetch('time_series', {
    symbol,
    interval,
    outputsize,
    dp: 2,
    timezone: 'UTC',
    order: 'asc'
  });
}

// ── 5. Get ATR ──
async function getATR(symbol = 'XAU/USD', interval = '5min') {
  return tdFetch('atr', {
    symbol,
    interval,
    time_period: 14,
    dp: 2,
    timezone: 'UTC'
  });
}

// ── 6. Get RSI ──
async function getRSI(symbol = 'XAU/USD', interval = '1h') {
  return tdFetch('rsi', {
    symbol,
    interval,
    time_period: 14,
    dp: 2,
    timezone: 'UTC'
  });
}

// ── 7. Get Bollinger Bands ──
async function getBBands(symbol = 'XAU/USD', interval = '1h') {
  return tdFetch('bbands', {
    symbol,
    interval,
    time_period: 20,
    sd: 2,
    dp: 2,
    timezone: 'UTC'
  });
}

// ── 8. Get ADX ──
async function getADX(symbol = 'XAU/USD', interval = '1h') {
  return tdFetch('adx', {
    symbol,
    interval,
    time_period: 14,
    dp: 2,
    timezone: 'UTC'
  });
}

// ══════════════════════════════════════════════════════
// FULL ANALYSIS CYCLE (8 credits)
// ══════════════════════════════════════════════════════
async function runFullAnalysis() {
  const [
    m15Data,       // 1 credit
    dailyData,     // 1 credit
    h4Data,        // 1 credit
    h1Data,        // 1 credit
    atrData,       // 1 credit
    rsiData,       // 1 credit
    smtPrices      // 2 credits (XAU + XAG)
  ] = await Promise.all([
    getTimeSeries('XAU/USD', '15min', 100),
    getTimeSeries('XAU/USD', '1day', 60),
    getTimeSeries('XAU/USD', '4h', 50),
    getTimeSeries('XAU/USD', '1h', 100),
    getATR('XAU/USD', '5min'),
    getRSI('XAU/USD', '1h'),
    getSMTPrices()
  ]);

  return {
    currentPrice: smtPrices['XAU/USD']?.price,
    silverPrice: smtPrices['XAG/USD']?.price,
    candles: {
      m15: m15Data.values,
      daily: dailyData.values,
      h4: h4Data.values,
      h1: h1Data.values
    },
    indicators: {
      atr: atrData.values?.[0]?.atr,
      rsi: rsiData.values?.[0]?.rsi
    },
    timestamp: new Date().toISOString()
  };
}

// ══════════════════════════════════════════════════════
// IPDA RANGE COMPUTATION (from daily candles)
// ══════════════════════════════════════════════════════
function computeIPDA(dailyCandles) {
  const compute = (candles, days) => {
    const slice = candles.slice(-days);
    const highs = slice.map(c => parseFloat(c.high));
    const lows = slice.map(c => parseFloat(c.low));
    const high = Math.max(...highs);
    const low = Math.min(...lows);
    return {
      high,
      low,
      equilibrium: +((high + low) / 2).toFixed(2),
      range: +(high - low).toFixed(2)
    };
  };
  return {
    ipda20: compute(dailyCandles, 20),
    ipda40: compute(dailyCandles, 40),
    ipda60: compute(dailyCandles, 60)
  };
}

// ══════════════════════════════════════════════════════
// SESSION EXTREMES EXTRACTION (from H1/M15 candles)
// ══════════════════════════════════════════════════════
function extractSessionExtremes(candles) {
  const sessions = {
    asian:  { start: 0,  end: 7  },
    london: { start: 7,  end: 12 },
    nyAM:   { start: 12, end: 16 },
    nyPM:   { start: 16, end: 21 }
  };

  const today = new Date().toISOString().split('T')[0];
  const results = {};

  for (const [name, hours] of Object.entries(sessions)) {
    const sessionCandles = candles.filter(c => {
      const dt = new Date(c.datetime);
      const h = dt.getUTCHours();
      const d = dt.toISOString().split('T')[0];
      return d === today && h >= hours.start && h < hours.end;
    });

    if (sessionCandles.length > 0) {
      results[name] = {
        high: Math.max(...sessionCandles.map(c => parseFloat(c.high))),
        low: Math.min(...sessionCandles.map(c => parseFloat(c.low))),
        swept: false // updated by analysis engine
      };
    }
  }
  return results;
}

// ══════════════════════════════════════════════════════
// FVG SCANNER (from any timeframe candles)
// ══════════════════════════════════════════════════════
function scanFVGs(candles) {
  const fvgs = [];
  for (let i = 2; i < candles.length; i++) {
    const c1 = candles[i - 2]; // oldest
    const c2 = candles[i - 1]; // middle (displacement)
    const c3 = candles[i];     // newest

    const c1High = parseFloat(c1.high);
    const c1Low = parseFloat(c1.low);
    const c3High = parseFloat(c3.high);
    const c3Low = parseFloat(c3.low);

    // Bullish FVG: gap between c1 high and c3 low
    if (c3Low > c1High) {
      fvgs.push({
        type: 'BULLISH',
        top: c3Low,
        bottom: c1High,
        ce: +((c3Low + c1High) / 2).toFixed(2), // Consequent Encroachment
        datetime: c2.datetime,
        status: 'UNMITIGATED'
      });
    }

    // Bearish FVG: gap between c1 low and c3 high
    if (c3High < c1Low) {
      fvgs.push({
        type: 'BEARISH',
        top: c1Low,
        bottom: c3High,
        ce: +((c1Low + c3High) / 2).toFixed(2),
        datetime: c2.datetime,
        status: 'UNMITIGATED'
      });
    }
  }
  return fvgs;
}

// ══════════════════════════════════════════════════════
// VOLATILITY REGIME CLASSIFIER (from ATR value)
// ══════════════════════════════════════════════════════
function classifyVolatility(atrValue) {
  const atr = parseFloat(atrValue);
  if (atr < 1.5)  return { regime: 'DEAD_ZONE',  maxSL: 0,  tradeable: false };
  if (atr < 3.5)  return { regime: 'NORMAL',      maxSL: 10, tradeable: true  };
  if (atr < 5.0)  return { regime: 'ELEVATED',    maxSL: 10, tradeable: true  };
  if (atr < 8.0)  return { regime: 'HIGH',         maxSL: 15, tradeable: true  };
  if (atr < 15.0) return { regime: 'EXTREME',      maxSL: 20, tradeable: true  };
  return           { regime: 'CRISIS',       maxSL: 0,  tradeable: false };
}

export {
  runFullAnalysis,
  computeIPDA,
  extractSessionExtremes,
  scanFVGs,
  classifyVolatility,
  getPrice,
  getQuote,
  getTimeSeries,
  getATR,
  getRSI,
  getBBands,
  getADX
};
