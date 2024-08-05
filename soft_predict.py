import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('soft_pickle.pkl', 'rb') as file:
        data = pickle.load(file)
    return data
    
data = load_model()

dtree_load = data['model']
onehot_cou = data['one_cou']
onehot_ind = data['one_ind']
label_edu = data['label_edu']

def show_predict_page():
    st.title('Software Developer Salary Prediction')

    st.write("""### We need some information to predict the salary""")
    
    countries = (   
       'Argentina',
       'Australia',
       'Austria',
       'Bangladesh',
       'Belgium',
       'Brazil',
       'Bulgaria',
       'Canada',
       'China',
       'Colombia',
       'Czech Republic',
       'Denmark',
       'Finland',
       'France',
       'Germany',
       'Greece',
       'Hungary',
       'India',
       'Indonesia',
       'Iran, Islamic Republic of...',
       'Ireland',
       'Israel',
       'Italy',
       'Japan',
       'Lithuania',
       'Mexico',
       'Netherlands',
       'New Zealand',
       'Nigeria',
       'Norway',
       'Pakistan',
       'Philippines',
       'Poland',
       'Portugal',
       'Romania',
       'Russian Federation',
       'Serbia',
       'Slovakia',
       'South Africa',
       'Spain',
       'Sweden',
       'Switzerland',
       'Turkey',
       'Ukraine',
       'United Kingdom of Great Britain and Northern Ireland',
       'United States of America',
    )
    
    
    industry = (
       'Technology and Information Services', 
       'Finance and Insurance',
       'Manufacturing, Transportation, and Supply Chain',
       'Retail and Consumer Services', 
       'Education', 
       'Legal Services',
       'Healthcare', 
       'Energy', 
       'Advertising Services',
    )
    
    
    educaton = (
       'Bachelor’s degree', 
       'Less than a Bachelors', 
       'Master’s degree',
       'Post grad',
    )

    country = st.selectbox ("Country", countries)
    Education = st.selectbox ("Education level", educaton)
    Industry = st.selectbox ("Industry", industry)

    #range from 0-50 and the start value is 3
    experience = st.slider ("Years of Experience", 0, 50, 3)

    ok = st.button('Calculate Salary')
    if ok:
        X = np.array([[Education, experience, country, Industry]])
        encoded_countries = onehot_cou.transform(X[:, [2]])

        # Transform 'industry' column
        encoded_industries = onehot_ind.transform(X[:, [3]])
        # Transform 'education' column
        encoded_education = label_edu.transform(X[:, 0]).reshape(-1, 1)

        # Combine all transformed columns
        # Concatenate along axis 1
        X_transformed = np.concatenate([
            encoded_education,
            X[:, [1]].astype(float).reshape(-1, 1),  # Keep numerical columns as they are
            encoded_countries,
            encoded_industries
            ], 
            axis=1)

        salary = dtree_load.predict(X_transformed)
        st.subheader(f'The estimated salary is ${salary[0]:.2f}')
        
