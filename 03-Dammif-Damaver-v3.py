import os
import subprocess
import shutil
import time

print("############################################")
print("Manual:")
print("It will run Damaver from Dammif-Start-vx.sh using the default option")
print("Better to run it through a screen")
print("The script will copy all *-1.cif in one Damaver-X-Y folder")
print("############################################")

# Check the name of the gnome.out
files = [filename for filename in os.listdir() if filename.endswith('.out')]

if not files:
    print("No .out file found in the current directory.")
    exit()

GN = files[0]

print(f"Is your P(r) file named {GN} (y/n)")
resp = input()

if resp.lower() == "n":
    print("Give the name of your P(r) file")
    exit()

# Ask which folder to use
print("")
print("Enter first folder number (1, 2... 10... 20...)")
min = int(input())
print("Enter last folder number")
max = int(input())
print("##########################")
sym = "P1"
PS = input(f"Which symmetry need to be applied (P1, P2, P3....) [default={sym}] ")
PS = PS if PS else sym

# Check if the user is happy with the option
print(f"Average from folder {min} to {max} with {PS} (y/n)")
resp = input()

if resp.lower() == "n":
    print("See you")
    exit()

##############################
ten = 10

# Test if the Damaver folder exists
damf = f"Damaver-{min}-{max}/"
if os.path.exists(damf):
    print("The folder exists. Rename it to proceed.")
    exit()
else:
    os.mkdir(damf)

# Initialize i
i = min

# Copy the PDB from folders
while i <= max:
    if i < ten:
        folder = f"0{i}"
    else:
        folder = str(i)
    
    files_to_copy = [file for file in os.listdir(folder) if file.endswith("-1.cif")]
    
    for file in files_to_copy:
        source_path = os.path.join(folder, file)
        destination_path = os.path.join(damf, file)
        shutil.copyfile(source_path, destination_path)
    
    i += 1

# Sleep for 5 seconds
print("Sleeping for 5 seconds...")
time.sleep(5)

# Launch Damaver in Damaver-$min-$max
os.chdir(damf)
# create a scrpt to launch damaver 
damaver_name = f"damaver-{min_}-{max}.sh"
with open(pymol_name, "w") as f:
        f.write("damaver *.cif")
# Add the shebang line as the first line of pymol-XX-YY.sh
    if os.path.exists(damaver_name):
        with open(damaver_name, "r") as f:
            content = f.read()
            content = "#!/bin/sh\n" + content  # Add the shebang line
        with open(damaver_name, "w") as f:
            f.write(content)         

# Make the launcher script executable
    os.chmod(damaver_name, 0o755)
    # Launch Pymol
    path_to_script=f'./{pymol_name}'
    subprocess.run(path_to_script, check=False)
############
print(f"when it's done run Dammin as follows:")
print(f"dammin ../{GN} --mo=S --sy={PS} --lo=man --svfile=damaver-global-damstart.cif")
#subprocess.run([f"dammin ../{GN} --mo=S --sy={PS} --lo=man --svfile=damaver-global-damstart.cif"])
#print("C'est tout pour moi")

