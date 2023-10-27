import os
import subprocess
import yaml

# Path to the posts directory
POSTS_DIR = "blog/_posts/"

# Iterate over all markdown files in the directory
for filename in os.listdir(POSTS_DIR):
    if filename.endswith(".md"):
        filepath = os.path.join(POSTS_DIR, filename)
        
        # Get last modified date from Git (Note: This may not work as expected since these files are not in a git repository. We'll fallback to current date if git fails.)
        try:
            date = subprocess.check_output(["git", "log", "-1", "--format=%ad", "--date=short", "--", filepath]).decode('utf-8').strip()
        except:
            date = "Unknown"  # Placeholder if the git command fails
        
        # Read the file
        with open(filepath, 'r') as file:
            content = file.readlines()
            delimiter_count = content.count('---\n')
            
            if delimiter_count < 2:
                continue  # Skip files that don't have a proper front matter

            front_matter_index = content.index('---\n') + 1  # index after the first '---'
            end_front_matter_index = front_matter_index + content[front_matter_index:].index('---\n')  # index of the second '---'

            # Add the 'last_modified_at' field to the end of the front matter
            content.insert(end_front_matter_index, f"last_modified_at: {date}\n")
            
        # Write the updated content back to the file
        with open(filepath, 'w') as file:
            file.write("".join(content))
