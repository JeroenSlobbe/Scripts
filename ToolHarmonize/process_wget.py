# Using to process the output of wget that spidered a website: wget --spider --recursive --level=5 -nd http://systemUnderTest.htb -o wget.txt 

import os
import re
import requests
from termcolor import colored

# Define input file and output folder
input_file = "wget.txt"
output_folder = "wget"

# Ensure the output folder is clean before running
if os.path.exists(output_folder):
    for file in os.listdir(output_folder):
        os.remove(os.path.join(output_folder, file))
else:
    os.makedirs(output_folder)

# Define output files
urls_200 = os.path.join(output_folder, "urls.txt")
urls_403 = os.path.join(output_folder, "forbidden.txt")
urls_other = os.path.join(output_folder, "urls_others.txt")
directories_file = os.path.join(output_folder, "directories.txt")

# Initialize sets to avoid duplicates
urls_200_set = set()
urls_403_set = set()
urls_other_set = set()
directories_set = set()

# Regex pattern to extract URLs from wget logs
url_pattern = re.compile(r"--\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}--\s+(http[s]?://[^\s]+)")

# Read and process URLs from wget.txt
with open(input_file, "r") as f:
    for line in f:
        url_match = url_pattern.match(line.strip())
        if url_match:
            url = url_match.group(1)

            # Check HTTP status
            try:
                response = requests.get(url, timeout=5)
                status_code = response.status_code

                if status_code == 200:
                    urls_200_set.add(url)
                elif status_code == 403:
                    urls_403_set.add(url)
                else:
                    urls_other_set.add(url)

                # Extract directory from URL
                directory = "/".join(url.split("/")[:-1]) + "/"
                directories_set.add(directory)

            except requests.RequestException:
                urls_other_set.add(url)  # Handle errors like timeout

# Check directories for 403 errors
directories_403 = set()
for directory in directories_set:
    try:
        response = requests.get(directory, timeout=5)
        if response.status_code == 403:
            directories_403.add(directory)
    except requests.RequestException:
        pass  # Skip unreachable directories

# Write results to files
def write_to_file(filepath, data):
    with open(filepath, "w") as f:
        for item in sorted(data):  # Sort for better organization
            f.write(f"{item}\n")

write_to_file(urls_200, urls_200_set)
write_to_file(urls_403, urls_403_set)
write_to_file(urls_other, urls_other_set)
write_to_file(directories_file, directories_set)

# Print summary message
print(f"{colored(str(len(urls_200_set)), 'green')} URLs found (200 OK)")
print(f"{colored(str(len(urls_403_set)), 'red')} URLs found (403 Forbidden)")
print(f"{colored(str(len(urls_other_set)), 'blue')} URLs found (Other Status Codes)")
print(f"{colored(str(len(directories_set)), 'white')} Directories identified")

# Print formatted table with correct labels and color coding
print("\n### Summary Table ###")
print(f"{'URL':<60} {'Status':<10}")
print("=" * 70)
for category, status_code, color in [
    (urls_200_set, "200", "green"),
    (urls_403_set, "403", "red"),
    (urls_other_set, "Other", "blue"),
    (directories_403, "DIR", "white")
]:
    for url in sorted(category):  # Ensure sorted output
        print(colored(f"{url:<60} {status_code:<10}", color))
print("=" * 70)
