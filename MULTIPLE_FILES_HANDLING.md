# Multiple Files Handling in Unified Workflow

## ✅ How the Workflow Handles Multiple Files

The workflow **already handles multiple files** in a single commit. Here's how it works:

### Workflow Flow for Multiple Files

```
1. Get Commit Details
   ↓
   Returns: { files: [file1, file2, file3, ...] }
   
2. Split Out Files
   ↓
   Converts array into separate items:
   - Item 1: file1
   - Item 2: file2
   - Item 3: file3
   
3. Process Each File (in parallel)
   ↓
   For each file:
   - Check if deleted → Skip if deleted
   - Get file content from source
   - Check if exists in target
   - Update or Create file in target
   
4. Aggregate All Files
   ↓
   Waits for ALL files to complete
   Collects all results
   
5. Create PR
   ↓
   Creates ONE PR with all file changes
```

## Key Nodes for Multiple File Handling

### 1. Split Out Files Node
**Location:** After "Get Commit Details"
**Configuration:**
- Field to Split: `files`
- **What it does:** Takes the `files` array from commit details and creates one workflow item per file

**Example:**
```json
// Input (from Get Commit Details):
{
  "files": [
    { "filename": "file1.txt", "status": "modified" },
    { "filename": "file2.txt", "status": "added" },
    { "filename": "file3.txt", "status": "removed" }
  ]
}

// Output (after Split Out Files):
Item 1: { "filename": "file1.txt", "status": "modified" }
Item 2: { "filename": "file2.txt", "status": "added" }
Item 3: { "filename": "file3.txt", "status": "removed" }
```

### 2. If Not Deleted Node
**Location:** After "Split Out Files"
**Configuration:**
- Condition: `status` not equals `removed`
- **What it does:** Filters out deleted files (only processes modified/added files)

### 3. Process Each File
Each file goes through:
- **Get File Content** - Fetches content from source repository
- **Check If File Exists** - Checks if file exists in target repository
- **Update Existing File** OR **Create New File** - Updates or creates the file

### 4. Aggregate All Files Node
**Location:** After all file operations
**Configuration:**
- Mode: `aggregateAllItemData`
- **What it does:** 
  - Waits for ALL file operations to complete
  - Collects all results into a single item
  - Ensures PR is only created after all files are processed

### 5. Create PR Node
**Location:** After "Aggregate All Files"
**What it does:** Creates a single Pull Request containing all file changes

## Example Scenario

### Commit with 3 Files

**Commit Details:**
- `README.md` (modified)
- `src/app.js` (added)
- `old-file.txt` (removed)

**Workflow Execution:**

1. **Get Commit Details** → Returns commit with 3 files
2. **Split Out Files** → Creates 3 separate items
3. **If Not Deleted** → Filters out `old-file.txt` (removed)
4. **Process Remaining Files:**
   - Process `README.md` → Update in target repo
   - Process `src/app.js` → Create in target repo
5. **Aggregate All Files** → Waits for both files to complete
6. **Create PR** → Creates one PR with both file changes

**Result:** One PR with 2 files changed (README.md updated, src/app.js added)

## Verification

The workflow is correctly configured to handle multiple files:

✅ **Split Out Files** - Properly configured to split the `files` array
✅ **Parallel Processing** - Each file is processed independently
✅ **Aggregate Node** - Configured to wait for all files (`aggregateAllItemData`)
✅ **Single PR** - Creates one PR with all changes

## Testing Multiple Files

To test that multiple files work correctly:

1. **Create a commit with multiple files:**
   ```bash
   # In source repository
   echo "File 1" > file1.txt
   echo "File 2" > file2.txt
   echo "File 3" > file3.txt
   git add file1.txt file2.txt file3.txt
   git commit -m "Add multiple files"
   git push
   ```

2. **Check workflow execution:**
   - Open n8n execution log
   - Verify "Split Out Files" created 3 items
   - Verify all 3 files were processed
   - Verify one PR was created with all 3 files

3. **Verify in GitHub:**
   - Check the created PR
   - Should show all files in the "Files changed" tab
   - All files should be in the same PR

## Edge Cases Handled

### ✅ Single File Commit
- Works normally, processes one file

### ✅ Multiple Files Commit
- Splits files, processes each, aggregates, creates one PR

### ✅ Mixed File Types (added, modified, removed)
- Processes added/modified files
- Skips removed files (filtered by "If Not Deleted")

### ✅ Large Commits (10+ files)
- Handles any number of files
- Processes in parallel (n8n handles this automatically)
- Aggregates all results before creating PR

### ✅ Empty Commit (no files)
- "Split Out Files" creates no items
- Workflow stops (no files to process)
- No PR created (expected behavior)

## Performance Considerations

- **Parallel Processing:** n8n processes files in parallel automatically
- **Rate Limiting:** GitHub API rate limits apply (5,000 requests/hour)
- **Large Files:** Very large files may take longer to process
- **Many Files:** Commits with 100+ files will take longer but will complete

## Troubleshooting

### Issue: PR created before all files processed
**Solution:** Verify "Aggregate All Files" node is configured with `aggregateAllItemData`

### Issue: Some files missing from PR
**Solution:** 
- Check "If Not Deleted" filter isn't too restrictive
- Verify file paths are correct
- Check GitHub API responses for errors

### Issue: Workflow times out with many files
**Solution:**
- Increase n8n execution timeout
- Consider batching very large commits
- Check GitHub API rate limits

## Summary

✅ **The workflow correctly handles multiple files**
✅ **Each file is processed individually**
✅ **All files are aggregated before creating PR**
✅ **One PR is created with all file changes**

No changes needed - the workflow is already configured correctly!

