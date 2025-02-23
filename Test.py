import streamlit as st
import time  # to simulate processing time
from hacklytics_backend import get_response

# Set page configuration for wide layout
st.set_page_config(layout="wide")

# Inject custom CSS for styling
st.markdown("""
    <style>
        /* Load custom font from Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Anton:wght@400;500&display=swap');

        /* General background and font styles */
        body {
            background-color: #e3f2fd;  /* Light Blue background */
            font-family: 'Anton', sans-serif;  /* Use Anton font */
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

        /* Input labels (questions) - Change font size, weight, and color */
        .stTextInput label, .stNumberInput label, .stRadio label, .stSlider label {
            font-size: 18px;  /* Larger font size */
            font-weight: 500;  /* Medium weight */
            color: #333333;  /* Dark gray color */
            margin-bottom: 10px;  /* Space between label and input */
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

    # Check if the user is an individual or a family
    plan_type = st.radio("Select Plan Type:", ["Individual", "Family"])

    # Create Form
    with st.form(key="user_form"):

        # Family Plan Inputs
        family_ages = []
        if plan_type == "Family":
            # Ask for number of family members within the form itself
            st.session_state.family_size = st.number_input("Number of Family Members", min_value=1, step=1)
            if st.session_state.family_size > 0:
                for i in range(st.session_state.family_size):
                    member_age = st.number_input(f"Age of Family Member {i+1}", min_value=0, max_value=120, step=1, key=f"family_member_{i}")
                    family_ages.append(member_age)

        # Common Inputs
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        budget = st.slider("Select Yearly income($)", min_value=0, max_value=1000000, step=1000, value=50000)

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

        submit_button = st.form_submit_button(label="Submit")

    # **Display Loading Spinner while processing**
    

    if submit_button:
            # Prepare data as a JSON object
            user_data = {
                "name": name,
                "age": age,
                "conditions": [condition.strip() for condition in st.session_state.conditions] if st.session_state.conditions else [],

                "budget": budget,
            }

            # Send the JSON data to backend for processing
            processed_data = get_response(user_data)

           

# Column 2: Display suitable insurance plans
# Column 2: Display suitable insurance plans and processed HTML data
with col2:
    st.header("Suitable Insurance Plans")

    # # Placeholder for estimated monthly cost
    # st.markdown(f"## Estimated Monthly Cost: **${budget // 12:,}**")  # Approximate monthly budget

    # # Display insurance options (simulate a loading effect)
    # st.markdown("### Select an Insurance Plan:")

    # cols = st.columns(4)  # Create four equal columns

    # # Here, you can simulate the time it takes to fetch insurance plans
    # with st.spinner("Fetching insurance options..."):
    #     time.sleep(3)  # Simulate some delay before displaying plans

    # plans = get_suitable_insurance(age, st.session_state.conditions, plan_type, budget, family_ages)

    # for idx, plan in enumerate(plans):
    #     with cols[idx % 4]:
    #         st.markdown(
    #             f"""
    #             <div class="insurance-card">
    #                 <div>
    #                     <div class="insurance-plan-title">{plan}</div>
    #                     <div class="insurance-plan-description">Details for {plan}</div>
    #                 </div>
    #             </div>
    #             """,
    #             unsafe_allow_html=True
    #         )
    
    # Display the processed HTML data in col2 after form submission
    if submit_button:
        st.markdown(f"## Processed Data", unsafe_allow_html=True)
        st.markdown(
        
                processed_data
            , 
            unsafe_allow_html=True)  # Render HTML from processed_data
