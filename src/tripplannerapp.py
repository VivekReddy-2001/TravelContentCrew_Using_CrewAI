import streamlit as st
from tripcrewai import TravelContentCrew  


st.title("Make My Trip - Travel Planning Assistant")
st.write("""
Welcome to the Travel Planning Assistant! This app helps you gather the best options for flights, food, accommodation, and itineraries for your trip.
""")

# User inputs
with st.form("travel_form"):
    from_location = st.text_input("Starting Point of Your Trip", placeholder="e.g., New York")
    to_location = st.text_input("Destination", placeholder="e.g., Paris")
    travel_date = st.text_input("Travel Date Range", placeholder="e.g., 2024-12-10 to 2024-12-20")
    no_of_days = st.text_input("No of Days", placeholder="e.g., 2 Days")
    submit_button = st.form_submit_button("Generate Travel Plan")

# Process the inputs and display the results
if submit_button:
    if from_location and to_location and travel_date:
        st.info("Generating your travel plan. This might take a few moments...")

        # Initializes and runs the TravelContentCrew
        try:
            travel_crew = TravelContentCrew(
                from_location=from_location,
                to_location=to_location,
                travel_date=travel_date,
                no_of_days=no_of_days,  
            )
            result = travel_crew.run_crew()
            
            try:
                main_output = result.raw  # Replace 'raw' with the correct attribute name
                if main_output:
                    st.success("Travel plan generated successfully!")
                    st.subheader("Your Travel Plan")
                    # Render the output as Markdown to include clickable links
                    st.markdown(main_output, unsafe_allow_html=True)
                else:
                    st.warning("No travel plan details found in the output.")
            except AttributeError:
                st.error("Unexpected format in the output. Unable to retrieve travel details.")
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please fill in all the fields before submitting.")

# Footer
st.write("Powered by CrewAI and Streamlit")

