import streamlit as st
import requests
from PIL import Image
import folium
from streamlit_folium import st_folium
import pandas as pd
from fpdf import FPDF

# -------------------------------------------------------------------
# Dummy Data & Functions (Replace with real API calls as needed)
# -------------------------------------------------------------------

# A sample list of London attractions with dummy image URLs (sourced from Unsplash)
attractions_data = [
    {
        "name": "The British Museum",
        "description": "A museum dedicated to human history, art, and culture.",
        "lat": 51.5194,
        "lon": -0.1270,
        "image_url": "https://source.unsplash.com/400x300/?british+museum"
    },
    {
        "name": "Tower of London",
        "description": "Historic castle located on the north bank of the River Thames.",
        "lat": 51.5081,
        "lon": -0.0759,
        "image_url": "https://source.unsplash.com/400x300/?tower+of+london"
    },
    {
        "name": "London Eye",
        "description": "A giant Ferris wheel on the South Bank of the River Thames.",
        "lat": 51.5033,
        "lon": -0.1196,
        "image_url": "https://source.unsplash.com/400x300/?london+eye"
    },
    {
        "name": "Natural History Museum",
        "description": "Exhibits a vast range of specimens from various segments of natural history.",
        "lat": 51.4967,
        "lon": -0.1764,
        "image_url": "https://source.unsplash.com/400x300/?natural+history+museum"
    },
    {
        "name": "Hyde Park",
        "description": "One of London's largest parks with plenty of leisure activities.",
        "lat": 51.5073,
        "lon": -0.1657,
        "image_url": "https://source.unsplash.com/400x300/?hyde+park"
    },
    {
        "name": "Tate Modern",
        "description": "Britain's national gallery of international modern art.",
        "lat": 51.5076,
        "lon": -0.0994,
        "image_url": "https://source.unsplash.com/400x300/?tate+modern"
    },
    # Add more attractions as needed.
]

def fetch_attraction_images():
    """
    This function simulates fetching attractions with images and descriptions.
    In production, call an API (e.g., Unsplash or Wikipedia) to get live data.
    """
    return attractions_data

def generate_itinerary(selected_attractions, trip_duration):
    """
    Generates a structured itinerary based on the number of days.
    For simplicity, each day is divided into three slots: Morning, Afternoon, Evening.
    If the number of selected attractions is less than the total slots,
    the list will cycle through the selections.
    """
    itinerary = {}
    total_slots = trip_duration * 3
    selected_count = len(selected_attractions)
    
    schedule = []
    if selected_count >= total_slots:
        schedule = selected_attractions[:total_slots]
    else:
        # Cycle through the selected attractions if fewer than needed.
        while len(schedule) < total_slots:
            schedule.extend(selected_attractions)
        schedule = schedule[:total_slots]
    
    slots = ["Morning", "Afternoon", "Evening"]
    for day in range(1, trip_duration + 1):
        day_key = f"Day {day}"
        itinerary[day_key] = {}
        for i, slot in enumerate(slots):
            idx = (day - 1) * 3 + i
            itinerary[day_key][slot] = schedule[idx]
    return itinerary

def get_public_transport_recommendation(origin, destination):
    """
    Dummy function to simulate public transport recommendations.
    In practice, you might use a transport API to get accurate routes and travel times.
    """
    # Calculate a dummy “distance” using Euclidean distance
    distance = ((origin[0] - destination[0])**2 + (origin[1] - destination[1])**2) ** 0.5
    # Rough conversion: 1 degree ~ 111 km, and then estimate travel time
    km_distance = distance * 111
    travel_time = max(5, int(km_distance / 5 * 60))  # Ensure a minimum of 5 mins
    recommendation = f"Take a bus or Tube. Estimated travel time: {travel_time} mins."
    return recommendation

def create_folium_map(selected_attractions):
    """
    Creates and returns a Folium map with markers for each selected attraction.
    """
    m = folium.Map(location=[51.5074, -0.1278], zoom_start=12)
    for attraction in selected_attractions:
        folium.Marker(
            location=[attraction["lat"], attraction["lon"]],
            popup=attraction["name"],
            tooltip=attraction["name"]
        ).add_to(m)
    return m

