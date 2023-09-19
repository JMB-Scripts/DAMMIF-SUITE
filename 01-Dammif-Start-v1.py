import os
import subprocess
import time

def main():
    print("############################################")
    print("Manual:")
    print("It will run Dammif and ask some silly questions")
    print("put the script with your *.out file.")
    print("Then the script will create one folder for each run (01...10..)")
    print("Try to run at least 10x dammif ideally 20 is good")
    print("Then you can use the Damsel.input-v6.sh script to get the final shape")
    print("JMB 2021")
    print("############################################")

    # Check the name of the gnome.out
    GN = next((filename for filename in os.listdir() if filename.endswith('.out')), None)

    if GN is None:
        print("No .out file found in the current directory.")
        return

    print(f"Is your P(r) file named {GN} (y/n)")
    resp = input()

    if resp.lower() == "n":
        print("Give the name of your P(r) file")
        GN = input()

    # User inputs
    print("Enter first model number (1, 2... 10... 20...)")
    i = int(input())
    print("Enter last model number")
    limit = int(input())
    print("##########################")

    sym = "P1"
    PS = input(f"Which symmetry needs to be applied (P1, P2, P3...) [default={sym}] ")
    PS = PS if PS else sym

    AN = "unknown"
    aniso = input(f"Enter the anisotropy of the shape [default={AN}] or enter P or O? ")
    aniso = aniso if aniso else AN

    default = 120
    RD = input(f"Enter the time in seconds between each run [default={default}] ")
    RD = int(RD) if RD else default

    print("##########################")

    print(f"We are going to run from {i} to {limit} with {PS} symmetry, {aniso} shape, and {RD} seconds in between. Proceed? (y/n)")
    resp = input()
    ten = 10

    if resp.lower() == "n":
        return
    else:
        while i <= limit:
            if i < ten:
                dir = f"0{i}"
            else:
                dir = str(i)

            # Check if the directory already exists
            if not os.path.exists(dir):
                os.mkdir(dir)
                os.chdir(dir)
                print(os.getcwd())
                subprocess.Popen(["dammif", f"-p={dir}", "-m=S", f"-s={PS}", f"-a={aniso}", "--shape=unknown", f"../{GN}"])
                time.sleep(RD)
                os.chdir("..")
                print(os.getcwd())
            else:
                print(f"Directory {os.path.abspath(dir)} already exists. Skipping...")

            i += 1

    print("# ALL DONE # you can analyze your data with Dammif-Analysis-vX.py, and start Damaver-vX.py")

if __name__ == "__main__":
    main()
