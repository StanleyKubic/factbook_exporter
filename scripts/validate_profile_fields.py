#!/usr/bin/env python3
"""
Script to validate that all fields in field_profiles.yaml exist in fields_complete.yaml
"""

import yaml
from pathlib import Path

def load_field_profiles():
    """Load field profiles configuration"""
    profiles_path = Path('config/field_profiles.yaml')
    with open(profiles_path) as f:
        return yaml.safe_load(f)

def load_complete_fields():
    """Load complete fields configuration"""
    fields_path = Path('config/fields_complete.yaml')
    with open(fields_path) as f:
        return yaml.safe_load(f)

def validate_profile_fields():
    """Validate that all profile fields exist in complete fields"""
    profiles_config = load_field_profiles()
    complete_fields = load_complete_fields()
    
    # Create a set of all available json paths from fields_complete.yaml
    available_paths = {field['json_path'] for field in complete_fields['fields']}
    
    print("Validating field profiles against fields_complete.yaml...")
    print("=" * 60)
    
    all_valid = True
    
    for profile_name, profile_data in profiles_config['profiles'].items():
        print(f"\nProfile: {profile_name}")
        print(f"Description: {profile_data['description']}")
        print(f"Fields: {len(profile_data['fields'])}")
        
        invalid_fields = []
        for field_path in profile_data['fields']:
            if field_path not in available_paths:
                invalid_fields.append(field_path)
        
        if invalid_fields:
            print(f"❌ INVALID FIELDS ({len(invalid_fields)}):")
            for field in invalid_fields:
                print(f"  - {field}")
            all_valid = False
        else:
            print("✅ All fields are valid")
    
    print("\n" + "=" * 60)
    if all_valid:
        print("✅ ALL PROFILE FIELDS ARE VALID")
    else:
        print("❌ SOME PROFILE FIELDS ARE INVALID")
        
    return all_valid

if __name__ == '__main__':
    validate_profile_fields()
