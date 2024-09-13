-- Insert business domains
INSERT INTO business_domain (name, description, db_name, custom_fields)
VALUES 
('Finance', 'Handles all finance-related datasets.', 'finance_db', '{}'),
('Sales', 'Handles all sales-related datasets.', 'sales_db', '{}');

-- Insert datasets for Finance domain
INSERT INTO dataset (name, description, business_domain_id, owner, last_updated, number_of_records, access_level, recent_views, custom_fields)
VALUES
('Finance Transactions', 'Dataset containing financial transactions', 1, 'finance_manager', '2024-09-01', 100000, 'public', 25, '{}'),
('Finance Reports', 'Dataset containing financial reports', 1, 'finance_analyst', '2024-09-02', 5000, 'restricted', 15, '{}');

-- Insert datasets for Sales domain
INSERT INTO dataset (name, description, business_domain_id, owner, last_updated, number_of_records, access_level, recent_views, custom_fields)
VALUES
('Sales Leads', 'Dataset containing sales leads', 2, 'sales_manager', '2024-09-01', 20000, 'public', 30, '{}'),
('Sales Performance', 'Dataset containing sales performance reports', 2, 'sales_analyst', '2024-09-03', 1000, 'restricted', 10, '{}');

-- Insert data assets (tables) for Finance Transactions dataset
INSERT INTO data_asset (name, description, dataset_id, asset_type, storage_location, constraints, update_frequency, estimated_size, row_doc_count, processing_instruction, custom_fields)
VALUES
('Transactions 2024', 'Financial transactions for the year 2024', 1, 'CSV', '/path/to/transactions2024.csv', NULL, 'daily', 100, 10000, 'none', '{}'),
('Transactions 2023', 'Financial transactions for the year 2023', 1, 'CSV', '/path/to/transactions2023.csv', NULL, 'monthly', 80, 8000, 'none', '{}');

-- Insert data assets (tables) for Finance Reports dataset
INSERT INTO data_asset (name, description, dataset_id, asset_type, storage_location, constraints, update_frequency, estimated_size, row_doc_count, processing_instruction, custom_fields)
VALUES
('Reports 2024', 'Financial reports for the year 2024', 2, 'PDF', '/path/to/reports2024.pdf', NULL, 'monthly', 10, 100, 'none', '{}'),
('Reports 2023', 'Financial reports for the year 2023', 2, 'PDF', '/path/to/reports2023.pdf', NULL, 'quarterly', 8, 80, 'none', '{}');

-- Insert data assets (tables) for Sales Leads dataset
INSERT INTO data_asset (name, description, dataset_id, asset_type, storage_location, constraints, update_frequency, estimated_size, row_doc_count, processing_instruction, custom_fields)
VALUES
('Leads Q1 2024', 'Sales leads for Q1 2024', 3, 'CSV', '/path/to/leads_q1_2024.csv', NULL, 'daily', 50, 5000, 'none', '{}'),
('Leads Q4 2023', 'Sales leads for Q4 2023', 3, 'CSV', '/path/to/leads_q4_2023.csv', NULL, 'monthly', 45, 4500, 'none', '{}');

-- Insert data assets (tables) for Sales Performance dataset
INSERT INTO data_asset (name, description, dataset_id, asset_type, storage_location, constraints, update_frequency, estimated_size, row_doc_count, processing_instruction, custom_fields)
VALUES
('Performance Q1 2024', 'Sales performance data for Q1 2024', 4, 'CSV', '/path/to/performance_q1_2024.csv', NULL, 'monthly', 30, 3000, 'none', '{}'),
('Performance Q4 2023', 'Sales performance data for Q4 2023', 4, 'CSV', '/path/to/performance_q4_2023.csv', NULL, 'monthly', 25, 2500, 'none', '{}');

-- Insert columns for Transactions 2024 table
INSERT INTO column_info (name, description, genai_description, sample_values, data_type, is_required, data_asset_id, custom_fields)
VALUES
('Transaction ID', 'Unique identifier for each transaction', NULL, 'T001, T002, T003', 'INTEGER', TRUE, 1, '{}'),
('Date', 'Transaction date', NULL, '2024-01-01, 2024-01-02', 'DATE', TRUE, 1, '{}'),
('Amount', 'Transaction amount', NULL, '100.50, 200.75', 'DECIMAL', TRUE, 1, '{}'),
('Currency', 'Currency of the transaction', NULL, 'USD, EUR', 'VARCHAR(3)', TRUE, 1, '{}'),
('Customer ID', 'Identifier for the customer', NULL, 'C001, C002', 'INTEGER', FALSE, 1, '{}'),
('Merchant ID', 'Identifier for the merchant', NULL, 'M001, M002', 'INTEGER', FALSE, 1, '{}'),
('Status', 'Transaction status', NULL, 'Completed, Pending', 'VARCHAR(20)', TRUE, 1, '{}'),
('Payment Method', 'Method of payment', NULL, 'Credit Card, PayPal', 'VARCHAR(50)', TRUE, 1, '{}'),
('Country', 'Country of the transaction', NULL, 'US, DE', 'VARCHAR(50)', FALSE, 1, '{}'),
('Category', 'Category of the transaction', NULL, 'Groceries, Electronics', 'VARCHAR(100)', FALSE, 1, '{}');

