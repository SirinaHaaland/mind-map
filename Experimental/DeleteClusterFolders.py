import os
import shutil

def delete_cluster_folders(directory):
    
    subdirectories = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
    
    for subdirectory in subdirectories:
        if subdirectory.startswith('cluster'):
            target_dir = os.path.join(directory, subdirectory)
            try:
                shutil.rmtree(target_dir)
                print(f"Deleted directory: {target_dir}")
            except Exception as e:
                print(f"Error deleting directory {target_dir}: {e}")

if __name__ == "__main__":
    target_directory = '_Cluster'

    delete_cluster_folders(target_directory)
