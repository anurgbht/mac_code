from sklearn.datasets import load_breast_cancer
data = load_breast_cancer()
X = data.data
y = data.target

print(X.shape)
print(y.shape)

from sklearn.model_selection import train_test_split
seed = 42
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=seed)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

from sklearn import linear_model
logreg_model = linear_model.LogisticRegression()
logreg_model.fit(X_train, y_train)

predicted_train = logreg_model.predict(X_train)
probs_train = logreg_model.predict_proba(X_train)
predicted_test = logreg_model.predict(X_test)
probs_test = logreg_model.predict_proba(X_test)

from sklearn import metrics
def model_evaluation_metrices(y_actual, y_predicted, y_probs, type = "Test"):
	print(type + ": Accuracy score: ",metrics.accuracy_score(y_actual, y_predicted))
	print(type + ": AUC: ", metrics.roc_auc_score(y_actual, y_probs[:, 1]))
	print(type + ": confusion matrix: \n", metrics.confusion_matrix(y_actual, y_predicted))
	print(type + ": classification report: \n", metrics.classification_report(y_actual, y_predicted))

model_evaluation_metrices(y_train, predicted_train, probs_train, type = "Train")

model_evaluation_metrices(y_test, predicted_test, probs_test, type = "Test")
