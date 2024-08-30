import ftplib
from termcolor import colored
import sys
import os

# Pastikan encoding yang benar digunakan untuk output ke konsol
sys.stdout.reconfigure(encoding='utf-8')

# Mengatur flag debug (nonaktifkan debug)
DEBUG = False

# Fungsi untuk membersihkan terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fungsi untuk mengatur title terminal
def set_terminal_title():
    if os.name == 'nt':  # Jika Windows
        os.system('title FTP Checker by kliverz')
    else:  # Jika Linux/MacOS
        print("\033]0;FTP Checker by kliverz\007")

# Fungsi untuk menampilkan banner dan title
def display_banner():
    banner = r"""
███████╗████████╗██████╗      ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
██╔════╝╚══██╔══╝██╔══██╗    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
█████╗     ██║   ██████╔╝    ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
██╔══╝     ██║   ██╔═══╝     ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
██║        ██║   ██║         ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
╚═╝        ╚═╝   ╚═╝          ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
"""
    print(colored(banner, "green"))
    print(colored("--> Use format : host:21:user:password\n", "yellow"))

# Fungsi untuk mencoba login ke FTP dan menyimpan hasil sukses
def check_ftp_login(ftp_host, ftp_port, ftp_user, ftp_pass):
    if DEBUG:
        print(colored(f"Debug: Attempting to connect to {ftp_host}:{ftp_port}", "cyan"))

    try:
        print(colored(f"Connecting to {ftp_host} on port {ftp_port}...", "yellow"))
        ftp = ftplib.FTP()
        ftp.connect(ftp_host, ftp_port, timeout=10)
        if DEBUG:
            print(colored(f"Debug: Connected to {ftp_host}:{ftp_port}", "cyan"))

        ftp.login(ftp_user, ftp_pass)
        print(colored(f"Login successful for {ftp_user}@{ftp_host}", "green"))

        # Simpan hasil sukses ke file
        with open('successful_logins.txt', 'a', encoding='utf-8') as f:
            f.write(f"{ftp_host}:{ftp_port}:{ftp_user}:{ftp_pass}\n")

        # Coba untuk mendapatkan daftar file di direktori root FTP
        try:
            files = ftp.nlst()  # Mendapatkan daftar file di direktori root
            file_list = files[:5]  # Ambil 5 file pertama
            with open('ftp_file_list.txt', 'a', encoding='utf-8') as f:
                f.write(f"FTP server: {ftp_host}:{ftp_port}\n")
                for file in file_list:
                    f.write(f"{file}\n")
                    print(colored(f"File: {file}", "cyan"))  # Tampilkan di konsol
                f.write("\n")  # Tambahkan baris kosong untuk pemisah antara server
            print(colored("File list saved to 'ftp_file_list.txt'", "green"))
        except ftplib.error_perm as e:
            print(colored(f"Could not list files on {ftp_host}: {str(e)}", "red"))

        ftp.quit()
        if DEBUG:
            print(colored(f"Debug: Closed FTP connection to {ftp_host}", "cyan"))

    except ftplib.all_errors as e:
        print(colored(f"Login failed for {ftp_user}@{ftp_host}: {str(e)}", "red"))
        if DEBUG:
            print(colored(f"Debug: Login failed for {ftp_user}@{ftp_host}: {str(e)}", "cyan"))

# Membaca file list FTP
def read_ftp_list(file):
    if DEBUG:
        print(colored(f"Debug: Reading FTP list from file {file}", "cyan"))

    try:
        with open(file, 'r', encoding='utf-8') as f:
            print(colored("Starting FTP login checks...", "blue"))
            for line in f:
                line = line.strip()
                parts = line.split(':')
                if len(parts) == 4:
                    ftp_host, ftp_port, ftp_user, ftp_pass = parts
                    ftp_port = int(ftp_port)  # Pastikan port adalah integer
                    check_ftp_login(ftp_host, ftp_port, ftp_user, ftp_pass)
                else:
                    print(colored(f"Invalid entry: {line}", "red"))
            print(colored("Finished checking all FTP entries.", "blue"))
        if DEBUG:
            print(colored(f"Debug: Finished processing file {file}", "cyan"))
    except FileNotFoundError:
        print(colored(f"File '{file}' not found!", "red"))
        if DEBUG:
            print(colored(f"Debug: File '{file}' not found!", "cyan"))

# Main program
if __name__ == "__main__":
    clear_terminal()
    set_terminal_title()
    display_banner()

    while True:
        file = input(colored("FTP list file (or type 'exit' to quit): ", "cyan")).strip()
        if file.lower() == 'exit':
            print(colored("Exiting program...", "green"))
            break
        read_ftp_list(file)
