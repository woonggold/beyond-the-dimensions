import seaborn as sns  
from sklearn.model_selection import train_test_split  
from sklearn.preprocessing import StandardScaler  
from sklearn.svm import SVC  
import numpy as np

# Titanic 데이터셋 로드 및 전처리
passengers = sns.load_dataset('titanic')  
passengers['sex'] = passengers['sex'].map({'female': 1, 'male': 0})
passengers['age'].fillna(value=passengers['age'].mean(), inplace=True)
passengers['FirstClass'] = passengers['pclass'].apply(lambda x: 1 if x == 1 else 0)  
passengers['SecondClass'] = passengers['pclass'].apply(lambda x: 1 if x == 2 else 0)

# 특성 및 레이블 정의
features = passengers[['sex', 'age', 'FirstClass', 'SecondClass']]  
survival = passengers['survived']

# 학습용 데이터와 테스트용 데이터로 분할
train_features, test_features, train_labels, test_labels = train_test_split(features, survival)

# 데이터 표준화
scaler = StandardScaler()  
train_features = scaler.fit_transform(train_features)  
test_features = scaler.transform(test_features)

# SVM 모델 생성 및 학습
model = SVC(probability=True)  
model.fit(train_features, train_labels)

# 샘플 데이터 정의
man_1 = np.array([0.0, 20.0, 0.0, 0.0])  
woman_1 = np.array([1.0, 17.0, 1.0, 0.0])  
man_2 = np.array([0.0, 32.0, 1.0, 0.0])

sample_passengers = np.array([man_1, woman_1, man_2])

# 샘플 데이터 표준화
sample_passengers = scaler.transform(sample_passengers)

# 클래스 확률 예측
print(model.predict_proba(sample_passengers))
