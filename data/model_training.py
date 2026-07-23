import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
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
# 4. TRAIN THE RANDOM FOREST MODEL (SUPERB ROUTE)
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
# 5. EVALUATE THE MODEL
# ---------------------------------------------------------
print("\n--- MODEL PERFORMANCE ---")
predictions = rf_model.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, predictions):.2f}")
print("\nDetailed Classification Report:")
print(classification_report(y_test, predictions))

# ---------------------------------------------------------
# 6. EXPORT FOR POWER BI
# ---------------------------------------------------------
# ---------------------------------------------------------
# 6. EXPORT FOR POWER BI (TEXT VERSION)
# ---------------------------------------------------------
print("\nPreparing text-based dataset for Power BI...")

# Pull a fresh copy of the original text data from your database
df_for_powerbi = pd.read_sql("SELECT * FROM cleaned_loan_view", engine)

# Attach the ML predictions we just made to this fresh text dataset
df_for_powerbi['predicted_default_risk'] = rf_model.predict(X)

# Export this readable version to CSV
df_for_powerbi.to_csv('Final_ML_Dataset_For_PowerBI.csv', index=False)
print("Data exported to 'Final_ML_Dataset_For_PowerBI.csv'. Ready for Dashboard!")