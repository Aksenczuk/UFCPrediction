import pandas as pd
import numpy as np
import os
import pickle
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from imblearn.over_sampling import ADASYN
from sklearn.model_selection import cross_val_score, StratifiedKFold

SEED = 42
WORKERS = 4
os.environ['PYTHONHASHSEED'] = str(SEED)
np.random.seed(SEED)

df = pd.read_csv("datasets/ufc_train.csv")
X = df.drop(["date", "Winner", "R_fighter", "B_fighter"], axis=1).values
y = df["Winner"].values

# over-sampling
X, y = ADASYN().fit_resample(X, y)

# model creation
lr_model = LogisticRegression(random_state=SEED, n_jobs=WORKERS, max_iter=3000)
lr_model.fit(X,y)

rf_model = RandomForestClassifier(random_state=SEED)
rf_model.fit(X,y)

et_model = ExtraTreesClassifier(random_state=SEED)
et_model.fit(X,y)

gb_model = GradientBoostingClassifier(random_state=SEED)
gb_model.fit(X,y)

# model evaluation
kfold = StratifiedKFold( n_splits=10 )
modelNames = ["Logistic Regression", "Random Forest", "Extra Trees", "Gradient Boosting"]
models = [lr_model, rf_model, et_model, gb_model]

def evaluate_model(model, x):
    modelScore = cross_val_score(model, X=X, y = y, scoring = "accuracy", cv = kfold, n_jobs=WORKERS).mean()
    print(f"{modelNames[x]} K-Fold val-avg-Accuracy: {modelScore}")

for x in range (4):
    evaluate_model(models[x], x)

# voting ensemble creation
ensemble = VotingClassifier(estimators = [("Logistic Regression", lr_model), ("Random Forest", rf_model), 
("Extra Trees", et_model), ("Gradient Boosting", gb_model)], voting="soft", n_jobs=WORKERS)
ensemble.fit(X,y)
print(f"{len([x[0] for x in ensemble.estimators])} Models in Ensemble: {[x[0] for x in ensemble.estimators]}")

# ensemble evaluation
test_data = pd.read_csv("datasets/ufc_test.csv")
X_test = df.drop(["date", "Winner", "R_fighter", "B_fighter"], axis=1).values
y_test = df["Winner"].values

modelScore = cross_val_score(ensemble, X=X_test, y = y_test, scoring = "accuracy", cv = kfold, n_jobs=WORKERS).mean()
print(f"Ensemble K-Fold val-avg-Accuracy: {modelScore}")

# pickle dump
pickle.dump(ensemble, open('resources/ensemble_model.pickle', 'wb'))