# Steelseries Gamesense OLED FPS counter

A simple FPS counter for your Steelseries Gamesense OLED screen

## How it works

Gets the currently focused window, records and sends FPS to OLED screen using Gamesense local http APi at regular intervals

Possible improvement: listen to window focus changes instead of requesting the PID of the currently focused window at the begining of each interval

## Install

Download latest version from the releases page

Run the program

## Compatibility

Windows for now

Tested on Apex Pro TKL Wireless (2023) and Windows 11 22H2

## Develop

### Create and activate venv
```PS
python -m venv .
.\Scripts\Activate.ps1
```

### Install packages
```PS
pip install -r .\requirements.txt
```

### Patch fps_inspector_sdk
The fps_inspector_sdk lib has a bug (issue referenced [here](https://github.com/Andrey1994/fps_inspector_sdk/issues/2)), a patch is required

```PS
python .\Lib\site-packages\patch.py .\fps_inspector_sdk.patch
```

### Run (in elevated Powershell)
```PS
python .\fps_counter.py
```
