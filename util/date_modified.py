import os
import subprocess
import yaml

# Path to the posts directory
POSTS_DIR = "blog/_posts/"

# Iterate over all markdown files in the directory
for filename in os.listdir(POSTS_DIR):
    if filename.endswith(".md"):
        filepath = os.path.join(POSTS_DIR, filename)
        
        # Get last modified date from Git
        date = subprocess.check_output(["git", "log", "-1", "--format=%ad", "--", filepath]).decode('utf-8').strip()
        
        # Read the file
        with open(filepath, 'r') as file:
            content = file.read().split("---")
            front_matter = yaml.safe_load(content[1])
            
            # Update or add the 'updated' field
            front_matter['updated'] = date
            
            # Combine the content
            content[1] = yaml.dump(front_matter)
            updated_content = "---".join(content)
            
        # Write the updated content back to the file
        with open(filepath, 'w') as file:
            file.write(updated_content)
