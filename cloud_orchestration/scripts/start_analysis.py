import httpx
import asyncio
import time

async def trigger_remote_analysis():
    """
    Simple script to trigger the /analyze endpoint.
    Can be scheduled via crontab or GitHub Actions.
    """
    url = "http://localhost:8000/analyze" # Change to production URL when deployed
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url)
            print(f"Triggered analysis: {response.json()}")
        except Exception as e:
            print(f"Failed to trigger analysis: {e}")

if __name__ == "__main__":
    asyncio.run(trigger_remote_analysis())
