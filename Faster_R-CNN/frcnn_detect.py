from display import disp
from inference_frcnn import detect
from slice_os import slice_img
from stitch import stitch
import argparse
import os
import shutil

def run(opt): 
    print(vars(opt))
    src, out, checkpt, config, labelmap, confth, del_img, thickness = opt.source, opt.output, opt.checkpt, opt.config, opt.labelmap, opt.conf_thres, opt.nosave, opt.line_thickness
    
    print('slicing...')
    if src[len(src)-1] =='/':
        src = src[0:len(src)-1]
    if out[len(out)-1] =='/':
        out = out[0:len(out)-1]
    slice_img(src, './cache/cropped_images', './cache/xml_out')
    img_source = src
    cropped_imgs = './cache/cropped_images'
    test_out = out
    n = 2
    while os.path.exists(test_out):
        test_out = f'{out}{n}'
        n += 1
    out = test_out
    cropped_out = './cache/detected/exp'
    print('detecting...')
    root_to_labels = detect(config, checkpt, cropped_imgs, labelmap, cropped_out, confth)
    print('stitching...')
    stitch(f'{root_to_labels}', './cache/xml_out', 'frcnn', f'{out}/bboxes')
    print('deleting sliced images..')
    print('displaying images...')
    if not del_img:
        disp(src,f'{out}/bboxes', f'{out}/images', thick = thickness)
        print(f'images saved to {out}/image')
    #delete unneeded data for next detection session
    try: 
        shutil.rmtree('./cache')
    except OSError as e:
        print(f'Error: while removing folders')
    

if __name__ =='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default='../Images', help='root folder to image(s)')
    parser.add_argument('--config', type=str, default='./export/pipeline.config', help='path to config')
    parser.add_argument('--checkpt', type=str, default='./export/checkpoint/ckpt-0', help='path to checkpoint')
    parser.add_argument('--labelmap', type=str, default="./export/label_map.pbtxt", help='path to label map')
    parser.add_argument('--output', type=str, default='./runs/detect/exp', help='path to output folder')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold') 
    parser.add_argument('--nosave', action='store_true', help='dont save the image')
    parser.add_argument('--line-thickness', type=int, default = 2, help = 'thickness of lines of bounding boxes')
    opt = parser.parse_args()
    run(opt)
