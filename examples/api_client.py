#!/usr/bin/env python3
"""
Example: API client for interacting with the server
"""

import asyncio
import json
import httpx
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))


class QuestAPIClient:
    """Simple client for Quest API"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    async def health_check(self) -> dict:
        """Check system health"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/health")
            return response.json()

    async def create_task(self, objective: str, params: dict = None) -> dict:
        """Create a new automation task"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/tasks",
                json={"objective": objective, "params": params or {}},
            )
            return response.json()

    async def get_task_status(self, task_id: str) -> dict:
        """Get task status"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/tasks/{task_id}")
            return response.json()

    async def get_task_result(self, task_id: str) -> dict:
        """Get task result"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/tasks/{task_id}/result")
            return response.json()

    async def get_audit_log(self, task_id: str) -> list:
        """Get task audit log"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/tasks/{task_id}/audit")
            return response.json()

    async def wait_for_completion(
        self, task_id: str, timeout: int = 600, poll_interval: int = 5
    ) -> dict:
        """Wait for task to complete"""
        start_time = time.time()

        while time.time() - start_time < timeout:
            status = await self.get_task_status(task_id)

            if status["status"] in ["completed", "failed"]:
                return await self.get_task_result(task_id)

            print(
                f"  Task status: {status['status']} (actions: {status['num_actions']})"
            )
            await asyncio.sleep(poll_interval)

        raise TimeoutError(f"Task {task_id} did not complete within {timeout}s")


async def main():
    """Example usage of API client"""
    client = QuestAPIClient()

    print("🤖 Quest API Client Example\n")

    # Health check
    print("📡 Checking system health...")
    try:
        health = await client.health_check()
        print(f"  ✓ Status: {health['status']}")
        print(f"  ✓ Model: {health['model']}\n")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        print("  Make sure the server is running: python main.py\n")
        return

    # Create task
    print("📝 Creating automation task...")
    task_response = await client.create_task(
        objective="Navigate to example.com and take a screenshot",
        params={},
    )
    task_id = task_response["task_id"]
    print(f"  ✓ Task ID: {task_id}\n")

    # Wait for completion
    print("⏳ Waiting for task completion...")
    try:
        result = await client.wait_for_completion(task_id, timeout=300)
        print(f"\n✅ Task completed!\n")
        print(f"Result: {json.dumps(result, indent=2)}")
    except TimeoutError as e:
        print(f"\n✗ {e}")

    # Get audit log
    print("\n📋 Fetching audit log...")
    try:
        audit_log = await client.get_audit_log(task_id)
        print(f"  ✓ Audit entries: {len(audit_log)}")
        for i, entry in enumerate(audit_log[:3]):
            print(f"    {i+1}. {entry.get('action_type', entry.get('event_type'))}")
    except Exception as e:
        print(f"  Note: {e}")


if __name__ == "__main__":
    asyncio.run(main())
