-- Business Domain table
CREATE TABLE business_domain (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    db_name VARCHAR(255),
    custom_fields JSON
);

-- Dataset table
CREATE TABLE dataset (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    business_domain_id INTEGER REFERENCES business_domain(id),
    owner VARCHAR(255),
    last_updated DATE,
    number_of_records INTEGER,
    access_level VARCHAR(50),
    recent_views INTEGER DEFAULT 0,
    custom_fields JSON
);

-- Data Asset table
CREATE TABLE data_asset (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    dataset_id INTEGER REFERENCES dataset(id),
    asset_type VARCHAR(50) NOT NULL, -- e.g., 'CSV', 'JSON', 'XML'
    storage_location VARCHAR(255), -- URL or path to the data
    constraints TEXT,
    update_frequency VARCHAR(50),
    estimated_size INTEGER,
    row_doc_count INTEGER,
    processing_instruction VARCHAR(50),
    custom_fields JSON
);

-- Column table (for structured data assets)
CREATE TABLE column_info (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    genai_description TEXT,
    sample_values TEXT,
    data_type VARCHAR(50),
    is_required BOOLEAN DEFAULT FALSE,
    data_asset_id INTEGER REFERENCES data_asset(id),
    custom_fields JSON
);

-- Tag table
CREATE TABLE tag (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    UNIQUE(name)
);

-- Junction table for tags (allows many-to-many relationships)
CREATE TABLE entity_tag (
    id SERIAL PRIMARY KEY,
    tag_id INTEGER REFERENCES tag(id),
    entity_type VARCHAR(50) NOT NULL, -- 'business_domain', 'dataset', 'data_asset', or 'column'
    entity_id INTEGER NOT NULL
);


-- Indexes for better query performance
CREATE INDEX idx_dataset_business_domain ON dataset(business_domain_id);
CREATE INDEX idx_data_asset_dataset ON data_asset(dataset_id);
CREATE INDEX idx_column_data_asset ON column_info(data_asset_id);
