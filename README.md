                                          ## Bi-Directional GitHub Repository Sync Automation
## Description
This project implements a comprehensive automation workflow in n8n that enables seamless two-way synchronization between GitHub repositories across different ownership types. 
The solution supports synchronization between personal and organizational repositories in all possible combinations.

## Supported Synchronization Flows
The automation supports the following bi-directional synchronization patterns:
1. Organization to Organization — Sync between two organizational repositories
2. Organization to Personal — Sync from organizational repository to personal repository
3. Personal to Organization — Sync from personal repository to organizational repository
4. Personal to Personal — Sync between two personal repositories
   
## Requirements
### Components
1. **GitHub API**: Create branches, push changes, and open PRs.
2. **Authentication**: Secure access to both repositories.

## Authentication Mechanisms
### Personal Access Tokens
Personal Access Tokens provide broader scopes and simpler setup for quick implementation.

#### Required Scopes
- `repo` — Full control of private repositories
- `admin:repo_hook` — Manage webhooks
- `workflow` — Update GitHub Actions workflows (if needed)

#### How to Generate
1. Go to GitHub → Settings → Developer Settings → Personal Access Tokens
2. Choose "Fine-grained tokens" (recommended) or "Tokens (classic)"
3. Set expiration and select required permissions
4. Copy and store securely in n8n credentials

### GitHub API Rate Limits
- **5,000 requests/hour** for authenticated requests

### Key API Endpoints
The following GitHub REST API endpoints are required for the automation workflow:
1. GET Create: GET/commit/repos/{owner}/{repo}/commits/{sha}
2. Create Branch: POST/repos/{owner}/{repo}/git/refs
3. Get File Content: GET/repos/{owner}/{repo}/contents/{path}
4. Update/Create File: PUT/repos/{owner}/{repo}/contents/{path}
5. Create PR: POST/repos/{owner}/{repo}/pulls

## Merging Multiple Workflows into One

If you have multiple separate workflows for different repository pairs, you can merge them into a single unified workflow for easier maintenance.

### Quick Start
See **[QUICK_START.md](QUICK_START.md)** for a 3-step summary of the merge process.

### Detailed Guides
- **[STEP_BY_STEP_IMPLEMENTATION.md](STEP_BY_STEP_IMPLEMENTATION.md)** - Complete step-by-step guide with all node configurations
- **[UNIFIED_WORKFLOW_STRUCTURE.md](UNIFIED_WORKFLOW_STRUCTURE.md)** - Visual architecture and workflow structure
- **[WORKFLOW_MERGE_GUIDE.md](WORKFLOW_MERGE_GUIDE.md)** - Conceptual overview and best practices

### Approach
The recommended approach uses a **Switch Router** pattern:
1. Multiple GitHub triggers (one per source repository)
2. Merge node to combine all triggers
3. Switch node to route based on repository owner/name
4. Shared sync logic with parameterized URLs

This reduces maintenance overhead and ensures consistent behavior across all repository pairs.