-- Insert columns for Transactions 2023 table
INSERT INTO column_info (name, description, genai_description, sample_values, data_type, is_required, data_asset_id, custom_fields)
VALUES
('Transaction ID', 'Unique identifier for each transaction', NULL, 'T1001, T1002', 'INTEGER', TRUE, 2, '{}'),
('Date', 'Transaction date', NULL, '2023-12-01, 2023-12-02', 'DATE', TRUE, 2, '{}'),
('Amount', 'Transaction amount', NULL, '300.00, 400.50', 'DECIMAL', TRUE, 2, '{}'),
('Currency', 'Currency of the transaction', NULL, 'USD, GBP', 'VARCHAR(3)', TRUE, 2, '{}'),
('Customer ID', 'Identifier for the customer', NULL, 'C1001, C1002', 'INTEGER', FALSE, 2, '{}'),
('Merchant ID', 'Identifier for the merchant', NULL, 'M1001, M1002', 'INTEGER', FALSE, 2, '{}'),
('Status', 'Transaction status', NULL, 'Completed, Failed', 'VARCHAR(20)', TRUE, 2, '{}'),
('Payment Method', 'Method of payment', NULL, 'Bank Transfer, Credit Card', 'VARCHAR(50)', TRUE, 2, '{}'),
('Country', 'Country of the transaction', NULL, 'US, UK', 'VARCHAR(50)', FALSE, 2, '{}'),
('Category', 'Category of the transaction', NULL, 'Travel, Entertainment', 'VARCHAR(100)', FALSE, 2, '{}');

-- Insert columns for Reports 2024 table
INSERT INTO column_info (name, description, genai_description, sample_values, data_type, is_required, data_asset_id, custom_fields)
VALUES
('Report ID', 'Unique identifier for each report', NULL, 'R001, R002', 'INTEGER', TRUE, 3, '{}'),
('Title', 'Title of the report', NULL, 'Annual Report 2024, Q1 Report 2024', 'VARCHAR(255)', TRUE, 3, '{}'),
('Author', 'Author of the report', NULL, 'John Doe, Jane Smith', 'VARCHAR(100)', TRUE, 3, '{}'),
('Date', 'Date of the report', NULL, '2024-04-01, 2024-05-01', 'DATE', TRUE, 3, '{}'),
('Report Type', 'Type of report', NULL, 'Annual, Quarterly', 'VARCHAR(50)', TRUE, 3, '{}'),
('Pages', 'Number of pages in the report', NULL, '10, 20', 'INTEGER', FALSE, 3, '{}'),
('Summary', 'Summary of the report', NULL, 'Financial summary of Q1', 'TEXT', FALSE, 3, '{}'),
('Department', 'Department generating the report', NULL, 'Finance, Accounting', 'VARCHAR(100)', TRUE, 3, '{}'),
('Approval Status', 'Status of report approval', NULL, 'Approved, Pending', 'VARCHAR(20)', TRUE, 3, '{}'),
('Region', 'Region the report covers', NULL, 'US, Europe', 'VARCHAR(50)', FALSE, 3, '{}');

-- You can repeat similar DML statements for other tables and columns


--- Gemini Generated 
-- Insert data into business_domain table
INSERT INTO business_domain (name, description, db_name, custom_fields) VALUES
('Healthcare', 'Data related to healthcare industry', 'healthcare_db', '{"industry": "healthcare"}'),
('Finance', 'Data related to financial industry', 'finance_db', '{"industry": "finance"}'),
('Retail', 'Data related to retail industry', 'retail_db', '{"industry": "retail"}'),
('Manufacturing', 'Data related to manufacturing industry', 'manufacturing_db', '{"industry": "manufacturing"}'),
('Education', 'Data related to education industry', 'education_db', '{"industry": "education"}');

