import os
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
import cv2
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd 

#######################################################################
#                         Load Model                                  #
#######################################################################
# Load pipeline config and build a detection model


def detect(path_to_config ,path_to_checkpoint , img_root_path, path_to_label_map,   out_path, conf_threshold = 0.50):
    
    
    
    configs = config_util.get_configs_from_pipeline_file(path_to_config)

    detection_model = model_builder.build(model_config=configs['model'], is_training=False)
            # Restore checkpoint
            # Korrigiere evtl den Checkpoint
    ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
    ckpt.restore(path_to_checkpoint).expect_partial()




    category_index = label_map_util.create_category_index_from_labelmap(path_to_label_map)
    
    out_path = f'{out_path}'
    outpath_ = out_path
    n = 2
    while os.path.exists(outpath_):
        outpath_ = f'{out_path}{n}'
        n += 1
    out_path = outpath_
    if not os.path.exists(out_path):
        os.makedirs(f'{out_path}')

            #######################################################################
            #                         Detect Neurons                              #
            #######################################################################

    for file in os.listdir(img_root_path):
        try:
            IMAGE_PATH = f'{img_root_path}/{file}' 
            filename = file.split('.')[0]
            
            img = cv2.imread(IMAGE_PATH)

            image_np = np.array(img)

            input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
            detections = detect_fn(input_tensor, detection_model)
            

            num_detections = int(detections.pop('num_detections'))
            #print(num_detections)
            detections = {key: value[0, :num_detections].numpy()
                        for key, value in detections.items()}
            #print(detections)
            detections.pop('raw_detection_boxes',None)
            detections.pop('detection_anchor_indices',None)
            detections.pop('raw_detection_scores',None)
            detections.pop('detection_multiclass_scores',None)
            xmin = []
            ymin = []
            xmax = []
            ymax = []
            for array in detections['detection_boxes']:
                xmin.append(array[1])
                xmax.append(array[3])
                ymin.append(array[0])
                ymax.append(array[2])
            detections.pop('detection_boxes', None)
            detections['xmin'] = xmin
            detections['ymin'] = ymin
            detections['xmax'] = xmax
            detections['ymax'] = ymax
            detections = pd.DataFrame.from_dict(data = detections)
            #print(detections.keys())
            #print(detections.values())


            #FRCNN Inception

            #print(detections['detection_scores'])
            #print(detections['detection_boxes'])
            # boxes absolute            ymin                      xmin                      ymax                        xmax
            # boxes relative   int(ymin_relative*HEIGHT) int(xmin_relative*WIDTH)   int(ymax_relative*HEIGHT)  int(xmax_relative*WIDTH)

            # Einlesen des Bildes
            #imge = cv2.imread(IMAGE_PATH,  cv2.IMREAD_UNCHANGED)
            #HEIGHT, WIDTH = imge.shape[:2]

            #print(detection_scores)

            # Filtern der detections
            detections = detections[detections.detection_scores >= conf_threshold]

            # Rechtecke ins Bild ziehen
            #for index, row in detections.iterrows():
                #cv2.rectangle(imge, (int(row['xmin']*WIDTH),int(row['ymin']*HEIGHT)), ( int(row['xmax']*WIDTH),int(row['ymax']*HEIGHT)), (0, 255, 0), 2)

            #cv2.imwrite(out_path,imge)


            detections.to_csv(f'{out_path}/{filename}.csv', sep = ' ', index = False) 
            
            #TODO documentation
        except ValueError:
            print('error')
    print(f'saving labels to {out_path}')
    return out_path
    
@tf.function
def detect_fn(image, detection_model):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections

if __name__ == '__main__':
    detect()

