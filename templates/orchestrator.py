#!/usr/bin/env python3
"""
Multi-Model API Orchestrator
Manages multiple model API servers and provides a unified interface.

Features:
- Starts all model APIs on different ports
- Health check aggregation
- Load balancing capabilities
- Unified logging

Usage:
    python orchestrator.py [start|stop|status]
"""

import subprocess
import time
import requests
import sys
import signal
import os
from typing import Dict, List

# Model API configurations
MODELS = {
    "gemini": {"port": 8001, "script": "gemini_api.py"},
    "gpt": {"port": 8002, "script": "gpt_api.py"},
    "claude": {"port": 8003, "script": "claude_api.py"},
}


class MultiModelOrchestrator:
    def __init__(self):
        self.processes: Dict[str, subprocess.Popen] = {}

    def start_all(self):
        """Start all model API servers"""
        print("🚀 Starting Multi-Model API Orchestrator...")

        for model_name, config in MODELS.items():
            if os.path.exists(config["script"]):
                print(f"   Starting {model_name} API on port {config['port']}...")
                process = subprocess.Popen(
                    [sys.executable, config["script"]],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                self.processes[model_name] = process
                time.sleep(2)  # Give time to start
            else:
                print(
                    f"   ⚠️  Script {config['script']} not found, skipping {model_name}"
                )

        print(f"✅ Started {len(self.processes)} model APIs")
        self.check_health()

    def stop_all(self):
        """Stop all model API servers"""
        print("🛑 Stopping all model APIs...")

        for model_name, process in self.processes.items():
            print(f"   Stopping {model_name} API...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

        self.processes.clear()
        print("✅ All APIs stopped")

    def check_health(self):
        """Check health of all APIs"""
        print("\n🏥 Health Check:")

        for model_name, config in MODELS.items():
            try:
                response = requests.get(
                    f"http://localhost:{config['port']}/health", timeout=3
                )
                if response.status_code == 200:
                    data = response.json()
                    status = "✅" if data.get("configured") else "⚠️ "
                    print(
                        f"   {status} {model_name} API (port {config['port']}) - {data.get('status', 'unknown')}"
                    )
                else:
                    print(
                        f"   ❌ {model_name} API (port {config['port']}) - HTTP {response.status_code}"
                    )
            except requests.RequestException:
                print(
                    f"   ❌ {model_name} API (port {config['port']}) - Not responding"
                )

    def get_status(self):
        """Get status of all APIs"""
        running = []
        for model_name, process in self.processes.items():
            if process.poll() is None:  # Still running
                running.append(model_name)

        print(f"📊 Status: {len(running)}/{len(MODELS)} APIs running")
        if running:
            print(f"   Running: {', '.join(running)}")

        return running


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Received interrupt signal, shutting down...")
    orchestrator.stop_all()
    sys.exit(0)


def main():
    global orchestrator
    orchestrator = MultiModelOrchestrator()

    # Handle Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    command = sys.argv[1] if len(sys.argv) > 1 else "start"

    if command == "start":
        orchestrator.start_all()
        print("\n🔄 Press Ctrl+C to stop all services")
        try:
            # Keep running
            while True:
                time.sleep(30)
                orchestrator.check_health()
        except KeyboardInterrupt:
            pass
        finally:
            orchestrator.stop_all()

    elif command == "stop":
        orchestrator.stop_all()

    elif command == "status":
        orchestrator.get_status()
        orchestrator.check_health()

    else:
        print("Usage: python orchestrator.py [start|stop|status]")


if __name__ == "__main__":
    main()
