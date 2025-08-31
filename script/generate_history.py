#!/usr/bin/env python3
"""
Generate historical data for Home Assistant custom integrations.

This script processes the raw daily JSON files from docs/raw/custom_integrations/
and creates historical time series data for each integration showing how
installation counts changed over time.

For each integration, it creates:
- docs/history/{integration}/total.json: {date: total_count} mapping
- docs/history/{integration}/version-{version}.json: {date: version_count} mapping
"""

import json
import os
from datetime import datetime
from typing import Dict, Any
import glob
from pathlib import Path


RAW_PATH = "docs/raw/custom_integrations/"
HISTORY_PATH = "docs/history/"


def write_git_friendly_json(file_handle, data):
    """Write JSON in a git-friendly format with each key-value pair on a new line."""
    file_handle.write("{\n")
    sorted_items = sorted(data.items())
    for i, (key, value) in enumerate(sorted_items):
        comma = "," if i < len(sorted_items) - 1 else ""
        file_handle.write(f'"{key}": {value}{comma}\n')
    file_handle.write("}\n")


def load_raw_data_files() -> Dict[str, Dict[str, Any]]:
    """Load all raw data files and return sorted by date."""
    raw_data = {}
    
    # Get all JSON files from raw directory
    raw_files = glob.glob(os.path.join(RAW_PATH, "*.json"))
    
    for file_path in raw_files:
        # Extract date from filename (e.g., "2024-01-01.json" -> "2024-01-01")
        filename = os.path.basename(file_path)
        if not filename.endswith(".json"):
            continue
        
        date_str = filename[:-5]  # Remove .json extension
        
        try:
            # Validate date format
            datetime.strptime(date_str, "%Y-%m-%d")
            
            with open(file_path, 'r') as f:
                data = json.load(f)
                raw_data[date_str] = data
                
        except (ValueError, json.JSONDecodeError) as e:
            print(f"Skipping invalid file {filename}: {e}")
            continue
    
    return raw_data


def process_integration_history(integration_name: str, date_data: Dict[str, Dict[str, Any]]) -> None:
    """Process historical data for a single integration."""
    
    # Create integration directory
    integration_dir = os.path.join(HISTORY_PATH, integration_name)
    os.makedirs(integration_dir, exist_ok=True)
    
    # Collect historical data
    total_history = {}
    version_histories = {}
    
    # Sort dates to ensure chronological order
    sorted_dates = sorted(date_data.keys())
    
    for date in sorted_dates:
        day_data = date_data[date]
        
        if integration_name not in day_data:
            continue
            
        integration_data = day_data[integration_name]
        
        # Record total installations for this date
        if "total" in integration_data:
            total_history[date] = integration_data["total"]
        
        # Record version-specific installations
        if "versions" in integration_data:
            for version, count in integration_data["versions"].items():
                if version not in version_histories:
                    version_histories[version] = {}
                version_histories[version][date] = count
    
    # Write total history file
    if total_history:
        total_file_path = os.path.join(integration_dir, "total.json")
        with open(total_file_path, 'w') as f:
            write_git_friendly_json(f, total_history)
    
    # Write version history files
    for version, version_history in version_histories.items():
        if version_history:
            # Sanitize version string for filename
            safe_version = version.replace("/", "_").replace("\\", "_")
            version_file_path = os.path.join(integration_dir, f"version-{safe_version}.json")
            with open(version_file_path, 'w') as f:
                write_git_friendly_json(f, version_history)


def cleanup_old_version_files(integration_dir: str, current_versions: set) -> None:
    """Remove version files that are no longer present in current data."""
    if not os.path.exists(integration_dir):
        return
    
    # Find all existing version files
    version_files = glob.glob(os.path.join(integration_dir, "version-*.json"))
    
    for version_file in version_files:
        filename = os.path.basename(version_file)
        # Extract version from filename (version-{version}.json)
        if filename.startswith("version-") and filename.endswith(".json"):
            version = filename[8:-5]  # Remove "version-" prefix and ".json" suffix
            # Restore original version string (undo sanitization)
            original_version = version.replace("_", "/")
            
            # Check both sanitized and original version
            if version not in current_versions and original_version not in current_versions:
                try:
                    os.remove(version_file)
                    print(f"Removed old version file: {version_file}")
                except OSError as e:
                    print(f"Error removing {version_file}: {e}")


def main():
    """Main function to generate all historical data."""
    print("Loading raw data files...")
    date_data = load_raw_data_files()
    
    if not date_data:
        print("No valid data files found.")
        return
    
    print(f"Loaded {len(date_data)} data files from {min(date_data.keys())} to {max(date_data.keys())}")
    
    # Create history directory
    os.makedirs(HISTORY_PATH, exist_ok=True)
    
    # Get all unique integration names across all dates
    all_integrations = set()
    current_integrations = set()  # Track integrations in latest data
    
    latest_date = max(date_data.keys())
    
    for date, day_data in date_data.items():
        for integration_name in day_data.keys():
            all_integrations.add(integration_name)
            if date == latest_date:
                current_integrations.add(integration_name)
    
    print(f"Processing {len(all_integrations)} integrations...")
    
    # Process each integration
    for integration_name in sorted(all_integrations):
        print(f"Processing {integration_name}...")
        
        # Get current versions for cleanup
        current_versions = set()
        if latest_date in date_data and integration_name in date_data[latest_date]:
            latest_data = date_data[latest_date][integration_name]
            if "versions" in latest_data:
                current_versions = set(latest_data["versions"].keys())
        
        # Clean up old version files first
        integration_dir = os.path.join(HISTORY_PATH, integration_name)
        cleanup_old_version_files(integration_dir, current_versions)
        
        # Process historical data for this integration
        process_integration_history(integration_name, date_data)
    
    # Clean up directories for integrations that no longer exist
    if os.path.exists(HISTORY_PATH):
        existing_dirs = [d for d in os.listdir(HISTORY_PATH) 
                        if os.path.isdir(os.path.join(HISTORY_PATH, d))]
        
        for dir_name in existing_dirs:
            if dir_name not in current_integrations:
                # Integration no longer exists, remove its directory
                import shutil
                dir_path = os.path.join(HISTORY_PATH, dir_name)
                try:
                    shutil.rmtree(dir_path)
                    print(f"Removed directory for obsolete integration: {dir_path}")
                except OSError as e:
                    print(f"Error removing directory {dir_path}: {e}")
    
    print("Historical data generation completed!")


if __name__ == "__main__":
    main()