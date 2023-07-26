from sys import argv
from time import perf_counter
import cv2


def get_video() -> cv2.VideoCapture:
    """
    Function to open a video file using OpenCV.
    If command-line arguments are present - function considers
    second argument as path to video file, otherwise - path is inputted manually.

    ### Returns:
        * cv2.VideoCapture: Opened video file as VideoCapture object.

    ### Raises:
        * ValueError: If the video file cannot be opened or does not exist.
    """

    # Second CLI argument is path to video file
    if len(argv) == 2:
        filename = argv[1]
    else:
        filename = input("Enter path to video file: ")

    video = cv2.VideoCapture(filename)

    if video.isOpened() is False:
        raise ValueError(f"Failed to open video: {filename}")

    return video


def main():
    # Getting VideoCapture object
    video = get_video()
    angle = 0
    frame_time = 0

    # Reading all necessary information about video file
    VIDEO_FRAMES, VIDEO_FPS = video.get(cv2.CAP_PROP_FRAME_COUNT), int(video.get(cv2.CAP_PROP_FPS))
    VIDEO_SIZE = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    while True:
        # Saving current time at the beginning of loop iteration
        # to synchronize video playback speed and video FPS
        frame_time = perf_counter()

        # Reading next image frame from given video
        success, img = video.read()

        if success is False:
            raise RuntimeError("Something went wrong while reading videofile")

        # Looping video if all frames have been read
        if video.get(cv2.CAP_PROP_POS_FRAMES) == VIDEO_FRAMES:
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)

        # Rotating image
        rotate_matrix = cv2.getRotationMatrix2D((VIDEO_SIZE[0]//2, VIDEO_SIZE[1]//2), angle, 1)
        cv2.warpAffine(img, rotate_matrix, VIDEO_SIZE, img)

        # Reading keypresses
        key = cv2.waitKeyEx(1)

        # Space key press
        if key == 32:
            angle += 5

        # Waiting specific amount of time
        # to synchronize video playback speed and video FPS
        while 1 / VIDEO_FPS > perf_counter() - frame_time:
            pass

        # Show rotated image
        cv2.imshow("Video", img)


if __name__ == "__main__":
    main()
