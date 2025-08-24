import tkinter as tk
from tkinter import scrolledtext
import wmi
import uuid
import getpass
import platform
import winreg
import subprocess
import hashlib

def safe_call(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return f"Error: {e}"

def get_system_info():
    return f"PC Name: {platform.node()}\nOS: {platform.system()} {platform.release()} ({platform.version()})"

def get_machine_guid():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
        guid, _ = winreg.QueryValueEx(key, "MachineGuid")
        return f"MachineGuid: {guid}"
    except Exception as e:
        return f"MachineGuid Error: {e}"

def get_windows_product_id():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows NT\CurrentVersion")
        value, _ = winreg.QueryValueEx(key, "ProductId")
        return f"Windows Product ID: {value}"
    except Exception as e:
        return f"Product ID Error: {e}"

def get_user_sid():
    try:
        username = getpass.getuser()
        result = subprocess.check_output(f'wmic useraccount where name="{username}" get sid', shell=True)
        lines = result.decode().splitlines()
        sid = [line.strip() for line in lines if line.strip() and "SID" not in line]
        return f"User SID: {sid[0] if sid else 'N/A'}"
    except Exception as e:
        return f"SID Error: {e}"

def get_network_adapters():
    try:
        c = wmi.WMI()
        adapters = []
        for adapter in c.Win32_NetworkAdapter():
            if adapter.MACAddress:
                guid = adapter.GUID if adapter.GUID else 'N/A'
                device_id = adapter.DeviceID if adapter.DeviceID else 'N/A'
                pnp_device_id = adapter.PNPDeviceID if adapter.PNPDeviceID else 'N/A'
                service_name = adapter.ServiceName if adapter.ServiceName else 'N/A'
                adapters.append(f"{adapter.Description} : {adapter.MACAddress}\nGUID: {guid}\nDeviceID: {device_id}\nPNPDeviceID: {pnp_device_id}\nServiceName: {service_name})")
        if adapters:
            return "---------- Network Adapters (Hardware IDs): ----------\n" + "\n".join(adapters)
        else:
            return "No Network Adapters found"
    except Exception as e:
        return f"Network Adapters Error: {e}"

def get_cpu_info():
    try:
        c = wmi.WMI()
        cpus = []
        for cpu in c.Win32_Processor():
            cpus.append(f"CPU ID: {cpu.ProcessorId.strip()}\nName: {cpu.Name}\nManufacturer: {cpu.Manufacturer}\nMaxClockSpeed: {cpu.MaxClockSpeed} MHz\nUniqueId: {getattr(cpu, 'UniqueId', 'N/A')}")
        return "---------- CPU Info: ----------\n" + "\n".join(cpus)
    except Exception as e:
        return f"CPU Error: {e}"

def get_disk_info():
    try:
        c = wmi.WMI()
        disks = []
        for disk in c.Win32_DiskDrive():
            disks.append(
                f"Model: {disk.Model}\n"
                f"Serial: {disk.SerialNumber.strip() if disk.SerialNumber else 'N/A'}\n"
                f"InterfaceType: {disk.InterfaceType}\n"
                f"Size: {int(disk.Size)//(1024**3)} GB\n"
                f"MediaType: {getattr(disk, 'MediaType', 'N/A')}\n"
                f"PNPDeviceID: {getattr(disk, 'PNPDeviceID', 'N/A')}\n"
                f"DeviceID: {getattr(disk, 'DeviceID', 'N/A')}\n============"
            )
        return "---------- Physical Disk Info (Hardware IDs): ----------\n" + "\n".join(disks)
    except Exception as e:
        return f"Disk Error: {e}"

def get_logical_disk_info():
    try:
        c = wmi.WMI()
        disks = []
        for disk in c.Win32_LogicalDisk():
            serial = disk.VolumeSerialNumber
            if serial:
                disks.append(f"Drive: {disk.DeviceID}\n- VolumeSerial: {serial}\n- FileSystem: {disk.FileSystem}\n- Description: {disk.Description}")
        if disks:
            return "---------- Logical Disk Info (Volume Serials): ----------\n" + "\n".join(disks)
        else:
            return "No Logical Disks found"
    except Exception as e:
        return f"Logical Disk Error: {e}"

def get_mb_info():
    try:
        c = wmi.WMI()
        boards = []
        for board in c.Win32_BaseBoard():
            boards.append(f"Manufacturer: {board.Manufacturer}\nProduct: {board.Product}\nSerial: {board.SerialNumber}\nVersion: {board.Version}")
        return "---------- Motherboard Info: ----------\n" + "\n".join(boards)
    except Exception as e:
        return f"Motherboard Error: {e}"

def get_bios_info():
    try:
        c = wmi.WMI()
        bioses = []
        for bios in c.Win32_BIOS():
            bioses.append(f"Manufacturer: {bios.Manufacturer}\nVersion: {bios.SMBIOSBIOSVersion}\nSerial: {bios.SerialNumber}\nReleaseDate: {bios.ReleaseDate}")
        return "---------- BIOS Info: ----------\n" + "\n".join(bioses)
    except Exception as e:
        return f"BIOS Error: {e}"

def get_ram_info():
    try:
        c = wmi.WMI()
        rams = []
        for ram in c.Win32_PhysicalMemory():
            rams.append(f"Capacity: {int(ram.Capacity)//(1024**3)} GB\nManufacturer: {ram.Manufacturer}\nSpeed: {ram.Speed} MHz\nSerial: {ram.SerialNumber}\nPartNumber: {ram.PartNumber}\n")
        return "---------- RAM Info: ----------\n" + "\n".join(rams)
    except Exception as e:
        return f"RAM Error: {e}"

def get_gpu_info():
    try:
        c = wmi.WMI()
        gpus = []
        for gpu in c.Win32_VideoController():
            gpus.append(f"Name: {gpu.Name}\nDriverVersion: {gpu.DriverVersion}\nVideoProcessor: {gpu.VideoProcessor}\nDeviceID: {gpu.DeviceID}\nPNPDeviceID: {gpu.PNPDeviceID}\nAdapterCompatibility: {gpu.AdapterCompatibility}")
        return "---------- GPU Info (Hardware IDs): ----------\n" + "\n".join(gpus)
    except Exception as e:
        return f"GPU Error: {e}"

def get_system_enclosure():
    try:
        c = wmi.WMI()
        enclosures = []
        for enc in c.Win32_SystemEnclosure():
            enclosures.append(f"Manufacturer: {enc.Manufacturer}\nSerialNumber: {enc.SerialNumber}\nVersion: {enc.Version}\nSMBIOSAssetTag: {enc.SMBIOSAssetTag}")
        return "---------- System Enclosure (Chassis Info): ----------\n" + "\n".join(enclosures)
    except Exception as e:
        return f"System Enclosure Error: {e}"

def get_computer_system_product():
    try:
        c = wmi.WMI()
        products = []
        for prod in c.Win32_ComputerSystemProduct():
            products.append(f"IdentifyingNumber: {prod.IdentifyingNumber}\nName: {prod.Name}\nUUID: {prod.UUID}\nVendor: {prod.Vendor}\nVersion: {prod.Version}")
        return "---------- Computer System Product (Hardware UUID): ----------\n" + "\n".join(products)
    except Exception as e:
        return f"Computer System Product Error: {e}"

def get_usb_devices():
    try:
        c = wmi.WMI()
        usbs = []
        for usb in c.Win32_USBHub():
            usbs.append(f"Name: {usb.Name}\nDeviceID: {usb.DeviceID}\nPNPDeviceID: {usb.PNPDeviceID}")
        return "---------- USB Devices (Hardware IDs): ----------\n" + "\n".join(usbs)
    except Exception as e:
        return f"USB Error: {e}"

def get_pointing_devices():
    try:
        c = wmi.WMI()
        points = []
        for point in c.Win32_PointingDevice():
            points.append(f"Description: {point.Description}\nDeviceID: {point.DeviceID}\nPNPDeviceID: {point.PNPDeviceID}\nHardwareType: {point.HardwareType}")
        return "---------- Pointing Devices (Mouse Hardware IDs): ----------\n" + "\n".join(points)
    except Exception as e:
        return f"Pointing Device Error: {e}"

def get_drivers_info():
    try:
        c = wmi.WMI()
        drivers = c.Win32_PnPSignedDriver()
        driver_list = []
        for d in drivers:
            hardware_id = d.HardWareID if d.HardWareID else 'N/A'
            device_id = d.DeviceID if d.DeviceID else 'N/A'
            pnp_device_id = getattr(d, 'PDO', 'N/A')  # Approximate, as PDO might be physical device object
            driver_list.append(f"{d.DeviceName}\n- DeviceID: {device_id}\n- HardWareID: {hardware_id}\n- PNPDeviceID: {pnp_device_id}")
        return "\n---------- All Drivers Info (Hardware IDs): ----------\n" + "\n".join(driver_list)
    except Exception as e:
        return f"Drivers Error: {e}"

def get_processes_info():
    try:
        c = wmi.WMI()
        procs = c.Win32_Process()
        proc_names = [p.Name for p in procs[:30]]
        return "\n---------- Running Processes (first 30): ---------- \n" + ", ".join(proc_names)
    except Exception as e:
        return f"Processes Error: {e}"

def check_virtualization():
    try:
        c = wmi.WMI()
        bios = c.Win32_BIOS()[0]
        comp = c.Win32_ComputerSystem()[0]
        vm_indicators = []
        if any(word in bios.Manufacturer.lower() for word in ["vmware", "virtualbox", "qemu", "xen"]):
            vm_indicators.append("BIOS Manufacturer indicates VM")
        if "virtual" in bios.SerialNumber.lower():
            vm_indicators.append("BIOS Serial indicates VM")
        if any(word in comp.Manufacturer.lower() for word in ["vmware", "virtualbox", "qemu", "xen", "microsoft corporation", "parallels"]):
            vm_indicators.append("ComputerSystem Manufacturer indicates VM")
        if any(word in comp.Model.lower() for word in ["virtual machine", "vmware", "virtualbox"]):
            vm_indicators.append("ComputerSystem Model indicates VM")
        if vm_indicators:
            return "Virtualization Detected: " + "; ".join(vm_indicators)
        else:
            return "Virtualization: Not detected"
    except Exception as e:
        return f"Virtualization Check Error: {e}"

def get_install_date():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
        value, _ = winreg.QueryValueEx(key, "InstallDate")
        import datetime
        date = datetime.datetime.fromtimestamp(int(value))
        return f"Windows Install Date: {date.strftime('%Y-%m-%d %H:%M:%S')}"
    except Exception as e:
        return f"Install Date Error: {e}"

def show_all_info():
    result_text.delete(1.0, tk.END)
    sections = [
        get_system_info(),
        get_machine_guid(),
        get_windows_product_id(),
        get_install_date(),
        get_user_sid(),
        get_network_adapters(),
        get_cpu_info(),
        get_disk_info(),
        get_logical_disk_info(),
        get_mb_info(),
        get_bios_info(),
        get_ram_info(),
        get_gpu_info(),
        get_system_enclosure(),
        get_computer_system_product(),
        get_usb_devices(),
        get_pointing_devices(),
        get_drivers_info(),
        get_processes_info(),
        check_virtualization(),
    ]
    result_text.insert(tk.END, "\n\n".join(sections))

window = tk.Tk()
window.title("HWID Checker")
window.geometry("700x1000")
window.resizable(True, True)

label = tk.Label(window, text="Complete System HWID & Info Collector\n(for Anti-Cheat Tracking Detection)", font=("Segoe UI", 14, "bold"))
label.pack(pady=10)

result_text = scrolledtext.ScrolledText(window, width=85, height=35, font=("Courier New", 9))
result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

check_button = tk.Button(window, text="Load Full System Info", command=show_all_info, font=("Segoe UI", 11))
check_button.pack(pady=5)

window.mainloop()
