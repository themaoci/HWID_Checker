# HWID_Checker
Allows you to check your hardware id in multiple places (using only usermode to check)

Info Collected:
- PC Name
- OS
- MachineGuid
- Windows Product ID
- Windows Installation Date
- User SID
- Network Atapters:
  - Name
  - GUID
  - DeviceID
  - PNPDeviceID
  - ServiceName
- CPU:
  - CPU ID
  - Name
  - Manufacturer
  - MaxClockSpeed
  - UniqueId
- Disk:
  - Model
  - Serial
  - InterfaceType
  - Size
  - MediaType
  - PNPDeviceID
  - DeviceID
- Logical Disk:
  - Drive
  - VolumeSerial
  - FileSystem
  - Description
- Motherboard:
  - Manufacturer
  - Product
  - Serial
  - Version
- BIOS:
  - Manufacturer
  - Version
  - Serial
  - ReleaseDate
- RAM:
  - Capacity
  - Manufacturer
  - Speed
  - Serial
  - PartNumber
- GPU:
  - Name
  - DriverVersion
  - VideoProcessor
  - DeviceID
  - PNPDeviceId
  - AdapterCompatibility
- Chasis Info:
  - Manufacturer
  - Serial Number
  - Version
  - SMBiosAssetTag
- HW UUID:
  - Identifying Number
  - Name
  - UUID
  - Vendor
  - Version
- USB Devices:
  - Name
  - DeviceID
  - PNPDeviceID 
- Mouse Devices:
  - Description
  - DeviceID
  - PNPDeviceID
  - HardwareType
- Drivers Info:
  - Name
  - DeviceID
  - HardwareID
  - PNPDeviceID
- Running Processes (first 30)
- Is Virtualization Detected (basic method)

### install python 3.13+
`https://www.python.org/downloads/release/python-3137`
scroll down and choose proper installation

_"py -m " can be skipped if not using windows or included python into PATH_

### install missing libs
`py -m pip install tkinter`

### compile
`py -m pip install pyinstaller`
`py -m PyInstaller --onefile hwid-checker.py`

### run
`py hwid-checker.py`
