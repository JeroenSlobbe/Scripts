import subprocess
import sys
import os
import shutil
import importlib
import importlib.util

# Check if a URL argument is provided
if len(sys.argv) != 2:
    print("Usage: python scanner.py <target_url>")
    sys.exit(1)

target_url = sys.argv[1]

# Set up directory structure
base_dir = "attacksurface"
output_dir = os.path.join(base_dir, "rawOutput")

for path in [base_dir, output_dir]:
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

# Define output file paths and commands
commands = {
    "whatweb": f"whatweb -a 3 {target_url} >> {output_dir}/whatweb.txt",
    "curl": f"curl -I {target_url} -o {output_dir}/curlHeaders.txt",
    "dirb": f"dirb {target_url} /usr/share/dirb/wordlists/common.txt -o {output_dir}/dirb_results.txt",
    "wget": f"wget --spider --recursive --level=5 -nd {target_url} -o {output_dir}/wget.txt",
    "nmap": f"nmap -sV {target_url} -oN {output_dir}/nmap_results.txt"
}

# Execute each command with live output
for name, cmd in commands.items():
    print(f"[+] Running {name}...")
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(line.strip())
        process.wait()

        if process.returncode == 0:
            print(f"[+] {name} completed successfully!\n")
        else:
            print(f"[-] {name} failed with exit code {process.returncode}\n")

    except Exception as e:
        print(f"[-] Error running {name}: {e}\n")

# Dynamically import and run all `process_*` functions from `processors/*.py`
print("[+] Executing processors from 'processors/' folder...\n")

processors_dir = "processors"
if os.path.exists(processors_dir):
    for filename in os.listdir(processors_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            module_path = os.path.join(processors_dir, filename)
            try:
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                for attr in dir(module):
                    if attr.startswith("process_") and callable(getattr(module, attr)):
                        print(f"[+] Running {module_name}.{attr}()")
                        getattr(module, attr)()

            except Exception as e:
                print(f"[-] Failed to import or run {module_name}: {e}")
else:
    print("[-] No 'processors/' directory found.")
