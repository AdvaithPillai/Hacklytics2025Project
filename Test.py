#Import Streamlit Library
import streamlit as st


st.set_page_config(layout="wide")

#Placeholder Data for the right side
def get_suitable_insurance(age, conditions, plan_type, budget, family_ages=[]):
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


#Column 1 (Form Data)
with col1:

    # Heading
    st.header("Patient Data Input")

    # Create Form
    with st.form(key="user_form"):
    
        # Plan Type Selection
        plan_type = st.radio("Select Plan Type:", ["Individual", "Family"])

        # Common Inputs
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)

        # **Budget Slider**
        budget = st.slider("Select Budget ($)", min_value=0, max_value=200000, step=1000, value=50000)

        # Handling Multiple Medical Conditions
        st.subheader("Medical Conditions")

        new_condition = st.text_input("Enter a medical condition", key="condition_input")

        col_add, col_remove = st.columns([1, 1])
        with col_add:
            if st.form_submit_button("+ Add Condition"):
                if new_condition and new_condition not in st.session_state.conditions:
                    st.session_state.conditions.append(new_condition)
                    #st.session_state["condition_input"] = ""  # Reset text input field

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

    #Check when submit button is pressed
    # **Processing Submission**
    if submit_button:  # This runs only when form is submitted
        # Construct JSON Data
        data = {
            "name": name,
            "age": age,
            "conditions": st.session_state.conditions,
            "plan_type": plan_type,
            "family_ages": family_ages if plan_type == "Family" else []
        }

        #Print out Submit data (Debugging)
        st.write(data)

        #try:
            # Send JSON Data to Backend
            #response = requests.post(BACKEND_URL, json=data)

            #if response.status_code == 200:
                #result = response.json()  # Expecting JSON response from backend
                #st.success("Insurance plans received successfully!")
                #st.write(result)

                # Update session state with the result from backend
                #st.session_state.insurance_plans = result

            #else:
                #st.error("Error from backend: " + response.text)

        #except requests.exceptions.RequestException as e:
            #st.error(f"Request failed: {e}")
            
            # Optionally, you could fallback to default or local logic
            #plans = get_suitable_insurance(age, st.session_state.conditions, plan_type, budget)
            #st.session_state.insurance_plans = plans

    # Display the insurance plans stored in session state
    #if "insurance_plans" in st.session_state:
        #st.write(st.session_state.insurance_plans)



# **This prevents col2 from being cleared when updating conditions**
#Column 2
with col2:

    st.header("Suitable Insurance Plans")

    # **Top section - Placeholder for total estimated price**
    st.markdown(f"## Estimated Monthly Cost: **${budget // 12:,}**")  # Approximate monthly budget

    # **Bottom section - Four blank cards**
    st.markdown("### Select an Insurance Plan:")

    cols = st.columns(4)  # Create four equal columns

    for idx in range(4):
        with cols[idx]:
            st.markdown(
                f"""
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