-- Comparison of Managed and External Tables
-- Binôme 1 - Personne 2

-- 1. Create a Managed Table
CREATE TABLE IF NOT EXISTS managed_sales (
    id INT,
    product STRING,
    amount DOUBLE
)
STORED AS TEXTFILE;

INSERT INTO managed_sales VALUES (1, 'Laptop', 1200.00), (2, 'Phone', 800.00);

-- 2. Create an External Table
-- First, ensure a directory exists in HDFS (simulation through location)
CREATE EXTERNAL TABLE IF NOT EXISTS external_sales (
    id INT,
    product STRING,
    amount DOUBLE
)
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/external_sales_data';

INSERT INTO external_sales VALUES (3, 'Monitor', 300.00), (4, 'Keyboard', 50.00);

-- Verification
SHOW TABLES;
DESCRIBE FORMATTED managed_sales;
DESCRIBE FORMATTED external_sales;

-- To test behavior after DROP:
-- DROP TABLE managed_sales; -- Data in /user/hive/warehouse/managed_sales will be deleted.
-- DROP TABLE external_sales; -- Only metadata is deleted; data in /user/hive/warehouse/external_sales_data remains.
