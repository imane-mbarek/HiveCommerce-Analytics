-- Comparison of File Formats: CSV vs ORC vs Parquet
-- Binôme 1 - Personne 2

-- 1. Create Source Table (CSV/Text)
CREATE TABLE IF NOT EXISTS sales_csv (
    id INT,
    product STRING,
    amount DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- 2. Create ORC Table
CREATE TABLE IF NOT EXISTS sales_orc (
    id INT,
    product STRING,
    amount DOUBLE
)
STORED AS ORC;

-- 3. Create Parquet Table
CREATE TABLE IF NOT EXISTS sales_parquet (
    id INT,
    product STRING,
    amount DOUBLE
)
STORED AS PARQUET;

-- 4. Load data from CSV to ORC and Parquet
INSERT OVERWRITE TABLE sales_orc SELECT * FROM sales_csv;
INSERT OVERWRITE TABLE sales_parquet SELECT * FROM sales_csv;

-- 5. Performance Check (Metadata)
DESCRIBE FORMATTED sales_orc;
DESCRIBE FORMATTED sales_parquet;
