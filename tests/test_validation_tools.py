#!/usr/bin/env python3
"""
Test script to verify pre-commit and validation tools are working correctly.
This matches the requirements from GitHub issue #10 for enhanced Copilot support.
"""
import subprocess
import sys
import os


def run_command(cmd):
    """Run a shell command and return success status"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=60
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"


def test_tools():
    """Test all validation tools"""
    print("🧪 Testing Validation Tools Setup...")
    print("=" * 50)

    tests = [
        ("black --version", "Black formatter"),
        ("flake8 --version", "Flake8 linter"),
        ("shellcheck --version", "Shellcheck validator"),
        ("pre-commit --version", "Pre-commit tool"),
    ]

    all_passed = True
    
    for cmd, name in tests:
        success, stdout, stderr = run_command(cmd)
        if success:
            version = stdout.strip().split('\n')[0] if stdout else "installed"
            print(f"   ✅ {name}: {version}")
        else:
            print(f"   ❌ {name}: Not found or failed")
            all_passed = False

    # Test Trivy separately as it may not be installed
    print("\n🔒 Security Tools:")
    trivy_success, trivy_out, trivy_err = run_command("trivy --version")
    if trivy_success:
        version = trivy_out.strip().split('\n')[0] if trivy_out else "installed"
        print(f"   ✅ Trivy scanner: {version}")
    else:
        print(f"   ⚠️  Trivy scanner: Not found (optional in CI)")

    print("\n📋 Configuration Files:")
    configs = [
        (".pre-commit-config.yaml", "Pre-commit configuration"),
        (".github/workflows/pre-commit.yml", "GitHub Actions workflow"),
        ("setup-pre-commit.sh", "Setup script"),
    ]

    for file_path, description in configs:
        if os.path.exists(file_path):
            print(f"   ✅ {description}: {file_path}")
        else:
            print(f"   ❌ {description}: Missing {file_path}")
            all_passed = False

    print("\n📊 Test Summary:")
    if all_passed:
        print("🎉 All validation tools are properly configured!")
        print("🚀 Pre-commit hooks and GitHub Actions are ready!")
        return True
    else:
        print("❌ Some tools are missing. Run ./setup-pre-commit.sh")
        return False


if __name__ == "__main__":
    success = test_tools()
    sys.exit(0 if success else 1)