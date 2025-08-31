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

# Track file changes for reporting
file_changes = {
    "added": [],
    "modified": [],
    "removed": []
}


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
    
    # Check if this is a new file
    is_new_file = not os.path.exists(path)
    
    with open(path, "w") as file:
        json.dump(json_body, file)
    
    if is_new_file:
        file_changes["added"].append(path)
        print(f"Added new raw data file: {path}")
    else:
        file_changes["modified"].append(path)
        print(f"Updated raw data file: {path}")

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
            version = filename.removeprefix("version-").removesuffix(".json")  # Remove "version-" prefix and ".json" suffix
            if version not in current_versions:
                try:
                    os.remove(version_file)
                    file_changes["removed"].append(version_file)
                    print(f"Removed old version file: {version_file}")
                except OSError as e:
                    print(f"Error removing {version_file}: {e}")


def write_badge_file(file_path: str, badge_data: dict[str, Any]):
    """Write badge file and track changes"""
    is_new_file = not os.path.exists(file_path)
    
    with open(file_path, "w") as file:
        json.dump(badge_data, file)
    
    if is_new_file:
        file_changes["added"].append(file_path)
        print(f"Created new badge file: {file_path}")
    else:
        file_changes["modified"].append(file_path)
        print(f"Updated badge file: {file_path}")


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
            write_badge_file(f"{path}/total.json", badge)
        # Generate per-version badges
        if "versions" in data[integration]:
            for version in data[integration]["versions"]:
                badge = generate_badge(data[integration]["versions"][version])
                write_badge_file(f"{path}/version-{version}.json", badge)


def print_summary():
    """Print summary of file changes"""
    print("\n=== BADGE GENERATION SUMMARY ===")
    
    total_changes = len(file_changes["added"]) + len(file_changes["modified"]) + len(file_changes["removed"])
    print(f"Total files changed: {total_changes}")
    
    if file_changes["added"]:
        print(f"\nAdded files ({len(file_changes['added'])}):")
        for file_path in file_changes["added"]:
            print(f"  + {file_path}")
    
    if file_changes["modified"]:
        print(f"\nModified files ({len(file_changes['modified'])}):")
        for file_path in file_changes["modified"]:
            print(f"  ~ {file_path}")
    
    if file_changes["removed"]:
        print(f"\nRemoved files ({len(file_changes['removed'])}):")
        for file_path in file_changes["removed"]:
            print(f"  - {file_path}")
    
    if total_changes == 0:
        print("No files were changed.")
    
    print("================================\n")
    
    # Write summary to file for GitHub Action to read
    summary_data = {
        "total_changes": total_changes,
        "added": file_changes["added"],
        "modified": file_changes["modified"], 
        "removed": file_changes["removed"]
    }
    
    with open("badge_changes_summary.json", "w") as f:
        json.dump(summary_data, f, indent=2)
    
    print("Summary saved to badge_changes_summary.json")


loop = asyncio.get_event_loop()
loop.run_until_complete(async_test())
print_summary()
loop.close()
