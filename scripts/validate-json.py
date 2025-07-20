#!/usr/bin/env python3
"""
🔍 JSON Validator for Langflow Workflows
Checks JSON syntax and workflow structure correctness.
"""

import json
import os
import sys
import argparse
from pathlib import Path


def validate_json_syntax(filepath):
    """Checks basic JSON syntax"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return True, data, None
    except json.JSONDecodeError as e:
        return False, None, f"JSON Syntax Error: {e}"
    except Exception as e:
        return False, None, f"File Error: {e}"


def validate_langflow_structure(data, filepath):
    """Checks Langflow workflow structure"""
    warnings = []
    errors = []

    # Check basic structure
    if not isinstance(data, dict):
        errors.append("Root element must be a dictionary")
        return errors, warnings

    # Check required fields
    required_fields = ["data", "name", "description"]
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    # Check data structure
    if "data" in data:
        data_section = data["data"]
        if not isinstance(data_section, dict):
            errors.append("'data' field must be a dictionary")
        else:
            # Check nodes
            if "nodes" not in data_section:
                errors.append("Missing 'nodes' in data section")
            elif not isinstance(data_section["nodes"], list):
                errors.append("'nodes' must be a list")
            else:
                nodes = data_section["nodes"]
                if len(nodes) == 0:
                    warnings.append("No nodes found in workflow")

                # Check each node
                for i, node in enumerate(nodes):
                    if not isinstance(node, dict):
                        errors.append(f"Node {i} is not a dictionary")
                        continue

                    node_required = ["id", "type", "position", "data"]
                    for req_field in node_required:
                        if req_field not in node:
                            errors.append(
                                f"Node {i} missing required field: {req_field}"
                            )

            # Check edges
            if "edges" not in data_section:
                errors.append("Missing 'edges' in data section")
            elif not isinstance(data_section["edges"], list):
                errors.append("'edges' must be a list")
            else:
                edges = data_section["edges"]

                # Check each connection
                for i, edge in enumerate(edges):
                    if not isinstance(edge, dict):
                        errors.append(f"Edge {i} is not a dictionary")
                        continue

                    edge_required = ["source", "target", "sourceHandle", "targetHandle"]
                    for req_field in edge_required:
                        if req_field not in edge:
                            errors.append(
                                f"Edge {i} missing required field: {req_field}"
                            )

                    # Check if handles have correct format
                    for handle_field in ["sourceHandle", "targetHandle"]:
                        if handle_field in edge:
                            handle = edge[handle_field]
                            INVALID_UNICODE_SEQUENCE = "id∶"  # Define invalid sequence
                            # Check for invalid Unicode sequence in handle
                            if isinstance(handle, str) and INVALID_UNICODE_SEQUENCE in handle:
                                errors.append(
                                   f"Edge {i} {handle_field} contains invalid Unicode characters ({INVALID_UNICODE_SEQUENCE})"
                               )

    # Check metadata
    if "name" in data and not data["name"].strip():
        warnings.append("Workflow name is empty")

    if "description" in data and not data["description"].strip():
        warnings.append("Workflow description is empty")

    return errors, warnings


def validate_file(filepath):
    """Validates a single file"""
    print(f"🔍 Checking: {filepath}")

    # Check JSON syntax
    is_valid, data, error = validate_json_syntax(filepath)
    if not is_valid:
        print(f"❌ {filepath}: {error}")
        return False

    # Check Langflow structure
    errors, warnings = validate_langflow_structure(data, filepath)

    # Display results
    if errors:
        print(f"❌ {filepath}: Structure errors")
        for error in errors:
            print(f"   • {error}")
        return False

    if warnings:
        print(f"⚠️  {filepath}: Warnings")
        for warning in warnings:
            print(f"   • {warning}")

    # Statistics
    if data and "data" in data:
        nodes_count = len(data["data"].get("nodes", []))
        edges_count = len(data["data"].get("edges", []))
        print(f"✅ {filepath}: OK - {nodes_count} nodes, {edges_count} connections")
    else:
        print(f"✅ {filepath}: OK")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="JSON validator for Langflow workflows"
    )
    parser.add_argument(
        "files", nargs="*", help="Files to check (default: examples/*.json)"
    )
    parser.add_argument(
        "--strict", action="store_true", help="Treat warnings as errors"
    )

    args = parser.parse_args()

    # Determine files to check
    if args.files:
        files_to_check = args.files
    else:
        # By default check all JSON in examples/
        examples_dir = Path("examples")
        if examples_dir.exists():
            files_to_check = list(examples_dir.glob("*.json"))
        else:
            print("❌ Directory 'examples' does not exist")
            return 1

    if not files_to_check:
        print("❌ No files found to check")
        return 1

    print("🔍 JSON Validator for Langflow Workflows")
    print(f"📂 Checking {len(files_to_check)} files...\n")

    all_valid = True
    valid_files = 0

    for filepath in files_to_check:
        is_valid = validate_file(filepath)
        if is_valid:
            valid_files += 1
        else:
            all_valid = False
        print()  # Empty line between files

    # Summary
    print("=" * 50)
    print(f"📊 Results: {valid_files}/{len(files_to_check)} files valid")

    if all_valid:
        print("🎉 All files are correct!")
        return 0
    else:
        print("❌ Some files need fixes")
        return 1


if __name__ == "__main__":
    sys.exit(main())
