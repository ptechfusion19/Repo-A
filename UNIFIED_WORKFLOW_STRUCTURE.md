# Unified Workflow Structure - Visual Guide

## Workflow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    UNIFIED SYNC WORKFLOW                        │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ GitHub       │  │ GitHub       │  │ GitHub       │
│ Trigger 1    │  │ Trigger 2    │  │ Trigger 3    │
│ Repo-A       │  │ Repo-B       │  │ Org_Testing  │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ GitHub       │  │ GitHub       │  │ GitHub       │
│ Trigger 4    │  │ Trigger 5    │  │ Trigger 6    │
│ Per_Testing  │  │ Repo1        │  │ Repo2        │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
                  ┌──────▼──────┐
                  │   Merge     │
                  │   Node      │
                  └──────┬──────┘
                         │
                  ┌──────▼──────┐
                  │     If      │
                  │ Check Branch│
                  │ & Sync Msg  │
                  └──────┬──────┘
                         │
                  ┌──────▼──────┐
                  │ Set Fields  │
                  │ Extract Info│
                  └──────┬──────┘
                         │
                  ┌──────▼──────┐
                  │   Switch    │
                  │  Router     │
                  └──────┬──────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
   │ Route 1 │      │ Route 2 │      │ Route 3 │
   │ A→B     │      │ B→A     │      │ Org→Per │
   └────┬────┘      └────┬────┘      └────┬────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
   │ Route 4 │      │ Route 5 │      │ Route 6 │
   │ Per→Org │      │ Repo1→2 │     │ Repo2→1 │
   └────┬────┘      └────┬────┘      └────┬────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                  ┌──────▼──────┐
                  │  SHARED     │
                  │  SYNC LOGIC │
                  └──────┬──────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
   │ Get SHA │      │ Create  │      │ Get     │
   │         │      │ Branch  │      │ Commit  │
   └────┬────┘      └────┬────┘      └────┬────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                  ┌──────▼──────┐
                  │ Split Files │
                  │ Process Each│
                  └──────┬──────┘
                         │
                  ┌──────▼──────┐
                  │ Update/     │
                  │ Create File │
                  └──────┬──────┘
                         │
                  ┌──────▼──────┐
                  │ Aggregate   │
                  └──────┬──────┘
                         │
                  ┌──────▼──────┐
                  │ Create PR   │
                  └─────────────┘
```

## Key Nodes Configuration

### 1. Merge Node (After All Triggers)
- **Type**: Merge
- **Mode**: Merge All Items
- **Purpose**: Combine outputs from all 6 triggers

### 2. Initial If Node (Filter)
```javascript
Conditions:
1. Branch Check:
   - Left: {{ $json.body.ref }}
   - Operator: equals
   - Right: refs/heads/main

2. Not Sync Message:
   - Left: {{ $json.body.head_commit.message }}
   - Operator: notContains
   - Right: "Sync from Repo"
```

### 3. Set Fields Node (Extract Repository Info)
```javascript
Assignments:
- sourceOwner: {{ $json.body.repository.owner.login }}
- sourceRepo: {{ $json.body.repository.name }}
- branchName: sync-from-{{ $json.body.repository.name }}-{{ $now.toMillis() }}
- commitMessage: {{ $json.body.head_commit.message }}
- commitSha: {{ $json.body.after }}
- authorName: {{ $json.body.head_commit.author.name }}
```

### 4. Switch Node (Router)
**Output 1: Repo-A → Repo-B**
```javascript
Condition:
{{ $json.body.repository.owner.login }} === "ptechfusion19" 
AND 
{{ $json.body.repository.name }} === "Repo-A"

Set:
- targetOwner: "ptechfusion19"
- targetRepo: "Repo-B"
```

**Output 2: Repo-B → Repo-A**
```javascript
Condition:
{{ $json.body.repository.owner.login }} === "ptechfusion19" 
AND 
{{ $json.body.repository.name }} === "Repo-B"

Set:
- targetOwner: "ptechfusion19"
- targetRepo: "Repo-A"
```

**Output 3: Org_Testing_Repo → Per_Testing_Repo**
```javascript
Condition:
{{ $json.body.repository.owner.login }} === "ptechfusion19" 
AND 
{{ $json.body.repository.name }} === "Org_Testing_Repo"

