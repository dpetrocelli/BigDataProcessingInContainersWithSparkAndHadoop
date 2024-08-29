import subprocess
import json
import re

def get_fsck_output():
    # Run the hdfs fsck command and get the output
    result = subprocess.run(
        ["docker", "exec", "-it", "namenode", "hdfs", "fsck", "/hdfs/path", "-files", "-blocks", "-locations"],
        stdout=subprocess.PIPE,
        text=True
    )
    return result.stdout

def extract_ips(fsck_output):
    # Use regex to extract IP addresses from the fsck output
    ip_pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')
    ips = ip_pattern.findall(fsck_output)
    return set(ips)

def get_container_names():
    # Get the list of containers and their IPs
    result = subprocess.run(
        ["docker", "network", "inspect", "custom_network"],
        stdout=subprocess.PIPE,
        text=True
    )
    network_data = json.loads(result.stdout)
    
    container_names = {}
    for container in network_data[0]['Containers'].values():
        container_ip = container['IPv4Address'].split('/')[0]
        container_name = container['Name']
        container_names[container_ip] = container_name
    
    return container_names

def match_ips_to_containers(ips, container_names):
    # Match IPs to container names
    matches = {}
    for ip in ips:
        if ip in container_names:
            matches[ip] = container_names[ip]
        else:
            matches[ip] = "Unknown"
    return matches

def display_results(fsck_output, matches):
    # Display the fsck output with matched container names
    print("HDFS FSCK Output:\n")
    print(fsck_output)
    
    print("\nContainer Matches:\n")
    for ip, name in matches.items():
        print(f"IP: {ip}, Container: {name}")

def main():
    fsck_output = get_fsck_output()
    ips = extract_ips(fsck_output)
    container_names = get_container_names()
    matches = match_ips_to_containers(ips, container_names)
    
    display_results(fsck_output, matches)

if __name__ == "__main__":
    main()
