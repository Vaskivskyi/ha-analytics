#!/usr/bin/env python3
"""
Simulation script that runs the actual cleanup logic from the main script
to show exactly what files would be affected for the asusrouter integration.
"""

import json
import os
import glob
from typing import Any

BADGES_PATH = "docs/badges/"
RAW_DATA_PATH = "docs/raw/custom_integrations/"

def load_latest_raw_data():
    """Load the most recent raw data file"""
    raw_files = glob.glob(os.path.join(RAW_DATA_PATH, "*.json"))
    if not raw_files:
        raise FileNotFoundError("No raw data files found")
    
    latest_file = max(raw_files)
    with open(latest_file, 'r') as f:
        data = json.load(f)
    return data, os.path.basename(latest_file)

def cleanup_old_version_files_simulation(integration_path: str, current_versions: list[str], integration_name: str):
    """
    Simulate the cleanup function from the main script without actually deleting files.
    This is exactly the same logic as in the main script but with simulation output.
    """
    print(f"\n🔧 SIMULATING cleanup_old_version_files() for '{integration_name}':")
    print(f"   Integration path: {integration_path}")
    print(f"   Current versions from API: {len(current_versions)} versions")
    
    if not os.path.exists(integration_path):
        print(f"   ⚠️  Path does not exist, cleanup would return early")
        return
    
    # This is the exact same logic as in the main script
    version_files = glob.glob(os.path.join(integration_path, "version-*.json"))
    print(f"   📁 Found {len(version_files)} version files to examine")
    
    files_to_remove = []
    files_to_keep = []
    
    for version_file in version_files:
        # Extract version from filename (version-{version}.json)
        filename = os.path.basename(version_file)
        if filename.startswith("version-") and filename.endswith(".json"):
            version = filename[8:-5]  # Remove "version-" prefix and ".json" suffix
            if version not in current_versions:
                files_to_remove.append((version_file, version))
                print(f"   ❌ WOULD REMOVE: {filename} (version {version} not in current API)")
            else:
                files_to_keep.append((version_file, version))
                print(f"   ✅ WOULD KEEP:   {filename} (version {version} in current API)")
    
    print(f"\n   📊 CLEANUP SUMMARY:")
    print(f"     Files to remove: {len(files_to_remove)}")
    print(f"     Files to keep:   {len(files_to_keep)}")
    print(f"     Total examined:  {len(version_files)}")
    
    return files_to_remove, files_to_keep

def simulate_main_script_logic(integration_name: str, api_data: dict):
    """
    Simulate the main script logic for a specific integration
    """
    print(f"\n🏃 SIMULATING MAIN SCRIPT LOGIC for '{integration_name}':")
    print("=" * 70)
    
    integration_data = api_data[integration_name]
    path = BADGES_PATH + integration_name
    
    # Check the path (same as main script)
    print(f"📁 Checking integration path: {path}")
    if not os.path.exists(path):
        print(f"   ⚠️  Directory does not exist, would create it")
        print(f"   📝 os.makedirs('{path}')")
    else:
        print(f"   ✅ Directory exists")
    
    # Get current versions for cleanup (same as main script)
    current_versions = []
    if "versions" in integration_data:
        current_versions = list(integration_data["versions"].keys())
    
    print(f"📊 Current versions from API: {len(current_versions)}")
    for i, version in enumerate(sorted(current_versions)):
        if i < 5:  # Show first 5
            print(f"   - {version}")
        elif i == 5:
            print(f"   ... and {len(current_versions) - 5} more")
            break
    
    # Clean up old version files before writing new ones (same as main script)
    print(f"\n🧹 CALLING cleanup_old_version_files('{path}', current_versions)")
    files_to_remove, files_to_keep = cleanup_old_version_files_simulation(path, current_versions, integration_name)
    
    # Generate total badge (same as main script)
    print(f"\n📄 GENERATING BADGES:")
    if "total" in integration_data:
        total_installs = integration_data["total"]
        total_file = f"{path}/total.json"
        print(f"   📊 Total badge: {total_installs:,} installations → {total_file}")
        print(f"   📝 Would write/update total.json")
    
    # Generate per-version badges (same as main script)
    if "versions" in integration_data:
        print(f"   📊 Version badges: {len(current_versions)} files to write/update")
        for version in sorted(current_versions):
            installs = integration_data["versions"][version]
            version_file = f"{path}/version-{version}.json"
            print(f"   📝 {version}: {installs:,} installations → version-{version}.json")
    
    return files_to_remove, files_to_keep

def main():
    """Main simulation function"""
    integration_name = "asusrouter"
    
    print("🎭 ASUSROUTER INTEGRATION - MAIN SCRIPT SIMULATION")
    print("=" * 70)
    print(f"Simulating complete main script execution for '{integration_name}' integration")
    print("This is a SIMULATION - no files will be modified")
    
    try:
        # Load API data from raw files
        api_data, data_date = load_latest_raw_data()
        print(f"📡 Using API data from: {data_date}")
        print(f"✅ Loaded {len(api_data)} integrations from API data")
        
        if integration_name not in api_data:
            print(f"❌ Integration '{integration_name}' not found in API data")
            return
        
        print(f"✅ Found '{integration_name}' in API data")
        
        # Simulate the main script logic
        files_to_remove, files_to_keep = simulate_main_script_logic(integration_name, api_data)
        
        # Final summary
        print(f"\n🎯 FINAL SIMULATION RESULTS:")
        print("=" * 70)
        print(f"If the main script were run right now, it would:")
        print(f"  1. 🗂️  Ensure directory exists: docs/badges/{integration_name}/")
        print(f"  2. 🧹 Remove {len(files_to_remove)} old version files:")
        for version_file, version in files_to_remove[:10]:  # Show first 10
            filename = os.path.basename(version_file)
            print(f"     - {filename}")
        if len(files_to_remove) > 10:
            print(f"     ... and {len(files_to_remove) - 10} more")
        
        print(f"  3. 📄 Keep {len(files_to_keep)} current version files")
        print(f"  4. 📝 Write/update total.json file")
        print(f"  5. 📝 Write/update {len(api_data[integration_name].get('versions', {}))} version badge files")
        
        total_ops = len(files_to_remove) + len(files_to_keep) + 1 + len(api_data[integration_name].get('versions', {}))
        print(f"\n  📊 Total file operations: {total_ops}")
        print(f"     Net file count change: {len(api_data[integration_name].get('versions', {})) - (len(files_to_remove) + len(files_to_keep)):+d}")
        
        print(f"\n✅ Simulation completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Simulation failed with error: {e}")
        raise

if __name__ == "__main__":
    main()