import streamlit as st

# Set page configuration for wide layout
st.set_page_config(layout="wide")

# Inject custom CSS for styling
st.markdown("""
    <style>
        /* General background and font styles */
        body {
            background-color: #e3f2fd;  /* Light Blue background */
            font-family: 'Arial', sans-serif;
        }

        /* Center the content */
        .stApp {
            margin: 0 auto;
            max-width: 1200px;
        }

        /* Header Styles */
        h1, h2 {
            color: #1e88e5;  /* Blue color for headers */
        }

        /* Form Section (left column) */
        .stTextInput>div>input, .stNumberInput>div>input {
            border: 2px solid #1e88e5;
            padding: 10px;
            border-radius: 8px;
            font-size: 16px;
            width: 100%;
        }

        /* Slider style */
        .stSlider>div>label {
            font-size: 14px;
            color: #333333;
        }

        /* Radio button style */
        .stRadio>div>label {
            font-size: 16px;
            font-weight: bold;
        }

        /* Button styles */
        .stButton>button {
            background-color: #1e88e5;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
        }

        .stButton>button:hover {
            background-color: #1565c0;
        }

        /* Form Submit Button */
        .stFormSubmitButton>button {
            background-color: #007BFF;
            color: white;
            font-size: 18px;
            border-radius: 8px;
            padding: 10px 20px;
            width: 100%;
        }

        .stFormSubmitButton>button:hover {
            background-color: #0069d9;
        }

        /* Insurance plan cards style */
        .insurance-card {
            height: 150px;
            background-color: #ffffff;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-top: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease-in-out;
        }

        .insurance-card:hover {
            transform: scale(1.05);
        }

        /* Columns for insurance cards */
        .stColumns>div {
            margin-right: 10px;
            margin-left: 10px;
        }

        /* Text for the insurance plan cards */
        .insurance-plan-title {
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }

        .insurance-plan-description {
            color: #777;
        }

    </style>
""", unsafe_allow_html=True)

# Function to get suitable insurance based on input
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

# Column 1 (Form Data)
with col1:
    # Heading
    st.header("Patient Data Input")

    # Create Form
    with st.form(key="user_form"):
        plan_type = st.radio("Select Plan Type:", ["Individual", "Family"])

        # Common Inputs
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        budget = st.slider("Select Budget ($)", min_value=0, max_value=200000, step=1000, value=50000)

        st.subheader("Medical Conditions")
        new_condition = st.text_input("Enter a medical condition", key="condition_input")

        col_add, col_remove = st.columns([1, 1])
        with col_add:
            if st.form_submit_button("+ Add Condition"):
                if new_condition and new_condition not in st.session_state.conditions:
                    st.session_state.conditions.append(new_condition)

        with col_remove:
            if st.form_submit_button("- Clear Conditions"):
                st.session_state.conditions = []

        if st.session_state.conditions:
            st.write("Current Conditions:")
            for cond in st.session_state.conditions:
                st.write(f"- {cond}")

        # Family Plan Inputs
        family_ages = []
        if plan_type == "Family":
            family_size = st.number_input("Number of Family Members", min_value=1, step=1)
            for i in range(family_size):
                member_age = st.number_input(f"Age of Family Member {i+1}", min_value=0, max_value=120, step=1, key=f"family_member_{i}")
                family_ages.append(member_age)

        submit_button = st.form_submit_button(label="Submit")

    # Check when submit button is pressed
    if submit_button:  # This runs only when form is submitted
        data = {
            "name": name,
            "age": age,
            "conditions": st.session_state.conditions,
            "plan_type": plan_type,
            "family_ages": family_ages if plan_type == "Family" else []
        }

        st.write(data)

# **This prevents col2 from being cleared when updating conditions**
# Column 2
with col2:
    st.header("Suitable Insurance Plans")

    # **Top section - Placeholder for total estimated price**
    st.markdown(f"## Estimated Monthly Cost: **${budget // 12:,}**")  # Approximate monthly budget

    # **Bottom section - Four blank cards**
    st.markdown("### Select an Insurance Plan:")

    cols = st.columns(4)  # Create four equal columns

    plans = get_suitable_insurance(age, st.session_state.conditions, plan_type, budget, family_ages)

    for idx, plan in enumerate(plans):
        with cols[idx % 4]:
            st.markdown(
                f"""
                <div class="insurance-card">
                    <div>
                        <div class="insurance-plan-title">{plan}</div>
                        <div class="insurance-plan-description">Details for {plan}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
