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
            if schnitt(true_bbox.iloc[a], test_bbox.iloc[b]):
                correctly_detected_neurons.append(b)
                
                
                
    print(f'Of the {number_neurons_to_be_detected} neurons, {len(correctly_detected_neurons)} have been correctly identified ({100* len(correctly_detected_neurons)/number_neurons_to_be_detected}%)')
    print()
    
    print(f'{number_neurons_to_be_detected -len(correctly_detected_neurons)} neurons have not been identified({100 *(number_neurons_to_be_detected -len(correctly_detected_neurons))/number_neurons_to_be_detected}%)')
    print()
    
    print(f'Of the {number_detected_neurons} detected neurons, {number_detected_neurons-len(correctly_detected_neurons)} have been falsely detected as a neuron ({100*(number_detected_neurons-len(correctly_detected_neurons))/number_detected_neurons}%)')
    print()
                    
if __name__ == '__main__':
    print('Frcnn vs original')
    print('0910_35419.csv')
    evaluate('../Bilder/more_labels/fertig/Images/labels/0910_35419.csv','runs/detect8/bboxes/0910_35419.csv')
    print('0910_36539.csv')
    evaluate('../Bilder/more_labels/fertig/Images/labels/0910_36539.csv','runs/detect8/bboxes/0910_36539.csv')
    print('0916_36534.csv')
    evaluate('../Bilder/more_labels/fertig/Images/labels/0916_36534.csv','runs/detect8/bboxes/0916_36534.csv')
    print('0917_36538.csv')
    evaluate('../Bilder/more_labels/fertig/Images/labels/0917_36538.csv','runs/detect8/bboxes/0917_36538.csv')
    print('0917_36539.csv')
    evaluate('../Bilder/more_labels/fertig/Images/labels/0917_36539.csv','runs/detect8/bboxes/0917_36539.csv')
