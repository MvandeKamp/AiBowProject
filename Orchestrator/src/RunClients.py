import os
import subprocess
import uuid
import time
import pygetwindow as gw
import pyautogui
import shutil
import nbtlib
import minecraft_launcher_lib

# Configuration
minecraft_version = '1.21.1-forge-52.0.8'
minecraft_dir = 'C:\\Users\\zerop\\AppData\\Roaming\\.minecraft'  # Update this path
base_username = 'Client'
base_access_token = 'YourAccessToken'  # Replace with a valid access token

java_path = 'C:\\Program Files\\Java\\jdk-21\\bin\\java.exe'

minecraft_version_dir = os.path.join(minecraft_dir, 'versions', minecraft_version)
minecraft_jar = os.path.join(minecraft_version_dir, f'{minecraft_version}.jar')
original_world_dir = 'C:\\Users\\zerop\\AppData\\Roaming\\.minecraft\\saves\\AiTrain'


# Function to generate a unique UUID for each client
def generate_uuid():
    return str(uuid.uuid4())

def create_world_copy(client_name):
    saves_dir = os.path.join(minecraft_dir, "saves")
    client_world_dir = os.path.join(saves_dir, client_name)

    # Check if the client world directory already exists
    if os.path.exists(client_world_dir):
        # Delete the existing directory
        shutil.rmtree(client_world_dir)

    # Copy the original world directory to the client world directory
    shutil.copytree(original_world_dir, client_world_dir)

    # Modify the level.dat to set the world name
    level_dat_path = os.path.join(client_world_dir, 'level.dat')
    if os.path.exists(level_dat_path):
        nbt_file = nbtlib.load(level_dat_path)
        nbt_file['Data']['LevelName'] = nbtlib.String(client_name)
        nbt_file.save()

    return client_world_dir


# Function to launch a Minecraft instance
def launch_minecraft_instance(client_number):
    username = f"{base_username}{client_number}"
    client_uuid = generate_uuid()
    access_token = base_access_token  # Use a valid access token

    # Create a copy of the world for this client
    client_world_dir = create_world_copy(username)

    options = {
        "username": username,
        "uuid": client_uuid,
        "token": access_token,
        "jvmArguments": [
            '-Xms512m',
            '-Xmx1g'
        ]
    }
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(minecraft_version, minecraft_dir, options)
    # Launch the process
    process = subprocess.Popen(minecraft_command)
    return process, client_world_dir


# Function to arrange windows in a 3x3 grid
def arrange_windows(instanceAmount):
    time.sleep(15)
    time.sleep(instanceAmount * 2)  # Wait for windows to open
    screen_width, screen_height = pyautogui.size()
    grid_width = screen_width // 3
    grid_height = screen_height // 3

    positions = [(x * grid_width, y * grid_height) for y in range(3) for x in range(3)]

    windows = gw.getWindowsWithTitle('Minecraft')
    for win, (x, y) in zip(windows, positions):
        win.moveTo(x, y)
        win.resizeTo(grid_width, grid_height)


# Launch 9 instances in a 3x3 grid
processes = []
client_world_dirs = []
instanceAmount = 4
for i in range(1, instanceAmount + 1):
    process, client_world_dir = launch_minecraft_instance(i)
    processes.append(process)
    client_world_dirs.append(client_world_dir)
    time.sleep(instanceAmount / 2)  # Slight delay to stagger launches

arrange_windows(instanceAmount)

# Wait for all processes to close
for process in processes:
    process.wait()

# Remove all client world directories after all processes have closed
for client_world_dir in client_world_dirs:
    if os.path.exists(client_world_dir):
        shutil.rmtree(client_world_dir)