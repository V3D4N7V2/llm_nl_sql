import json
import os
import requests

# Define subdirectory and file path
subdirectory = "data"
file_path = os.path.join(subdirectory, "dataset_info.json")

# Ensure the subdirectory exists
os.makedirs(subdirectory, exist_ok=True)

# Initialize or load JSON data
try:
    with open(file_path, "r") as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"Error: {file_path} not found. Creating a new file.")
    data = {}

# List of file download links
links = [
    "https://raw.githubusercontent.com/V3D4N7V2/filedump/refs/heads/main/output2XOXO.json",
    # "https://example.com/file2.txt"
    # Add more links as needed
]

# Loop through each link and download the file
for link in links:
    try:
        # Extract the filename from the URL
        filename = link.split("/")[-1]
        local_path = os.path.join(subdirectory, filename)

        # Download the file
        response = requests.get(link, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors

        with open(local_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Downloaded {filename} to {local_path}.")

        # Extract the filename without extension
        entry_key = os.path.splitext(filename)[0]

        # Define the new entry to add
        new_entry_value = {"file_name": filename}

        # Update the JSON data with the new entry
        data[entry_key] = new_entry_value

        print(f"Added {entry_key} to the dataset info.")

    except requests.RequestException as e:
        print(f"Failed to download {link}: {e}")

# Write the updated JSON back to the file in the subdirectory
with open(file_path, "w") as file:
    json.dump(data, file, indent=2)

print(f"Final data saved to {file_path}.")
