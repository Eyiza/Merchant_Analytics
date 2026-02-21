CREATE TABLE IF NOT EXISTS activities (
    event_id UUID PRIMARY KEY,
    merchant_id VARCHAR NOT NULL CHECK (merchant_id LIKE 'MRC%'),
    event_timestamp TIMESTAMP NOT NULL,
    product VARCHAR NOT NULL CHECK (product IN ('POS', 'AIRTIME', 'BILLS', 'CARD_PAYMENT', 'SAVINGS', 'MONIEBOOK', 'KYC')),
    event_type VARCHAR NOT NULL,
    amount NUMERIC(18,2) NOT NULL CHECK (amount >= 0),
    status VARCHAR NOT NULL CHECK (status IN ('SUCCESS', 'FAILED', 'PENDING')),
    channel VARCHAR NOT NULL CHECK (channel IN ('POS', 'APP', 'USSD', 'WEB', 'OFFLINE')),
    region VARCHAR,
    merchant_tier VARCHAR NOT NULL CHECK (merchant_tier IN ('STARTER', 'VERIFIED', 'PREMIUM'))
);

CREATE INDEX IF NOT EXISTS idx_merchant ON activities(merchant_id);
CREATE INDEX IF NOT EXISTS idx_product ON activities(product);
CREATE INDEX IF NOT EXISTS idx_status ON activities(status);
CREATE INDEX IF NOT EXISTS idx_timestamp ON activities(event_timestamp);
CREATE INDEX IF NOT EXISTS idx_event_type ON activities(event_type);
CREATE INDEX IF NOT EXISTS idx_timestamp_status ON activities(event_timestamp, status);