import os
import sys
import datetime
import imageio

########################################################################################
########################################################################################
########################################################################################

def create_gif(filenames, duration, save_path):
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    output_file = save_path + '\portal animation\Gif-%s.gif' % datetime.datetime.now().strftime('%Y-%M-%d-%H-%M-%S')
    print(output_file)
    imageio.mimsave(output_file, images, duration=duration)

########################################################################################
########################################################################################
########################################################################################
    
or_path = os.getcwd()
os.chdir(or_path + '//portal//')
duration = 1
filenames = os.listdir()

create_gif(filenames, duration, or_path)
