from sklearn.datasets import load_breast_cancer
data = load_breast_cancer()
X = data.data
y = data.target

from sklearn.model_selection import train_test_split
seed = 42
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=seed)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout

model = Sequential()
model.add(Dense(20, activation = 'relu', input_dim = 30))
model.add(Dropout(0.2))
model.add(Dense(1, activation = 'sigmoid',input_dim = 20))
model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

model.fit(X_train, y_train, batch_size=32,nb_epoch=100)

probs_train = model.predict(X_train)
probs_test = model.predict(X_test)

probs_train = probs_train.flatten()
probs_test = probs_test.flatten()
predicted_train = (probs_train > 0.5).astype(int)
predicted_test = (probs_test > 0.5).astype(int)

from sklearn import metrics
def model_evaluation_metrices(y_actual, y_predicted, y_probs, type = "Test"):
	print(type + ": Accuracy score: ",metrics.accuracy_score(y_actual, y_predicted))
	print(type + ": AUC: ", metrics.roc_auc_score(y_actual, y_probs))
	print(type + ": confusion matrix: \n", metrics.confusion_matrix(y_actual, y_predicted))
	print(type + ": classification report: \n", metrics.classification_report(y_actual, y_predicted))

model_evaluation_metrices(y_train, predicted_train, probs_train, type = "Train")

model_evaluation_metrices(y_test, predicted_test, probs_test, type = "Test")
