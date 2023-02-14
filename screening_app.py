import streamlit as st
import pandas as pd
import altair as alt

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Screening Test Performance Calculator")
st.write("*By:* A. Vera")

# Getting user input
tp = st.number_input("Enter True Positives:", step=1, format="%d")
tn = st.number_input("Enter True Negatives:", step=1, format="%d")
fp = st.number_input("Enter False Positives:", step=1, format="%d")
fn = st.number_input("Enter False Negatives:", step=1, format="%d")
prev = st.number_input("Enter Prevalence Rate (in %):")

if st.button("Compute"):
    # Displaying 2X2 contingency table
    st.write("Contingency Table")
    cont_tbl = pd.DataFrame({
        "Actual Positive": [tp, fn],
        "Actual Negative": [fp, tn]
    }, index=["Test Positive", "Test Negative"])
    st.write(cont_tbl)

    # Computing and displaying test specificity
    specificity = tn / (tn + fp)
    st.write(f"Specificity: {specificity:.2f}")

    # Computing and displaying test sensitivity
    sensitivity = tp / (tp + fn)
    st.write(f"Sensitivity: {sensitivity:.2f}")

    # Computing and displaying positive and negative predictive values
    ppv = (tp / (tp + fp)) * (prev / 100) / ((tp / (tp + fp)) * (prev / 100) + (fn / (tn + fn)) * ((100 - prev) / 100))
    npv = (tn / (tn + fn)) * ((100 - prev) / 100) / ((tn / (tn + fn)) * ((100 - prev) / 100) + (fp / (tp + fp)) * (prev / 100))
    st.write(f"Positive Predictive Value: {ppv:.2f}")
    st.write(f"Negative Predictive Value: {npv:.2f}")

    # Creating charts for PPV and NPV
    prev_list = list(range(1, 101))
    ppv_list = []
    npv_list = []
    for p in prev_list:
        ppv_list.append((tp / (tp + fp)) * (p / 100) / ((tp / (tp + fp)) * (p / 100) + (fn / (tn + fn)) * ((100 - p) / 100)))
        npv_list.append((tn / (tn + fn)) * ((100 - p) / 100) / ((tn / (tn + fn)) * ((100 - p) / 100) + (fp / (tp + fp)) * (p / 100)))

    data = pd.DataFrame({
        "Prevalence Rate": prev_list,
        "Positive Predictive Value": ppv_list,
        "Negative Predictive Value": npv_list
    })

    # Creating Altair charts
    ppv_chart = alt.Chart(data).mark_line(color='red').encode(
        x=alt.X('Prevalence Rate', title='Prevalence Rate (%)'),
        y=alt.Y('Positive Predictive Value', title='Positive Predictive Value')
    ).properties(title='PPV vs Prevalence Rate')

    npv_chart = alt.Chart(data).mark_line(color='blue').encode(
        x=alt.X('Prevalence Rate', title='Prevalence Rate (%)'),
        y=alt.Y('Negative Predictive Value', title='Negative Predictive Value')
    ).properties(title='NPV vs Prevalence Rate')

    # Displaying charts
    st.write(ppv_chart)
    st.write(npv_chart)
