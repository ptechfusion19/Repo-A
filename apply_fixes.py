#!/usr/bin/env python3
"""
Apply fixes to n8n workflow JSON to handle multiple files per commit.

This script fixes:
1. All "If File Exists" nodes to check statusCode === 200 instead of sha existence
2. Aggregate nodes to properly collect all items
3. Update Existing File nodes to use correct sha reference
"""

import json
import sys
import re

def fix_if_file_exists_nodes(workflow):
    """Fix all If File Exists nodes to check statusCode instead of sha"""
    nodes = workflow.get("nodes", [])
    fixed_count = 0
    
    for node in nodes:
        if node.get("type") == "n8n-nodes-base.if":
            node_name = node.get("name", "")
            if "If File Exists" in node_name:
                params = node.get("parameters", {})
                conditions = params.get("conditions", {})
                if conditions:
                    condition_list = conditions.get("conditions", [])
                    for condition in condition_list:
                        if condition.get("id") == "file-exists":
                            # Check if it needs fixing
                            if condition.get("leftValue") == "={{ $json.sha }}":
                                # Fix: Change from checking sha existence to checking statusCode === 200
                                condition["leftValue"] = "={{ $json.statusCode }}"
                                condition["rightValue"] = "200"
                                condition["operator"] = {
                                    "type": "number",
                                    "operation": "equals"
                                }
                                fixed_count += 1
                                print(f"Fixed: {node_name}")
    
    print(f"Fixed {fixed_count} 'If File Exists' nodes")
    return workflow

def fix_aggregate_nodes(workflow):
    """Ensure Aggregate nodes are properly configured"""
    nodes = workflow.get("nodes", [])
    fixed_count = 0
    
    for node in nodes:
        if node.get("type") == "n8n-nodes-base.aggregate":
            params = node.get("parameters", {})
            if "options" not in params:
                params["options"] = {}
            if params["options"].get("keepOnlySet") is None:
                params["options"]["keepOnlySet"] = False
                fixed_count += 1
                print(f"Fixed Aggregate node: {node.get('name', 'Unknown')}")
    
    print(f"Fixed {fixed_count} Aggregate nodes")
    return workflow

def fix_update_file_nodes(workflow):
    """Fix Update Existing File nodes to use correct sha reference"""
    nodes = workflow.get("nodes", [])
    fixed_count = 0
    
    # Create a map of node names to their IDs for reference
    node_map = {node.get("id"): node.get("name", "") for node in nodes}
    
    for node in nodes:
        if node.get("type") == "n8n-nodes-base.httpRequest":
            node_name = node.get("name", "")
            if "Update Existing File" in node_name:
                params = node.get("parameters", {})
                body_params = params.get("bodyParameters", {}).get("parameters", [])
                for param in body_params:
                    if param.get("name") == "sha":
                        current_value = param.get("value", "")
                        # Check if it references the wrong node or needs fixing
                        # The sha should come from "Check If File Exists" node
                        check_node_name = node_name.replace("Update Existing File", "Check If File Exists")
                        # Remove number suffix if present for matching
                        check_node_base = re.sub(r'\d+$', '', check_node_name)
                        
                        # Try to find the corresponding Check If File Exists node
                        for other_node in nodes:
                            other_name = other_node.get("name", "")
                            if "Check If File Exists" in other_name:
                                # Match by route number or position
                                if (check_node_base in other_name or 
                                    (node_name.endswith("File") and other_name.endswith("Exists")) or
                                    (not any(c.isdigit() for c in node_name[-5:]) and not any(c.isdigit() for c in other_name[-5:]))):
                                    param["value"] = f"={{ $('{other_name}').item.json.sha }}"
                                    fixed_count += 1
                                    print(f"Fixed sha reference in: {node_name}")
                                    break
    
    print(f"Fixed {fixed_count} Update Existing File nodes")
    return workflow

def main():
    if len(sys.argv) < 2:
        print("Usage: python apply_fixes.py <input_workflow.json> [output_workflow.json]")
        print("\nThis script fixes the workflow to handle multiple files per commit:")
        print("1. Fixes 'If File Exists' nodes to check statusCode === 200")
        print("2. Configures Aggregate nodes to collect all items")
        print("3. Fixes Update Existing File nodes to use correct sha reference")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace(".json", "_fixed.json")
    
    print(f"Reading workflow from: {input_file}")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            workflow = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file: {e}")
        sys.exit(1)
    
    print("\nApplying fixes...")
    print("-" * 50)
    
    # Apply all fixes
    workflow = fix_if_file_exists_nodes(workflow)
    workflow = fix_aggregate_nodes(workflow)
    workflow = fix_update_file_nodes(workflow)
    
    print("-" * 50)
    print(f"\nWriting fixed workflow to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)
    
    print("Done! The workflow has been fixed to handle multiple files per commit.")
    print("\nKey changes:")
    print("✓ All 'If File Exists' nodes now check statusCode === 200")
    print("✓ Aggregate nodes configured to collect all file operations")
    print("✓ Update Existing File nodes use correct sha references")

if __name__ == "__main__":
    main()

