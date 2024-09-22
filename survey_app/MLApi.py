import pickle
import numpy as np
import pandas as pd

# тестовое
def test():
    # Шаг 1: Загрузка модели и скалера
    with open('svc_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)

    with open('scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)

    # Шаг 2: Новые данные (пример)
    new_data = {
        'Age': 45,
        'Gender': 'Male',
        'Polyuria': 'Yes',
        'Polydipsia': 'Yes',
        'sudden weight loss': 'No',
        'weakness': 'Yes',
        'Polyphagia': 'No',
        'Genital thrush': 'No',
        'visual blurring': 'Yes',
        'Itching': 'No',
        'Irritability': 'No',
        'delayed healing': 'Yes',
        'partial paresis': 'No',
        'muscle stiffness': 'Yes',
        'Alopecia': 'No',
        'Obesity': 'No'
    }

    # Шаг 3: Преобразование данных
    # Сначала создаем DataFrame для новых данных
    new_data_df = pd.DataFrame([new_data])

    # Кодируем категориальные данные
    new_data_df['Gender'] = new_data_df['Gender'].map({'Male': 1, 'Female': 0})
    columns_to_encode = new_data_df.columns.difference(['Age', 'Gender'])

    new_data_df[columns_to_encode] = new_data_df[columns_to_encode].map(lambda x: 1 if x == 'Yes' else 0)

    # Шаг 4: Применение скалера (масштабирование данных)
    scaled_data = scaler.transform(new_data_df)

    # Шаг 5: Предсказание с помощью модели
    prediction = model.predict(scaled_data)

    # Шаг 6: Вывод результата
    if prediction[0] == 1:
        print("Модель предсказывает, что пациент болен диабетом (Positive).")
    else:
        print("Модель предсказывает, что пациент НЕ болен диабетом (Negative).")

def parse_survey_answer(survey_answer):
    #['22', 'женский', 'нет', 'нет', 'да', 'нет', 'нет', 'нет', 'нет', 'нет', 'нет', 'нет', 'нет', 'да', 'нет', 'нет']
    answers = []
    answers.append(survey_answer[0])
    if survey_answer[1] == 'мужской':
        gender = 'Male'
    else:
        gender = 'Female'
    answers.append(gender)
    for answer_id in range(2, 16):
        if survey_answer[answer_id] == 'да':
            answers.append('Yes')
        else:
            answers.append('No')
    parse_data = {
        'Age': answers[0],
        'Gender': answers[1],
        'Polyuria': answers[2],
        'Polydipsia': answers[3],
        'sudden weight loss': answers[4],
        'weakness': answers[5],
        'Polyphagia': answers[6],
        'Genital thrush': answers[7],
        'visual blurring': answers[8],
        'Itching': answers[9],
        'Irritability': answers[10],
        'delayed healing': answers[11],
        'partial paresis': answers[12],
        'muscle stiffness': answers[13],
        'Alopecia': answers[14],
        'Obesity': answers[15]
    }
    #print(parse_data)
    return parse_data

def get_model_answer(survey_answer):
    # Шаг 1: Загрузка модели и скалера
    with open('survey_app/svc_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)

    with open('survey_app/scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
    survey_answer = parse_survey_answer(survey_answer)

    new_data_df = pd.DataFrame([survey_answer])

    # Кодируем категориальные данные
    new_data_df['Gender'] = new_data_df['Gender'].map({'Male': 1, 'Female': 0})
    columns_to_encode = new_data_df.columns.difference(['Age', 'Gender'])

    new_data_df[columns_to_encode] = new_data_df[columns_to_encode].map(lambda x: 1 if x == 'Yes' else 0)

    # Шаг 4: Применение скалера (масштабирование данных)
    scaled_data = scaler.transform(new_data_df)

    # Шаг 5: Предсказание с помощью модели
    prediction = model.predict(scaled_data)

    # Шаг 6: Вывод результата
    if prediction[0] == 1:
        #print("Модель предсказывает, что пациент болен диабетом (Positive).")
        return True
    else:
        #print("Модель предсказывает, что пациент НЕ болен диабетом (Negative).")
        return False