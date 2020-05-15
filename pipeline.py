from moviepy.editor import VideoFileClip
import helpers
import matplotlib.pyplot as plt
import numpy as np


def process_image(image):
    # CONVERT TO GRAYSCALE
    gray = helpers.grayscale(image)

    # APPLY GAUSSIAN BLUR
    kernel_size = 13  # Must be an odd number.
    blur_gray = helpers.gaussian_blur(gray, kernel_size)

    # APPLY CANNY EDGE DETECTOR
    low_threshold = 70
    high_threshold = 140
    edges = helpers.canny(blur_gray, low_threshold, high_threshold)

    # DEFINE REGION OF INTEREST
    imshape = image.shape
    line_height = 330
    vertices = np.array([[(0, imshape[0]), (435, line_height), (540, line_height),
                          (imshape[1], imshape[0])]], dtype=np.int32)

    masked_edges = helpers.region_of_interest(edges, vertices)

    # APPLY HOUGH TRANSFORMATION
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 20  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 20  # maximum gap in pixels between connectable line segments
    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = helpers.hough_lines(masked_edges, rho, theta, threshold,
                                min_line_length, max_line_gap, line_height)

    # Draw the lines on the edge image
    lines_edges = helpers.weighted_img(lines, image, 0.8, 1, 0)

    plt.imshow(lines_edges, cmap='gray')
    return lines_edges


# VIDEO #1
white_output = 'test_videos_output/solidWhiteRight.mp4'
clip1 = VideoFileClip("test_videos/solidWhiteRight.mp4").subclip(0, 3)
white_clip = clip1.fl_image(process_image)
white_clip.write_videofile(white_output, audio=False)

# VIDEO #2
yellow_output = 'test_videos_output/solidYellowLeft.mp4'
clip2 = VideoFileClip('test_videos/solidYellowLeft.mp4').subclip(0, 4)
yellow_clip = clip2.fl_image(process_image)
yellow_clip.write_videofile(yellow_output, audio=False)
