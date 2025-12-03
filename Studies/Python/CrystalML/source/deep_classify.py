# importing necessary libraries
import pandas as pd
from pathlib import Path
from config import N_SG, INPUT_DIR, OUTPUT_DIR, INTERESTING_COLUMNS, CUBIC

import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder

def load_data(cubic):
    input_file = Path(OUTPUT_DIR,f'data_to_model_{cubic}_{N_SG}.xlsx')
    print(f"Processing: {input_file}")
    df = pd.read_excel(input_file)
    return df[INTERESTING_COLUMNS[:-1]],df[INTERESTING_COLUMNS[-1]]

# First define baseline model. Then use it in Keras Classifier for the training
def baseline_model():
    # Create model here
    model = Sequential()
    model.add(Dense(15, input_dim = 6, activation = 'relu')) # Rectified Linear Unit Activation Function
    model.add(Dense(15, activation = 'relu'))
    model.add(Dense(15, activation = 'relu'))
    model.add(Dense(15, activation = 'relu'))
    model.add(Dense(N_SG, activation = 'softmax')) # Softmax for multi-class classification
    # Compile model here
    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
    return model


if __name__ == "__main__":

    # Random seed for reproducibility
    seed = 42
    np.random.seed(seed)

    X, Y = load_data(cubic=CUBIC)

    # Normalize features within range 0 (minimum) and 1 (maximum)
    scaler = MinMaxScaler(feature_range=(0, 1))
    X = scaler.fit_transform(X)
    X = pd.DataFrame(X)

    # First encode target values as integers from string
    # Then perform one hot encoding
    encoder = LabelEncoder()
    encoder.fit(Y)
    Y = encoder.transform(Y)
    Y = np_utils.to_categorical(Y)

    # For Keras, convert dataframe to array values (Inbuilt requirement of Keras)
    X = X.values

    # Create Keras Classifier and use predefined baseline model
    estimator = KerasClassifier(build_fn = baseline_model, epochs = 100, batch_size = 10, verbose = 0)
    # Try different values for epoch and batch size

    # KFold Cross Validation
    kfold = KFold(n_splits = 5, shuffle = True, random_state = seed)
    # Try different values of splits e.g., 10

    # Object to describe the result
    results = cross_val_score(estimator, X, Y, cv = kfold)
    # Result
    print("Result: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))

