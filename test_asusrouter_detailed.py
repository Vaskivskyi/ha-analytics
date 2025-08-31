#!/usr/bin/env python3
"""
Enhanced test script to show detailed information about what would happen
during the asusrouter cleanup, including installation counts.
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

def load_existing_badge_data(integration_name: str, version: str):
    """Load installation count from existing badge file"""
    badge_file = os.path.join(BADGES_PATH, integration_name, f"version-{version}.json")
    if os.path.exists(badge_file):
        with open(badge_file, 'r') as f:
            badge_data = json.load(f)
            return int(badge_data.get('message', 0))
    return 0

def main():
    """Enhanced main test function"""
    integration_name = "asusrouter"
    
    print("🧪 ENHANCED ASUSROUTER INTEGRATION CLEANUP TEST")
    print("=" * 70)
    print(f"Testing cleanup behavior for '{integration_name}' integration")
    print("This is a DRY RUN - no files will be modified")
    
    try:
        # Load API data from raw files
        api_data, data_date = load_latest_raw_data()
        print(f"📡 Using API data from: {data_date}")
        print(f"✅ API data loaded successfully ({len(api_data)} integrations)")
        
        if integration_name not in api_data:
            print(f"❌ Integration '{integration_name}' not found in API data")
            return
        
        integration_data = api_data[integration_name]
        
        # Get current API versions and installation counts
        api_versions = integration_data.get('versions', {})
        total_installs = integration_data.get('total', 0)
        
        print(f"\n📊 API DATA SUMMARY:")
        print(f"   Total installations: {total_installs:,}")
        print(f"   Available versions: {len(api_versions)}")
        
        # Get existing files
        integration_path = os.path.join(BADGES_PATH, integration_name)
        existing_version_files = glob.glob(os.path.join(integration_path, "version-*.json"))
        existing_versions = []
        
        for version_file in existing_version_files:
            filename = os.path.basename(version_file)
            if filename.startswith("version-") and filename.endswith(".json"):
                version = filename[8:-5]
                existing_versions.append(version)
        
        print(f"\n📁 EXISTING FILES SUMMARY:")
        print(f"   Existing version files: {len(existing_versions)}")
        print(f"   Total.json exists: {os.path.exists(os.path.join(integration_path, 'total.json'))}")
        
        # Analyze changes
        versions_to_add = [v for v in api_versions.keys() if v not in existing_versions]
        versions_to_remove = [v for v in existing_versions if v not in api_versions]
        versions_to_update = [v for v in api_versions.keys() if v in existing_versions]
        
        print(f"\n🔄 DETAILED CHANGE ANALYSIS:")
        print("=" * 70)
        
        if versions_to_remove:
            print(f"\n❌ VERSIONS TO BE REMOVED ({len(versions_to_remove)}):")
            print("   These versions are no longer in the API data and will be deleted:")
            removed_installs = 0
            for version in sorted(versions_to_remove):
                installs = load_existing_badge_data(integration_name, version)
                removed_installs += installs
                print(f"   - {version:20s} ({installs:>6,} installations)")
            print(f"   Total installations in removed files: {removed_installs:,}")
        
        if versions_to_update:
            print(f"\n🔄 VERSIONS TO BE UPDATED ({len(versions_to_update)}):")
            print("   These versions exist in both places and will be updated:")
            for version in sorted(versions_to_update):
                old_installs = load_existing_badge_data(integration_name, version)
                new_installs = api_versions[version]
                change = new_installs - old_installs
                change_str = f"({change:+,})" if change != 0 else "(no change)"
                print(f"   ~ {version:20s} {old_installs:>6,} → {new_installs:>6,} {change_str}")
        
        if versions_to_add:
            print(f"\n➕ VERSIONS TO BE ADDED ({len(versions_to_add)}):")
            print("   These are new versions from the API:")
            added_installs = 0
            for version in sorted(versions_to_add):
                installs = api_versions[version]
                added_installs += installs
                print(f"   + {version:20s} ({installs:>6,} installations)")
            print(f"   Total installations in new files: {added_installs:,}")
        
        # Summary stats
        print(f"\n📊 OPERATION SUMMARY:")
        print("=" * 70)
        print(f"   Files before cleanup: {len(existing_versions)} + 1 total.json")
        print(f"   Files after cleanup:  {len(api_versions)} + 1 total.json")
        print(f"   Net change:           {len(api_versions) - len(existing_versions):+d} version files")
        print(f"   Operations to perform:")
        print(f"     - Remove:           {len(versions_to_remove)} files")
        print(f"     - Update:           {len(versions_to_update)} files")  
        print(f"     - Add:              {len(versions_to_add)} files")
        print(f"     - Update total.json: 1 file")
        print(f"   Total operations:     {len(versions_to_remove) + len(versions_to_update) + len(versions_to_add) + 1}")
        
        print(f"\n✅ Enhanced test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        raise

if __name__ == "__main__":
    main()