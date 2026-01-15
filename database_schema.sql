-- Database Schema for Sync Automation System
-- PostgreSQL schema definitions

-- Workflow executions table
CREATE TABLE IF NOT EXISTS workflow_executions (
    id SERIAL PRIMARY KEY,
    execution_id VARCHAR(255) UNIQUE NOT NULL,
    workflow_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    source_repo VARCHAR(255),
    target_repo VARCHAR(255),
    files_count INTEGER DEFAULT 0,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- File syncs table
CREATE TABLE IF NOT EXISTS file_syncs (
    id SERIAL PRIMARY KEY,
    execution_id VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    operation_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    source_sha VARCHAR(255),
    target_sha VARCHAR(255),
    file_size_bytes BIGINT,
    processing_time_ms INTEGER,
    error_message TEXT,
    synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (execution_id) REFERENCES workflow_executions(execution_id)
);

-- Pull requests table
CREATE TABLE IF NOT EXISTS pull_requests (
    id SERIAL PRIMARY KEY,
    pr_number INTEGER,
    repository VARCHAR(255) NOT NULL,
    branch_name VARCHAR(255) NOT NULL,
    title VARCHAR(500),
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    merged_at TIMESTAMP,
    closed_at TIMESTAMP,
    files_count INTEGER DEFAULT 0,
    execution_id VARCHAR(255),
    FOREIGN KEY (execution_id) REFERENCES workflow_executions(execution_id)
);

-- API requests log table
CREATE TABLE IF NOT EXISTS api_requests (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(500) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INTEGER,
    response_time_ms INTEGER,
    request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    error_message TEXT
);

-- Repository configurations table
CREATE TABLE IF NOT EXISTS repository_configs (
    id SERIAL PRIMARY KEY,
    source_owner VARCHAR(255) NOT NULL,
    source_repo VARCHAR(255) NOT NULL,
    target_owner VARCHAR(255) NOT NULL,
    target_repo VARCHAR(255) NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    sync_direction VARCHAR(50) DEFAULT 'bidirectional',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_owner, source_repo, target_owner, target_repo)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_workflow_executions_status ON workflow_executions(status);
CREATE INDEX IF NOT EXISTS idx_workflow_executions_started_at ON workflow_executions(started_at);
CREATE INDEX IF NOT EXISTS idx_file_syncs_execution_id ON file_syncs(execution_id);
CREATE INDEX IF NOT EXISTS idx_file_syncs_status ON file_syncs(status);
CREATE INDEX IF NOT EXISTS idx_pull_requests_repository ON pull_requests(repository);
CREATE INDEX IF NOT EXISTS idx_pull_requests_status ON pull_requests(status);
CREATE INDEX IF NOT EXISTS idx_api_requests_request_time ON api_requests(request_time);

-- Views for common queries
CREATE OR REPLACE VIEW sync_statistics AS
SELECT 
    DATE_TRUNC('day', started_at) as date,
    COUNT(*) as total_executions,
    COUNT(CASE WHEN status = 'success' THEN 1 END) as successful_executions,
    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_executions,
    AVG(files_count) as avg_files_per_execution,
    SUM(files_count) as total_files_synced
FROM workflow_executions
GROUP BY DATE_TRUNC('day', started_at);

CREATE OR REPLACE VIEW repository_sync_summary AS
SELECT 
    source_repo,
    target_repo,
    COUNT(*) as total_syncs,
    COUNT(CASE WHEN status = 'success' THEN 1 END) as successful_syncs,
    AVG(files_count) as avg_files,
    MAX(started_at) as last_sync
FROM workflow_executions
WHERE source_repo IS NOT NULL AND target_repo IS NOT NULL
GROUP BY source_repo, target_repo;

