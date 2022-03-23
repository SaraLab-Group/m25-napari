"""
Contains the flags for communication between the PSoC and the Python GUI sent through UART
"""
    
# Signaling Flags
CHANGE_CONFIG = 0x1
DROPPED_FRAME = 0x2
SET_RTC = 0x4
ACK_CMD = 0x8
START_COUNT = 0x10
COUNTING = 0x20
STOP_COUNT = 0x40
ACQUIRE_CAMERAS = 0x80
CAMERAS_ACQUIRED = 0x100
RELEASE_CAMERAS = 0x200
AQUIRE_FAIL = 0x400
START_CAPTURE = 0x800
CAPTURING = 0x1000
USB_HERE = 0x2000  # Use this as flag for Server alive too, since we wont trigger without USB
CONVERTING = 0x4000
FINISHED_CONVERT = 0x8000
ACQUIRING_CAMERAS = 0x10000
CONFIG_CHANGED = 0x20000
START_LIVE = 0x100000
LIVE_RUNNING = 0x200000
STOP_LIVE = 0x400000
START_Z_STACK = 0x800000
Z_STACK_RUNNING = 0x1000000
STOP_Z_STACK = 0x2000000
EXIT_THREAD = 0x80000000
DEFAULT_FPS = 65

# shared mem flags
WRITING_BUFF1 = 0x1
WRITING_BUFF2 = 0x2
READING_BUFF1 = 0x4
READING_BUFF2 = 0x8