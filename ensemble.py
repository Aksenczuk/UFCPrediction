from asyncio import as_completed
import sklearn
import pandas as pd
import numpy as np
import os
from sklearn import metrics
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from imblearn.over_sampling import ADASYN # over-sampling
from sklearn.model_selection import cross_val_score, StratifiedKFold


SEED = 42
WORKERS = 4
os.environ['PYTHONHASHSEED'] = str(SEED)
np.random.seed(SEED)

df = pd.read_csv("datasets/ufc_train.csv")

X = df.drop(["date", "Winner", "R_fighter", "B_fighter", "weight_class"], axis=1).values
y = df["Winner"].values

# over-sampling
X, y = ADASYN().fit_resample(X, y)

lr_model = LogisticRegression(random_state=SEED, n_jobs=WORKERS, max_iter=5000)
lr_model.fit(X,y)

rf_model = RandomForestClassifier(random_state=SEED)
rf_model.fit(X,y)

ex_model = ExtraTreesClassifier(random_state=SEED)
ex_model.fit(X,y)

gb_model = GradientBoostingClassifier(random_state=SEED)
gb_model.fit(X,y)

xgb_model = XGBClassifier(random_state=SEED, use_label_encoder=False, eval_metric='mlogloss')
xgb_model.fit(X,y)

kfold = StratifiedKFold( n_splits=10 )

lr_modelScore = cross_val_score(lr_model, X=X, y = y, scoring = "accuracy", cv = kfold, n_jobs=WORKERS).mean()
print(f"Logistic Regression K-Fold val-avg-Accuracy: {lr_modelScore}")

rf_modelScore = cross_val_score(rf_model, X=X, y = y, scoring = "accuracy", cv = kfold, n_jobs=WORKERS).mean()
print(f"Random Forest K-Fold val-avg-Accuracy: {rf_modelScore}")

ex_modelScore = cross_val_score(ex_model, X=X, y = y, scoring = "accuracy", cv = kfold, n_jobs=WORKERS).mean()
print(f"Extra Trees K-Fold val-avg-Accuracy: {ex_modelScore}")

gb_modelScore = cross_val_score(gb_model, X=X, y = y, scoring = "accuracy", cv = kfold, n_jobs=WORKERS).mean()
print(f"Gradient Boosting K-Fold val-avg-Accuracy: {gb_modelScore}")

xgb_modelScore = cross_val_score(xgb_model, X=X, y = y, scoring = "accuracy", cv = kfold, n_jobs=WORKERS).mean()
print(f"XBG K-Fold val-avg-Accuracy: {xgb_modelScore}")