# Required Packages
import streamlit as st
import pandas as pd
import pickle
from style import webapp_style
from input import user_input_features
from PIL import Image

# Web Page configuration
st.set_page_config(
    page_title="Customer Churn Web-App",
    layout="wide",
    initial_sidebar_state="expanded")

# Title for the app
image = Image.open('data/customer.png')
col1, mid, col2 = st.beta_columns([1, 5, 25])
with col1:
    st.image(image, channels="BGR", width = 150)
with col2:
    st.title("""
                # Customer Churn Prediction App
                This app predicts if the customer will churn or not.\n
                Data obtained from the Kaggle - [Telco Customer Churn](https://www.kaggle.com/blastchar/telco-customer-churn)
                """)

# Sidebar
st.sidebar.header('User Input Features')
st.sidebar.markdown('[Example CSV Input file](https://github.com/SourabhR23/teleco-churn-webapp/blob/master/Telecom'
                    '/churn_example.csv)')

# Collect user input features into dataframe
# Upload the CSV file
uploaded_file = st.sidebar.file_uploader('Upload your input CSV file', type=['csv'])
if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
else:
    # Enter manually
    st.sidebar.write('Enter the data manually')
    input_df = user_input_features()

# Combining the user input features with entire churn dataset
# This will be useful for the encoding phase
raw_churn_data = pd.read_csv(r'Telecom/Churn.csv')
raw_churn_data = raw_churn_data.drop(columns=['customerID', 'Churn'])
df = pd.concat([input_df, raw_churn_data], axis=0)

# Encoding of the ordinal features
encode = ['gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
          'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
          'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
          'PaperlessBilling', 'PaymentMethod']
for col in encode:
    dummy = pd.get_dummies(df[col], prefix=col, drop_first=True)
    df = pd.concat([df, dummy], axis=1)
    del df[col]
# Select only the first row (the user input data)
df = df[: 1]
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'])

# Displays the user input features
st.subheader('# User Input features')
if uploaded_file:
    st.write(input_df)
else:
    st.write('Awaiting CSV file to be uploaded. Currently using below example.')
    st.write(input_df.iloc[:, :7])
    st.write(input_df.iloc[:, 7: 15])
    st.write(input_df.iloc[:, 15:])

# Load the saved model
load_clf = pickle.load(open('Model/modelForPrediction.sav', 'rb'))

# Apply model on the prediction
st.subheader('# Prediction')
st.write('Hit "Predict" button to run the app!')
predict = st.button('Predict')
if predict:
    # predictions
    prediction = load_clf.predict(df)
    prediction_proba = load_clf.predict_proba(df)

    # output results
    if prediction == 1:
        st.write('This customer is likely to be churned.')
        st.write(f'Confidence: {prediction_proba[:, 1] * 100}')
    else:
        st.write('This customer is likely to continue with the service.')
        st.write(f'Confidence: {prediction_proba[:, 0] * 100}')

# WebApp Style Settings
webapp_style()
