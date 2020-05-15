import cv2
import numpy as np


def canny(img, low_threshold, high_threshold):
    return cv2.Canny(img, low_threshold, high_threshold)


def calculate_position(x1, y1, x2, y2, height):
    m = (y1 - y2) / (x2 - x1)
    b = y1 + (m * x1)
    y = height
    x = (b - y) / m
    return int(x)


def draw_lines(img, lines, line_height, color=[255, 0, 0], thickness=5):

    image_height = img.shape[0]

    for line in lines:
        for x1, y1, x2, y2 in line:
            new_x1 = calculate_position(x1, y1, x2, y2, image_height)
            new_x2 = calculate_position(x1, y1, x2, y2, line_height)
            cv2.line(img, (new_x1, image_height), (new_x2, line_height), color, thickness)


def gaussian_blur(img, kernel_size):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def hough_lines(img: object, rho: object, theta: object, threshold: object, min_line_len: object,
                max_line_gap: object, line_height: object) -> object:
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                            maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines, line_height)
    return line_img


def region_of_interest(img, vertices):
    # defining a blank mask to start with
    mask = np.zeros_like(img)

    # defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = 255 * channel_count
    else:
        ignore_mask_color = 255

    # filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    # returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def weighted_img(img, initial_img, α=0.8, β=1., γ=0.):
    return cv2.addWeighted(initial_img, α, img, β, γ)