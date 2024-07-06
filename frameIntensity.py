import os
import shutil
import re
from PIL import Image, ImageDraw
import cv2
import matplotlib.pyplot as plt


class frameIntensity:
    """
    Default Initialization
    dir_name = 'data2',
    x-coordinates = 0, y-coordinates = 0,
    videoFileName used for generation= 'output_grayscale_video.mp4',
    frame interval= 1
    """

    def __init__(self, dir_name,
                 videoFileName,
                 frameInterval):

        self.dir_name = dir_name
        self.videoFileName = videoFileName
        self.frameInterval = frameInterval

        self.frameLength = 0
        self.sorted_files = []

    """
    Calculate the height and width of the video eg. 1080x1090
    """

    def calcualteFrameShape(self):

        cam = cv2.VideoCapture(self.videoFileName)
        ret, frame = cam.read()

        height, width, channels = frame.shape

        return height, width

    def deletedir(self):
        if os.path.exists(self.dir_name):
            shutil.rmtree(self.dir_name)
        else:
            pass

    """
    Create Images(frames) from a video
    """

    def createImageFromVideo(self):

        print('Files deleted')
        try:

            # creating a folder named data
            if not os.path.exists(self.dir_name):
                print('Creating directory path')
                os.makedirs(self.dir_name)

            # if not created then raise error
        except OSError:
            print('Error: Creating directory of data')
        currentframe = 1
        cam = cv2.VideoCapture(self.videoFileName)
        while (True):

            # reading from frame
            ret, frame = cam.read()

            if ret:
                # if video is still left continue creating images
                name = f'./{self.dir_name}/frame' + str(currentframe) + '.jpg'
                #print('Creating...' + name)

                # writing the extracted images
                cv2.imwrite(name, frame)

                # increasing counter so that it will
                # show how many frames are created
                currentframe = currentframe + self.frameInterval
                for _ in range(self.frameInterval - 1):
                    cam.read()
            else:
                break

        # Release all space and windows once done
        cam.release()
        cv2.destroyAllWindows()

    """
    Image path = Set the Path of the frames generated
    """

    def imagePath(self):
        # Use the provided dir_name or the instance attribute
        #dir_to_use = dir_name if dir_name else self.dir_name

        # if not dir_to_use:
        #    raise ValueError("No directory name provided")

        fl_name = []
        # i = 0

        #with open('file_paths.txt', 'w') as file:
        for filename in os.listdir(self.dir_name):
            if filename.endswith(('.png', '.jpg', '.jpeg')):  # Add more image formats if needed
                # Load the image
                image_path = os.path.join(self.dir_name, filename)
                fl_name.append(image_path)



        self.frameLength = self.numberOfFramesAvailable(fl_name)

        return fl_name

    """
    Calcualate the number of frames
    """

    @staticmethod
    def numberOfFramesAvailable(sortedfileslist):

        return len(sortedfileslist)
    """
    calculateImageIntensity = 

    """

    def calculateCoordinateIntensity(self, x, y, filename):

        my_dict = {}
        t = 1

        for im_path in self.sortingfile(filename):
            cap = cv2.VideoCapture(im_path)

            # Check if the video file opened successfully
            if not cap.isOpened():
                print(f"Error: Failed to open video file '{im_path}'")
                continue

            ret, frame = cap.read()

            # Check if frame was read successfully
            if not ret:
                print(f"Error: Failed to read frame from '{im_path}'")
                continue

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Check if the given coordinates (x, y) are within frame dimensions
            height, width = gray_frame.shape
            if x < 0 or x >= width or y < 0 or y >= height:
                print(f"Error: Coordinates ({x}, {y}) are out of frame bounds ({width}, {height})")
                continue

            intensity_value = gray_frame[y][x]
            my_dict[t] = intensity_value
            t += 1

            cap.release()
        return my_dict

    def sortingfile(self, fileName):
        # Function to extract the numeric part from the filename
        value = []
        def extract_number(filename):
            match = re.search(r'(\d+)', filename)
            return int(match.group(0)) if match else -1

        # Sort the list using the extracted number as the key
        sorted_filenames = sorted(fileName, key=extract_number)

        return sorted_filenames

    def plotGraph_temp(self, my_dict, x, y):
        height, width = self.calcualteFrameShape()
        # Print the matrix
        if x <= width and y <= height:
            enumerated_data = enumerate(my_dict.items())

            # Separate the enumerated data into index, keys, and values
            indices, items = zip(*enumerated_data)
            keys, values = zip(*items)

                # Plot the temp array
            plt.plot(indices, values, marker='o', linestyle='-', color='b')

            # Add title and labels
            plt.title('Plot of Values from Pixel Intensity over Time')
            plt.xlabel('Time')
            plt.ylabel(f'Value at [{x}][{y}]')

            # Save the plot to a file
            saveplot = f"Plot {x} and {y} coordinates"
            os.makedirs(saveplot, exist_ok=True)

            mypath = os.path.join(saveplot, f'Image at {x} and {y} coordinates ')
            plt.savefig(mypath + '.jpg', format='jpg')
            # Display the plot
            plt.show()

            filename = f'Pixel Intensity at {x} and {y} coordinates.txt'
            file_path = os.path.join(saveplot, filename)
            with open(file_path, 'w') as file:
                for index, (key, value) in enumerate(my_dict.items()):
                    file.write(f"{index}  {value}\n")
        else:
                print(f'Max value for X-coordinate is {width} '
                      f'and for Y-Coordinate is {height}')


    def mark(self,x, y, filename):

        pattern = r'frame\d+'
    # Load an image
        for im_path in self.sortingfile(filename):
            image = Image.open(im_path)  # Replace with your image file path

        # Create a drawing object
            draw = ImageDraw.Draw(image)

            # Define the position and size of the circle
            circle_position = (x, y)  # Center of the circle (x, y)
            circle_radius = 5

            # Draw the circle (ellipse in this case)
            draw.ellipse((circle_position[0] - circle_radius, circle_position[1] - circle_radius,
                          circle_position[0] + circle_radius, circle_position[1] + circle_radius),
                         outline='red', width=5)

            # Save the edited image
            saveplot = f"Plot {x} and {y} coordinates"
            os.makedirs(saveplot, exist_ok=True)

            match = re.search(pattern, im_path)

            if match:
                selected_frame = match.group()
                #print(selected_frame)

            mypath = os.path.join(saveplot, selected_frame+'.jpg')
            image.save(mypath)

    """
                plt.imshow(image)
                plt.scatter(y, x, color='red', marker='x', s=100)
                # Add title and labels
                plt.title(f"image_data {i}")
                plt.xlabel("X axis")
                plt.ylabel("Y axis")
    
                # Optionally, save the image to a file
                # Save the plot to a file
                saveplot = f"Plot {x} and {y} coordinates"
                os.makedirs(saveplot, exist_ok=True)
    
                mypath = os.path.join(saveplot, selected_frame)
                plt.savefig(mypath + '.jpg', format='jpg')
                plt.close()

"""

