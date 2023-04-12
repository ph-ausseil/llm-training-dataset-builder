#!/bin/bash

# Get the directory path from the command line argument or use the current directory
dir_path=${1:-.}

# Find all first-level directories in the specified directory
find "$dir_path" -mindepth 1 -maxdepth 1 -type d | while read -r folder; do
  # Calculate the size of each file and group them by their file extensions
  find "$folder" -type f -exec stat -f "%z %N" {} \; | \
  gawk -v folder="$folder" '
  {
      # Get the file extension
      ext = match($2, /\.([^.]*)$/, arr) ? arr[1] : "No extension";
      # Accumulate the file size for each file extension
      file_sizes[ext] += $1
  }
  END {
      # Sort the file sizes in descending order
      n = asort(file_sizes, sorted_file_sizes, "@val_num_desc");

      # Print the folder name
      printf("\nFolder: %s\n", folder);

      # Print the total file size for each file extension in descending order
      for (i = 1; i <= n; i++) {
          ext = sorted_file_sizes[i];
          printf("Extension: .%s - Total weight: %d bytes\n", ext, file_sizes[ext]);
      }
  }
  '
done
