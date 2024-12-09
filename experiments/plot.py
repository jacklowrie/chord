import matplotlib.pyplot as plt
import numpy as np

# File path
file_path = "/tmp/h16n.log"  # Replace with your actual .log file path

# Initialize lists to store keys and hops
keys = []
hops = []

# Read the .log file and parse the data
with open(file_path, 'r') as f:
    for line in f:
        # Check if the line matches the expected format
        if ':' in line:
            try:
                key, hop = map(int, line.strip().split(':'))
                keys.append(key)
                hops.append(hop)
            except ValueError:
                print(f"Skipping invalid line: {line.strip()}")

# Print a summary of the data
print(f"Loaded {len(keys)} data points.")

# Compute statistics
average_hops = np.mean(hops)
max_hops = np.max(hops)
min_hops = np.min(hops)

print(f"Average Hops: {average_hops}")
print(f"Max Hops: {max_hops}")
print(f"Min Hops: {min_hops}")

# Plot the data
plt.figure(figsize=(12, 7))
plt.plot(keys, hops, marker='o', linestyle='-', markersize=3, label="Hops per Key")

# Highlight average, max, and min hops
plt.axhline(y=average_hops, color='r', linestyle='--', label=f"Average Hops: {average_hops:.2f}")
plt.axhline(y=max_hops, color='g', linestyle='--', label=f"Max Hops: {max_hops}")
plt.axhline(y=min_hops, color='b', linestyle='--', label=f"Min Hops: {min_hops}")

# Annotate the statistics on the plot
plt.text(0.95 * max(keys), average_hops, f"Avg: {average_hops:.2f}", color="red", fontsize=10)
plt.text(0.95 * max(keys), max_hops, f"Max: {max_hops}", color="green", fontsize=10)
plt.text(0.95 * max(keys), min_hops, f"Min: {min_hops}", color="blue", fontsize=10)

# Add labels, title, and legend
plt.xlabel("Keys")
plt.ylabel("Hops")
plt.text(0.05 * max(keys), max_hops, "n = 16", fontsize=12, color="black", bbox=dict(facecolor='white', alpha=0.5))
plt.title("Chord Lookup: Keys vs. Hops")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

# Save the plot as an image (optional)
output_image = "keys_vs_hops_with_stats_n16.png"
plt.savefig(output_image, dpi=300)
print(f"Plot saved as {output_image}")
