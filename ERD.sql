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
CREATE INDEX idx_metadata_entity ON metadata(entity_type, entity_id);
CREATE INDEX idx_entity_tag_entity ON entity_tag(entity_type, entity_id);
CREATE INDEX idx_quick_action_dataset ON quick_action(dataset_id);

--- permissions 

-- User table
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user', -- 'admin', 'user'
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP 
);

-- Permission table
CREATE TABLE permission (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT
);

-- UserPermission junction table
CREATE TABLE user_permission (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user(id),
    permission_id INTEGER REFERENCES permission(id)
);

-- BusinessDomainPermission junction table
CREATE TABLE business_domain_permission (
    id SERIAL PRIMARY KEY,
    business_domain_id INTEGER REFERENCES business_domain(id),
    permission_id INTEGER REFERENCES permission(id)
);

-- DatasetPermission junction table
CREATE TABLE dataset_permission (
    id SERIAL PRIMARY KEY,
    dataset_id INTEGER REFERENCES dataset(id),
    permission_id INTEGER REFERENCES permission(id)
);

-- DataAssetPermission junction table
CREATE TABLE data_asset_permission (
    id SERIAL PRIMARY KEY,
    data_asset_id INTEGER REFERENCES data_asset(id),
    permission_id INTEGER REFERENCES permission(id)
);

-- ColumnPermission junction table
CREATE TABLE column_permission (
    id SERIAL PRIMARY KEY,
    column_info_id INTEGER REFERENCES column_info(id),
    permission_id INTEGER REFERENCES permission(id)
);

-- Add indexes for better query performance
CREATE INDEX idx_user_permission ON user_permission(user_id, permission_id);
CREATE INDEX idx_business_domain_permission ON business_domain_permission(business_domain_id, permission_id);
CREATE INDEX idx_dataset_permission ON dataset_permission(dataset_id, permission_id);
CREATE INDEX idx_data_asset_permission ON data_asset_permission(data_asset_id, permission_id);
CREATE INDEX idx_column_permission ON column_permission(column_info_id, permission_id);

---- Staging and batching 

CREATE TABLE staging_dataset (
    id SERIAL,
    name VARCHAR(255),
    description TEXT,
    business_domain_id INTEGER,
    owner VARCHAR(255),
    last_updated DATE,
    number_of_records INTEGER,
    access_level VARCHAR(50),
    recent_views INTEGER DEFAULT 0,
    custom_fields JSON
);

CREATE TABLE staging_data_asset (
    id SERIAL,
    name VARCHAR(255),
    description TEXT,
    dataset_id INTEGER,
    asset_type VARCHAR(50),
    storage_location VARCHAR(255),
    constraints TEXT,
    update_frequency VARCHAR(50),
    estimated_size INTEGER,
    row_doc_count INTEGER,
    processing_instruction VARCHAR(50),
    custom_fields JSON
);

CREATE TABLE staging_column_info (
    id SERIAL,
    name VARCHAR(255),
    description TEXT,
    genai_description TEXT,
    sample_values TEXT,
    data_type VARCHAR(50),
    is_required BOOLEAN DEFAULT FALSE,
    data_asset_id INTEGER,
    custom_fields JSON
);

CREATE TABLE batch_status (
    batch_id SERIAL PRIMARY KEY,
    entity_name VARCHAR(50), -- Name of the entity being processed, e.g., 'dataset', 'data_asset', 'column_info'
    batch_start_time TIMESTAMP,
    batch_end_time TIMESTAMP,
    status VARCHAR(50), -- 'SUCCESS', 'FAILED', 'IN_PROGRESS'
    error_message TEXT,
    row_count INTEGER, -- Number of rows processed in the batch
    processed_by VARCHAR(255) -- The name of the ETL job or system
);

CREATE TABLE batch_errors (
    error_id SERIAL PRIMARY KEY,
    batch_id INTEGER REFERENCES batch_status(batch_id),
    entity_name VARCHAR(50), -- Name of the entity being processed
    error_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    error_message TEXT,
    error_details TEXT -- Additional details like row number, field name, etc.
);

------------- GenAI Analytics 

CREATE TABLE chat_interaction (
    interaction_id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES user(id), -- References the person table
    session_id TEXT NOT NULL,
    message TEXT NOT NULL, -- The message content
    sender VARCHAR(50) NOT NULL, -- 'USER' or 'CHATBOT'
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Time the message was sent
);

CREATE TABLE chatbot_rating (
    rating_id SERIAL PRIMARY KEY,
    interaction_id INTEGER REFERENCES chat_interaction(interaction_id), -- References the chat interaction
    rating VARCHAR(10) NOT NULL, -- 'LIKE' or 'DISLIKE'
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Time the rating was given
);



