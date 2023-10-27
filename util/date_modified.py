import os
import subprocess
import yaml


# Goal: Set last_modified_at for all blog posts using git data
# Problem: Well, now that I've used this script once, the last modified date per git is
#          the very commit where I set the last modified date, for all blog posts. 
#          To avoid that, I guess we'd have to exclude the git commits where this script is run.


# Path to the posts directory
POSTS_DIR = "blog/_posts/"

# remove last_modified_at
for filename in os.listdir(POSTS_DIR):
    if filename.endswith(".md"):
        filepath = os.path.join(POSTS_DIR, filename)
        with open(filepath, 'r') as file:
            content = file.readlines()
        # Remove lines starting with "last_modified_at"
        content = [line for line in content if not line.strip().startswith("last_modified_at:")]
        
        # Write the modified content back to the file
        with open(filepath, 'w') as file:
            file.writelines(content)

# set last_modified_at using git dates
for filename in os.listdir(POSTS_DIR):
    if filename.endswith(".md"):
        filepath = os.path.join(POSTS_DIR, filename)
        
        # Get last modified date from Git
        try:
            date = subprocess.check_output(["git", "log", "-1", "--format=%ad", "--date=short", "--", filepath]).decode('utf-8').strip()
        except:
            date = "Unknown"  
        
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
