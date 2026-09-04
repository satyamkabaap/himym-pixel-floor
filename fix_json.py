import json
import os

files_to_fix = ["world_state.json", "sim_data.json", "memory_store.json"]

for filename in files_to_fix:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            # Load the messy JSON
            data = json.load(f)
        
        # Recursive function to strip trailing spaces from all string keys and values
        def clean_data(obj):
            if isinstance(obj, dict):
                return {k.strip(): clean_data(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [clean_data(item) for item in obj]
            elif isinstance(obj, str):
                return obj.strip()
            return obj
        
        cleaned_data = clean_data(data)
        
        with open(filename, 'w') as f:
            json.dump(cleaned_data, f, indent=2)
        print(f"✅ Fixed {filename}")
    else:
        print(f"⚠️ {filename} not found, will be created fresh by director.py")

print("Done! You can now delete fix_json.py")
