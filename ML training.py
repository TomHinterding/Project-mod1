import pandas as pd
import pandasql as ps
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import os
import joblib
table_dir = os.path.join("data/", "table/", "dataset_56_vote.csv")
Table = pd.read_csv(table_dir)

# only if we run the python fiel directly the ML model gets trained, this avoids retraining the model everytime we need
# to acces something else in this file e.g. the function to acess the saved ML model

if __name__ == '__main__':
    #cleaning the Table
    vote_map = {'y': 1, 'n': -1, '?': 0}
    Table = Table.map(lambda v: vote_map.get(v, v))
    #split table into train and test data
    Train_x, Test_x, Train_y, Test_y = train_test_split(Table.drop('Class', axis = 1), Table['Class'], test_size = 0.2, random_state = 42)

    #create ML model
    knn_class = KNeighborsClassifier(n_neighbors=5)
    knn_class.fit(Train_x, Train_y)
    prediction = knn_class.predict(Test_x)
    acc = accuracy_score(Test_y, prediction)
    prec = precision_score(Test_y, prediction, pos_label='democrat')
    rec = recall_score(Test_y, prediction, pos_label='democrat')
    f1 = f1_score(Test_y, prediction, pos_label='democrat')

    #evaluate model
    #we determine if it has no/a negative impact or a positive impact on the model if we leave out a feature when training a moddel
    negative_impact = []
    pOrNo_impact = []
    for col in Train_x:
        knn_compare = KNeighborsClassifier(n_neighbors=5)
        Train_x2, Test_x2, Train_y2, Test_y2 = train_test_split(Table.drop('Class', axis = 1).drop(col, axis=1), Table['Class'], test_size = 0.2, random_state = 42)
        knn_compare.fit(Train_x2, Train_y)
        comp_prediction = knn_compare.predict(Test_x2)
        acc_comp = accuracy_score(Test_y, comp_prediction)
        #prec_comp = precision_score(Test_y, comp_prediction, pos_label='democrat')
        #rec_comp = recall_score(Test_y, comp_prediction, pos_label='democrat')
        f1_comp = f1_score(Test_y, comp_prediction, pos_label='democrat')
        diffacc = acc - acc_comp
        difff1 = f1 - f1_comp
        if diffacc > 0 and difff1 > 0:
            negative_impact.append(col)
        else : 
            pOrNo_impact.append(col)
    #print(f"negative: {negative_impact} \n positive: {pOrNo_impact}")

    #prints a List of features that have a negative impact on the ML performance when removed
    print("Used features:")
    print(negative_impact)

    #we create a final Table that only includes the features that have a positive impact when included
    finalTable = Table
    for col in pOrNo_impact:
        finalTable = finalTable.drop(col, axis = 1)
    knn_final = KNeighborsClassifier(n_neighbors=5)
    Train_x_final, Test_x_final, Train_y_final, Test_y_final = train_test_split(finalTable.drop('Class', axis=1), finalTable['Class'], test_size = 0.2, random_state = 42)
    knn_final.fit(Train_x_final, Train_y_final)

    #Evaluation of the final ML model
    final_prediction = knn_final.predict(Test_x_final)
    acc_final = accuracy_score(Test_y_final, final_prediction)
    prec_final = precision_score(Test_y_final, final_prediction, pos_label='democrat')
    rec_final = recall_score(Test_y_final, final_prediction, pos_label='democrat')
    f1_final = f1_score(Test_y_final, final_prediction, pos_label='democrat')

    #Evaluation result and the improvement compared to using all features
    print(f"Final accuracy: {round(acc_final*100, 2)}% | improved by: {round(acc_final*100 - acc*100, 2)}")
    print(f"Final precision: {round(prec_final*100, 2)}% | improved by: {round(prec_final*100 - prec*100, 2)}")
    print(f"Final recall: {round(rec_final*100, 2)}% | improved by: {round(rec_final*100 - rec*100, 2)}")
    print(f"Final f1 : {round(f1_final*100, 2)}% | improved by: {round(f1_final*100 - f1*100, 2)}")

#saving the final MLModel
joblib.dump(knn_final, os.path.join("data/", "MLmodel/", "ClassPrediction.pkl"))

#getter method for the final ML model
def getMLmodel():
    model = joblib.load(os.path.join("data/", "MLmodel/", "ClassPrediction.pkl"))
    return model