-- Insert data into dataset table
INSERT INTO dataset (name, description, business_domain_id, owner, last_updated, number_of_records, access_level, recent_views, custom_fields) VALUES
('Patient Data', 'Data about patients and their medical records', 1, 'Dr. Smith', '2023-01-01', 100000, 'Private', 10, '{"sensitive": true}'),
('Sales Data', 'Data about sales transactions and customers', 2, 'John Doe', '2023-02-01', 500000, 'Internal', 20, '{"important": true}'),
('Product Data', 'Data about products and their inventory', 3, 'Jane Smith', '2023-03-01', 200000, 'Public', 30, '{"publicly_available": true}'),
('Machine Data', 'Data generated by machines and sensors', 4, 'System Admin', '2023-04-01', 10000000, 'Private', 40, '{"technical": true}'),
('Student Data', 'Data about students and their academic records', 5, 'Professor Jones', '2023-05-01', 50000, 'Internal', 50, '{"confidential": true}');

-- Insert data into data_asset table
INSERT INTO data_asset (name, description, dataset_id, asset_type, storage_location, constraints, update_frequency, estimated_size, row_doc_count, processing_instruction, custom_fields) VALUES
('Patient Records', 'Detailed information about patients and their medical history', 1, 'CSV', '/data/healthcare/patient_records.csv', 'Patient ID is unique', 'Monthly', 100000000, 100000, 'Remove duplicate records', '{"pii": true}'),
('Sales Transactions', 'Data about sales transactions, including products sold and customer information', 2, 'JSON', '/data/finance/sales_transactions.json', 'Transaction ID is unique', 'Daily', 500000000, 500000, 'Enrich with customer data', '{"gdpr_compliant": true}'),
('Product Catalog', 'Data about products, including descriptions, prices, and inventory levels', 3, 'XML', '/data/retail/product_catalog.xml', 'Product ID is unique', 'Weekly', 200000000, 200000, 'Normalize data', '{"publicly_available": true}'),
('Sensor Data', 'Data collected from sensors, including temperature, humidity, and motion', 4, 'Parquet', '/data/manufacturing/sensor_data.parquet', 'Timestamp is unique', 'Real-time', 1000000000000, 100000000, 'Aggregate data', '{"technical": true}'),
('Student Grades', 'Data about student grades and academic performance', 5, 'CSV', '/data/education/student_grades.csv', 'Student ID is unique', 'Quarterly', 50000000, 50000, 'Calculate GPA', '{"pii": true}');

-- Insert data into column_info table
INSERT INTO column_info (name, description, genai_description, sample_values, data_type, is_required, data_asset_id, custom_fields) VALUES
('Patient ID', 'Unique identifier for each patient', 'Unique identifier generated by the healthcare system', '1234567890', 'Integer', TRUE, 1, '{"pii": true}'),
('Medical History', 'Detailed information about patient's medical history', 'Asthma, Diabetes, Hypertension', 'Text', FALSE, 1, '{"pii": true}'),
('Transaction ID', 'Unique identifier for each sales transaction', '1234567890', 'Integer', TRUE, 2, '{"gdpr_compliant": true}'),
('Product ID', 'Unique identifier for each product', '1234567890', 'Integer', TRUE, 3, '{"publicly_available": true}'),
('Temperature', 'Temperature reading from sensor', '20.5', 'Float', TRUE, 4, '{"technical": true}'),
('Student ID', 'Unique identifier for each student', '1234567890', 'Integer', TRUE, 5, '{"pii": true}'),
('Grade', 'Letter grade for each course', 'A, B, C, D, F', 'Text', FALSE, 5, '{"academic": true}');

-- Insert data into tag table
INSERT INTO tag (name) VALUES
('Healthcare', 'Finance', 'Retail', 'Manufacturing', 'Education', 'PII', 'GDPR-Compliant', 'Public', 'Technical', 'Academic');

-- Insert data into entity_tag table
INSERT INTO entity_tag (tag_id, entity_type, entity_id) VALUES
(1, 'business_domain', 1),
(2, 'business_domain', 2),
(3, 'business_domain', 3),
(4, 'business_domain', 4),
(5, 'business_domain', 5),
(6, 'dataset', 1),
(7, 'dataset', 2),
(8, 'dataset', 3),
(9, 'dataset', 4),
(10, 'dataset', 5),
(11, 'data_asset', 1),
(12, 'data_asset', 2),
(13, 'data_asset', 3),
(14, 'data_asset', 4),
(15, 'data_asset', 5),
(16, 'column', 1),
(17, 'column', 2),
(18, 'column', 3),
(19, 'column', 4),
(20, 'column', 5),
(21, 'column', 6);