def generate_pdf(itinerary):
    """
    Generates a PDF of the itinerary using the FPDF library.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for day, slots in itinerary.items():
        pdf.cell(200, 10, txt=day, ln=True, align='L')
        for slot, attraction in slots.items():
            line = f"{slot}: {attraction['name']} - {attraction['description']}"
            pdf.multi_cell(0, 10, txt=line)
        pdf.ln(5)
    return pdf

# -------------------------------------------------------------------
# Main Application Code
# -------------------------------------------------------------------
def main():
    st.title("London Travel Planner")
    st.markdown("Plan your perfect London trip with a customized itinerary, map view, and public transport tips.")

    # Sidebar for Trip Details and Preferences
    st.sidebar.header("Trip Details")
    trip_duration = st.sidebar.selectbox("Trip Duration (Days)", options=[1, 2, 3, 4, 5, 6, 7], index=2)
    interests = st.sidebar.multiselect(
        "Interests", 
        options=["History", "Art", "Food", "Shopping", "Parks"], 
        default=["History", "Art"]
    )
    activity_types = st.sidebar.multiselect(
        "Activity Types", 
        options=["Museums", "Outdoor Spots", "Restaurants", "Historical Sites"], 
        default=["Museums", "Historical Sites"]
    )
    walking_tolerance = st.sidebar.radio("Walking Tolerance", options=["Low", "Medium", "High"], index=1)
    restaurant_toggle = st.sidebar.checkbox("Include Restaurant Recommendations", value=True)

    st.header("Explore Attractions in London")
    st.markdown("Select the attractions you’d like to include in your itinerary.")

    # Fetch attractions (simulated API call)
    attractions = fetch_attraction_images()

    # Container for user-selected attractions
    if "selected_attractions" not in st.session_state:
        st.session_state.selected_attractions = []

    # Display attractions in cards with image and description
    for attraction in attractions:
        with st.container():
            cols = st.columns([1, 3])
            with cols[0]:
                st.image(attraction["image_url"], width=150)
            with cols[1]:
                st.subheader(attraction["name"])
                st.write(attraction["description"])
                if st.button(f"Select {attraction['name']}", key=attraction["name"]):
                    if attraction not in st.session_state.selected_attractions:
                        st.session_state.selected_attractions.append(attraction)
                        st.success(f"Added {attraction['name']} to your selection!")

    # Optional: Show message if restaurant recommendations will be included
    if restaurant_toggle:
        st.info("Restaurant recommendations will be included in your itinerary.")

    # Display list of selected attractions
    if st.session_state.selected_attractions:
        st.subheader("Your Selected Attractions")
        for attr in st.session_state.selected_attractions:
            st.write(f"- {attr['name']}")

        # Button to generate the itinerary
        if st.button("Generate Itinerary"):
            itinerary = generate_itinerary(st.session_state.selected_attractions, trip_duration)
            st.session_state.itinerary = itinerary
            st.success("Itinerary Generated!")

    # Display the itinerary if it exists
    if "itinerary" in st.session_state:
        st.subheader("Your Itinerary")
        for day, slots in st.session_state.itinerary.items():
            st.markdown(f"### {day}")
            previous = None
            for slot, attraction in slots.items():
                # Provide public transport recommendation between slots (if not morning)
                transport = ""
                if slot != "Morning" and previous:
                    transport = get_public_transport_recommendation(
                        (previous["lat"], previous["lon"]),
                        (attraction["lat"], attraction["lon"])
                    )
                st.write(f"**{slot}**: {attraction['name']}  \n_{attraction['description']}_")
                if transport:
                    st.write(f"**Public Transport**: {transport}")
                previous = attraction

        # Map Integration: Show selected attractions on a Folium map
        st.subheader("Map View")
        folium_map = create_folium_map(st.session_state.selected_attractions)
        st_data = st_folium(folium_map, width=700)

        # Editing & Customization: Display itinerary in a table that can be rearranged.
        st.subheader("Edit Your Itinerary")
        itinerary_list = []
        for day, slots in st.session_state.itinerary.items():
            for time_slot, attraction in slots.items():
                itinerary_list.append({"Day": day, "Time Slot": time_slot, "Attraction": attraction["name"]})
        itinerary_df = pd.DataFrame(itinerary_list)
        st.markdown("_(Drag and drop rows to rearrange — simulated functionality)_")
        edited_df = st.experimental_data_editor(itinerary_df, num_rows="dynamic")

        # PDF Download Section
        st.subheader("Download Your Itinerary")
        if st.button("Generate PDF"):
            pdf = generate_pdf(st.session_state.itinerary)
            pdf_bytes = pdf.output(dest="S").encode("latin-1")
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name="London_Itinerary.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()
