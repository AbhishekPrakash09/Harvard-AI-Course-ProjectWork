import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    
    # Read data in from file
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        evidence = []
        labels = []
        
        for row in reader:
            
            evidence_row = []
            
            #Administrative (int)
            evidence_row.append(int(row[0]))  
            
            #Administrative_Duration (float)
            evidence_row.append(float(row[1])) 
            
            #Informational (int)
            evidence_row.append(int(row[2])) 
            
            #Informational_Duration (float)
            evidence_row.append(float(row[3]))
            
            #ProductRelated (int)
            evidence_row.append(int(row[4]))  
            
            #ProductRelated_Duration, BounceRates, ExitRates, PageValues, SpecialDay (float)
            for cell in row[5:10] : evidence_row.append(float(cell))
            
            #Month (int)
            months = {'Jan':0,'Feb':1,'Mar':2,'Apr':3,'May':4,'June':5,'Jul':6,'Aug':7,'Sep':8,'Oct':9,'Nov':10,'Dec':11}
            evidence_row.append(months[row[10]])
            
            #OperatingSystems, Browser, Region, TrafficType (int)
            for cell in row[11:15] : evidence_row.append(int(cell))
            
            #VisitorType (int)
            visitortypes={'Returning_Visitor':1,'New_Visitor':0,'Other':0}
            evidence_row.append(visitortypes[row[15]])
            
            csv_data_boolean = {'FALSE':0, 'TRUE':1}
            #Weekend (int)
            evidence_row.append(csv_data_boolean[row[16]])
            
            evidence.append(evidence_row)
            
            labels.append(csv_data_boolean[row[17]])
            
    return(evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    
    sensitivity, specificity = 0.0, 0.0
    actual_positives = 0
    actual_negatives = 0
    
    correctly_identified_positives =  0
    correctly_identified_negatives = 0
    
    for i in range(len(labels)) :
        if(labels[i] == 0):
            actual_negatives = actual_negatives + 1
            
            if(predictions [i] ==0):
                correctly_identified_negatives = correctly_identified_negatives + 1
            
        else:
            actual_positives = actual_positives + 1
            
            if (predictions[i] == 1):
                correctly_identified_positives = correctly_identified_positives + 1
    
    return (correctly_identified_positives / actual_positives, correctly_identified_negatives / actual_negatives)


if __name__ == "__main__":
    main()
