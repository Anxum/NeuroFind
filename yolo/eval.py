from overlap import schnitt
import pandas as pd

def evaluate(true_bbox_path, test_bbox_path):
    true_bbox = pd.read_csv(true_bbox_path, sep = ',')
    test_bbox = pd.read_csv(test_bbox_path, sep = ',')
    
    number_neurons_to_be_detected = true_bbox.shape[0]
    number_detected_neurons = test_bbox.shape[0]
    
    correctly_detected_neurons = []
    
    for a in range(0, true_bbox.shape[0]):
        for b in range(0, test_bbox.shape[0]):
            if schnitt(true_bbox.iloc[a], test_bbox.iloc[b], 0.5):
                correctly_detected_neurons.append(b)
    print(f'Of the {number_neurons_to_be_detected} neurons, {len(correctly_detected_neurons)} have been correctly identified ({100* len(correctly_detected_neurons)/number_neurons_to_be_detected}%)')
    print()
    
    print(f'{number_neurons_to_be_detected -len(correctly_detected_neurons)} neurons have not been identified({100 *(number_neurons_to_be_detected -len(correctly_detected_neurons))/number_neurons_to_be_detected}%)')
    print()
    
    print(f'Of the {number_detected_neurons} detected neurons, {number_detected_neurons-len(correctly_detected_neurons)} have been falsely detected as a neuron ({100*(number_detected_neurons-len(correctly_detected_neurons))/number_detected_neurons}%)')
    print()
                    
if __name__ == '__main__':
    print('Yolov5 vs Faster RCNN')
    print('0902_35419.png')
    evaluate('runs/detect/exp/bboxes/0902_35419.csv', '../Faster_RCNN/runs/detect/bboxes/0902_35419.csv')
