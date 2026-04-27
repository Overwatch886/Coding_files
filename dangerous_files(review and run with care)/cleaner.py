import os
import shutil
import tkinter as tk
from tkinter import filedialog

# 1. SETUP: Where do you want to clean? 
# CHANGE THIS to your target folder - NEVER use os.getcwd() without explicit confirmation!
folder_to_clean = None

# 2. CRITICAL FOLDERS TO AVOID (always skip these)
CRITICAL_FOLDERS = {
    "Windows", "Program Files", "Program Files (x86)", "ProgramData",
    "AppData", "System32", "SysWOW64", "Microsoft", "Intel", "AMD"
}

# 3. DEFINE RULES: Which extensions go where?
directories = {
    "Images": [".jpeg", ".jpg", ".png", ".gif", ".ico", ".htm", ".html"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".csv", ".tsv", ".pptx", ".srt"],
    "Software": [".exe", ".msi", ".zip", ".apk"],
    "Videos": [".mp4", ".mkv", ".avi", ".webm"],
    "Audios": [".mp3", ".aac", ".m4a"],
    "Code": [".py", ".css", ".js", ".r"]
}

def folder_contains_exe(folder_path):
    """Check if folder (or any parent up to root) contains .exe files"""
    try:
        current = os.path.abspath(folder_path)
        root_path = os.path.abspath(folder_to_clean)
        
        # Check current folder and all parents up to the root we're cleaning
        while current != os.path.dirname(current):  # Stop at root
            # Check if current folder contains .exe files
            if os.path.isdir(current):
                for item in os.listdir(current):
                    if item.lower().endswith('.exe'):
                        return True
            
            # Stop if we've reached the root of our cleaning operation
            if current == root_path:
                break
                
            current = os.path.dirname(current)
        return False
    except (PermissionError, OSError):
        return True  # If we can't check, assume it's critical and skip

def is_critical_folder(folder_path):
    """Check if folder is in our critical folders list"""
    folder_name = os.path.basename(folder_path)
    return folder_name in CRITICAL_FOLDERS

def should_skip_folder(folder_path):
    """Determine if we should skip this folder. Returns (should_skip, reason)"""
    # Skip critical system folders
    if is_critical_folder(folder_path):
        return (True, "critical folder")
    
    # Skip folders containing .exe files (your idea!)
    if folder_contains_exe(folder_path):
        return (True, "contains .exe")
    
    return (False, None)

def choose_folder_to_clean():
    """Open a folder picker dialog and return the selected path (or None if canceled)."""
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        selected_folder = filedialog.askdirectory(title="Select folder to clean")

        root.destroy()

        if selected_folder:
            return os.path.abspath(selected_folder)
        return None
    except Exception as e:
        print(f"Could not open folder picker window: {e}")
        return None

def clean_folder():
    print(f"🧹 Starting cleanup in: {folder_to_clean}")
    
    # Safety confirmation
    print(f"⚠️  Target: {os.path.abspath(folder_to_clean)}")
    response = input("Continue? (yes/no): ")
    if response.lower() != "yes":
        print("Aborted.")
        return
    
    skipped_folders = {}  # Dict: {folder_path: reason}
    
    # Loop through every file in the folder
    for root, dirs, files in os.walk(folder_to_clean, topdown=True):
        # Check if we should skip this folder
        should_skip, reason = should_skip_folder(root)
        if should_skip:
            skipped_folders[root] = reason
            # Remove from dirs so os.walk won't descend into it
            dirs[:] = []
            continue
        
        # Also skip subdirectories that are critical
        dirs_to_keep = []
        for d in dirs:
            subdir_path = os.path.join(root, d)
            should_skip_subdir, reason = should_skip_folder(subdir_path)
            if should_skip_subdir:
                skipped_folders[subdir_path] = reason
            else:
                dirs_to_keep.append(d)
        dirs[:] = dirs_to_keep
        
        for filename in files:
            # Skip this script itself
            if filename == "cleaner.py":
                continue
            
            # Get the file extension (e.g., '.pdf')
            file_ext = os.path.splitext(filename)[1].lower()
            
            # Check against our rules
            for category, extensions in directories.items():
                if file_ext in extensions:
                    # Make the category folder if it doesn't exist
                    category_path = os.path.join(folder_to_clean, category)
                    os.makedirs(category_path, exist_ok=True)
                    
                    # Move the file
                    old_path = os.path.join(root, filename)
                    new_path = os.path.join(category_path, filename)
                    
                    try:
                        if old_path == new_path:
                            pass
                        else:
                            shutil.move(old_path, new_path)
                            print(f"Moved: {filename} -> {category}/")
                    except Exception as e:
                        print(f"Error moving {filename}: {e}")
                    
                    break  # Stop checking other categories for this file

    if skipped_folders:
        print(f"\n⚠️  Skipped {len(skipped_folders)} folders:")
        for folder_path, reason in sorted(skipped_folders.items()):
            print(f"   - {folder_path} ({reason})")
    
    print("✨ Cleanup Complete!")

def delete_empty_folders():
    print("Deleting empty folders")
    skipped_count = 0
    
    for root, dirs, files in os.walk(folder_to_clean, topdown=False):
        # Don't delete critical folders
        if should_skip_folder(root):
            skipped_count += 1
            continue
            
        for d in dirs:
            dirpath = os.path.join(root, d)
            # Never remove the base folder itself
            if os.path.abspath(dirpath) == os.path.abspath(folder_to_clean):
                continue
            
            # Don't delete critical folders
            if should_skip_folder(dirpath):
                continue
                
            try:
                if not os.listdir(dirpath):
                    os.rmdir(dirpath)
                    print(f"Removed empty folder: {dirpath}")
            except Exception as e:
                print(f"Could not remove {dirpath}: {e}")
    
    if skipped_count > 0:
        print(f"Skipped {skipped_count} critical/executable folders")

if __name__ == "__main__":
    folder_to_clean = choose_folder_to_clean()

    if not folder_to_clean:
        print("No folder selected. Aborted.")
        raise SystemExit(0)

    clean_folder()
    delete_empty_folders()