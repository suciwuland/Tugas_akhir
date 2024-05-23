import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from apphealth.models.model_init import DataSetCollection

collectionDataset = DataSetCollection()
def preprocess_data(df):
    # Memproses kolom 'Blood Pressure' untuk memisahkan Systolic dan Diastolic
    df[['Systolic', 'Diastolic']] = df['Blood Pressure'].str.split('/', expand=True).astype(int)
    df.drop(columns=['Blood Pressure'], inplace=True)
    
    # Encode categorical data
    df['Sex'] = df['Sex'].map({'Male': 0, 'Female': 1})
    df['Diet'] = df['Diet'].map({'Healthy': 0, 'Average': 1, 'Unhealthy': 2})
    
    return df

def train_svm_model(data):
    # Konversi ke DataFrame
    df = pd.DataFrame(data)
    
    # Preprocessing data
    df = preprocess_data(df)
    
    # Memisahkan fitur dan label
    X = df.drop(columns=['Heart Attack Risk'])
    y = df['Heart Attack Risk']
    
    # Normalisasi data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Membagi data menjadi training dan testing set
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)
    
    # Membuat model SVM
    svm_model = SVC(kernel='linear', random_state=42)
    
    # Validasi silang untuk evaluasi model
    scores = cross_val_score(svm_model, X_train, y_train, cv=5)
    # print(f"Cross-validation scores: {scores}")
    # print(f"Average cross-validation score: {scores.mean()}")
    
    # Melatih model
    svm_model.fit(X_train, y_train)
    
    # Memprediksi menggunakan testing set
    y_pred = svm_model.predict(X_test)
    
    # Menampilkan hasil
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, zero_division=0)
    # print("Accuracy:", accuracy)
    # print("Classification Report:\n", report)
    
    # Menampilkan confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    # print("Confusion Matrix:\n", cm)
    
    return svm_model, scaler, X.columns

def test_svm_model(model, scaler, new_data, feature_names):
    # Konversi ke DataFrame
    df_new = pd.DataFrame(new_data)
    
    # Preprocessing data
    df_new = preprocess_data(df_new)
    
    # Menyelaraskan kolom data baru dengan data pelatihan
    df_new = df_new[feature_names]
    
    # Normalisasi data
    X_new_scaled = scaler.transform(df_new)
    
    # Memprediksi menggunakan model yang telah dilatih
    y_new_pred = model.predict(X_new_scaled)
    return y_new_pred[0]


def training_dataset():
    age = []
    sex = []
    cholesterol= []
    blood_pressure = []
    heart_rate=[]
    diabetes=[]
    family_history=[]
    smoking=[]
    obesity=[]
    diet=[]
    bmi=[]
    heart_attack_status=[]
    dataset = list(collectionDataset.find())
    for data in dataset:
        age.append(int(data.get('age')))
        sex.append(data.get('sex'))
        cholesterol.append(int(data.get('cholesterol')))
        blood_pressure.append(data.get('blood_pressure'))
        heart_rate.append(int(data.get('heart_rate')))
        diabetes.append(int(data.get('diabetes')))
        family_history.append(int(data.get('family_history')))
        smoking.append(int(data.get('smoking')))
        obesity.append(int(data.get('obesity')))
        diet.append(data.get('diet'))
        bmi.append(float(data.get('bmi')))
        heart_attack_status.append(int(data.get('heart_attack_risk')))


    training_data = {
        'Age': age,
        'Sex': sex,
        'Cholesterol': cholesterol,
        'Blood Pressure': blood_pressure,
        'Heart Rate': heart_rate,
        'Diabetes': diabetes,
        'Family History': family_history,
        'Smoking': smoking,
        'Obesity': obesity,
        'Diet': diet,
        'BMI': bmi,
        'Heart Attack Risk': heart_attack_status
    }
    return training_data


def clasificationPredict(data_test):
    training_data = training_dataset()
    model, scaler, feature_names = train_svm_model(training_data)
    prediction = test_svm_model(model, scaler, data_test, feature_names)
    return prediction

