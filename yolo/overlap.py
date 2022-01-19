
def schnitt(box1, box2, threshold = 0.5): # Schnittstelle noch ändern --> dataframe mit 2 Boxen als Eingabe
        overlap = False # boolscher Wert
        xl1 = box1['cx'] - box1['wn'] / 2   #linke Kante der 1. Box
        xr1 = box1['cx'] + box1['wn'] / 2   #rechte Kante der 1. Box
        xl2 = box2['cx'] - box2['wn'] / 2 #linke Kante der 2. Box
        xr2 = box2['cx'] + box2['wn'] / 2 #rechte Kante der 2. Box
        yo1 = box1['cy'] - box1['hn'] / 2   #obere Kante der 1. Box
        yu1 = box1['cy'] + box1['hn'] / 2   #untere Kante der 1. Box
        yo2 = box2['cy'] - box2['hn'] / 2 #obere Kante der 2. Box
        yu2 = box2['cy'] + box2['hn'] / 2 #untere Kante der 2. Box
        A1 = (xr1-xl1)*(yu1-yo1) # Fläche der 1. Box
        A2 = (xr2-xl2)*(yu2-yo2) # Fläche der 2. Box
        # Schnittrechtecks
        if xl1 > xl2:
            xl = xl1
        else:
            xl = xl2
            
        if xr1 > xr2:
            xr = xr2
        else:
            xr = xr1
        if yo1 > yo2:
            yo = yo1
        else:
            yo = yo2
        if yu1 > yu2:
            yu = yu2
        else:
            yu = yu1
            
        # Schnittfläche berechnen 
        x = xr - xl
        y = yu - yo
        if x<0:
            x = 0
        if y<0:
            y =0
        A = x*y
        # Bedingung overlap
        if A >= threshold*A1 or A>= threshold*A2 :  # mindest 50% von einer der Boxen - oder größste Box?
            overlap = True
        
        return overlap # für Überlappung Box mit kleiner Wkt. löschen (Funktion für rauslöschen einer Box schreiben)\
        # für Evaluation noch Funktion zum Zählen schreiben (gleiche Detektion der Neuronen zählen)
 
