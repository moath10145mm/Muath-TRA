import re
import csv
import json
from collections import Counter
from datetime import datetime

# File paths
INPUT_FILE = "firewall.log"
CSV_FILE = "output.csv"
JSON_FILE = "output.json"
THREAT_FILE = "threats.txt"

# Improved regex (more flexible spacing)
log_pattern = re.compile(
    r"(\d{4})\s+(\d{2})\s+(\d{2})\s+"
    r"(\d{2}:\d{2}:\d{2})\s+"
    r"(ACCEPT|DROP)\s+"
    r"(TCP|UDP|ICMP)\s+"
    r"SRC=([\d\.]+)\s+SPT=(\d+)\s+"
    r"DST=([\d\.]+)\s+DPT=(\d+)\s+LEN=(\d+)"
)

entries = []
malformed_count = 0
action_counter = Counter()
port_counter = Counter()
ip_counter = Counter()

# Read file
with open("firewall.log", "r") as f:
    lines = f.read().splitlines()

# ✅ FIXED: Proper log reconstruction
combined_logs = []
temp = []

for line in lines:
    line = line.strip()

    if not line:
        continue

    temp.append(line)

    # End of a log entry
    if "LEN=" in line:
        combined_logs.append(" ".join(temp))
        temp = []

# Catch leftover (in case)
if temp:
    combined_logs.append(" ".join(temp))

# Parse logs
for log in combined_logs:
    match = log_pattern.search(log)

    if not match:
        malformed_count += 1
        continue

    year, month, day, time, action, protocol, src_ip, src_port, dst_ip, dst_port, pkt_size = match.groups()

    timestamp = f"{year}-{month}-{day} {time}"

    entry = {
        "timestamp": timestamp,
        "action": action,
        "protocol": protocol,
        "source_ip": src_ip,
        "source_port": int(src_port),
        "destination_ip": dst_ip,
        "destination_port": int(dst_port),
        "packet_size": int(pkt_size)
    }

    entries.append(entry)

    # Analysis tracking
    action_counter[action] += 1
    port_counter[dst_port] += 1
    ip_counter[src_ip] += 1

# ✅ SAFETY CHECK (prevents your crash)
if not entries:
    print("❌ No valid log entries found. Check your log format.")
    exit()

# Analysis
top_ports = port_counter.most_common(3)
suspicious_ips = {ip: count for ip, count in ip_counter.items() if count >= 3}

# Save CSV
with open(CSV_FILE, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=entries[0].keys())
    writer.writeheader()
    writer.writerows(entries)

# Save JSON
with open(JSON_FILE, "w") as f:
    json.dump(entries, f, indent=4)

# Save Threat Report
with open(THREAT_FILE, "w") as f:
    f.write(f"THREAT REPORT - Generated: {datetime.now()}\n")
    f.write("=" * 50 + "\n")
    f.write("Suspicious IPs (3+ log appearances)\n\n")

    if suspicious_ips:
        for ip, count in suspicious_ips.items():
            f.write(f"IP: {ip} | Occurrences: {count}\n")
    else:
        f.write("No suspicious IPs detected.\n")

# Terminal Report
print("=" * 60)
print("FIREWALL LOG ANALYSIS REPORT")
print("=" * 60)

print(f"Total entries processed : {len(combined_logs)}")
print(f"Valid entries parsed    : {len(entries)}")
print(f"Malformed entries skipped: {malformed_count}")

print("\n--- Action Summary ---")
print(f"ACCEPT : {action_counter['ACCEPT']}")
print(f"DROP   : {action_counter['DROP']}")

print("\n--- Top 3 Targeted Destination Ports ---")
for i, (port, count) in enumerate(top_ports, start=1):
    print(f"{i}. Port {port} — {count} hits")

print("\n--- Suspicious Source IPs (3+ appearances) ---")
if suspicious_ips:
    for ip, count in suspicious_ips.items():
        print(f"{ip} — {count} occurrences")
else:
    print("None")

print("\nOutput saved:")
print(CSV_FILE)
print(JSON_FILE)
print(THREAT_FILE)

print("=" * 60)
