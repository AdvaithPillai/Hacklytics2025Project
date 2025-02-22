import streamlit as st

# Function to get suitable insurance (same logic as before)
def get_suitable_insurance(age, conditions, plan_type, family_ages=[]):
    insurance_options = {
        "General Health": ["Plan A", "Plan B"],
        "Chronic Condition": ["Plan C", "Plan D"],
        "Senior Care": ["Plan E", "Plan F"]
    }
    
    if age > 60:
        plans = insurance_options["Senior Care"]
    elif any(cond.lower() in ["diabetes", "hypertension"] for cond in conditions):
        plans = insurance_options["Chronic Condition"]
    else:
        plans = insurance_options["General Health"]

    if plan_type == "Family":
        plans = [plan + " (Family Plan)" for plan in plans]  

    return plans

# Initialize session state for conditions and new condition input
if "conditions" not in st.session_state:
    st.session_state.conditions = []

if "new_condition" not in st.session_state:
    st.session_state.new_condition = ""

# Function to clear the input field
def clear_condition_input():
    st.session_state["new_condition"] = ""

# Layout: Input on one side, Output on the other
col1, spacer, col2 = st.columns([1, 0.5, 1])

with col1:
    st.header("Patient Data Input")
    
    # Plan Type Selection
    plan_type = st.radio("Select Plan Type:", ["Individual", "Family"])

    # Common Inputs
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)

    # Handling Multiple Medical Conditions
    st.subheader("Medical Conditions")

    with st.form("condition_form"):
        f1, f2 = st.columns([3, 1])  # Wider input, smaller button
        with f1:
            st.text_input("Enter a medical condition", key="new_condition")
        with f2:
            st.form_submit_button(label="+", on_click=clear_condition_input)

        # Submit button for adding condition
        add_condition = st.form_submit_button(label ="Add Condition")
        if add_condition and st.session_state.new_condition.strip():
            condition = st.session_state.new_condition.strip()
            if condition not in st.session_state.conditions:
                st.session_state.conditions.append(condition)
              # Clear input field after adding

    # Display added conditions
    if st.session_state.conditions:
        st.write("Current Conditions:")
        for cond in st.session_state.conditions:
            st.write(f"- {cond}")

    # Clear all conditions button
    if st.button("- Clear Conditions"):
        st.session_state.conditions = []

    # Family Plan Inputs
    family_ages = []
    if plan_type == "Family":
        family_size = st.number_input("Number of Family Members", min_value=1, step=1)
        
        # Dynamically generate input boxes for each family member's age
        for i in range(family_size):
            member_age = st.number_input(f"Age of Family Member {i+1}", min_value=0, max_value=120, step=1)
            family_ages.append(member_age)

with col2:
    st.header("Suitable Insurance Plans")
    
    if age and st.session_state.conditions:
        suitable_insurance = get_suitable_insurance(age, st.session_state.conditions, plan_type, family_ages)
        st.write(f"Recommended Plans for {name}:")
        for plan in suitable_insurance:
            st.write(f"- {plan}")
