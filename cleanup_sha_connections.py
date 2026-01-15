#!/usr/bin/env python3
"""
Clean up remaining connections to removed "Get Latest Branch SHA" nodes.
These connections need to be updated to point directly to Create New File nodes.
"""

import json
import sys

def cleanup_connections(input_file: str, output_file: str):
    """Remove connections to deleted SHA nodes and fix If File Exists connections"""
    print(f"Reading workflow from {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        workflow = json.load(f)
    
    connections = workflow.get("connections", {})
    
    # Find all "If File Exists" nodes that connect to SHA nodes
    sha_node_names = [
        "Get Latest Branch SHA",
        "Get Latest Branch SHA1", 
        "Get Latest Branch SHA2",
        "Get Latest Branch SHA3",
        "Get Latest Branch SHA4",
        "Get Latest Branch SHA5"
    ]
    
    # Map SHA nodes to their corresponding Create New File nodes
    sha_to_create_mapping = {
        "Get Latest Branch SHA": "Create New File",
        "Get Latest Branch SHA1": "Create New File1",
        "Get Latest Branch SHA2": "Create New File2",
        "Get Latest Branch SHA3": "Create New File3",
        "Get Latest Branch SHA4": "Create New File4",
        "Get Latest Branch SHA5": "Create New File5",
    }
    
    # Find what each SHA node was connecting to (should be Create New File)
    sha_node_targets = {}
    for sha_name in sha_node_names:
        if sha_name in connections:
            sha_conn = connections[sha_name]
            if sha_conn.get("main") and sha_conn["main"][0]:
                target = sha_conn["main"][0][0].get("node")
                sha_node_targets[sha_name] = target
                print(f"  Found: {sha_name} -> {target}")
    
    # Update "If File Exists" nodes to connect directly to Create New File
    updated_count = 0
    for conn_name, conn_data in connections.items():
        if conn_name.startswith("If File Exists"):
            main_conn = conn_data.get("main", [])
            # Check the false branch (index 1) which goes to Create New File
            if len(main_conn) > 1:
                false_branch = main_conn[1]
                for link in false_branch:
                    if link.get("node") in sha_node_names:
                        # Replace with the Create New File node
                        create_node = sha_node_targets.get(link.get("node"))
                        if create_node:
                            link["node"] = create_node
                            updated_count += 1
                            print(f"  ✅ Updated {conn_name} -> {create_node}")
    
    # Remove SHA node connections
    removed_count = 0
    for sha_name in sha_node_names:
        if sha_name in connections:
            del connections[sha_name]
            removed_count += 1
            print(f"  ✅ Removed connection: {sha_name}")
    
    print(f"\nWriting cleaned workflow to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Cleanup complete!")
    print(f"  - Updated {updated_count} connections")
    print(f"  - Removed {removed_count} SHA node connections")

if __name__ == "__main__":
    input_file = "WORKFLOW_FIXED_COMPLETE.json"
    output_file = "WORKFLOW_FIXED_COMPLETE.json"
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    cleanup_connections(input_file, output_file)

