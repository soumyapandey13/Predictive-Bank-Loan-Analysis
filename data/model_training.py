import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split, cross_val_predict, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

# ---------------------------------------------------------
# 1. LOAD DATA FROM SQL
# ---------------------------------------------------------
engine = create_engine('mysql+pymysql://root:password@localhost:3306/bank_loan_db')

print("Pulling data from SQL View...")
df = pd.read_sql("SELECT * FROM cleaned_loan_view", engine)

# ---------------------------------------------------------
# 2. PREPROCESSING (Converting text to numbers)
# ---------------------------------------------------------
print("Encoding categorical variables...")
le = LabelEncoder()

categorical_cols = ['address_state', 'emp_length', 'grade', 'home_ownership', 
                    'purpose', 'term', 'verification_status']

for col in categorical_cols:
    df[col] = le.fit_transform(df[col].astype(str))

# ---------------------------------------------------------
# 3. SPLIT DATA FOR TRAINING
# ---------------------------------------------------------
print("Splitting data into Training and Testing sets...")
X = df.drop('is_bad_loan', axis=1)
y = df['is_bad_loan']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ---------------------------------------------------------
# 4. TRAIN THE RANDOM FOREST MODEL (on the training split only)
# ---------------------------------------------------------
print("Training the Balanced Random Forest Classifier...")

# The class_weight='balanced' parameter forces the model to care about Bad Loans
rf_model = RandomForestClassifier(
    n_estimators=100, 
    class_weight='balanced', 
    random_state=42
)
rf_model.fit(X_train, y_train)

# ---------------------------------------------------------
# 5. EVALUATE THE MODEL (on the held-out test set ONLY)
# ---------------------------------------------------------
# This is the honest, out-of-sample performance number to report/README.
print("\n--- MODEL PERFORMANCE (held-out test set) ---")
predictions = rf_model.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, predictions):.2f}")
print("\nDetailed Classification Report:")
print(classification_report(y_test, predictions))

# ---------------------------------------------------------
# 6. GENERATE OUT-OF-FOLD PREDICTIONS FOR THE FULL PORTFOLIO
# ---------------------------------------------------------
# The dashboard needs a prediction for every loan, not just the 20% test
# split. But we can't just call rf_model.predict(X) here, because rf_model
# was trained on X_train, and X_train is part of X — so those rows would
# get predictions from a model that already memorized their true label
# (data leakage, and it makes predicted_default_risk ~= is_bad_loan).
#
# cross_val_predict fixes this: it fits a fresh model on each fold and only
# predicts on the fold held out of that fit, so every row's prediction
# comes from a model that never saw that row during training.
print("\nGenerating out-of-fold predictions for the full portfolio...")

cv_model = RandomForestClassifier(
    n_estimators=100,
    class_weight='balanced',
    random_state=42
)
cv_splitter = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

oof_predictions = cross_val_predict(cv_model, X, y, cv=cv_splitter)

print("Out-of-fold performance (sanity check, should be close to the test-set numbers above):")
print(classification_report(y, oof_predictions))

# ---------------------------------------------------------
# 7. EXPORT FOR POWER BI (TEXT VERSION)
# ---------------------------------------------------------
print("\nPreparing text-based dataset for Power BI...")

# Pull a fresh copy of the original text data from your database
df_for_powerbi = pd.read_sql("SELECT * FROM cleaned_loan_view", engine)

# Attach the honest, out-of-fold predictions — not in-sample predictions
df_for_powerbi['predicted_default_risk'] = oof_predictions

# Export this readable version to CSV
df_for_powerbi.to_csv('Final_ML_Dataset_For_PowerBI.csv', index=False)
print("Data exported to 'Final_ML_Dataset_For_PowerBI.csv'. Ready for Dashboard!")