# importing necessary libraries
import pandas as pd
from pathlib import Path
from config import N_SG, INPUT_DIR, OUTPUT_DIR, INTERESTING_COLUMNS, CUBIC

from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

def load_data(cubic):
    df = pd.read_excel(Path(OUTPUT_DIR,f'data_to_model_{cubic}_{N_SG}.xlsx'))
    return df[INTERESTING_COLUMNS[:-1]],df[INTERESTING_COLUMNS[-1]]

if __name__ == "__main__":

    X, y = load_data(cubic=CUBIC)

    print(X.head(), y.head())
    # dividing X, y into train and test data
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 0)

    # training a DescisionTreeClassifier
    dtree_model = DecisionTreeClassifier(max_depth = 10).fit(X_train, y_train)
    dtree_predictions = dtree_model.predict(X_test)

    # creating a confusion matrix
    cm = confusion_matrix(y_test, dtree_predictions)
    print(cm)