import cv2 as cv
import numpy as np
from PIL import Image


def clipping_digit_from_image(image_ndarray):
    """
    Returns a clipped version of the input image containing only the digit.
    """

    first_line = np.nonzero(image_ndarray)[0].min()
    last_line = np.nonzero(image_ndarray)[0].max()

    first_column = np.nonzero(image_ndarray)[1].min()
    last_column = np.nonzero(image_ndarray)[1].max()

    image_array = image_ndarray[
        first_line : last_line + 1, first_column : last_column + 1
    ]

    return image_array


def add_frame_and_resize_image(image_ndarray):
    """
    Adds a black frame to an input image and resizes it to a fixed size of 28x28 pixels.
    """
    # I Add a 6px Black Frame to The Clipped Digit
    black = [0, 0, 0]
    image_frame = cv.copyMakeBorder(
        image_ndarray, 6, 6, 6, 6, cv.BORDER_CONSTANT, value=black
    )

    resim = Image.fromarray(image_frame)
    resim = resim.resize((28, 28), Image.LANCZOS)

    return np.array(resim)
