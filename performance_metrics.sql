-- Performance Metrics and Analytics Queries
-- Useful for monitoring system performance and identifying bottlenecks

-- Average sync duration by repository pair
SELECT 
    source_repo,
    target_repo,
    COUNT(*) as total_syncs,
    AVG(EXTRACT(EPOCH FROM (completed_at - started_at))) as avg_duration_seconds,
    MIN(EXTRACT(EPOCH FROM (completed_at - started_at))) as min_duration_seconds,
    MAX(EXTRACT(EPOCH FROM (completed_at - started_at))) as max_duration_seconds,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (completed_at - started_at))) as median_duration_seconds
FROM sync_executions
WHERE started_at > NOW() - INTERVAL '30 days'
    AND status = 'completed'
GROUP BY source_repo, target_repo
ORDER BY avg_duration_seconds DESC;

-- File processing performance
SELECT 
    DATE_TRUNC('hour', processed_at) as hour,
    COUNT(*) as files_processed,
    AVG(file_size_bytes) as avg_file_size,
    AVG(processing_time_ms) as avg_processing_time_ms,
    SUM(file_size_bytes) as total_size_bytes
FROM file_operations
WHERE processed_at > NOW() - INTERVAL '7 days'
GROUP BY DATE_TRUNC('hour', processed_at)
ORDER BY hour DESC;

-- Error rate by operation type
SELECT 
    operation_type,
    COUNT(*) as total_operations,
    COUNT(CASE WHEN status = 'success' THEN 1 END) as success_count,
    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_count,
    ROUND(100.0 * COUNT(CASE WHEN status = 'failed' THEN 1 END) / COUNT(*), 2) as error_rate_percent,
    AVG(CASE WHEN status = 'failed' THEN retry_count ELSE NULL END) as avg_retries_on_failure
FROM operations
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY operation_type
ORDER BY error_rate_percent DESC;

-- Peak usage times
SELECT 
    EXTRACT(HOUR FROM started_at) as hour_of_day,
    COUNT(*) as sync_count,
    AVG(EXTRACT(EPOCH FROM (completed_at - started_at))) as avg_duration_seconds
FROM sync_executions
WHERE started_at > NOW() - INTERVAL '30 days'
GROUP BY EXTRACT(HOUR FROM started_at)
ORDER BY sync_count DESC;

-- Repository sync frequency analysis
SELECT 
    source_repo,
    target_repo,
    COUNT(*) as sync_count,
    COUNT(DISTINCT DATE(started_at)) as active_days,
    AVG(EXTRACT(EPOCH FROM (started_at - LAG(started_at) OVER (PARTITION BY source_repo, target_repo ORDER BY started_at)))) as avg_time_between_syncs_seconds
FROM sync_executions
WHERE started_at > NOW() - INTERVAL '30 days'
GROUP BY source_repo, target_repo
ORDER BY sync_count DESC;

-- API rate limit usage
SELECT 
    DATE_TRUNC('hour', request_time) as hour,
    COUNT(*) as api_requests,
    COUNT(DISTINCT endpoint) as unique_endpoints,
    AVG(response_time_ms) as avg_response_time_ms,
    COUNT(CASE WHEN status_code >= 400 THEN 1 END) as error_count
FROM api_requests
WHERE request_time > NOW() - INTERVAL '7 days'
GROUP BY DATE_TRUNC('hour', request_time)
ORDER BY hour DESC;

-- Most synced file types
SELECT 
    CASE 
        WHEN file_path LIKE '%.py' THEN 'Python'
        WHEN file_path LIKE '%.js' THEN 'JavaScript'
        WHEN file_path LIKE '%.html' THEN 'HTML'
        WHEN file_path LIKE '%.css' THEN 'CSS'
        WHEN file_path LIKE '%.cpp' THEN 'C++'
        WHEN file_path LIKE '%.md' THEN 'Markdown'
        WHEN file_path LIKE '%.json' THEN 'JSON'
        WHEN file_path LIKE '%.yaml' OR file_path LIKE '%.yml' THEN 'YAML'
        WHEN file_path LIKE '%.sql' THEN 'SQL'
        ELSE 'Other'
    END as file_type,
    COUNT(*) as sync_count,
    AVG(file_size_bytes) as avg_size_bytes,
    SUM(file_size_bytes) as total_size_bytes
FROM file_operations
WHERE processed_at > NOW() - INTERVAL '30 days'
GROUP BY file_type
ORDER BY sync_count DESC;

-- Workflow execution efficiency
SELECT 
    workflow_name,
    COUNT(*) as total_executions,
    COUNT(CASE WHEN status = 'success' THEN 1 END) as successful_executions,
    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_executions,
    AVG(EXTRACT(EPOCH FROM (ended_at - started_at))) as avg_execution_time_seconds,
    AVG(files_processed) as avg_files_per_execution
FROM workflow_executions
WHERE started_at > NOW() - INTERVAL '30 days'
GROUP BY workflow_name
ORDER BY total_executions DESC;

