# User Guide - GitHub Repository Sync Automation

## Overview

This system automates bi-directional synchronization between GitHub repositories, ensuring that changes in one repository are automatically reflected in another.

## Getting Started

### Prerequisites

- n8n instance (self-hosted or cloud)
- GitHub Personal Access Tokens
- Access to source and target repositories
- Proper repository permissions

### Initial Setup

1. **Import Workflow**
   - Open n8n workflow editor
   - Import `WORKFLOW_FIXED_COMPLETE.json`
   - Verify all nodes are connected correctly

2. **Configure Credentials**
   - Set up GitHub credentials in n8n
   - Use Account 4 for Ramzanx0553 repositories
   - Use Account 5 for wajeehaafi-alt repositories

3. **Test Configuration**
   - Create a test file in source repository
   - Commit and push to trigger workflow
   - Verify PR is created in target repository

## How It Works

### Workflow Process

1. **Trigger**: GitHub webhook detects push event
2. **Extract**: Commit details and file list are extracted
3. **Process**: Each file is processed sequentially
4. **Sync**: Files are created/updated in target repository
5. **Create PR**: Pull request is created with all changes

### Supported Routes

- Repo-A ↔ Repo-B
- Org_Testing ↔ Per_Testing
- Repo1 ↔ Repo2

## Features

### Multiple File Support
- Handles multiple files per commit
- Processes files sequentially to avoid conflicts
- Creates single PR with all files

### Error Handling
- Checks for existing PRs before creation
- Handles duplicate PR errors gracefully
- Retries failed operations automatically

### Branch Management
- Creates unique branches for each sync
- Uses branch naming: `sync-from-{source}-{timestamp}`
- Merges to `main` branch in target repository

## Common Tasks

### Syncing Files

1. Make changes in source repository
2. Commit changes with descriptive message
3. Push to trigger automatic sync
4. Review PR in target repository
5. Merge PR to complete sync

### Troubleshooting

**Issue**: PR not created
- Check n8n execution logs
- Verify webhook is configured
- Ensure credentials are correct

**Issue**: Only one file in PR
- Verify all files are committed together
- Check Aggregate node configuration
- Ensure `keepOnlySet: false` is set

**Issue**: Validation Failed error
- Check Accept header is set correctly
- Verify credentials match repository owner
- Ensure branch name is unique

## Best Practices

1. **Commit Messages**: Use descriptive commit messages
2. **File Size**: Keep files under 50MB
3. **Frequency**: Avoid rapid successive commits
4. **Review**: Always review PRs before merging
5. **Monitoring**: Check n8n logs regularly

## Advanced Configuration

### Custom Branch Names
Modify branch naming in "Set Source Fields" node:
```
sync-from-{{ $json.sourceRepo }}-{{ $now.toMillis() }}
```

### File Filtering
Add filters to exclude certain files:
- Log files (*.log)
- Temporary files (*.tmp)
- Environment files (.env)

### Rate Limiting
Configure rate limits in GitHub API settings:
- Default: 5000 requests/hour
- Adjust based on usage

## Support

For issues or questions:
- Check n8n execution logs
- Review GitHub API documentation
- Consult workflow JSON structure

## Version History

- **v6.0.0**: Added duplicate PR error handling
- **v5.0.0**: Multiple file support
- **v4.0.0**: Sequential processing
- **v3.0.0**: Initial release

