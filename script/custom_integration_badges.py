import aiohttp
import asyncio
from datetime import date
import json
import os
import glob
from typing import Any

DATA_URL = "https://analytics.home-assistant.io/custom_integrations.json"
PROCESSED_PATH = "docs/badges/"
RAW_PATH = "docs/raw/custom_integrations/"


async def async_get_data(session: aiohttp.ClientSession | None = None):
    """Load data"""

    _session = session if session is not None else aiohttp.ClientSession()

    async with _session.get(
        url=DATA_URL,
    ) as r:
        json_body = await r.json()

    await _session.close()

    # Save the raw data
    if not os.path.exists(RAW_PATH):
        os.makedirs(RAW_PATH)
    today = date.today()
    path = RAW_PATH + today.isoformat() + ".json"
    with open(path, "w") as file:
        json.dump(json_body, file)

    return json_body


def generate_badge(installations: int) -> dict[str, Any]:
    """Generate badge"""

    return {
        "schemaVersion": 1,
        "label": "Installations",
        "message": f"{installations}",
    }


def cleanup_old_version_files(integration_path: str, current_versions: list[str]):
    """Remove old version files that are no longer in current data"""
    if not os.path.exists(integration_path):
        return
    
    # Find all existing version files
    version_files = glob.glob(os.path.join(integration_path, "version-*.json"))
    
    for version_file in version_files:
        # Extract version from filename (version-{version}.json)
        filename = os.path.basename(version_file)
        if filename.startswith("version-") and filename.endswith(".json"):
            version = filename[8:-5]  # Remove "version-" prefix and ".json" suffix
            if version not in current_versions:
                try:
                    os.remove(version_file)
                    print(f"Removed old version file: {version_file}")
                except OSError as e:
                    print(f"Error removing {version_file}: {e}")


async def async_test():
    data = await async_get_data()

    for integration in data:
        path = PROCESSED_PATH + integration
        # Check the path
        if not os.path.exists(path):
            os.makedirs(path)

        # Get current versions for cleanup
        current_versions = []
        if "versions" in data[integration]:
            current_versions = list(data[integration]["versions"].keys())
        
        # Clean up old version files before writing new ones
        cleanup_old_version_files(path, current_versions)

        # Generate total badge
        if "total" in data[integration]:
            badge = generate_badge(data[integration]["total"])
            with open(f"{path}/total.json", "w") as file:
                json.dump(badge, file)
        # Generate per-version badges
        if "versions" in data[integration]:
            for version in data[integration]["versions"]:
                badge = generate_badge(data[integration]["versions"][version])
                with open(f"{path}/version-{version}.json", "w") as file:
                    json.dump(badge, file)


loop = asyncio.get_event_loop()
loop.run_until_complete(async_test())
loop.close()
