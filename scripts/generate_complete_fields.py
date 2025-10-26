#!/usr/bin/env python3
"""
Generate complete fields referential from coverage report.
Extracts all fields from reports/coverage_simple.yaml and transforms to config/fields.yaml format.
"""

import yaml
from collections import defaultdict

def extract_category_from_json_path(json_path):
    """Extract category from json_path by taking the first segment before the first dot."""
    return json_path.split('.')[0]

def generate_complete_fields():
    """Generate complete fields referential from coverage report."""
    
    # Read the coverage report
    with open('reports/coverage_simple.yaml', 'r', encoding='utf-8') as f:
        coverage_data = yaml.safe_load(f)
    
    # Transform and organize fields by category
    fields_by_category = defaultdict(list)
    
    for field in coverage_data['fields']:
        json_path = field['json_path']
        display_name = field['field_name']
        category = extract_category_from_json_path(json_path)
        
        fields_by_category[category].append({
            'json_path': json_path,
            'display_name': display_name,
            'category': category
        })
    
    # Sort categories alphabetically
    sorted_categories = sorted(fields_by_category.keys())
    
    # Generate the complete fields list
    complete_fields = []
    for category in sorted_categories:
        # Sort fields within each category by display name
        sorted_fields = sorted(fields_by_category[category], key=lambda x: x['display_name'])
        complete_fields.extend(sorted_fields)
    
    # Create the output data structure
    output_data = {
        'fields': complete_fields
    }
    
    # Write to new file
    with open('config/fields_complete.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(output_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    # Print summary
    total_fields = len(complete_fields)
    total_categories = len(sorted_categories)
    
    print(f"Generated complete fields referential:")
    print(f"  Total fields: {total_fields}")
    print(f"  Total categories: {total_categories}")
    print(f"  Output file: config/fields_complete.yaml")
    
    print("\nField count by category:")
    for category in sorted_categories:
        count = len(fields_by_category[category])
        print(f"  {category}: {count} fields")
    
    return complete_fields

if __name__ == "__main__":
    generate_complete_fields()
