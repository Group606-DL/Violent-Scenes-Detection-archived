import math
import os
import cv2
import numpy as np

from src.utils.globals import logger

# Globals
FRAMES_PER_SECOND = 5
FRAME_WIDTH = 224
FRAME_HEIGHT = 224


def get_optical_flow(video_frames):
    """
    get_optical_flow -
    Optical flow is the pattern of apparent motion of image objects between two consecutive frames caused by the
     movement of object or camera. It is 2D vector field where each vector is a displacement vector showing
      the movement of points from first frame to second.
    :param video_frames: the input video with shape of [frames,height,width,channel]. dtype=np.array
    :return:  flows_x: the optical flow at x-axis, with the shape of [frames,height,width,channel]
        flows_y: the optical flow at y-axis, with the shape of [frames,height,width,channel]
    """
    # initialize the list of optical flows
    gray_video = []
    for i in range(len(video_frames)):
        img = cv2.cvtColor(video_frames[i], cv2.COLOR_RGB2GRAY)
        gray_video.append(np.reshape(img, (224, 224, 1)))

    flows = []
    for i in range(0, len(video_frames) - 1):
        # calculate optical flow between each pair of frames
        flow = cv2.calcOpticalFlowFarneback(prev=gray_video[i], next=gray_video[i + 1], flow=None, pyr_scale=0.5,
                                            levels=3, winsize=15, iterations=3, poly_n=5, poly_sigma=1.2,
                                            flags=cv2.OPTFLOW_FARNEBACK_GAUSSIAN)

        # subtract the mean in order to eliminate the movement of camera
        flow[..., 0] -= np.mean(flow[..., 0])
        flow[..., 1] -= np.mean(flow[..., 1])

        # normalize each component in optical flow
        flow[..., 0] = cv2.normalize(flow[..., 0], None, 0, 255, cv2.NORM_MINMAX)
        flow[..., 1] = cv2.normalize(flow[..., 1], None, 0, 255, cv2.NORM_MINMAX)
        # Add into list
        flows.append(flow)

    # Padding the last frame as empty array
    flows.append(np.zeros((224, 224, 2)))
    return np.array(flows, dtype=np.float32)


def video_to_frames(video_directory: str, video_file: str):
    video_path = os.path.join(video_directory, video_file)

    # Load video capture stream
    cap = cv2.VideoCapture(video_path)

    # Video capture settings
    n_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # Total number of frames
    f_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    f_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    f_rate = cap.get(cv2.CAP_PROP_FPS)  # Get frame rate of video

    logger.debug(f'video_fn: {video_file}, number of frames: {n_frames}, '
                 f'f_width: {f_width}, f_height: {f_height}, fps: {f_rate}')

    count = 0
    frames = []
    while cap.isOpened():
        frame_id = cap.get(1)  # current frame number
        success, frame = cap.read()  # if the frame is read correctly, it will be True
        if not success:
            break
        # TODO: check this if
        if frame_id % math.floor(FRAMES_PER_SECOND) == 0:
            # Resize pixels
            frame = cv2.resize(src=frame, dsize=(FRAME_WIDTH, FRAME_HEIGHT))
            frame = frame.reshape(FRAME_HEIGHT, FRAME_WIDTH, 3)

            frames.append(frame)
        count += 1

    # When everything is done, release the capture
    cap.release()
    frames = np.array(frames)
    logger.debug(f'done extraction: {video_path}')

    video_images = dict(frames=frames, name=video_file,
                        label=0, sequence_length=count)
    return video_images
