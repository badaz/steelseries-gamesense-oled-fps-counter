import time
import gamesense
from fps_inspector_sdk import fps_inspector
from win32gui import GetForegroundWindow
from win32process import GetWindowThreadProcessId
from PIL import Image
from pystray import Icon, Menu, MenuItem
import threading
import os
import sys


def start_counter():
    gs = gamesense.GameSense("FPS_COUNTER", "FPS Counter")

    register_resp = gs.register_game(icon_color_id=gamesense.GS_ICON_GOLD)
    if not register_resp.success:
        print(register_resp.data)

    screen_handler = {
        'device-type': 'screened',
        'zone': 'one',
        'mode': 'screen',
        'datas': [
            {
                "icon-id": 28,
                "lines": [
                    {
                        "has-text": True,
                        "context-frame-key": "title"
                    },
                    {
                        "has-text": True,
                        "context-frame-key": "fps",
                        "bold": True,
                    }
                ]
            }
        ],
    }

    event_bind_resp = gs.bind_event("RECEIVE_FPS", 0, 999, 0, [screen_handler])
    if not event_bind_resp.success:
        print(event_bind_resp.data)

    event_resp = gs.register_event("RECEIVE_FPS", 0, 999)
    if not event_resp.success:
        print(event_resp.data)

    while not exit_event.is_set():
        pid = int(GetWindowThreadProcessId(GetForegroundWindow())[1])
        fps_inspector.start_fliprate_recording(pid)
        time.sleep(0.5)
        fps_inspector.stop_fliprate_recording()
        data = fps_inspector.get_all_fliprates()

        fps = int(data.get('FPS').to_list()[0]) if len(
            data.get('FPS').to_list()) > 0 else None

        if fps is not None:
            data = {
                "value": fps,
                "frame": {
                    "title": "FPS",
                    "fps": fps
                }
            }

            send_event_resp = gs.send_event("RECEIVE_FPS", data)
            if not send_event_resp.success:
                print(send_event_resp.data)
        else:
            send_hb_resp = gs.send_heartbeat()
            if not send_hb_resp.success:
                print(send_hb_resp.data)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.join(os.path.dirname(__file__))

    return os.path.join(base_path, relative_path)


def exit(icon: Icon) -> None:
    icon.visible = False
    exit_event.set()
    icon.stop()


def setup(icon: Icon) -> None:
    icon.visible = True  # Required to make the systray icon show up

    while not exit_event.is_set():  # This exits the loop if exit is ever set -> program was quit
        start_counter()
        # allows exiting while waiting. time.sleep would block
        exit_event.wait(5)


def main():
    # This event is used to stop the loop.
    global exit_event
    exit_event = threading.Event()

    with Image.open(resource_path("meter.ico")) as im:
        im.load()
        icon = Icon('Steelseries Gamesense FPS Counter', im, 'Steelseries Gamesense FPS Counter', Menu(
            MenuItem('Quit', exit)
        ))

        icon.run(setup=setup)


if __name__ == "__main__":
    main()
