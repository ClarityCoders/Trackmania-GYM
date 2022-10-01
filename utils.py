import os
import arrow
from tminterface.interface import TMInterface

"""
Send iface and save inputs in searchable format.
"""

actions = [
    # Nothing
    {
        "accelerate":False,
        "left":False,
        "right":False,
        "brake":False,
    },
    # Just accelerate
    {
        "accelerate":True,
        "left":False,
        "right":False,
        "brake":False,
    },
    # Accelerate Left
    {
        "accelerate":True,
        "left":True,
        "right":False,
        "brake":False,
    },
    # Accelerate Right
    {
        "accelerate":True,
        "left":False,
        "right":True,
        "brake":False,
    },
    # Brake
    {
        "accelerate":False,
        "left":False,
        "right":False,
        "brake":True,
    },
    # Brake Left
    {
        "accelerate":False,
        "left":True,
        "right":False,
        "brake":True,
    },
    # Brake Right
    {
        "accelerate":False,
        "left":False,
        "right":True,
        "brake":True,
    }
]

def save_replay_script(iface: TMInterface, notes=""):
    print(notes,"YEAH")
    path = "scripts"
    local = arrow.utcnow().to('US/Central')
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)

    inputs = iface.get_event_buffer().to_commands_str()
    text_file = open(f"scripts/{local.format('YYMMDD-HH-mm-ss-S')}-{notes}.txt", "w")
    text_file.write(inputs)
    text_file.close()