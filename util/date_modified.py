import os
import subprocess
import yaml

# Path to the posts directory
POSTS_DIR = "blog/_posts/"

# Iterate over all markdown files in the directory
for filename in os.listdir(POSTS_DIR):
    if filename.endswith(".md"):
        filepath = os.path.join(POSTS_DIR, filename)
        
        # Get last modified date from Git in the format YYYY-MM-DD
        date = subprocess.check_output(["git", "log", "-1", "--format=%ad", "--date=short", "--", filepath]).decode('utf-8').strip()
        
        # Read the file
        with open(filepath, 'r') as file:
            content = file.readlines()
            delimiter_count = content.count('---\n')
            
            if delimiter_count < 2:
                continue  # Skip files that don't have a proper front matter

            front_matter_index = content.index('---\n') + 1  # index after the first '---'
            end_front_matter_index = front_matter_index + content[front_matter_index:].index('---\n')  # index of the second '---'

            front_matter = yaml.safe_load("".join(content[front_matter_index:end_front_matter_index]))
            
            # Update or add the 'last_modified_at' field
            front_matter['last_modified_at'] = date
            
            # Replace the old front matter with the updated one
            content[front_matter_index:end_front_matter_index] = yaml.dump(front_matter, default_flow_style=False, allow_unicode=True).splitlines()
            
        # Write the updated content back to the file
        with open(filepath, 'w') as file:
            file.write("\n".join(content))
