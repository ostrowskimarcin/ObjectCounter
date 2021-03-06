# recording parameters
FRAME_WIDTH = 160
FRAME_HEIGHT = 120
DEBUG_WINDOW_OFFSET = FRAME_WIDTH*2

# detection parameters
OBJECT_SIZE_DETECTION_THRESHOLD = (FRAME_WIDTH * FRAME_HEIGHT) / 120

# lines_height
ENTRANCE_LINE_HEIGHT = int(2 * (FRAME_HEIGHT / 5))
EXIT_LINE_HEIGHT = int(3 * (FRAME_HEIGHT / 5))
DETECTION_BORDER_ENTER = int(1 * (FRAME_HEIGHT / 5))
DETECTION_BORDER_EXIT = int(4 * (FRAME_HEIGHT / 5))

# colours
ENTRANCE_LINE_COLOUR = (0, 0, 255)
EXIT_LINE_COLOUR = (255, 0, 0)
BORDERS_COLOUR = (255, 255)
OBJECT_RECTANGLE_COLOUR = (0, 255, 0)
OBJECT_CIRCLE_COLOUR = (0, 0, 255)

# kernel sizes
OPEN_KERNEL_SIZE = (3, 3)
CLOSE_KERNEL_SIZE = (11, 11)

# algorithm parameters
MAX_OBJECT_AGE = 5
BINARYZATION_THRESHOLD = 100
MAX_PIXEL_VALUE = 255
GRAYSCALE = True
LIMIT = 5

# notifications and google drive
NOTIFICATIONS = True
SEND_PHOTOS_TO_DRIVE = True
ENTRANCE_DIRECTORY_DRIVE_ID = ''
EXIT_DIRECTORY_DRIVE_ID = ''
PUSH_KEY = ''
