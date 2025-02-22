import streamlit as st

def get_suitable_insurance(age, conditions, plan_type, family_ages=[]):
    """Returns suitable insurance plans based on age, conditions, and plan type."""
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

# Initialize session state for conditions
if "conditions" not in st.session_state:
    st.session_state.conditions = []

# **Layout: Shift col1 more to the left & increase gap**
col1, spacer, col2 = st.columns([1.5, 0.8, 2])  # Increased col1 size & spacer

with col1:

    #Heading
    st.header("Patient Data Input")

    # Create Form
    with st.form(key="user_form"):
    
        # Plan Type Selection
        plan_type = st.radio("Select Plan Type:", ["Individual", "Family"])

        # Common Inputs
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)

        # Handling Multiple Medical Conditions
        st.subheader("Medical Conditions")

        new_condition = st.text_input("Enter a medical condition", key="condition_input")

        col_add, col_remove = st.columns([1, 1])
        with col_add:
            if st.form_submit_button("+ Add Condition"):
                if new_condition and new_condition not in st.session_state.conditions:
                    st.session_state.conditions.append(new_condition)
                    st.session_state["condition_input"] = ""  # Reset text input field
                    st.experimental_rerun()  # Force rerun to update UI

        with col_remove:
            if st.form_submit_button("- Clear Conditions"):
                st.session_state.conditions = []

        # Display added conditions
        if st.session_state.conditions:
            st.write("Current Conditions:")
            for cond in st.session_state.conditions:
                st.write(f"- {cond}")

        # Family Plan Inputs
        family_ages = []
        if plan_type == "Family":
            family_size = st.number_input("Number of Family Members", min_value=1, step=1)
            
            # Dynamically generate input boxes for each family member's age
            for i in range(family_size):
                member_age = st.number_input(f"Age of Family Member {i+1}", min_value=0, max_value=120, step=1, key=f"family_member_{i}")
                family_ages.append(member_age)

        # Submit Button for the form
        submit_button = st.form_submit_button(label="Submit")

# **Increased space between columns**
with col2:
    st.header("Suitable Insurance Plans")

    # **Top section - Placeholder for total estimated price**
    st.markdown("## Estimated Monthly Cost: **$____**")

    # **Bottom section - Four blank cards**
    st.markdown("### Select an Insurance Plan:")

    cols = st.columns(4)  # Create four equal columns

    for idx in range(4):
        with cols[idx]:
            st.markdown(
                """
                <div style="
                    height: 150px; 
                    background-color: #f0f0f0; 
                    border-radius: 10px; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center; 
                    font-weight: bold;
                ">
                    Plan {idx+1}
                </div>
                """,
                unsafe_allow_html=True
            )