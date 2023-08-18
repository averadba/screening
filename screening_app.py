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

# Create a 2x2 table
df = pd.DataFrame(columns=["Actual Positive", "Actual Negative"])
df.loc["Test Positive"] = [st.number_input("True Positives:", step=1, format="%d")]
df.loc["Test Negative"] = [st.number_input("True Negatives:", step=1, format="%d")]

# Get prevalence rate
prev = st.number_input("Enter Prevalence Rate (in %):")

if st.button("Compute"):
    # Compute test statistics
    tp = df.loc["Test Positive", 0]
    fn = df.loc["Test Positive", 1]
    fp = df.loc["Test Negative", 0]
    tn = df.loc["Test Negative", 1]

    specificity = tn / (tn + fp)
    sensitivity = tp / (tp + fn)
    ppv = (tp / (tp + fp)) * (prev / 100) / ((tp / (tp + fp)) * (prev / 100) + (fn / (tn + fn)) * ((100 - prev) / 100))
    npv = (tn / (tn + fn)) * ((100 - prev) / 100) / ((tn / (tn + fn)) * ((100 - prev) / 100) + (fp / (tp + fp)) * (prev / 100))

    # Display results
    st.write("Contingency Table")
    st.write(df)

    st.write(f"Specificity: {specificity:.2f}")
    st.write(f"Sensitivity: {sensitivity:.2f}")
    st.write(f"Positive Predictive Value: {ppv:.2f}")
    st.write(f"Negative Predictive Value: {npv:.2f}")

    # Create charts for PPV and NPV
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

    # Create Altair charts
    ppv_chart = alt.Chart(data).mark_line(color='red').encode(
        x=alt.X('Prevalence Rate', title='Prevalence Rate (%)'),
        y=alt.Y('Positive Predictive Value', title='Positive Predictive Value')
    ).properties(title='PPV vs Prevalence Rate')

    npv_chart = alt.Chart(data).mark_line(color='blue').encode(
        x=alt.X('Prevalence Rate', title='Prevalence Rate (%)'),
        y=alt.Y('Negative Predictive Value', title='Negative Predictive Value')
    ).properties(title='NPV vs Prevalence Rate')

    # Display charts
    st.write(ppv_chart)
    st.write(npv_chart)
