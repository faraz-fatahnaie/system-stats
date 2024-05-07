#!/bin/bash

# ./update_permissions.sh /home/ubuntu/monitor

# Check if directory parameter is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Directory path
directory="$1"

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