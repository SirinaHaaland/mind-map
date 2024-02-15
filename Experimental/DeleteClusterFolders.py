import os
import shutil

def delete_cluster_folders(directory):
    # List all directories in the specified directory
    subdirectories = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
    
    # Delete directories that start with "cluster"
    for subdirectory in subdirectories:
        if subdirectory.startswith('cluster'):
            target_dir = os.path.join(directory, subdirectory)
            try:
                # Remove the directory
                shutil.rmtree(target_dir)
                print(f"Deleted directory: {target_dir}")
            except Exception as e:
                print(f"Error deleting directory {target_dir}: {e}")

if __name__ == "__main__":
    # Directory containing the folders to be deleted
    target_directory = '_Cluster'  # Change this to your desired directory
    
    # Delete cluster folders
    delete_cluster_folders(target_directory)
