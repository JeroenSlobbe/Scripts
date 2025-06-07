# Goal of this script is to process dirb out (fetched from running: dirb http://systemUnderTest /usr/share/dirb/wordlists/common.txt -o dirb_results.txt) into files than can be used in other scripts.

import os
import re
from termcolor import colored

# Define input file and output folder
input_file = "dirb_results.txt"
output_folder = "dirb"

# Ensure the output folder is clean before running
if os.path.exists(output_folder):
    for file in os.listdir(output_folder):
        os.remove(os.path.join(output_folder, file))
else:
    os.makedirs(output_folder)

# Define output files
urls_200 = os.path.join(output_folder, "urls.txt")
urls_302 = os.path.join(output_folder, "urls_forbidden.txt")
urls_other = os.path.join(output_folder, "urls_others.txt")
directories = os.path.join(output_folder, "directories.txt")

# Initialize lists
urls_200_list = []
urls_302_list = []
urls_other_list = []
directories_list = []

# Regex patterns
url_pattern = re.compile(r"\+ (http[s]?://\S+) \(CODE:(\d+)")
dir_pattern = re.compile(r"==> DIRECTORY: (http[s]?://\S+)")

# Read and categorize the URLs
with open(input_file, "r") as f:
    for line in f:
        # Match directories
        dir_match = dir_pattern.match(line.strip())
        if dir_match:
            directories_list.append((dir_match.group(1), "DIR"))
            continue
        
        # Match URLs with status codes
        url_match = url_pattern.match(line.strip())
        if url_match:
            url, code = url_match.groups()
            if code == "200":
                urls_200_list.append((url, code))
            elif code == "302":
                urls_302_list.append((url, code))
            else:
                urls_other_list.append((url, code))

# Write results to files without status codes
def write_to_file(filepath, data):
    with open(filepath, "w") as f:
        for item in data:
            f.write(f"{item[0]}\n")  # Write only URL, omit status code

write_to_file(urls_200, urls_200_list)
write_to_file(urls_302, urls_302_list)
write_to_file(urls_other, urls_other_list)
write_to_file(directories, directories_list)

# Print summary message
print(f"{colored(str(len(urls_200_list)), 'green')} URLs found")
print(f"{colored(str(len(directories_list)), 'white')} directories found")

# Print formatted table with color coding
print("\n### Summary Table ###")
print(f"{'URL':<60} {'Code':<10}")
print("=" * 70)
for category, color in [(urls_200_list, "green"), (urls_302_list, "red"), (urls_other_list, "blue"), (directories_list, "white")]:
    for url, code in category:
        print(colored(f"{url:<60} {code:<10}", color))
print("=" * 70)
