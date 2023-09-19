import os
import subprocess

# Input parameters
print("############################################")
print("Manual:")
print("Create a report of Chi^2 and display models in Pymol")
print("############################################")
min_model = input("Enter first model number (01, 02, ... 10, 20, ...): ")
max_model = input("Enter last model number: ")
print("###########################")

# Output file
output_file = f"Dammif-{min_model}-{max_model}-chi2.txt"

# 1- Regroup the Chi^2 values in the text file
try:
    # Remove the old output file if present
    if os.path.exists(output_file):
        os.remove(output_file)

    # Add the meaning of the columns in the output file
    with open(output_file, "w") as f:
        f.write("file_name chi2_value\n")

    # Return the Chi^2 value for each file in the specified range
    for i in range(int(min_model), int(max_model) + 1):
        model_number = f"{i:02d}"

        for root, _, files in os.walk(model_number):
            for file in files:
                if file.endswith(".fir"):
                    file_path = os.path.join(root, file)
                    file_name = os.path.basename(file_path)

                    with open(file_path, "r") as f:
                        for line in f:
                            if "Chi^2=" in line:
                                chi2_value = line.split("Chi^2=")[1].strip()
                                with open(output_file, "a") as output:
                                    output.write(f"{file_name} {chi2_value}\n")

except Exception as e:
    print(f"An error occurred: {str(e)}")

# 2- Pymol
print("###########################")

# Check if Pymol is in the PATH
try:
    subprocess.run(["pymol", "--version"], check=True)
    print("Pymol is in your PATH.")
except subprocess.CalledProcessError:
    print("Pymol is not in your PATH. Please add it to your PATH.")

# Clean up old files
try:
    for old_file in ["a.pml", "tmp.txt"]:
        if os.path.exists(old_file):
            os.remove(old_file)

    # Setup the display in a Pymol script (a.pml)
    with open("a.pml", "w") as f:
        f.write('cmd.hide("everything","all")\n')
        f.write('cmd.show("spheres","all")\n')
        f.write('util.mass_align("01-1",0,_self=cmd)\n')
        f.write('cmd.delete("aln_all_to_01-1")\n')
        f.write('\n')

    # Create the Pymol launcher script (pymol-XX-YY.sh)
    pymol_name = f"pymol-{min_model}-{max_model}.sh"
    with open(pymol_name, "w") as f:
        f.write("pymol\n")
        for i in range(int(min_model), int(max_model) + 1):
            model_number = f"{i:02d}"
            for root, _, files in os.walk(model_number):
                for file in files:
                    if file.endswith(".cif"):
                        f.write(os.path.join(root, file) + " ")
        f.write("a.pml\n")

    # Replace carriage returns with spaces in pymol-XX-YY.sh
   
    if os.path.exists(pymol_name):
        with open(pymol_name, "r") as f:
            content = f.read()
            content = content.replace("\n", " ")
        with open(pymol_name, "w") as f:
            f.write(content)

   # Add the shebang line as the first line of pymol-XX-YY.sh
    if os.path.exists(pymol_name):
        with open(pymol_name, "r") as f:
            content = f.read()
            content = "#!/bin/sh\n" + content  # Add the shebang line
        with open(pymol_name, "w") as f:
            f.write(content)         
    
    # Make the launcher script executable
    os.chmod(pymol_name, 0o755)

    # Launch Pymol
    path_to_script=f'./{pymol_name}'
    subprocess.run(path_to_script, check=False)

except Exception as e:
    print(f"An error occurred: {str(e)}")
