import streamlit as st
import pandas as pd
import altair as alt
import math

# Function to compute the 95% confidence interval for a proportion
def compute_confidence_interval(p, n):
    """Compute the 95% confidence interval for a proportion."""
    Z = 1.96  # Z-score for 95% CI
    delta = Z * math.sqrt(p * (1 - p) / n)
    return (p - delta, p + delta)

# Function to create a results table
def create_results_table(tp, fn, fp, tn, prev):
    # Compute metrics
    specificity = tn / (tn + fp)
    sensitivity = tp / (tp + fn)
    ppv = (tp / (tp + fp)) * (prev / 100) / ((tp / (tp + fp)) * (prev / 100) + (fn / (tn + fn)) * ((100 - prev) / 100))
    npv = (tn / (tn + fn)) * ((100 - prev) / 100) / ((tn / (tn + fn)) * ((100 - prev) / 100) + (fp / (tp + fp)) * (prev / 100))
    
    # Compute 95% confidence intervals
    specificity_ci = compute_confidence_interval(specificity, tn + fp)
    sensitivity_ci = compute_confidence_interval(sensitivity, tp + fn)
    ppv_ci = compute_confidence_interval(ppv, tp + fp)
    npv_ci = compute_confidence_interval(npv, tn + fn)
    
    # Create a dataframe to display results in a table format
    data = {
        "Metric": ["Specificity", "Sensitivity", "Positive Predictive Value", "Negative Predictive Value"],
        "Value": [specificity, sensitivity, ppv, npv],
        "95% CI Lower Bound": [specificity_ci[0], sensitivity_ci[0], ppv_ci[0], npv_ci[0]],
        "95% CI Upper Bound": [specificity_ci[1], sensitivity_ci[1], ppv_ci[1], npv_ci[1]]
    }
    df_results = pd.DataFrame(data)
    
    return df_results

# Streamlit app code starts here
st.markdown(""" <style>
#GithubIcon {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Screening Test Performance Calculator")
st.markdown("*By:* Dr. Alexis Vera - [Contact me](mailto:alexisv@sanjuanbautista.edu)")


st.markdown("""

This app allows users to compute important metrics related to the performance of a screening test. 
By inputting the counts of true positives, false positives, true negatives, and false negatives, 
users can obtain metrics like specificity, sensitivity, positive predictive value (PPV), 
and negative predictive value (NPV), along with their 95% confidence intervals.

### Quick Instructions:
1. Edit the table to input your test results.
2. Enter the disease prevalence rate.
3. Click on the "Compute" button to view the results and charts.

### Formulas Used:
- **Specificity**: 
Specificity = True Negatives / (True Negatives + False Positives)
- **Sensitivity**: 
Sensitivity = True Positives / (True Positives + False Negatives)
- **Positive Predictive Value (PPV)**: Formula considering prevalence to adjust the value.
- **Negative Predictive Value (NPV)**: Formula considering prevalence to adjust the value.
- **95% Confidence Interval for Proportion**: 
CI = p ± Z × √(p(1-p)/n)
    - Where:
        - p is the proportion (e.g., sensitivity, specificity).
        - Z is the Z-score (for a 95% confidence interval, Z is approximately 1.96).
        - n is the total number of observations.
""")

st.divider()

# Create an editable 2x2 table for user input
initial_data = {
    "Actual Positive": [0, 0],
    "Actual Negative": [0, 0]
}
index = ["Test Positive", "Test Negative"]
df = pd.DataFrame(initial_data, index=index)
df_edited = st.data_editor(df) #Creating editable table

# Get values from the editable table
tp = df_edited.loc["Test Positive", "Actual Positive"]
fn = df_edited.loc["Test Negative", "Actual Positive"]
fp = df_edited.loc["Test Positive", "Actual Negative"]
tn = df_edited.loc["Test Negative", "Actual Negative"]

prev = st.number_input("Enter Prevalence Rate (in %):")

if st.button("Compute"):
    results_table = create_results_table(tp, fn, fp, tn, prev)
    st.table(results_table)

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
