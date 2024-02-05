import os
import shutil

def copy_files(source_folder, destination_folder):
    # Create the destination directory if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)
    
    # Walk through the source folder recursively
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            source_path = os.path.join(root, file)
            dest_path = os.path.join(destination_folder, file)
            
            # Copy the file
            shutil.copy2(source_path, dest_path)
            print(f"File copied: {dest_path}")

# Set the source and destination folders
source_folder = 'data'
destination_folder = 'all_images'

# Call the function to copy files
copy_files(source_folder, destination_folder)
