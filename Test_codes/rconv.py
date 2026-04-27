import json

# Replace with your notebook filename
notebook_file = "/storage/EFD6-7824/Documents/Coding_Files/Group_3.ipynb"
output_file = "/storage/EFD6-7824/Documents/Coding_Files/my_notebook.R"

# Load the notebook
with open(notebook_file, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Extract all code cells
r_code_cells = []
for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        r_code_cells.append("".join(cell["source"]))

# Combine all code into one string
r_code = "\n\n".join(r_code_cells)

# Save as .R script
with open(output_file, "w", encoding="utf-8") as f:
    f.write(r_code)

print(f"R script saved as {output_file}")
