import cv2
import numpy as np

left_prev_slope = 0

# RIGHT PREV SLOPE
right_slope = 0


def canny(img, low_threshold, high_threshold):
    return cv2.Canny(img, low_threshold, high_threshold)


def calculate_position(x1, y1, height, m):
    b = y1 + (m * x1)
    y = height
    x = (b - y) / m
    return int(x)


def calculate_slope(x1, y1, x2, y2):
    return (y1 - y2) / (x2 - x1)


def draw_lines(img, lines, line_height, color=[255, 0, 0], thickness=5):
    global left_prev_slope
    slope_list = []
    x1a = []
    y1a = []

    global right_slope
    slope_list1 = []
    x1b = []
    y1b = []

    image_height = img.shape[0]
    image_width = img.shape[1]

    for line in lines:
        for x1, y1, x2, y2 in line:
            # LEFT LANE
            if (x1 > 0) & (x1 < image_width / 2):
                x1a.append(x1)
                y1a.append(y1)
                slope_list.append(abs(calculate_slope(x1, y1, x2, y2)))
            # RIGHT LANE
            if (x1 > 0) & (x1 > image_width / 2):
                x1b.append(x1)
                y1b.append(y1)
                slope_list1.append(abs(calculate_slope(x1, y1, x2, y2)))

    if sum(slope_list) > 0:
        current_average = sum(slope_list) / len(slope_list)

        x1 = sum(x1a) / len(x1a)
        y1 = sum(y1a) / len(y1a)
        # print(current_average)

        if left_prev_slope > 0:
            # NEXT AVERAGE
            next_ave = (current_average + left_prev_slope) / 2
        else:
            next_ave = current_average

        left_prev_slope = next_ave

        new_x1 = calculate_position(x1, y1, image_height, next_ave)
        new_x2 = calculate_position(x1, y1, line_height, next_ave)
        cv2.line(img, (new_x1, image_height), (new_x2, line_height), color, thickness)

    if sum(slope_list1) > 0:
        current_average = sum(slope_list1) / len(slope_list1)

        x1 = sum(x1b) / len(x1b)
        y1 = sum(y1b) / len(y1b)

        right_slope = current_average

        if right_slope > 0:
            ave = (current_average + right_slope) / 2
        else:
            ave = current_average

        new_x1 = calculate_position(x1, y1, image_height, -ave)
        new_x2 = calculate_position(x1, y1, line_height, -ave)
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
