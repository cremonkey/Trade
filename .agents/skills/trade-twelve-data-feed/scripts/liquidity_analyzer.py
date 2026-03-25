import json
import os

def detect_fvgs(candles):
    """
    Scans candles for Fair Value Gaps (FVG).
    Format: [{'datetime': str, 'open': float, 'high': float, 'low': float, 'close': float}, ...]
    """
    fvgs = []
    # Convert string prices to float
    c = []
    for candle in candles:
        c.append({
            'datetime': candle['datetime'],
            'open': float(candle['open']),
            'high': float(candle['high']),
            'low': float(candle['low']),
            'close': float(candle['close'])
        })
    
    # We scan 3-candle sequences [i-2, i-1, i] (oldest to newest)
    for i in range(2, len(c)):
        c1, c2, c3 = c[i-2], c[i-1], c[i]
        
        # Bullish FVG (Gap between C1 High and C3 Low)
        if c3['low'] > c1['high']:
            fvgs.append({
                'type': 'BULLISH',
                'top': round(c3['low'], 2),
                'bottom': round(c1['high'], 2),
                'ce': round((c3['low'] + c1['high']) / 2, 2), # Consequent Encroachment
                'datetime': c2['datetime'],
                'strength': round(c3['low'] - c1['high'], 2)
            })
            
        # Bearish FVG (Gap between C1 Low and C3 High)
        if c3['high'] < c1['low']:
            fvgs.append({
                'type': 'BEARISH',
                'top': round(c1['low'], 2),
                'bottom': round(c3['high'], 2),
                'ce': round((c1['low'] + c3['high']) / 2, 2),
                'datetime': c2['datetime'],
                'strength': round(c1['low'] - c3['high'], 2)
            })
    return fvgs

def detect_orderblocks(candles):
    """
    Basic Order Block Detection.
    Look for the last candle in opposite direction before a displacement.
    """
    obs = []
    # Simplistic version for now: identify large displacements (BOS)
    # A real OB is the candle before a displacement that results in BOS/CHoCH.
    # For this POC, we look for impulsive moves.
    return obs # To be refined in next step

def calculate_ipda_ranges(daily_candles):
    """Compute IPDA 20/40/60 day ranges."""
    def get_range(slice_size):
        subset = daily_candles[:slice_size]
        highs = [float(x['high']) for x in subset]
        lows = [float(x['low']) for x in subset]
        h = max(highs)
        l = min(lows)
        return {
            'high': round(h, 2),
            'low': round(l, 2),
            'eq': round((h + l) / 2, 2),
            'range': round(h - l, 2)
        }
    
    return {
        'ipda20': get_range(20),
        'ipda40': get_range(40),
        'ipda60': get_range(60)
    }

def analyze_volatility(atr_value):
    """Classify regime based on ATR."""
    atr = float(atr_value)
    if atr < 1.5:  return "DEAD_ZONE"
    if atr < 3.5:  return "NORMAL"
    if atr < 5.0:  return "ELEVATED"
    if atr < 8.0:  return "HIGH"
    if atr < 15.0: return "EXTREME"
    return "CRISIS"
