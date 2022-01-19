import os.path
import cv2
import numpy as np
from xml.dom import minidom

def load_im(IMG_FILENAME_READ, file):
    img_read = cv2.imread(IMG_FILENAME_READ)
    print(f"Loaded Image: {IMG_FILENAME_READ}")
    if (".tif" in file):
        red_channel = img_read[:, :, 2]
        img_read = np.zeros(img_read.shape)
        img_read[:, :, 2] = red_channel
    return img_read

def to_xml(imagedata, f_mn, xml_outpath): #image_data: Name, WIDTH,HIGHT,w,h,N,M  #f_mn: name_smaller_picture, r, c where it starts

    root = minidom.Document()

    # annotation element
    image = root.createElement('image')

    # general element
    general = root.createElement('general')

    # filename element
    name = root.createElement('Imagename')
    name.appendChild(root.createTextNode(str(imagedata[0])))
    general.appendChild(name)

    # width element
    width = root.createElement('W')
    width.appendChild(root.createTextNode(str(imagedata[1])))
    general.appendChild(width)

    # height element
    height = root.createElement('H')
    height.appendChild(root.createTextNode(str(imagedata[2])))
    general.appendChild(height)

    # w element
    height = root.createElement('w')
    height.appendChild(root.createTextNode(str(imagedata[3])))
    general.appendChild(height)

    # h element
    height = root.createElement('h')
    height.appendChild(root.createTextNode(str(imagedata[4])))
    general.appendChild(height)

    # n element
    height = root.createElement('N')
    height.appendChild(root.createTextNode(str(imagedata[5])))
    general.appendChild(height)

    # m element
    height = root.createElement('M')
    height.appendChild(root.createTextNode(str(imagedata[6])))
    general.appendChild(height)

    image.appendChild(general)

    #
    # # Hier beginnt deine Schleife
    # #########################################


    for r in range(0,f_mn.shape[0]):
        for c in range(0,f_mn.shape[1]):
            # window
            window = root.createElement('window')

            # name
            name = root.createElement('name')
            name.appendChild(root.createTextNode(str(list(f_mn[r,c])[0])))
            window.appendChild(name)

            # r
            n = root.createElement('r')
            n.appendChild(root.createTextNode(str(list(f_mn[r,c])[1])))
            window.appendChild(n)

            # c
            m = root.createElement('c')
            m.appendChild(root.createTextNode(str(list(f_mn[r,c])[2])))
            window.appendChild(m)

            # n
            n = root.createElement('n')
            n.appendChild(root.createTextNode(str(r)))
            window.appendChild(n)

            # m
            m = root.createElement('m')
            m.appendChild(root.createTextNode(str(c)))
            window.appendChild(m)

            image.appendChild(window)
            #
            # #####################################################
            # # Hier endet deine Schleife
            #

    # Abspeichern der Datei mit ensprechendem Namen
    root.appendChild(image)

    xml_str = root.toprettyxml()

    save_path_file = f"{xml_outpath}/{str(imagedata[0]).split('.')[0]}.xml"
    print(f'saving  xml to {save_path_file}')

    with open(save_path_file, "w") as f:
        f.write(xml_str)

    f = open(save_path_file, "r")
    f_content = f.readlines()
    f.close()

    f_content.pop(0)

    f = open(save_path_file, "w")
    f.writelines(f_content)
    f.close()
    
def slice_img(img_inpath, img_outpath, xml_outpath, windowsize_w = 640, windowsize_h = 640, diameter_neuron = 75):
    #windowsize_h = 640
    #windowsize_w = 640
    #diameter_neuron = 75
    number = 0
    if not os.path.exists(img_outpath):
        os.makedirs(img_outpath)
    if not os.path.exists(xml_outpath):
        os.makedirs(xml_outpath)

    for file in os.listdir(img_inpath):
        if (".png" in file) or (".tif" in file):
            IMG_FILENAME = f'{file}'
            img = load_im(f'{img_inpath}/{IMG_FILENAME}', file)
            HEIGHT, WIDTH = img.shape[:2]
            #print(f"Height: {HEIGHT}, Width: {WIDTH}")

            number_h = int(np.ceil((HEIGHT - 2 * diameter_neuron) / (windowsize_h - 2 * diameter_neuron)))
            number_w = int(np.ceil((WIDTH - 2 * diameter_neuron) / (windowsize_w - 2 * diameter_neuron)))

            try:
                overlap_h = (number_h * windowsize_h - HEIGHT) / (number_h - 1)
                overlap_w = (number_w * windowsize_w - WIDTH) / (number_w - 1)
            except ZeroDivisionError:
                if number_h == 1:
                    overlap_h = 0
                if number_h == 1 & number_w != 1:
                    overlap_w = (number_w * windowsize_w - WIDTH) / (number_w - 1)
                if number_h == 1:
                    overlap_h = 0

            image_data = np.array([IMG_FILENAME, WIDTH, HEIGHT, windowsize_w, windowsize_h, number_w, number_h], dtype=object)
            f_mn = np.ndarray(shape=(number_h, number_w, 3), dtype=object)
            #names_mn = np.ndarray(shape=(number_h, number_w), dtype=str)
            # Crop out the window and calculate the histogram
            for i in range(0, number_h):
                for k in range(0, number_w):
                    r = int(np.round(i * (windowsize_h - overlap_h)))
                    c = int(np.round(k * (windowsize_w - overlap_w)))
                    window = img[r:r + windowsize_w, c:c + windowsize_h]
                    # if k == number_w - 1 and i == number_h - 1:
                    #     if r + windowsize_w != HEIGHT or c + windowsize_h != WIDTH:
                    #         print("ERROR")

                    if window.shape[0] != windowsize_h or window.shape[1] != windowsize_w:
                        print(f"Höhenauflösung neues Bild (zu klein): {window.shape[0]}")
                        print(f"Breitenauflösung neues Bild (zu klein): {window.shape[1]}")

                    name_picture = f"{number:05}.png"
                    cv2.imwrite(f"{img_outpath}/{name_picture}", window)
                    f_mn[i, k] = [name_picture, r, c]
                    number += 1
            to_xml(image_data, f_mn, xml_outpath)#image_data: Name, WIDTH,HIGHT,w,h,N,M  #f_mn: name_smaller_picture, r, c where it starts
if __name__ =='__main__':
    slice_img(".","cropped_images","output") 
