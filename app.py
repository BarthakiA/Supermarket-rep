import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="HR Attrition Dashboard", layout="wide")

# 1. Title
st.title("HR Attrition Dashboard")
st.markdown("This dashboard helps HR Directors and stakeholders analyze attrition patterns at both macro and micro levels with rich interactive visualizations and insights.")

# 2. Load Data
@st.cache_data
def load_data():
    return pd.read_csv('data/EA.csv')

df = load_data()

st.header("About the Data")
st.write("The dataset contains employee information including demographics, employment details, and an 'Attrition' label indicating if they left. Below is a preview:")
st.dataframe(df.head())

# 3. Filters
st.sidebar.header("Filter Options")
department_options = df['Department'].dropna().unique().tolist() if 'Department' in df.columns else []
selected_department = st.sidebar.multiselect("Select Department", department_options, default=department_options)

age_range = st.sidebar.slider("Age Range", int(df['Age'].min()), int(df['Age'].max()), (int(df['Age'].min()), int(df['Age'].max())))

gender_options = df['Gender'].dropna().unique().tolist() if 'Gender' in df.columns else []
selected_gender = st.sidebar.multiselect("Select Gender", gender_options, default=gender_options)

# Apply filters
filtered_df = df.copy()
if 'Department' in df.columns:
    filtered_df = filtered_df[filtered_df['Department'].isin(selected_department)]
if 'Gender' in df.columns:
    filtered_df = filtered_df[filtered_df['Gender'].isin(selected_gender)]
filtered_df = filtered_df[(filtered_df['Age'] >= age_range[0]) & (filtered_df['Age'] <= age_range[1])]

st.subheader("Filtered Data")
st.dataframe(filtered_df)

# 4. Visualization sections
st.header("Attrition Overview")
st.markdown("**1. Overall Attrition Rate**\nShows the percentage of employees who have left.")

attrition_rate = filtered_df['Attrition'].value_counts(normalize=True) * 100
fig1 = px.pie(names=attrition_rate.index, values=attrition_rate.values, title="Overall Attrition Rate")
st.plotly_chart(fig1, use_container_width=True)

st.markdown("**2. Attrition Count by Department**\nHighlights departments with high attrition.")
if 'Department' in filtered_df.columns:
    fig2 = px.bar(filtered_df, x='Department', color='Attrition', barmode='group', title="Attrition by Department")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("**3. Attrition by Age**\nShows how attrition varies across age groups.")
fig3 = px.histogram(filtered_df, x='Age', color='Attrition', nbins=20)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("**4. Attrition by Gender**\nCompare attrition rates by gender.")
if 'Gender' in filtered_df.columns:
    fig4 = px.histogram(filtered_df, x='Gender', color='Attrition')
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("**5. Education Level Distribution**\nDistribution of education levels among employees.")
if 'Education' in filtered_df.columns:
    fig5 = px.histogram(filtered_df, x='Education', color='Attrition')
    st.plotly_chart(fig5, use_container_width=True)

st.header("Tenure and Experience")
st.markdown("**6. Years at Company Distribution**\nHighlights employee tenure patterns.")
if 'YearsAtCompany' in filtered_df.columns:
    fig6 = px.histogram(filtered_df, x='YearsAtCompany', color='Attrition')
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("**7. Boxplot of Age vs Attrition**")
fig7 = px.box(filtered_df, x='Attrition', y='Age')
st.plotly_chart(fig7, use_container_width=True)

st.markdown("**8. Boxplot of Monthly Income vs Attrition**")
if 'MonthlyIncome' in filtered_df.columns:
    fig8 = px.box(filtered_df, x='Attrition', y='MonthlyIncome')
    st.plotly_chart(fig8, use_container_width=True)

st.header("KPI Tables")
st.markdown("**9. Attrition Rate by Department**")
if 'Department' in filtered_df.columns:
    table1 = pd.crosstab(filtered_df['Department'], filtered_df['Attrition'], normalize='index') * 100
    st.dataframe(table1.style.format("{:.2f}"))

st.markdown("**10. Attrition Rate by Gender**")
if 'Gender' in filtered_df.columns:
    table2 = pd.crosstab(filtered_df['Gender'], filtered_df['Attrition'], normalize='index') * 100
    st.dataframe(table2.style.format("{:.2f}"))

st.header("Correlation Analysis")
st.markdown("**11. Heatmap of Numerical Features**\nIdentifies relationships between variables.")
numeric_cols = filtered_df.select_dtypes(include=['number']).columns
if len(numeric_cols) > 1:
    corr = filtered_df[numeric_cols].corr()
    fig9, ax = plt.subplots()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
    st.pyplot(fig9)

st.header("Advanced Visuals")
st.markdown("**12. Pairplot of Selected Features**")
selected_features = st.multiselect("Select Features for Pairplot", numeric_cols, default=numeric_cols[:3])
if len(selected_features) >= 2:
    fig10 = sns.pairplot(filtered_df[selected_features], hue='Attrition')
    st.pyplot(fig10)

st.markdown("**13. Monthly Income Distribution by Age**")
if 'MonthlyIncome' in filtered_df.columns and 'Age' in filtered_df.columns:
    fig11 = px.scatter(filtered_df, x='Age', y='MonthlyIncome', color='Attrition')
    st.plotly_chart(fig11, use_container_width=True)

st.markdown("**14. Education vs Monthly Income**")
if 'Education' in filtered_df.columns and 'MonthlyIncome' in filtered_df.columns:
    fig12 = px.box(filtered_df, x='Education', y='MonthlyIncome', color='Attrition')
    st.plotly_chart(fig12, use_container_width=True)

st.markdown("**15. Years at Company vs Monthly Income**")
if 'YearsAtCompany' in filtered_df.columns and 'MonthlyIncome' in filtered_df.columns:
    fig13 = px.scatter(filtered_df, x='YearsAtCompany', y='MonthlyIncome', color='Attrition')
    st.plotly_chart(fig13, use_container_width=True)

st.markdown("**16. Countplot of Marital Status**")
if 'MaritalStatus' in filtered_df.columns:
    fig14 = px.histogram(filtered_df, x='MaritalStatus', color='Attrition')
    st.plotly_chart(fig14, use_container_width=True)

st.markdown("**17. Attrition by Job Role**")
if 'JobRole' in filtered_df.columns:
    fig15 = px.histogram(filtered_df, x='JobRole', color='Attrition')
    st.plotly_chart(fig15, use_container_width=True)

st.markdown("**18. Years Since Last Promotion vs Attrition**")
if 'YearsSinceLastPromotion' in filtered_df.columns:
    fig16 = px.box(filtered_df, x='Attrition', y='YearsSinceLastPromotion')
    st.plotly_chart(fig16, use_container_width=True)

st.markdown("**19. Years with Current Manager vs Attrition**")
if 'YearsWithCurrManager' in filtered_df.columns:
    fig17 = px.box(filtered_df, x='Attrition', y='YearsWithCurrManager')
    st.plotly_chart(fig17, use_container_width=True)

st.markdown("**20. Interactive Table**\nApply search and sorting.")
st.dataframe(filtered_df)

st.markdown("**21. Raw Data Download**")
st.download_button("Download Filtered Data", data=filtered_df.to_csv(index=False), file_name='filtered_data.csv')

st.success("Explore further by adjusting filters in the sidebar!")

