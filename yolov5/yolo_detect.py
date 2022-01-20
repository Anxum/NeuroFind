from stitch import stitch
from slice_os import slice_img
from inference_yolo import main
import argparse
from display import disp
import os
import shutil
import sys

def detect(opt):
    print(vars(opt))
    print('slicing...')
    slice_img(opt.source, './cache/cropped_images', './cache/xml_out')
    img_source = opt.source
    nosave = opt.nosave
    opt.nosave = True
    opt.source = './cache/cropped_images'
    out = f'{opt.project}/{opt.name}'
    test_out = out
    n = 2
    while os.path.exists(test_out):
        test_out = f'{out}{n}'
        n += 1
    out = test_out
    opt.project = './cache/detected'
    opt.name = 'exp'
    print('detecting...')
    root_to_labels = main(opt)
    print('stitching...')
    stitch(f'{root_to_labels}/labels', './cache/xml_out', 'yolo', f'{out}/bboxes')
    print('deleting sliced images..')
    if not (nosave):
        print('displaying images...')
        disp(img_source,f'{out}/bboxes', f'{out}/images', thick = opt.line_thickness)
        print(f'images saved to {out}/image')
    #delete unneeded data for next detection session
    try: 
        shutil.rmtree('./cache')
    except OSError as e:
        print(f'Error: while removing folders')
    
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='./runs/train/weights/best.pt', help='model path(s)')
    parser.add_argument('--source', type=str, default='../Images', help='file/dir/URL/glob, 0 for webcam')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='show results')
    parser.add_argument('--save-txt', action='store_true', default = True, help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', default = True, help='save confidences in --save-txt labels')
    parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default='./runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--line-thickness', default=2, type=int, help='bounding box thickness (pixels)')
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1 #expand
    #print_args(FILE.stem, opt)
    detect(opt)
