CREATE TABLE IF NOT EXISTS activities (
    event_id UUID PRIMARY KEY,
    merchant_id VARCHAR NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    product VARCHAR NOT NULL,
    event_type VARCHAR NOT NULL,
    amount NUMERIC(18,2),
    status VARCHAR NOT NULL,
    channel VARCHAR,
    region VARCHAR,
    merchant_tier VARCHAR
);

CREATE INDEX IF NOT EXISTS idx_merchant ON activities(merchant_id);
CREATE INDEX IF NOT EXISTS idx_product ON activities(product);
CREATE INDEX IF NOT EXISTS idx_status ON activities(status);
CREATE INDEX IF NOT EXISTS idx_timestamp ON activities(event_timestamp);
CREATE INDEX IF NOT EXISTS idx_event_type ON activities(event_type);