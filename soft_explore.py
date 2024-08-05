import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_cat(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_exp(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_edu(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    elif 'Master’s degree' in x:
        return 'Master’s degree'
    elif 'Professional degree' in x:
        return 'Post grad'
    else:     
        return 'Less than a Bachelors'
    
def clean_ind(x):
    if 'Information Services' in x or 'IT' in x or 'Software Development' in x or 'other Technology' in x:
        return 'Technology and Information Services'
    elif 'Financial Services' in x or 'Insurance' in x:
        return 'Finance and Insurance'
    elif 'Manufacturing' in x or 'Transportation' in x or 'Supply Chain' in x:
        return 'Manufacturing, Transportation, and Supply Chain'
    elif 'Healthcare' in x:
        return 'Healthcare'
    elif 'Retail' in x or 'Consumer Services' in x or 'Wholesale' in x:
        return 'Retail and Consumer Services'
    elif 'Higher Education' in x or 'Education' in x:
        return 'Education'
    elif 'Advertising' in x:
        return 'Advertising Services'
    elif 'Legal Services' in x:
        return 'Legal Services'
    elif 'Oil & Gas' in x:
        return 'Energy'
    else:
        return 'Other'

@st.cache_data #once we run it one time, then it can cache it and its available the next time again    
def load_data():
    df = pd.read_csv(r"C:\Users\user\Documents\survey_results_public.csv")
    df = df[['Country', 'EdLevel', 'YearsCodePro', 'Employment', 'ConvertedCompYearly', 'Industry']]
    df = df.rename({'ConvertedCompYearly': 'Salary'}, axis = 1)
    df = df.drop(0,axis=0)
    median_value = df['Salary'].median()
    df['Salary'].fillna(median_value, inplace=True)
    df = df.dropna()
    Employement_teir =  ['Employed, full-time',                                                                              
                 'Employed, full-time;Independent contractor, freelancer, or self-employed',                       
                 'Independent contractor, freelancer, or self-employed',                                           
                 'Employed, part-time',                                                                             
                 'Employed, full-time;Independent contractor, freelancer, or self-employed;Employed, part-time',     
                 'Independent contractor, freelancer, or self-employed;Employed, part-time'] 
    
    df = df[df['Employment'].isin(Employement_teir)]
    df = df.drop('Employment', axis=1)
    country_map = shorten_cat(df.Country.value_counts(), 114)
    df['Country'] = df['Country'].map(country_map)
    df = df[df['Salary'] <= 250000]
    df = df[df['Salary'] >= 10000]
    df = df[df['Country'] != 'Other']
    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_exp)
    df['EdLevel'] = df['EdLevel'].apply(clean_edu)
    df['Industry'] = df['Industry'].apply(clean_ind)
    return df

df = load_data()

def show_explore_page():
    st.title('Exolore Software Engineer Salaries')

    st.write(
         """
    ### Stack Overflow Developer Survey 2023
    """
    )

    data = df['Country'].value_counts().head(10)

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels = data.index, autopct='%1.f%%', shadow=True, startangle=90)
    ax1.axis('equal')

    st.write("""### Number of Data from different countries""")

    st.pyplot(fig1)

    st.write(
        """
    ### Mean Salary Based on Country
    """
    )

    data = df.groupby(['Country'])['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """
    ### Mean Salary Based on Experience
    """
    )

    data = df.groupby(['YearsCodePro'])['Salary'].mean().sort_values(ascending=True)
    st.line_chart(data)