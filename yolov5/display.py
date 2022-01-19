import cv2 as cv 
import pandas as pd
import os

def disp(img_root, bbox_root, outpath, show_conf = True, color = (0,255,0), thick = 2):
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    for file in os.listdir(img_root):
        try:
            img = cv.imread(f'{img_root}/{file}')
            name = file.split('.')[0]
            bbox = pd.read_csv(f'{bbox_root}/{name}.csv', sep = ',')
            rectangles = pd.DataFrame(data = {'top_left_x':[],'top_left_y':[], 'bottom_right_x':[], 'bottom_right_y':[], 'confidence':[]})
            rectangles['top_left_x'] = bbox['cx']-bbox['wn']/2
            rectangles['top_left_y'] = bbox['cy']-bbox['hn']/2
            rectangles['bottom_right_x'] = bbox['cx']+bbox['wn']/2
            rectangles['bottom_right_y'] = bbox['cy']+bbox['hn']/2
            if show_conf:
                rectangles['confidence'] = bbox['conf']
        
            for a in range(rectangles.shape[0]):
                top_left = (round(rectangles['top_left_x'][a]), round(rectangles['top_left_y'][a]))
                
                bot_right = (round(rectangles['bottom_right_x'][a]),round(rectangles['bottom_right_y'][a]))
                
                img = cv.rectangle(img, top_left, bot_right , color, thick)
                if show_conf:
                    cv.putText(img,str(rectangles['confidence'][a])[0:5], top_left, cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,100,100))
            cv.imwrite(f'{outpath}/{name}.png',img)
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    disp('../os/Inference_Images','../os/Inference_Images/original','../os/Inference_Images/original', False)
