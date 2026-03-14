CREATE TABLE IF NOT EXISTS assets (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL
    logo_url VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS prices (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES assets(id),
    date DATE NOT NULL,
    close_price NUMERIC(12,4) NOT NULL,
    volume BIGINT, 
    UNIQUE(asset_id, date)
);

-- Index para buscar dos ativos e pela data
CREATE INDEX IF NOT EXISTS idx_prices_asset_date
    ON prices(asset_id, date);


