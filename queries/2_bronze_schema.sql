CREATE SCHEMA IF NOT EXISTS bronze;

CREATE OR REPLACE TABLE bronze.raw_customers AS 
SELECT * 
FROM read_csv_auto('https://raw.githubusercontent.com/araj2/customer-database/master/Ecommerce%20Customers.csv', header=True);

CREATE OR REPLACE TABLE bronze.raw_subscriptions AS
SELECT *
FROM read_csv_auto('https://raw.githubusercontent.com/albayraktaroglu/Datasets/master/churn.csv', header=True);