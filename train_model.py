import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

def train_and_save_model():
    print("Loading expanded dataset...")
    df = pd.read_csv("final_clinical_dataset.csv")
    
    # تحديد المتغيرات المستقلة والهدف
    X = df[['Age', 'Sex', 'IFIT3', 'IFIH1', 'CXCL10', 'STAT2', 'Anti_dsDNA', 'C3_Level', 'SLEDAI_Score']]
    y = df['Label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # معالجة البيانات (تنسيق المتغيرات العددية والنصية مثل الجنس)
    numeric_features = ['Age', 'IFIT3', 'IFIH1', 'CXCL10', 'STAT2', 'Anti_dsDNA', 'C3_Level', 'SLEDAI_Score']
    categorical_features = ['Sex']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    print("Training model on expanded clinical data...")
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    print(f"Model trained successfully! Test Accuracy: {accuracy * 100:.2f}%")
    
    # حفظ الموديل
    joblib.dump(model, "sle_clinical_model.pkl")
    print("Model saved as 'sle_clinical_model.pkl'.")

if __name__ == "__main__":
    train_and_save_model()