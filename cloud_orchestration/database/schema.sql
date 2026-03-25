-- System Configuration & State
CREATE TABLE system_config (
    id SERIAL PRIMARY KEY,
    balance DECIMAL(12, 2) DEFAULT 88.00,
    equity DECIMAL(12, 2) DEFAULT 88.00,
    lot_cap DECIMAL(5, 2) DEFAULT 5.00,
    phase TEXT DEFAULT 'Sovereign Moonshot',
    discipline_lock_until TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Initialize system_config
INSERT INTO system_config (balance, equity, lot_cap, phase) VALUES (88.00, 88.00, 5.00, 'Sovereign Moonshot');

-- Trading Journal
CREATE TABLE trading_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    pair TEXT DEFAULT 'XAU/USD',
    direction TEXT, -- 'LONG' or 'SHORT'
    entry_price DECIMAL(10, 2),
    exit_price DECIMAL(10, 2),
    lots DECIMAL(5, 2),
    profit_loss DECIMAL(12, 2),
    ftcs_score INTEGER,
    status TEXT DEFAULT 'OPEN' -- 'OPEN', 'CLOSED'
);

-- Daily Session Metrics
CREATE TABLE session_summaries (
    id SERIAL PRIMARY KEY,
    session_date DATE UNIQUE DEFAULT CURRENT_DATE,
    ftcs_daily_avg INTEGER,
    total_trades INTEGER DEFAULT 0,
    daily_pnl DECIMAL(12, 2) DEFAULT 0.00,
    opex_deduction DECIMAL(12, 2) DEFAULT 0.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
