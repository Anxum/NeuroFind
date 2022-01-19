#include <stdbool.h>

bool schnitt(float threshold, float cxone, float cyone, float wnone, float hnone, float cxtwo, float cytwo, float wntwo, float hntwo){ // Schnittstelle noch ändern --> dataframe mit 2 Boxen als Eingabe
    /*diameter_neuron = 75 //in pixeln
    if (cxone-cxtwo)**2 + (cxone-cxtwo)**2 > diameter_neuron**2:
        return 0
    else:*/
        bool overlap = false; // boolscher Wert
        float xl1 = cxone - wnone / 2;   //linke Kante der 1. Box
        float xr1 = cxone + wnone / 2;   //rechte Kante der 1. Box
        float xl2 = cxtwo - wntwo / 2; //linke Kante der 2. Box
        float xr2 = cxtwo + wntwo / 2; //rechte Kante der 2. Box
        float yo1 = cyone - hnone / 2;   //obere Kante der 1. Box
        float yu1 = cyone + hnone / 2;   //untere Kante der 1. Box
        float yo2 = cytwo - hntwo / 2; //obere Kante der 2. Box
        float yu2 = cytwo + hntwo / 2; //untere Kante der 2. Box
        float A1 = (xr1-xl1)*(yu1-yo1); // Fläche der 1. Box
        float A2 = (xr2-xl2)*(yu2-yo2); // Fläche der 2. Box
        // Schnittrechtecks
        float xl,xr,yo,yu;
        
        
        
        if(xl1 > xl2)
        {
            xl = xl1;
        }
        else
        {
            xl = xl2;
        }
            
        if(xr1 > xr2)
        {
            xr = xr2;
        }
        else
        {
            xr = xr1;
        }
        
        if(yo1 > yo2)
        {
            yo = yo1;
        }
        else
        {
            yo = yo2;
        }
        
        if(yu1 > yu2)
        {
            yu = yu2;
        }
        else
        {
            yu = yu1;
        }
            
        // Schnittfläche berechnen 
        float x = xr - xl;
        float y = yu - yo;
        if (x<0)
        { 
            x = 0;
        }
            
        if(y<0)
        {
            y =0;
        }
        
        float A = x*y;
        // Bedingung overlap
        if (A >= threshold*A1 | A >= threshold*A2)  // mindest 50% von einer der Boxen - oder größste Box?
        {
            overlap = true;
        }
        
        return overlap; // für Überlappung Box mit kleiner Wkt. löschen (Funktion für rauslöschen einer Box schreiben)\
        // für Evaluation noch Funktion zum Zählen schreiben (gleiche Detektion der Neuronen zählen)
}

int remove_elements(float * list, bool * staying, int length)
{
    int new_length = length;
    for(int i = length - 1; i >= 0; i--)
    {
        if(!staying[i])
        {
            new_length--;
            for(int a = i + 1; a < length; a++)
            {
                list[a - 1] = list[a];
            }
        }
    }
    
    return new_length;
}



 int sort_out(float* class, float* cx, float* cy, float* wn, float* hn, float* confidence, int length, float threshold){
    bool staying[length];
    int count = 0;
    for(int i = 0; i < length; i++)
    {
        staying[i] = true;
    }
    for(int a = 0; a < length; a++)
    {
        if(staying[a] == true)
        {
            for(int b = a + 1; b < length; b++)
            {
                if(staying[b] == true)
                {
                    if(schnitt(threshold, cx[a], cy[a], wn[a], hn[a], cx[b], cy[b], wn[b], hn[b]))
                    {
                        count ++;
                        if(confidence[a] > confidence[b])
                        {
                            staying[b] = false;
                        }
                        else
                        {
                            staying[a] = false;
                        }
                    }
                }
            }
        }
    }
    
    int new_length = remove_elements(cx, staying, length);
    remove_elements(cy, staying, length);
    remove_elements(wn, staying, length);
    remove_elements(hn, staying, length);
    remove_elements(confidence, staying, length);
    remove_elements(class, staying, length);
    
    
    //TODO remove overlapping elements
    return new_length;
    
}
