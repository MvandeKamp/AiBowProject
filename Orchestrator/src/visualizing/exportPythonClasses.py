import os

def find_files_by_extensions(root_folder, extensions):
    matched_files = []
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                matched_files.append(os.path.join(dirpath, filename))
    return matched_files

def print_file_contents(file_paths):
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                print(f"{file_path}:\n{content}\n")
        except FileNotFoundError:
            print(f"Error: The file {file_path} does not exist.")
        except Exception as e:
            print(f"An error occurred while reading {file_path}: {e}")

# Example usage
root_folder = r'C:\Users\zerop\IdeaProjects\AiBowProject\src\main'
extensions = ['.py', '.ini', '.java', '.class', '.json', 'pack.mcmeta', '.proto',]  # List of file extensions to search for
file_paths = find_files_by_extensions(root_folder, extensions)
print_file_contents(file_paths)