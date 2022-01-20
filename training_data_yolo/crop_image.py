import os
# import um Excel auszulesen
import pandas as pd
import numpy as np
from xml.dom import minidom
#from create_yolo_txt import to_txt
# import um Bild anzuzeigen
'''Anleitung um OpenCV zu installieren:
In Kommandozeile:
    pip install opencv-contrib-python
    pip install opencv-python

    pip uninstall opencv-python-headless
    '''
import cv2
from shutil import copyfile
import numpy as np

import random as rand
import os, os.path
import shutil

from pathlib import Path
import time

    
    
def main():
    LABEL_DATA = "./original_data/labeldata.xlsx"
    number = 0

    print('old training data (in ./training_data) will be overwritten in 10s')
    for i in range(10):
        print(10 - i)
        time.sleep(1)
    print('0')
    shutil.rmtree('./training_data')

    if not os.path.exists(f"training_data"):
        os.makedirs(f"training_data")
        
    if not os.path.exists(f"training_data/labels"):
        os.makedirs(f"training_data/labels")
    if not os.path.exists(f"training_data/images"):
        os.makedirs(f"training_data/images")
        
    if not os.path.exists(f"training_data/images/test"):
        os.makedirs(f"training_data/images/test")
    if not os.path.exists(f"training_data/images/train"):
        os.makedirs(f"training_data/images/train")
    if not os.path.exists(f"training_data/images/val"):
        os.makedirs(f"training_data/images/val")
    
    if not os.path.exists(f"training_data/labels/test"):
        os.makedirs(f"training_data/labels/test")
    if not os.path.exists(f"training_data/labels/train"):
        os.makedirs(f"training_data/labels/train")
    if not os.path.exists(f"training_data/labels/val"):
        os.makedirs(f"training_data/labels/val")
    

    for file in os.listdir('./original_data'):
        if (".png"in file) or (".tif" in file):

            IMG_FILENAME = file
            img = cv2.imread(f'./original_data/{IMG_FILENAME}')
            print(f"Loaded Image: {IMG_FILENAME}")
            
            if (".tif" in file):
                red_channel = img[:,:,2]
                img = np.zeros(img.shape)
                img[:,:,2] = red_channel
                
            HEIGHT, WIDTH = img.shape[:2]
            print(f"Height: {HEIGHT}, Width: {WIDTH}")

            df = pd.read_excel(LABEL_DATA, sheet_name=IMG_FILENAME)

            xmins = list(df['xmin'])
            ymins = list(df['ymin'])

            x_width = list(df["x_breite"])
            y_height = list(df["y_höhe"])
            
            xmax = np.add(xmins, x_width)
            ymax = np.add(ymins, y_height)
            #for i in range(0, len(xmax)):
            #    cv2.rectangle(img, (xmins[i], ymins[i]), (xmax[i], ymax[i]), (0, 255, 0), 2)

            # Define the window size
            windowsize_r = 640#int(HEIGHT/6)
            windowsize_c = 640#int(WIDTH/6)
            print(f"Höhenauflösung neues Bild: {windowsize_r}")
            print(f"Breitenauflösung neues Bild: {windowsize_c}")

            # Crop out the window and calculate the histogram
            for r in range(0,img.shape[0] - windowsize_r, windowsize_r):

                for c in range(0,img.shape[1] - windowsize_c, windowsize_c):
                    df_window = pd.DataFrame({'xmin':[],'ymin':[], 'x_breite':[], 'y_höhe':[]})
                    window = img[r:r+windowsize_r,c:c+windowsize_c]

                    number += 1
                    cv2.imwrite(f"training_data/images/train/{number:05}.png", window)
                    
                    
                    for i in range(0, len(xmax)):
                        if (xmax[i] < c+windowsize_c)& (ymax[i] < r+windowsize_r) &(xmins[i] > c)& (ymins[i] > r):
                            #cv2.rectangle(window, (xmins[i]-c, ymins[i]-r), (xmax[i]-c, ymax[i]-r), (0, 255, 0), 2)
                            new_row = {'xmin':xmins[i]-c,'ymin':ymins[i]-r, 'x_breite':x_width[i], 'y_höhe':y_height[i]}
                            df_window = df_window.append(new_row, ignore_index = True)
                    to_txt(df_window, windowsize_r, windowsize_c, "./training_data/labels/train/", f"{number:05}")

                
                    #cv2.imshow("Image", window)

                    #cv2.waitKey()
                    #cv2.destroyAllWindows()

                    #cv2.imwrite(f"trainign_data/images/{number:05}.png", window)
                    
    split()
    write_names()


def to_txt(df, image_height, image_width, out_path, image_name):
    df_txt = pd.DataFrame({'object':[], 'center_x':[], 'center_y':[], 'width':[], 'height':[]})
    for index, row in df.iterrows():
        center_x = row['xmin'] + row['x_breite'] * 0.5
        center_y = row['ymin'] + row['y_höhe']*0.5
        center_x = center_x / image_width
        center_y = center_y / image_height
        width = row['x_breite'] / image_width
        height = row['y_höhe'] / image_height
        new_row = {'object': 0, 'center_x' : center_x, 'center_y' : center_y, 'width' : width, 'height' : height}
        df_txt=df_txt.append(new_row, ignore_index = True)
        #print(row['xmin'], row['ymin'], row['x_breite'], row['y_höhe'])
    df_txt = df_txt.astype({'object': int, 'center_x': float, 'center_y': float, 'width': float, 'height': float})
    df_txt.to_csv(f"{out_path}{image_name}.txt",header = None, index = None, sep = ' ')



def split():
    number_of_files = len(os.listdir('./training_data/images/train'))
    print (f'number of smaller images: {number_of_files}')

    test_idx = rand.sample(range(1,number_of_files+1), round(number_of_files*0.2))	
    train_idx = list(range(1,number_of_files+1))
    for i in test_idx:
        train_idx.remove(i)
        
    print(f'smaller pictures for training: {train_idx}\nrest is for validation')

    for i in test_idx:
        shutil.move (f'./training_data/images/train/{i:05}.png', './training_data/images/val')
        shutil.move (f'./training_data/labels/train/{i:05}.txt', './training_data/labels/val')


def write_names():


    pictures_path = Path("./training_data/images")

    for directory_name in iter_subdirs(pictures_path):#['test', 'train', 'val']:
        list_file = './training_data/' + str(directory_name).removeprefix(f'{pictures_path}/') + '.txt'
        f = open(list_file, 'w')
        for file_path in iter_file_paths(directory_name):
          #  print(file_path)
            f.write('./')
            f.write(str(file_path))
            f.write('\n')
        f.close()

def iter_file_paths(base_path):
    return (path for path in base_path.iterdir() if path.is_file())

def iter_subdirs(base_path):
    return (path for path in base_path.iterdir() if path.is_dir())

if __name__ == '__main__':
    main()
