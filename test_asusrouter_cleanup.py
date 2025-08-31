#!/usr/bin/env python3
"""
Test script to demonstrate what files would be removed/updated/added
for the asusrouter integration based on current API data and existing files.
"""

import json
import os
import glob
from typing import Any

BADGES_PATH = "docs/badges/"
RAW_DATA_PATH = "docs/raw/custom_integrations/"

def load_latest_raw_data():
    """Load the most recent raw data file"""
    print("📡 Loading latest raw API data...")
    
    # Find the most recent raw data file
    raw_files = glob.glob(os.path.join(RAW_DATA_PATH, "*.json"))
    if not raw_files:
        raise FileNotFoundError("No raw data files found")
    
    latest_file = max(raw_files)
    print(f"📁 Using data from: {os.path.basename(latest_file)}")
    
    with open(latest_file, 'r') as f:
        data = json.load(f)
    
    print(f"✅ API data loaded successfully ({len(data)} integrations)")
    return data

def get_existing_files(integration_name: str) -> dict:
    """Get information about existing files for an integration"""
    integration_path = os.path.join(BADGES_PATH, integration_name)
    
    if not os.path.exists(integration_path):
        return {
            'path_exists': False,
            'total_file': False,
            'version_files': []
        }
    
    # Check for total.json
    total_file = os.path.exists(os.path.join(integration_path, 'total.json'))
    
    # Find all version files
    version_files = glob.glob(os.path.join(integration_path, "version-*.json"))
    version_list = []
    
    for version_file in version_files:
        filename = os.path.basename(version_file)
        if filename.startswith("version-") and filename.endswith(".json"):
            version = filename[8:-5]  # Remove "version-" prefix and ".json" suffix
            version_list.append(version)
    
    return {
        'path_exists': True,
        'total_file': total_file,
        'version_files': sorted(version_list)
    }

def analyze_changes(integration_name: str, api_data: dict, existing_files: dict) -> dict:
    """Analyze what changes would be made"""
    
    if integration_name not in api_data:
        return {
            'integration_in_api': False,
            'total_changes': None,
            'version_changes': None
        }
    
    integration_data = api_data[integration_name]
    
    # Analyze total.json changes
    total_changes = {
        'exists': existing_files['total_file'],
        'will_exist': 'total' in integration_data,
        'action': 'none'
    }
    
    if not existing_files['total_file'] and 'total' in integration_data:
        total_changes['action'] = 'add'
    elif existing_files['total_file'] and 'total' in integration_data:
        total_changes['action'] = 'update'
    elif existing_files['total_file'] and 'total' not in integration_data:
        total_changes['action'] = 'remove'
    
    # Analyze version file changes
    current_versions = list(integration_data.get('versions', {}).keys())
    existing_versions = existing_files['version_files']
    
    versions_to_add = [v for v in current_versions if v not in existing_versions]
    versions_to_remove = [v for v in existing_versions if v not in current_versions]
    versions_to_update = [v for v in current_versions if v in existing_versions]
    
    version_changes = {
        'current_api_versions': current_versions,
        'existing_versions': existing_versions,
        'to_add': versions_to_add,
        'to_remove': versions_to_remove,
        'to_update': versions_to_update
    }
    
    return {
        'integration_in_api': True,
        'total_changes': total_changes,
        'version_changes': version_changes
    }

def print_results(integration_name: str, existing_files: dict, changes: dict):
    """Print the analysis results in a clear format"""
    
    print(f"\n🔍 ANALYSIS RESULTS FOR '{integration_name}' INTEGRATION")
    print("=" * 60)
    
    if not existing_files['path_exists']:
        print("📁 Integration directory: DOES NOT EXIST")
    else:
        print("📁 Integration directory: EXISTS")
    
    if not changes['integration_in_api']:
        print("❌ Integration not found in current API data")
        print("   → No changes would be made (directory preserved)")
        return
    
    print("✅ Integration found in current API data")
    
    # Total.json analysis
    print(f"\n📄 TOTAL.JSON FILE:")
    total_changes = changes['total_changes']
    if total_changes['action'] == 'add':
        print("   ➕ WILL BE ADDED (new file)")
    elif total_changes['action'] == 'update':
        print("   🔄 WILL BE UPDATED (existing file)")
    elif total_changes['action'] == 'remove':
        print("   ❌ WILL BE REMOVED (no total data in API)")
    else:
        print("   ➖ NO CHANGE")
    
    # Version files analysis
    print(f"\n📄 VERSION FILES:")
    version_changes = changes['version_changes']
    
    print(f"   📊 Current API has {len(version_changes['current_api_versions'])} versions")
    print(f"   📁 Directory has {len(version_changes['existing_versions'])} version files")
    
    if version_changes['to_add']:
        print(f"\n   ➕ FILES TO ADD ({len(version_changes['to_add'])}):")
        for version in sorted(version_changes['to_add']):
            print(f"      + version-{version}.json")
    
    if version_changes['to_remove']:
        print(f"\n   ❌ FILES TO REMOVE ({len(version_changes['to_remove'])}):")
        for version in sorted(version_changes['to_remove']):
            print(f"      - version-{version}.json")
    
    if version_changes['to_update']:
        print(f"\n   🔄 FILES TO UPDATE ({len(version_changes['to_update'])}):")
        for version in sorted(version_changes['to_update']):
            print(f"      ~ version-{version}.json")
    
    # Summary
    total_operations = len(version_changes['to_add']) + len(version_changes['to_remove']) + len(version_changes['to_update'])
    if total_changes['action'] != 'none':
        total_operations += 1
    
    print(f"\n📋 SUMMARY:")
    print(f"   Total operations: {total_operations}")
    print(f"   Files to add: {len(version_changes['to_add']) + (1 if total_changes['action'] == 'add' else 0)}")
    print(f"   Files to remove: {len(version_changes['to_remove']) + (1 if total_changes['action'] == 'remove' else 0)}")
    print(f"   Files to update: {len(version_changes['to_update']) + (1 if total_changes['action'] == 'update' else 0)}")

def main():
    """Main test function"""
    integration_name = "asusrouter"
    
    print("🧪 ASUSROUTER INTEGRATION CLEANUP TEST")
    print("=" * 60)
    print(f"Testing cleanup behavior for '{integration_name}' integration")
    print("This is a DRY RUN - no files will be modified")
    
    try:
        # Load API data from raw files
        api_data = load_latest_raw_data()
        
        # Get existing file information
        print(f"\n📁 Analyzing existing files for '{integration_name}'...")
        existing_files = get_existing_files(integration_name)
        
        # Analyze what changes would be made
        print(f"🔍 Comparing with current API data...")
        changes = analyze_changes(integration_name, api_data, existing_files)
        
        # Print results
        print_results(integration_name, existing_files, changes)
        
        print(f"\n✅ Test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        raise

if __name__ == "__main__":
    main()