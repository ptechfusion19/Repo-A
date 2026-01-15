# Deployment Guide

## Quick Start Deployment

This guide covers deploying the GitHub Repository Sync Automation system using Docker and Kubernetes.

## Prerequisites

- Docker 20.10+ or Kubernetes 1.25+
- PostgreSQL 14+ (for production)
- GitHub Personal Access Tokens
- Domain name (for webhooks)

## Docker Deployment

### Step 1: Prepare Environment

Create a `.env` file:

```bash
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your_secure_password
N8N_HOST=0.0.0.0
N8N_PORT=5678
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=postgres
DB_POSTGRESDB_DATABASE=n8n
DB_POSTGRESDB_USER=n8n
DB_POSTGRESDB_PASSWORD=your_db_password
```

### Step 2: Run with Docker Compose

```bash
docker-compose up -d
```

### Step 3: Import Workflow

1. Access n8n at `http://localhost:5678`
2. Import `WORKFLOW_FIXED_COMPLETE.json`
3. Configure GitHub credentials
4. Activate workflow

## Kubernetes Deployment

### Step 1: Create Namespace

```bash
kubectl create namespace workflow-automation
```

### Step 2: Create Secrets

```bash
kubectl create secret generic n8n-secrets \
  --from-literal=db-user=n8n \
  --from-literal=db-password=your_password \
  --namespace=workflow-automation
```

### Step 3: Deploy PostgreSQL

```bash
kubectl apply -f postgres-deployment.yaml
```

### Step 4: Deploy n8n

```bash
kubectl apply -f infrastructure_setup.yaml
```

### Step 5: Configure Ingress

```bash
kubectl apply -f ingress.yaml
```

## Post-Deployment Configuration

### 1. Configure GitHub Webhooks

For each repository:
1. Go to Settings → Webhooks
2. Add webhook URL: `https://your-domain.com/webhook`
3. Set content type: `application/json`
4. Select events: `push`
5. Save webhook

### 2. Set Up Credentials

In n8n:
1. Go to Credentials
2. Add GitHub credentials:
   - **Account 4**: For Ramzanx0553 repositories
   - **Account 5**: For wajeehaafi-alt repositories

### 3. Import and Activate Workflow

1. Import `WORKFLOW_FIXED_COMPLETE.json`
2. Verify all nodes are connected
3. Test with a single file
4. Activate workflow

## Monitoring

### Health Checks

```bash
# Check n8n health
curl http://localhost:5678/healthz

# Check database
kubectl exec -it postgres-pod -- psql -U n8n -d n8n -c "SELECT 1"
```

### Logs

```bash
# Docker
docker logs n8n-container

# Kubernetes
kubectl logs -n workflow-automation deployment/n8n-workflow
```

## Scaling

### Horizontal Scaling

```bash
kubectl scale statefulset n8n-workflow --replicas=3 -n workflow-automation
```

### Resource Limits

Adjust in `infrastructure_setup.yaml`:
- CPU: 500m - 2000m
- Memory: 1Gi - 4Gi

## Backup and Restore

### Backup Workflow

```bash
python backup_restore_utility.py
```

### Restore Workflow

```bash
python backup_restore_utility.py --restore backup_file.tar.gz
```

## Troubleshooting

### Common Issues

1. **Webhook not triggering**
   - Check webhook URL is accessible
   - Verify webhook secret matches
   - Check n8n logs

2. **Database connection failed**
   - Verify PostgreSQL is running
   - Check credentials
   - Test connection manually

3. **High memory usage**
   - Increase memory limits
   - Reduce concurrent executions
   - Enable database persistence

## Security Considerations

1. Use HTTPS for webhooks
2. Rotate credentials regularly
3. Enable audit logging
4. Restrict network access
5. Use secrets management

## Maintenance

### Regular Tasks

- Weekly: Review logs and metrics
- Monthly: Rotate credentials
- Quarterly: Update dependencies
- Annually: Security audit

## Support

For deployment issues:
- Check logs: `kubectl logs -n workflow-automation`
- Review documentation
- Consult infrastructure team

