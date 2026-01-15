#!/bin/bash
# System Monitoring Script
# Monitors system health and performance metrics

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "System Health Monitoring"
echo "=========================================="
echo ""

# Check n8n service status
check_n8n() {
    echo -n "Checking n8n service... "
    if curl -s -f http://localhost:5678/healthz > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Running${NC}"
    else
        echo -e "${RED}✗ Not responding${NC}"
        return 1
    fi
}

# Check database connection
check_database() {
    echo -n "Checking database connection... "
    if pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Connected${NC}"
    else
        echo -e "${RED}✗ Connection failed${NC}"
        return 1
    fi
}

# Check disk space
check_disk_space() {
    echo -n "Checking disk space... "
    USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$USAGE" -lt 80 ]; then
        echo -e "${GREEN}✓ ${USAGE}% used${NC}"
    elif [ "$USAGE" -lt 90 ]; then
        echo -e "${YELLOW}⚠ ${USAGE}% used${NC}"
    else
        echo -e "${RED}✗ ${USAGE}% used (Critical)${NC}"
        return 1
    fi
}

# Check memory usage
check_memory() {
    echo -n "Checking memory usage... "
    MEMORY=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
    if [ "$MEMORY" -lt 80 ]; then
        echo -e "${GREEN}✓ ${MEMORY}% used${NC}"
    elif [ "$MEMORY" -lt 90 ]; then
        echo -e "${YELLOW}⚠ ${MEMORY}% used${NC}"
    else
        echo -e "${RED}✗ ${MEMORY}% used (Critical)${NC}"
        return 1
    fi
}

# Check CPU load
check_cpu() {
    echo -n "Checking CPU load... "
    LOAD=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
    CORES=$(nproc)
    THRESHOLD=$(echo "$CORES * 0.8" | bc)
    
    if (( $(echo "$LOAD < $THRESHOLD" | bc -l) )); then
        echo -e "${GREEN}✓ Load: ${LOAD}${NC}"
    else
        echo -e "${YELLOW}⚠ Load: ${LOAD}${NC}"
    fi
}

# Check recent workflow executions
check_workflows() {
    echo -n "Checking recent workflow executions... "
    RECENT=$(find /var/log/n8n -name "*.log" -mtime -1 2>/dev/null | wc -l)
    if [ "$RECENT" -gt 0 ]; then
        echo -e "${GREEN}✓ ${RECENT} log files in last 24h${NC}"
    else
        echo -e "${YELLOW}⚠ No recent activity${NC}"
    fi
}

# Main execution
main() {
    check_n8n
    check_database
    check_disk_space
    check_memory
    check_cpu
    check_workflows
    
    echo ""
    echo "=========================================="
    echo "Monitoring complete"
    echo "=========================================="
}

main

