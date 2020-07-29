import numpy as np
from PIL import Image


def image_filter(np_image, background_range=80, threshold=0.5):
    """
    Given a numpy array, determine whether there is sufficient content by converting the image to greyscale,
    and counting how much of the histogram is not white

    :param np_image: 3d numpy array
    :param background_range: how many pixels to consider as background
    :param threshold: Percent of pixels in the non-background portion
    :return: True if there is enough image content to continue
    """

    # Get the number of pixels or each score (0-255)
    hist = Image.fromarray(np_image).convert('RGB').convert('L').histogram()
    percent_per_pixel = hist / np.sum(hist) * 100
    above_threshold = np.sum(percent_per_pixel[:hist.__len__() - background_range])
    if above_threshold > threshold:
        return True
    else:
        return False
