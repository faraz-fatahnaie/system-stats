#!/bin/bash

# Get the directory path where the script is located
script_dir="$(cd "$(dirname "$0")" && pwd)"

# Directory path
directory="$script_dir"

# Check if directory exists
if [ -d "$directory" ]; then
    # Change permissions
    sudo chmod u+w "$directory"

    # Check ownership
    owner=$(stat -c "%U" "$directory")
    current_user=$(whoami)

    if [ "$owner" != "$current_user" ]; then
        # Change ownership
        sudo chown "$current_user" "$directory"
    fi

    echo "Permissions and ownership updated successfully for $directory."
else
    echo "Directory $directory does not exist."
fi
