#!/usr/bin/env python3
"""
🔍 JSON Validator dla Langflow Workflows
Sprawdza poprawność składni JSON i struktury workflow.
"""

import json
import os
import sys
import argparse
from pathlib import Path


def validate_json_syntax(filepath):
    """Sprawdza podstawową składnię JSON"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return True, data, None
    except json.JSONDecodeError as e:
        return False, None, f"JSON Syntax Error: {e}"
    except Exception as e:
        return False, None, f"File Error: {e}"


def validate_langflow_structure(data, filepath):
    """Sprawdza strukturę workflow Langflow"""
    warnings = []
    errors = []

    # Sprawdź podstawową strukturę
    if not isinstance(data, dict):
        errors.append("Root element must be a dictionary")
        return errors, warnings

    # Sprawdź wymagane pola
    required_fields = ["data", "name", "description"]
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    # Sprawdź strukturę data
    if "data" in data:
        data_section = data["data"]
        if not isinstance(data_section, dict):
            errors.append("'data' field must be a dictionary")
        else:
            # Sprawdź nodes
            if "nodes" not in data_section:
                errors.append("Missing 'nodes' in data section")
            elif not isinstance(data_section["nodes"], list):
                errors.append("'nodes' must be a list")
            else:
                nodes = data_section["nodes"]
                if len(nodes) == 0:
                    warnings.append("No nodes found in workflow")

                # Sprawdź każdy node
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

            # Sprawdź edges
            if "edges" not in data_section:
                errors.append("Missing 'edges' in data section")
            elif not isinstance(data_section["edges"], list):
                errors.append("'edges' must be a list")
            else:
                edges = data_section["edges"]

                # Sprawdź każde połączenie
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

                    # Sprawdź czy handles mają poprawny format
                    for handle_field in ["sourceHandle", "targetHandle"]:
                        if handle_field in edge:
                            handle = edge[handle_field]
                            if isinstance(handle, str) and "œid∶" in handle:
                                errors.append(
                                    f"Edge {i} {handle_field} contains invalid Unicode characters (œid∶)"
                                )

    # Sprawdź metadane
    if "name" in data and not data["name"].strip():
        warnings.append("Workflow name is empty")

    if "description" in data and not data["description"].strip():
        warnings.append("Workflow description is empty")

    return errors, warnings


def validate_file(filepath):
    """Waliduje pojedynczy plik"""
    print(f"🔍 Sprawdzanie: {filepath}")

    # Sprawdź składnię JSON
    is_valid, data, error = validate_json_syntax(filepath)
    if not is_valid:
        print(f"❌ {filepath}: {error}")
        return False

    # Sprawdź strukturę Langflow
    errors, warnings = validate_langflow_structure(data, filepath)

    # Wyświetl wyniki
    if errors:
        print(f"❌ {filepath}: Błędy struktury")
        for error in errors:
            print(f"   • {error}")
        return False

    if warnings:
        print(f"⚠️  {filepath}: Ostrzeżenia")
        for warning in warnings:
            print(f"   • {warning}")

    # Statystyki
    if data and "data" in data:
        nodes_count = len(data["data"].get("nodes", []))
        edges_count = len(data["data"].get("edges", []))
        print(f"✅ {filepath}: OK - {nodes_count} węzłów, {edges_count} połączeń")
    else:
        print(f"✅ {filepath}: OK")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Walidator JSON dla Langflow workflows"
    )
    parser.add_argument(
        "files", nargs="*", help="Pliki do sprawdzenia (domyślnie: examples/*.json)"
    )
    parser.add_argument(
        "--strict", action="store_true", help="Traktuj ostrzeżenia jako błędy"
    )

    args = parser.parse_args()

    # Określ pliki do sprawdzenia
    if args.files:
        files_to_check = args.files
    else:
        # Domyślnie sprawdź wszystkie JSON w examples/
        examples_dir = Path("examples")
        if examples_dir.exists():
            files_to_check = list(examples_dir.glob("*.json"))
        else:
            print("❌ Katalog 'examples' nie istnieje")
            return 1

    if not files_to_check:
        print("❌ Nie znaleziono plików do sprawdzenia")
        return 1

    print("🔍 JSON Validator dla Langflow Workflows")
    print(f"📂 Sprawdzanie {len(files_to_check)} plików...\n")

    all_valid = True
    valid_files = 0

    for filepath in files_to_check:
        is_valid = validate_file(filepath)
        if is_valid:
            valid_files += 1
        else:
            all_valid = False
        print()  # Pusta linia między plikami

    # Podsumowanie
    print("=" * 50)
    print(f"📊 Wyniki: {valid_files}/{len(files_to_check)} plików prawidłowych")

    if all_valid:
        print("🎉 Wszystkie pliki są poprawne!")
        return 0
    else:
        print("❌ Niektóre pliki wymagają poprawy")
        return 1


if __name__ == "__main__":
    sys.exit(main())