Set:
- targetOwner: "Ramzanx0553"
- targetRepo: "Per_Testing_Repo"
```

**Output 4: Per_Testing_Repo → Org_Testing_Repo**
```javascript
Condition:
{{ $json.body.repository.owner.login }} === "Ramzanx0553" 
AND 
{{ $json.body.repository.name }} === "Per_Testing_Repo"

Set:
- targetOwner: "ptechfusion19"
- targetRepo: "Org_Testing_Repo"
```

**Output 5: Repo1 → Repo2**
```javascript
Condition:
{{ $json.body.repository.owner.login }} === "wajeehaafi-alt" 
AND 
{{ $json.body.repository.name }} === "Repo1"

Set:
- targetOwner: "Ramzanx0553"
- targetRepo: "Repo2"
```

**Output 6: Repo2 → Repo1**
```javascript
Condition:
{{ $json.body.repository.owner.login }} === "Ramzanx0553" 
AND 
{{ $json.body.repository.name }} === "Repo2"

Set:
- targetOwner: "wajeehaafi-alt"
- targetRepo: "Repo1"
```

## Simplified Implementation Steps

### Quick Start Guide

1. **Create New Workflow** in n8n
2. **Add 6 GitHub Triggers**:
   - Configure each with respective repository
   - All should listen to "push" events
3. **Add Merge Node**:
   - Connect all triggers to Merge node
   - Mode: "Merge All Items"
4. **Add If Node** (Filter):
   - Check for main branch
   - Check for sync message exclusion
5. **Add Set Node**:
   - Extract source repository info
   - Generate branch name
6. **Add Switch Node**:
   - Configure 6 outputs with conditions
   - Set target repository for each
7. **Add Common Sync Logic**:
   - Copy from existing workflow
   - Replace hardcoded URLs with variables
8. **Test Each Route**:
   - Make test commits to each repository
   - Verify correct routing and sync

## Variable Reference

Use these expressions throughout the workflow:

```javascript
// Source Repository
{{ $('Set Fields').item.json.sourceOwner }}
{{ $('Set Fields').item.json.sourceRepo }}

// Target Repository
{{ $('Set Fields').item.json.targetOwner }}
{{ $('Set Fields').item.json.targetRepo }}

// Branch Info
{{ $('Set Fields').item.json.branchName }}

// Commit Info
{{ $('Set Fields').item.json.commitMessage }}
{{ $('Set Fields').item.json.commitSha }}
{{ $('Set Fields').item.json.authorName }}
```

## URL Templates

Replace all hardcoded URLs with these templates:

```javascript
// Get SHA
https://api.github.com/repos/{{ $('Set Fields').item.json.targetOwner }}/{{ $('Set Fields').item.json.targetRepo }}/git/refs/heads/main

// Create Branch
https://api.github.com/repos/{{ $('Set Fields').item.json.targetOwner }}/{{ $('Set Fields').item.json.targetRepo }}/git/refs

// Get Commit Details
https://api.github.com/repos/{{ $('Set Fields').item.json.sourceOwner }}/{{ $('Set Fields').item.json.sourceRepo }}/commits/{{ $('Set Fields').item.json.commitSha }}

// Get File Content
https://api.github.com/repos/{{ $('Set Fields').item.json.sourceOwner }}/{{ $('Set Fields').item.json.sourceRepo }}/contents/{{ encodeURIComponent($json.filename) }}?ref=main

// Check If File Exists
https://api.github.com/repos/{{ $('Set Fields').item.json.targetOwner }}/{{ $('Set Fields').item.json.targetRepo }}/contents/{{ encodeURIComponent($json.path) }}?ref={{ $('Set Fields').item.json.branchName }}

// Update/Create File
https://api.github.com/repos/{{ $('Set Fields').item.json.targetOwner }}/{{ $('Set Fields').item.json.targetRepo }}/contents/{{ encodeURIComponent($('Get File Content').item.json.path) }}

// Create PR
https://api.github.com/repos/{{ $('Set Fields').item.json.targetOwner }}/{{ $('Set Fields').item.json.targetRepo }}/pulls
```

