import frameIntensity as fi

my_dir = input('Enter Directory name to save video frame : ')
frame_gap = int(input("Frame Interval: "))
videoFileName = input("Enter Video File Name : ")
fi1 = fi.frameIntensity(my_dir, videoFileName, frame_gap)

user_input = input('is the data/frames same (y/n): ')
if user_input.upper() == 'N':
    fi1.deletedir()
    height, width = fi1.calcualteFrameShape()
    print(f'height = {height} and width = {width}')
    fi1.createImageFromVideo()
    filename = fi1.imagePath()

else:
    pass


print('Plotting Graph')
user_input = ''
while user_input.upper() != 'N':
    x = int(input('Enter X - coordinate: '))
    y = int(input('Enter Y - coordinate: '))
    filename =fi1.imagePath()
    value = fi1.calculateCoordinateIntensity(x, y, filename)
    fi1.plotGraph_temp(value, x, y)
    fi1.mark(x, y,filename)
    user_input = input('Do you want to Continue (y/n): ')