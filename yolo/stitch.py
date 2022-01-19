from ctypes import CDLL
from xml.dom.minidom import parse, parseString
import pandas as pd
from overlap import schnitt
import os
import ctypes
import numpy as np



#dll_name = "sort.so"
#dllabspath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + dll_name
_sort: CDLL = ctypes.CDLL('./ctype/sort.so')
_sort.sort_out.argtypes = (ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_float)

class Image:
    def __init__(self):
        self.name = ""
        self.W = 0
        self.H = 0
        self.w = 0
        self.h = 0
        self.N = 0
        self.M = 0    
        self.windows = None


class window:
    def __init__(self):
        self.name = ""
        self.n=0
        self.m=0
        self.r=0
        self.c=0
        self.bboxes = None



def get_data_from_xml(path_to_xml): #read image data form xml file
    document = parse(path_to_xml)
    windowlist=[]
    windows = document.getElementsByTagName("window")
    for w in windows:
        window_ = window()
        for nodes in w.childNodes:
            if (nodes.nodeName == 'name'):
                window_.name = (nodes.childNodes[0].nodeValue)
            if (nodes.nodeName == 'n'):
                window_.n = int((nodes.childNodes[0].nodeValue))
            if (nodes.nodeName == 'm'):
                window_.m = int((nodes.childNodes[0].nodeValue))
            if (nodes.nodeName == 'r'):
                window_.r = int((nodes.childNodes[0].nodeValue))
            if (nodes.nodeName == 'c'):
                window_.c = int((nodes.childNodes[0].nodeValue))
        windowlist.append(window_)
    image = Image()
    general = document.getElementsByTagName("general")
    for data in general[0].childNodes:
        if (data.nodeName == 'imagename'):
            image.name = (data.childNodes[0].nodeValue)
        if (data.nodeName == 'W'):
            image.W = int((data.childNodes[0].nodeValue))
        if (data.nodeName == 'H'):
            image.H = int((data.childNodes[0].nodeValue))
        if (data.nodeName == 'w'):
            image.w = int((data.childNodes[0].nodeValue))
        if (data.nodeName == 'h'):
            image.h = int((data.childNodes[0].nodeValue))
        if (data.nodeName == 'N'):
            image.N = int((data.childNodes[0].nodeValue))
        if (data.nodeName == 'M'):
            image.M = int((data.childNodes[0].nodeValue))
    image.windows = windowlist
    return image
        

def read_bboxes(mode, name): #read bounding boxes from txt files
    if mode == 'yolo':
        bboxes = pd.read_csv(f'{name}txt', header = None, sep = " ")
        bboxes.columns = ["cls","cx", "cy", "wn", "hn", "conf"] 
        return bboxes
    
    if mode == 'frcnn':
        bboxes = pd.read_csv(f'{name}csv', sep = " ")
        df = pd.DataFrame(data = {"cls":[],"cx":[], "cy":[], "wn":[], "hn":[], "conf":[]})
        df["cls"] = bboxes["detection_classes"]
        df["conf"] = bboxes["detection_scores"]
        df["cx"] = (bboxes["xmax"] + bboxes["xmin"]) * 0.5 
        df["cy"] = (bboxes["ymax"] + bboxes["ymin"]) * 0.5
        df["wn"] = bboxes["xmax"] - bboxes["xmin"]
        df["hn"] = bboxes["ymax"] - bboxes["ymin"]
        return df


def stitch(bbox_root, xml_root, mode, out_path):    
    print(f'looking for labels at {bbox_root}')
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    for file in os.listdir(xml_root):
        if ('.xml' in file):
            image = get_data_from_xml(f'{xml_root}/{file}')
            print(f'Working on image {file[:-4]}')
            for w in image.windows:
                w.bboxes = read_bboxes(mode, f"{bbox_root}/{w.name[:-3]}")
            frames = [] # collect frames to concatinate later
            lower_idx = 0 #to create continous indexing in concatinated dataframe
            upper_idx = 0
            for win in image.windows:
                lower_idx = upper_idx 
                upper_idx = lower_idx+win.bboxes.shape[0]
                df = pd.DataFrame(data ={"cls":[],"cx":[], "cy":[], "wn":[], "hn":[], "conf":[]})
                df["cls"] = win.bboxes["cls"]
                df["conf"] = win.bboxes["conf"]
                #transform coordinates to absolute coordinates on original image
                df["cx"] = win.bboxes['cx']* image.w + win.c
                df["cy"] = win.bboxes['cy']* image.h + win.r
                df["wn"] = win.bboxes['wn']* image.w
                df["hn"] = win.bboxes['hn']* image.h
            
                df.index = list(range(lower_idx, upper_idx))
            
                frames.append(df)
            g_bb = pd.concat(frames)
            #delete objects, that were detected in multiple windows
            #get each pairing
            length = g_bb.shape[0]
            threshold = 0.5 #percent of overlapping area four bounding boxes marking the same object
            
            global _sort
            array_type = ctypes.c_float * length

            class_arr = array_type(*g_bb['cls'].values.tolist())
            cx_arr = array_type(*g_bb['cx'].values.tolist()) #.astype(int))
            cy_arr = array_type(*g_bb['cy'].values.tolist())
            wn_arr = array_type(*g_bb['wn'].values.tolist())
            hn_arr = array_type(*g_bb['hn'].values.tolist())
            conf_arr = array_type(*g_bb['conf'].values.tolist())

            new_length = _sort.sort_out(class_arr, cx_arr, cy_arr, wn_arr, hn_arr, conf_arr, ctypes.c_int(length), ctypes.c_float(threshold))
            num_delete_last_elements = length - new_length
            class_arr = class_arr[:-num_delete_last_elements]
            cx_arr = cx_arr[:-num_delete_last_elements]  # .astype(int))
            cy_arr = cy_arr[:-num_delete_last_elements]
            wn_arr = wn_arr[:-num_delete_last_elements]
            hn_arr = hn_arr[:-num_delete_last_elements]
            conf_arr = conf_arr[:-num_delete_last_elements]
            
            print(new_length)
            bb = pd.DataFrame({'cls': class_arr, 'cx': cx_arr, 'cy': cy_arr, 'wn': wn_arr, 'hn': hn_arr, 'conf': conf_arr})
            bb.to_csv(f'{out_path}/{file[:-3]}csv', index = False)
    print(f'labels saved to {out_path}')
    #remove sliced images for next detection session


if __name__ == '__main__':
    stitch('.', "./test.xml", 'yolo')
