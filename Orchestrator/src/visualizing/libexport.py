import os
import re

def list_installed_packages_with_versions(site_packages_path):
    if not os.path.exists(site_packages_path):
        print(f"Error: The path {site_packages_path} does not exist.")
        return

    # Regular expression to match .dist-info directories and extract package name and version
    dist_info_pattern = re.compile(r'^(.*?)-([\d\.]+.*)\.dist-info$')

    # Dictionary to store package names and their versions
    packages = {}

    # List all directories in site-packages
    for name in os.listdir(site_packages_path):
        full_path = os.path.join(site_packages_path, name)
        if os.path.isdir(full_path):
            match = dist_info_pattern.match(name)
            if match:
                package_name, version = match.groups()
                packages[package_name] = version
            else:
                # Add the package name without version if it's not a .dist-info directory
                if name not in packages:
                    packages[name] = None

    # Create a list of package names with versions
    package_list = []
    for package, version in packages.items():
        if version:
            package_list.append(f"{package}-{version}")
        else:
            package_list.append(package)

    # Join the package names into a comma-separated string
    packages_csv = ', '.join(package_list)

    print("Installed packages with versions:")
    print(packages_csv)

# Example usage
site_packages_path = r'C:\Users\zerop\IdeaProjects\AiBowProject\Orchestrator\venv\Lib\site-packages'  # Use raw string to handle backslashes
list_installed_packages_with_versions(site_packages_path)