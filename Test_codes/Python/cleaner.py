import os
import shutil

# 1. SETUP: Where do you want to clean? 
# Use a specific folder path. For now, let's use the current folder where this script is.
folder_to_clean = os.getcwd() 

# 2. DEFINE RULES: Which extensions go where?
directories = {
    "Images": [".jpeg", ".jpg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".csv"],
    "Software": [".exe", ".msi", ".zip", ".apk"],
    "Videos": [".mp4", ".mkv", ".avi"]
}

def clean_folder():
    print(f"🧹 Starting cleanup in: {folder_to_clean}")
    
    # Loop through every file in the folder
    for filename in os.listdir(folder_to_clean):
        
        # Skip this script itself so we don't move it!
        if filename == "cleaner.py":
            continue
            
        # Get the file extension (e.g., '.pdf')
        file_ext = os.path.splitext(filename)[1].lower()
        
        # Check against our rules
        for category, extensions in directories.items():
            if file_ext in extensions:
                
                # Make the category folder if it doesn't exist (e.g., create "Images" folder)
                category_path = os.path.join(folder_to_clean, category)
                os.makedirs(category_path, exist_ok=True)
                
                # Move the file
                old_path = os.path.join(folder_to_clean, filename)
                new_path = os.path.join(category_path, filename)
                
                try:
                    shutil.move(old_path, new_path)
                    print(f"Moved: {filename} -> {category}/")
                except Exception as e:
                    print(f"Error moving {filename}: {e}")
                
                break # Stop checking other categories for this file

    print("✨ Cleanup Complete! Time to sleep.")

if __name__ == "__main__":
    clean_folder()