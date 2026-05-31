-- Inventory Demand Forecasting System - Database Schema
-- Target Database: MySQL (with SQLite compatibility in application layer)

CREATE DATABASE IF NOT EXISTS inventory_forecast_db;
USE inventory_forecast_db;

-- 1. Table for historical sales data
CREATE TABLE IF NOT EXISTS sales_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    store INT NOT NULL,
    dept INT NOT NULL,
    date DATE NOT NULL,
    weekly_sales DOUBLE NOT NULL,
    is_holiday INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_store_dept_date (store, dept, date)
);

-- Indexing for fast search and aggregation
CREATE INDEX idx_sales_store_dept ON sales_data(store, dept);
CREATE INDEX idx_sales_date ON sales_data(date);

-- 2. Table for forecast results
CREATE TABLE IF NOT EXISTS forecast_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    store INT NOT NULL,
    dept INT NOT NULL,
    forecast_date DATE NOT NULL,
    horizon_days INT NOT NULL, -- 7, 30, or 90
    forecast_value DOUBLE NOT NULL,
    lower_ci DOUBLE, -- Lower Confidence Interval
    upper_ci DOUBLE, -- Upper Confidence Interval
    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_forecast_store_dept ON forecast_results(store, dept);
CREATE INDEX idx_forecast_run ON forecast_results(run_timestamp);

-- 3. Table for recommendation history
CREATE TABLE IF NOT EXISTS recommendation_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    store INT NOT NULL,
    dept INT NOT NULL,
    current_stock INT NOT NULL,
    forecasted_demand INT NOT NULL,
    recommendation_type VARCHAR(50) NOT NULL, -- 'LOW_STOCK_REORDER', 'OVERSTOCK_LIQUIDATE', 'OK_OPTIMAL'
    recommended_quantity INT NOT NULL,
    estimated_cost DOUBLE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_rec_store_dept ON recommendation_history(store, dept);
CREATE INDEX idx_rec_timestamp ON recommendation_history(timestamp);

-- 4. Table for user activity logs (Audit Trail)
CREATE TABLE IF NOT EXISTS user_activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100) DEFAULT 'admin',
    action_performed VARCHAR(255) NOT NULL,
    page_visited VARCHAR(100) NOT NULL,
    details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_logs_timestamp ON user_activity_logs(timestamp);
