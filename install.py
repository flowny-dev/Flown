class color:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    GRAY = "\033[90m"
    END = "\033[0m"
    BOLD = "\033[1m"

class console_messages:
    def clear():
        subprocess.run(["clear"])

    def info(message):
        print(f"{color.BLUE}[INFO]{color.END} {message}")

    def error(message):
        print(f"{color.RED}[ERROR]{color.END} {message}")

    def alert(message):
        print(f"{color.RED}[ALERT!] {message} {color.END}")

    def sucess(message):
        print(f"{color.GREEN}[SUCCESS!] {message} {color.END}")
    
    def check(message):
        print(f"✅ {message}")

    def uncheck(message):
        print(f"❌ {message}")
    
    def flown_info_screen():
        print(f"""{color.GRAY}Flown - 2.00 [PRVW]
Version under development! Thank you for your indulgence{color.END}
            
              
Do you want to install Flown? If you want to cancel, press 'Ctrl + C'""")
        input("Press 'enter' to continue!")
        
try:
    import subprocess
    import json
    import os
except ModuleNotFoundError:
    console_messages.error("The necessary python modules were not found")

class installation:
    def update_package():
        console_messages.info("Linux update in progress...")
        subprocess.run(["sudo", "apt", "update"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        console_messages.check("Done !")

    def install_package(package):
        console_messages.info(f"Installation of {package}...")
        subprocess.run(["sudo", "apt", "install", "-y", package], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        console_messages.check("Done !")

    def download_dependency(dependency): 
        console_messages.info(f"Downloading dependency from {dependency}")
        subprocess.run(["sudo", "curl", "-sS", dependency], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

class config:
    def check_root_access():
        if os.getuid() !=0:
            console_messages.error("You must run this script with root rights !")
            exit() ; return True
        else:
            return False

    def check_file_presence(file):
        if os.path.isfile(file):
            return True
        else:
            return False
        
    def create_flown_shortcut():
        try:
            with open("start-flown", "w") as file: 
                file.write("""Xephyr :2 -resizeable -fullscreen &
        sleep 10
        sudo -g root DISPLAY=:2 startplasma-x11 > /dev/null 2>&1 &
        sleep 10
        echo "Flown to start correctly, to close flown, run "kill-flown" in your terminal""")
            subprocess.run(["sudo", "mv", "start-flown", "/usr/local/bin"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            subprocess.run(["sudo", "chmod", "+x", "/usr/local/bin/start-flown"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        except Exception as a:
                    console_messages.error(f"""An unknown error has occurred
More details {a}""")
    try:
        with open("kill-flown", "w") as file: 
            file.write("""pkill Xephyr
        echo "Closure of Flown..." """)
        subprocess.run(["sudo", "mv", "kill-flown", "/usr/local/bin"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        subprocess.run(["sudo", "chmod", "+x", "/usr/local/bin/kill-flown"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    except Exception as a:
        console_messages.error(f"""An unknown error has occurred
More details {a}""")

def main():
    console_messages.clear()
    installation.update_package()

    installation.install_package("xserver-xephyr")
    installation.install_package("plasma-desktop")
    installation.install_package("mesa-utils")

    config.create_flown_shortcut()
    if config.check_file_presence("/usr/local/bin/start-flown"):
        if config.check_file_presence("/usr/local/bin/kill-flown"):
            console_messages.sucess("Shortcut created!")
    else:
        console_messages.alert("A problem occurred while creating the Flown launch shortcut.")
        
    console_messages.sucess("""The installation of Flownis complete!
You can launch Flown you can type in the terminal 'start-flown' and to close it 'kill-flown'""")

if __name__ == "__main__":
    try:
        console_messages.clear()
        config.check_root_access() # Remove Flown checks = potential danger
        console_messages.flown_info_screen()
        main()
    except Exception as a:
        console_messages.error(f"""An error occurred while executing the program
More details: {a}""")
        input("Press enter to exit")