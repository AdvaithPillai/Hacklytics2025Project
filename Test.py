import streamlit as st

def get_suitable_insurance(age, condition):
    insurance_options = {
        "General Health": ["Plan A", "Plan B"],
        "Chronic Condition": ["Plan C", "Plan D"],
        "Senior Care": ["Plan E", "Plan F"]
    }
    
    if age > 60:
        return insurance_options["Senior Care"]
    elif condition.lower() in ["diabetes", "hypertension"]:
        return insurance_options["Chronic Condition"]
    else:
        return insurance_options["General Health"]

# Using a spacer column
col1, spacer, col2 = st.columns([1, 0.5, 1])  

with col1:
    st.header("Patient Data Input")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    condition = st.text_input("Medical Condition")

with col2:
    st.header("Suitable Insurance Plans")
    
    if age and condition:
        suitable_insurance = get_suitable_insurance(age, condition)
        st.write(f"Recommended Plans for {name}:")
        for plan in suitable_insurance:
            st.write(f"- {plan}")
