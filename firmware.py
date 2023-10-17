import sys
import os
import base64
import threading
import requests
import time
import subprocess
from threading import Thread, Event
from io import BytesIO
from PIL import ImageTk, Image
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog

script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

adb_path = os.path.join(script_dir, "bin", "adb.exe")

oem_path = os.path.join(script_dir, "bin", "OEM_Checker.bat")

subprocess.run([adb_path, 'devices'], capture_output=False, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

def run_adb_command(command):
    try:
        result = subprocess.check_output(
            command, 
            shell=True, 
            text=True, 
            stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return result.strip()
    except subprocess.CalledProcessError as e:
        return None

def check_oem():

    subprocess.run([oem_path], capture_output=False, text=True)

def close_root():
    check.destroy()

def download_firmware():
    global download_window
    download_window = tk.Toplevel()
    download_window.title("Download Firmware")
    download_window.geometry("300x200")

    choose_label = tk.Label(download_window, text="Choose your Device")
    choose_label.pack(pady=10)

    pico3_button = tk.Button(download_window, text="Pico 3", command=open_pico3_window)
    pico4_button = tk.Button(download_window, text="Pico 4", command=open_pico4_window)

    pico3_button.pack(pady=5)
    pico4_button.pack(pady=5)

def open_pico4_window():
    download_window.destroy()
    global pico4_window
    pico4_window = tk.Toplevel()
    pico4_window.title("Choose OEM State")
    pico4_window.geometry("300x200")

    pico4_label = tk.Label(pico4_window, text="Choose your OEM State")
    pico4_label.pack(pady=10)

    oem_button = tk.Button(pico4_window, text="Pico 4 OEM", command=open_oem_window)
    nonoem_button = tk.Button(pico4_window, text="Pico 4 non_OEM", command=open_nonoem_window)

    oem_button.pack(pady=5)
    nonoem_button.pack(pady=5)
      
def open_pico3_window():
    download_window.destroy()

    pico3_window = tk.Toplevel()
    pico3_window.title("Pico 3 Firmware")

    global_label = tk.Label(pico3_window, text="Pico 3 Global")
    global_label.pack(pady=10)

    versions = [
        ("5.2.2", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico3/A7H10/beta/5.2.2-202212020144-RELEASE-user-neo3-b2405-e2f0482a98.zip"),
        ("5.2.3", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico3/A7H10/beta/5.2.3-202212090601-RELEASE-user-neo3-b2475-c8012b4f3e.zip"),
        ("5.4.2", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico3/A7H10/beta/5.4.2-202302022115-RELEASE-user-neo3-b2878-1b00056c1a.zip"),
        ("5.4.3", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico3/A7H10/beta/5.4.3-202302090023-RELEASE-user-neo3-b2915-5869286510.zip"),
        ("5.4.4", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico3/A7H10/beta/5.4.4-202302161153-RELEASE-user-neo3-b2967-6d52eaeb58.zip"),
        ("5.5.2", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico3/A7H10/beta/5.5.2-202303210021-RELEASE-user-neo3-b3186-5df5f0d193.zip"),
        ("5.5.3", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico3/A7H10/beta/5.5.3-202303281900-RELEASE-user-neo3-b3222-0bbea8b7fe.zip"),
        ("5.5.4", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico3/A7H10/beta/5.5.4-202304060113-RELEASE-user-neo3-b3309-8a1d186f01.zip"),
        ("5.6.0", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico3/A7H10/beta/5.6.0-202304181715-RELEASE-user-neo3-b3357-749f1c9d49.zip"),
        ("5.6.1", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico3/A7H10/beta/5.6.1-202304240021-RELEASE-user-neo3-b3381-4715c18385.zip"),
        ("5.6.2", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico3/A7H10/beta/5.6.2-202305101525-RELEASE-user-neo3-b3433-0a4ee1a5cf.zip"),
        ("5.6.3", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico3/A7H10/beta/5.6.3-202305190333-RELEASE-user-neo3-b3484-31441931eb.zip")
    ]

    for version, download_link in versions:
        version_button = tk.Button(pico3_window, text=version, command=lambda v=version, dl=download_link: download_firmware_thread(v, dl))
        version_button.pack(pady=5)

def open_oem_window():
    pico4_window.destroy()

    oem_window = tk.Toplevel()
    oem_window.title("Pico 4 OEM")

    global_label = tk.Label(oem_window, text="Pico 4 Global OEM")
    global_label.pack(pady=10)

    versions = [
        ("5.2.7", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico4/global/5.2.7-202212020445-RELEASE-user-phoenix-b2122-a15f46c085.zip"),
        ("5.3.1", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico4/global/5.3.1-202301051855-RELEASE-user-phoenix-b2672-e5008f4620.zip"),
        ("5.3.2", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico4/global/5.3.2-202301071817-RELEASE-user-phoenix-b2705-0d2c0cb6ec.zip"),
        ("5.4.0", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico4/global/5.4.0-202302171231-RELEASE-user-phoenix-b3159-21724b5b8e.zip"),
        ("5.5.0b", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico4/global/5.5.0-202303210100-RELEASE-user-phoenix-b3599-11e7c04f27.zip"),
        ("5.5.0", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico4/global/5.5.0-202304070244-RELEASE-user-phoenix-b3843-412cf6f56c.zip"),
        ("5.6.0b", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico4/global/5.6.0-202304240057-RELEASE-user-phoenix-b4030-5c2f151137.zip"),
        ("5.6.0", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico4/global/5.6.0-202305190440-RELEASE-user-phoenix-b4261-1a0a729e58.zip")
    ]

    for version, download_link in versions:
        version_button = tk.Button(oem_window, text=version, command=lambda v=version, dl=download_link: download_firmware_thread(v, dl))
        version_button.pack(pady=5)

def open_nonoem_window():
    pico4_window.destroy()

    nonoem_window = tk.Toplevel()
    nonoem_window.title("Pico 4 non_OEM")

    global_label = tk.Label(nonoem_window, text="Pico 4 Global non_OEM")
    global_label.pack(pady=10)

    versions = [
        ("5.2.7", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico4/global/non_oem/5.2.7-202212020323-RELEASE-user-phoenix-b2119-09638d5e07.zip"),
        ("5.3.1", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico4/global/non_oem/5.3.1-202301051632-RELEASE-user-phoenix-b2667-6c560f9e2b.zip"),
        ("5.3.2", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico4/global/non_oem/5.3.2-202301071642-RELEASE-user-phoenix-b2704-ae2fa5f1b3.zip"),
        ("5.4.0", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico4/global/non_oem/5.4.0-202302171557-RELEASE-user-phoenix-b3162-3d2f0dbe1b.zip"),
        ("5.5.0b", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico4/global/non_oem/5.5.0-202303210013-RELEASE-user-phoenix-b3597-4335638970.zip"),
        ("5.5.0", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico4/global/non_oem/5.5.0-202304070533-RELEASE-user-phoenix-b3850-bf9813ff5d.zip"),
        ("5.6.0b", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico4/global/non_oem/5.6.0-202304240012-RELEASE-user-phoenix-b4029-989010bca0.zip"),
        ("5.6.0", "https://new.mirror.lewd.wtf/archive/picoxr/firmware/pico4/global/non_oem/5.6.0-202305190206-RELEASE-user-phoenix-b4256-a8a60c5b55.zip")
    ]

    for version, download_link in versions:
        version_button = tk.Button(nonoem_window, text=version, command=lambda v=version, dl=download_link: download_firmware_thread(v, dl))
        version_button.pack(pady=5)

def download_firmware_thread(version, download_link):
    download_filename = os.path.join(script_dir, "Firmware", os.path.basename(download_link))

    response = requests.get(download_link, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    total_size_mb = total_size / (1024 * 1024)
    cancel_event = Event()

    def download_thread():
        nonlocal total_size

        downloaded_size = 0
        start_time = time.time()

        with open(download_filename, 'wb') as file:
            for data in response.iter_content(chunk_size=1024):
                if cancel_event.is_set():
                    break

                file.write(data)
                downloaded_size += len(data)
                downloaded_size_mb = downloaded_size / (1024)
                elapsed_time = time.time() - start_time

                if elapsed_time > 0:
                    download_speed = (downloaded_size / (1024 * 1024)) / elapsed_time
                else:
                    download_speed = 0

                pico3_window.after(10, update_progress_label, downloaded_size_mb, total_size_mb, download_speed)

        messagebox.showinfo("Success", f"Firmware {version} downloaded successfully")
        pico3_window.after(10, pico3_window.destroy)

    def update_progress_label(downloaded_size, total_size_mb, download_speed):
        progress_label.config(text=f"Downloaded: {downloaded_size / 1024:.2f} MB / {total_size_mb:.2f} MB  Speed: {download_speed:.2f} MB/s")
        progress.step(1024)

    def cancel_download():
        cancel_event.set()
        pico3_window.destroy()
    
    global pico3_window
    pico3_window = tk.Toplevel()
    pico3_window.title(f"Pico Firmware - {version}")
    pico3_window.geometry("400x250")

    if not os.path.exists(os.path.dirname(download_filename)):
        os.makedirs(os.path.dirname(download_filename))

    progress_label = tk.Label(pico3_window, text="")
    progress_label.pack(pady=5)

    progress = ttk.Progressbar(pico3_window, maximum=total_size, mode='determinate')
    progress.pack(pady=10)

    cancel_button = tk.Button(pico3_window, text="Cancel Download", command=cancel_download)
    cancel_button.pack(pady=5)

    progress_thread = Thread(target=download_thread)
    progress_thread.start()

def firmware_installation_thread():
    delete_dload_command = f'{adb_path} shell rm -r /sdcard/dload'
    run_adb_command(delete_dload_command)

    create_dload_command = f'{adb_path} shell mkdir /sdcard/dload'
    run_adb_command(create_dload_command)

    copy_firmware_command = f'{adb_path} push "{firmware_path}" /sdcard/dload/'
    run_adb_command(copy_firmware_command)
    
    install.destroy()
    messagebox.showinfo("Firmware Installation", "Firmware copied successfully.\n\nNow in Pico 4 go to Setting, General, System Version and then choose offline update")

def install_firmware():
    should_copy = messagebox.askyesno("Firmware Installation", "Do you want to copy the firmware to the headset?")

    if should_copy:

        global firmware_path
        firmware_path = filedialog.askopenfilename(
            initialdir=os.path.join(script_dir, "Firmware"),
            title="Select the firmware ZIP file",
            filetypes=[("ZIP-Dateien", "*.zip")]
        )
    
        if not firmware_path:
            messagebox.showinfo("Firmware Installation", "No firmware file selected.")
            return

        firmware_thread = threading.Thread(target=firmware_installation_thread)
        firmware_thread.start()

        global install        
        install = tk.Tk()
        install.title("Firmware Installation")
        install.resizable(False, False) 

        progress_label = tk.Label(install, text="Copying firmware to headset...")
        progress_label.pack(padx=20, pady=20)
    
        install.mainloop()
        
        firmware_thread.join()
    else:
        messagebox.showinfo("Firmware Installation", "Firmware was not copied.")

window = tk.Tk()
window.title("Firmware Upgrader 1.0       FallenAngel / PicoPiracy Team")
window.geometry("500x350")  

top_frame = tk.Frame(window)
top_frame.pack(side="top", pady=10)

middle_frame = tk.Frame(window)
middle_frame.pack(side="top", pady=10)

bottom_frame = tk.Frame(window)
bottom_frame.pack(side="top", pady=10)

image_base64 = "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"

image_data = base64.b64decode(image_base64)

image = Image.open(BytesIO(image_data))

width = 100 
height = 100  
image = image.resize((width, height))

photo = ImageTk.PhotoImage(image)

image_label = tk.Label(top_frame, image=photo)
image_label.pack()

only_label = tk.Label(window, text="only needed for pico 4. Pico 4 must be plugged in")
only_label.pack()

check_button = tk.Button(text="Check OEM State", command=check_oem)
download_button = tk.Button(text="Download Firmware", command=download_firmware)
install_button = tk.Button(text="Install Firmware", command=install_firmware)

check_button.pack(pady=0)
download_button.pack(pady=20)
install_button.pack(pady=0)

window.mainloop()