
# Finding Lane Lines on the Road
## Pipeline
We are going to do the following procedures to identify and draw lanes on the image/video:
First of all we are going to convert the image to grayscale for easier manipulation
Next, we are going to apply gaussian blur to smoothen edges
Then applying canny edge detection to easier detection of the object by their shape
Define region of interest to limit area of lane identification
Perform a hough transformation to find lanes within our region of interest
Calculate the soap for the lines
Draw lines based on the coordinates received from the hough transformation
Draw the line on the edge image
Export the video

## Identify any shortcomings
	Limitations of the following algorithm:
	1) It won’t work on curved lanes
	2) if the video has a vehicle hood in it, it will draw on the top of it.
	3) If the car is in front of our car it will draw lines on the top of it.
	4) little rocks and white paint on the road can make it look funky
## Possible Improvement
I would start with not relaying on the height of the image and fixing curve lanes, also check how the algorithm behaves when there is a car in front.
