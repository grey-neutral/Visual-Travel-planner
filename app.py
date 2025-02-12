import streamlit as st
from PIL import Image
import folium
from streamlit_folium import st_folium
import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import random
import requests
from io import BytesIO

# -------------------------------------------------------------------
# Dummy Data & Functions (Replace with real API calls as needed)
# -------------------------------------------------------------------

# A sample list of London attractions with updated image URLs
attractions_data = [
    # Museums
    {"name": "The British Museum", "description": "A museum dedicated to human history, art, and culture.", "lat": 51.5194, "lon": -0.1270, "image_url": "https://images.pexels.com/photos/27948896/pexels-photo-27948896/free-photo-of-the-great-hall-of-the-british-museum.jpeg", "type": "Museums"},
    {"name": "Natural History Museum", "description": "Exhibits a vast range of specimens from various segments of natural history.", "lat": 51.4967, "lon": -0.1764, "image_url": "https://images.pexels.com/photos/30397052/pexels-photo-30397052/free-photo-of-whale-skeleton-in-london-s-natural-history-museum.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500", "type": "Museums"},
    {"name": "Victoria and Albert Museum", "description": "The world's largest museum of applied and decorative arts and design.", "lat": 51.4966, "lon": -0.1722, "image_url": "https://images.pexels.com/photos/3765332/pexels-photo-3765332.jpeg?cs=srgb&dl=pexels-naveen-annam-734127-3765332.jpg&fm=jpg", "type": "Museums"},
    {"name": "Tate Modern", "description": "Britain's national gallery of international modern art.", "lat": 51.5076, "lon": -0.0994, "image_url": "https://images.pexels.com/photos/11235054/pexels-photo-11235054.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500", "type": "Museums"},
    {"name": "National Gallery", "description": "Houses a rich collection of over 2,300 paintings dating from the mid-13th century to 1900.", "lat": 51.5089, "lon": -0.1283, "image_url": "https://images.pexels.com/photos/7930261/pexels-photo-7930261.jpeg?auto=compress&cs=tinysrgb&h=627&fit=crop&w=1200", "type": "Museums"},
    {"name": "Imperial War Museum", "description": "Explores the impact of modern conflicts on people and society.", "lat": 51.4961, "lon": -0.1084, "image_url": "https://images.pexels.com/photos/18248830/pexels-photo-18248830.jpeg?cs=srgb&dl=pexels-mrphotographerlondon-18248830.jpg&fm=jpg", "type": "Museums"},
    {"name": "Royal Academy of Arts", "description": "Promotes the creation, enjoyment, and appreciation of the visual arts.", "lat": 51.5094, "lon": -0.1396, "image_url": "https://images.pexels.com/photos/18490899/pexels-photo-18490899/free-photo-of-statues-at-royal-academy-of-arts-in-london.jpeg", "type": "Museums"},

    # Outdoor Spots
    {"name": "Hyde Park", "description": "One of London's largest parks with plenty of leisure activities.", "lat": 51.5073, "lon": -0.1657, "image_url": "https://images.pexels.com/photos/8461958/pexels-photo-8461958.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500", "type": "Outdoor Spots"},
    {"name": "Regent's Park", "description": "A large park with gardens, a lake, and the London Zoo.", "lat": 51.5311, "lon": -0.1596, "image_url": "https://images.pexels.com/photos/19737302/pexels-photo-19737302/free-photo-of-people-on-a-bridge-in-a-park-in-fall.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500", "type": "Outdoor Spots"},
    {"name": "Kensington Gardens", "description": "A beautiful park with Kensington Palace and the Serpentine Gallery.", "lat": 51.5074, "lon": -0.1823, "image_url": "https://images.pexels.com/photos/28319140/pexels-photo-28319140/free-photo-of-royal-gardens-at-kensington-palace.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500", "type": "Outdoor Spots"},
    {"name": "Greenwich Park", "description": "A historic park with stunning views of the Thames and the city.", "lat": 51.4769, "lon": -0.0005, "image_url": "https://images.pexels.com/photos/16149662/pexels-photo-16149662.jpeg?cs=srgb&dl=pexels-wolfart-16149662.jpg&fm=jpg", "type": "Outdoor Spots"},
    {"name": "St James's Park", "description": "A royal park with a lake and views of Buckingham Palace.", "lat": 51.5034, "lon": -0.1346, "image_url": "https://images.pexels.com/photos/29989285/pexels-photo-29989285.jpeg?cs=srgb&dl=pexels-489957918-29989285.jpg&fm=jpg", "type": "Outdoor Spots"},
    {"name": "Victoria Park", "description": "A large park in East London with lakes, gardens, and sports facilities.", "lat": 51.5361, "lon": -0.0392, "image_url": "https://images.pexels.com/photos/1485452/pexels-photo-1485452.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500", "type": "Outdoor Spots"},

    # Restaurants
    {"name": "The Ledbury", "description": "A two-Michelin-starred restaurant offering modern European cuisine.", "lat": 51.5167, "lon": -0.2006, "image_url": "https://images.pexels.com/photos/6555512/pexels-photo-6555512.jpeg", "type": "Restaurants"},
    {"name": "Dishoom", "description": "A popular Bombay-style café serving Indian comfort food.", "lat": 51.5151, "lon": -0.1182, "image_url": "https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?cs=srgb&dl=pexels-marvin-ozz-1297854-2474661.jpg&fm=jpg", "type": "Restaurants"},
    {"name": "Sketch", "description": "A quirky restaurant with artistic interiors and French cuisine.", "lat": 51.5098, "lon": -0.1406, "image_url": "https://media.istockphoto.com/id/1370926806/photo/fried-thin-pancakes-crepe-stuffed-potato-with-herring-fish-in-plate.jpg?b=1&s=612x612&w=0&k=20&c=YQ0J8Tdj31QSh_juZEGxaYg12Iy4i8hq9TKzuqgsQ84=", "type": "Restaurants"},
    {"name": "Hakkasan", "description": "A high-end Chinese restaurant with a modern twist.", "lat": 51.5142, "lon": -0.1488, "image_url": "https://images.pexels.com/photos/5848607/pexels-photo-5848607.jpeg?cs=srgb&dl=pexels-polina-tankilevitch-5848607.jpg&fm=jpg", "type": "Restaurants"},
    {"name": "Barrafina", "description": "A Michelin-starred Spanish tapas bar.", "lat": 51.5123, "lon": -0.1312, "image_url": "https://media.istockphoto.com/id/172721308/de/foto/tapas-auswahl.jpg?b=1&s=612x612&w=0&k=20&c=b7To7sl4AzJ8PtvxH6J6pgkNAzh4J2sIHfg1wXHJIMw=", "type": "Restaurants"},
    {"name": "Gymkhana", "description": "A Michelin-starred Indian restaurant with a colonial club vibe.", "lat": 51.5121, "lon": -0.1465, "image_url": "https://images.pexels.com/photos/29173114/pexels-photo-29173114.jpeg?cs=srgb&dl=pexels-kunal-lakhotia-781256899-29173114.jpg&fm=jpg", "type": "Restaurants"},
    {"name": "The Ivy", "description": "A classic British restaurant with a celebrity following.", "lat": 51.5115, "lon": -0.1348, "image_url": "https://media.istockphoto.com/id/134178657/photo/fish-and-chips.jpg?b=1&s=612x612&w=0&k=20&c=5pIoZP1odQfpdlN4Y1HHpE-lX99yE0pWmv4vPyZ_URY=", "type": "Restaurants"},

    # Historical Sites
    {"name": "Tower of London", "description": "Historic castle located on the north bank of the River Thames.", "lat": 51.5081, "lon": -0.0759, "image_url": "https://images.pexels.com/photos/18504587/pexels-photo-18504587.jpeg?cs=srgb&dl=pexels-sofia-marquet-453708414-18504587.jpg&fm=jpg", "type": "Historical Sites"},
    {"name": "Westminster Abbey", "description": "A historic church where British monarchs are crowned.", "lat": 51.4994, "lon": -0.1273, "image_url": "https://images.pexels.com/photos/19764030/pexels-photo-19764030/free-photo-of-view-of-a-red-telephone-booth-and-the-westminster-abbey-in-london-england-uk.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500", "type": "Historical Sites"},
    {"name": "Houses of Parliament", "description": "The seat of the UK Parliament, including the iconic Big Ben.", "lat": 51.4997, "lon": -0.1247, "image_url": "https://images.pexels.com/photos/672532/pexels-photo-672532.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500", "type": "Historical Sites"},
    {"name": "St Paul's Cathedral", "description": "An iconic cathedral with a dome that dominates the London skyline.", "lat": 51.5138, "lon": -0.0983, "image_url": "https://images.pexels.com/photos/2425694/pexels-photo-2425694.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500", "type": "Historical Sites"},
    {"name": "Buckingham Palace", "description": "The London residence of the UK's sovereigns since 1837.", "lat": 51.5014, "lon": -0.1419, "image_url": "https://images.pexels.com/photos/15291566/pexels-photo-15291566.jpeg?cs=srgb&dl=pexels-njeromin-15291566.jpg&fm=jpg", "type": "Historical Sites"},
    {"name": "Kensington Palace", "description": "A royal residence set in Kensington Gardens.", "lat": 51.5054, "lon": -0.1874, "image_url": "https://images.pexels.com/photos/18950440/pexels-photo-18950440.jpeg?cs=srgb&dl=pexels-andreas-leindecker-730264322-18950440.jpg&fm=jpg", "type": "Historical Sites"},
    {"name": "The Shard", "description": "A modern skyscraper with an observation deck offering panoramic views.", "lat": 51.5045, "lon": -0.0865, "image_url": "https://images.pexels.com/photos/28352925/pexels-photo-28352925/free-photo-of-london-the-shard.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500", "type": "Historical Sites"},
    {"name": "Tower Bridge", "description": "A combined bascule and suspension bridge over the River Thames.", "lat": 51.5055, "lon": -0.0754, "image_url": "https://images.pexels.com/photos/51363/london-tower-bridge-bridge-monument-51363.jpeg?cs=srgb&dl=pexels-pixabay-51363.jpg&fm=jpg", "type": "Historical Sites"},

    # Activities
    {"name": "London Eye", "description": "A giant Ferris wheel on the South Bank of the River Thames.", "lat": 51.5033, "lon": -0.1196, "image_url": "https://images.pexels.com/photos/3835461/pexels-photo-3835461.jpeg?cs=srgb&dl=pexels-alex-chistol-1715967-3835461.jpg&fm=jpg", "type": "Activities"},
    {"name": "Madame Tussauds", "description": "A wax museum featuring lifelike figures of famous celebrities.", "lat": 51.5230, "lon": -0.1544, "image_url": "https://images.pexels.com/photos/16035584/pexels-photo-16035584/free-photo-of-wax-sculpture-in-a-museum.jpeg", "type": "Activities"},
    {"name": "The London Dungeon", "description": "A theatrical attraction showcasing London's dark history.", "lat": 51.5025, "lon": -0.1193, "image_url": "https://upload.wikimedia.org/wikipedia/commons/5/51/London_-_The_London_Dungeon_-_panoramio.jpg", "type": "Activities"},
    {"name": "London Zoo", "description": "The world's oldest scientific zoo with a wide range of animals.", "lat": 51.5353, "lon": -0.1534, "image_url": "https://images.pexels.com/photos/14477193/pexels-photo-14477193.jpeg?cs=srgb&dl=pexels-rico-14477193.jpg&fm=jpg", "type": "Activities"},
    {"name": "Shakespeare's Globe", "description": "A reconstruction of the Globe Theatre, showcasing Shakespearean plays.", "lat": 51.5081, "lon": -0.0972, "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Shakespeare%27s_Globe-London.jpg/2560px-Shakespeare%27s_Globe-London.jpg", "type": "Activities"},
    {"name": "The Royal Observatory", "description": "The historic site of the Prime Meridian and Greenwich Mean Time.", "lat": 51.4769, "lon": -0.0005, "image_url": "https://images.pexels.com/photos/13121987/pexels-photo-13121987/free-photo-of-london-the-royal-observatory-greenwich.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500", "type": "Activities"}
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
    If more, it will randomly pick different attractions for each day to provide variation
    """
    itinerary = {}
    total_slots = trip_duration * 3
    selected_count = len(selected_attractions)

    schedule = []
    if selected_count >= total_slots:
        # Randomly select attractions to fill the schedule and ensure variation
        schedule_pool = selected_attractions[:]  # Create a copy to avoid modifying original
        for _ in range(total_slots):
            attraction = random.choice(schedule_pool)
            schedule.append(attraction)
            if attraction in schedule_pool:
                schedule_pool.remove(attraction)
            if not schedule_pool:
                schedule_pool = selected_attractions[:]
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

def create_folium_map(selected_attractions):
    """
    Creates and returns a Folium map with visible markers
    for each selected attraction.
    """
    m = folium.Map(location=[51.5074, -0.1278], zoom_start=12)
    for attraction in selected_attractions:
        # Use a standard Folium Icon to avoid any missing icon issues
        folium.Marker(
            location=[attraction["lat"], attraction["lon"]],
            popup=attraction["name"],
            tooltip=attraction["name"],
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)
    return m

from fpdf import FPDF

def generate_pdf(itinerary, selected_attractions):
    """
    Generates a PDF of the itinerary using the FPDF library,
    but does NOT embed any images (only text).
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Optional title
    pdf.cell(0, 10, "Your London Itinerary", ln=True, align="C")
    pdf.ln(5)

    # Iterate over days and slots, printing text only
    for day, schedule in itinerary.items():
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, txt=day, ln=True, align='L')
        pdf.set_font("Arial", size=12)

        for slot, attraction in schedule.items():
            line_text = f"{slot}: {attraction['name']}"
            pdf.multi_cell(0, 8, txt=line_text)
            pdf.multi_cell(0, 8, txt=attraction['description'])
            pdf.ln(5)

        pdf.ln(5)

    return pdf

def validate_selection(selected_attractions, trip_duration):
    """
    Validates if the number of selected attractions is sufficient for the trip duration.
    """
    min_activities = 0
    if trip_duration == 1:
        min_activities = 3
    elif trip_duration == 2:
        min_activities = 6
    elif trip_duration == 3:
        min_activities = 9

    if len(selected_attractions) < min_activities:
        return (False, f"For a {trip_duration}-day trip, please select at least {min_activities} attractions. You have selected {len(selected_attractions)}.")
    return (True, None)

# -------------------------------------------------------------------
# Main Application Code
# -------------------------------------------------------------------
def main():
    st.title("Visual Travel Planner")
    st.markdown("Plan your perfect London trip with a customized itinerary and map view. (NOTE: This app is just a proof of concept and might not be fully functional.)")

    # Sidebar for Trip Details
    st.sidebar.header("Trip Details")
    trip_duration = st.sidebar.selectbox("Trip Duration (Days)", options=[1, 2, 3], index=0)
    activity_types = st.sidebar.multiselect(
        "Activity Types",
        options=["Museums", "Outdoor Spots", "Restaurants", "Historical Sites", "Activities"],
        default=["Museums", "Historical Sites"]
    )
    walking_tolerance = st.sidebar.radio("Walking Tolerance", options=["Low", "Medium", "High"], index=1)
    st.sidebar.caption("_(not functional yet)_")

    st.header("Explore Attractions in London")
    st.markdown("Select the attractions you’d like to include in your itinerary.")

    # Fetch attractions (simulated API call)
    all_attractions = fetch_attraction_images()

    # Filter attractions based on selected activity types
    if activity_types:
        attractions = [attr for attr in all_attractions if attr["type"] in activity_types]
    else:
        attractions = all_attractions

    # Container for user-selected attractions
    if "selected_attractions" not in st.session_state:
        st.session_state.selected_attractions = []

    # Display attractions in cards with image and description
    if not attractions:
        st.warning("No attractions match the selected activity types.")
    else:
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

    # Display list of selected attractions
    if st.session_state.selected_attractions:
        st.subheader("Your Selected Attractions")
        for attr in st.session_state.selected_attractions:
            st.write(f"- {attr['name']}")

        # Button to generate the itinerary
        if st.button("Generate Itinerary"):
            is_valid, error_message = validate_selection(st.session_state.selected_attractions, trip_duration)
            if not is_valid:
                st.error(error_message)
            else:
                itinerary = generate_itinerary(st.session_state.selected_attractions, trip_duration)
                st.session_state.itinerary = itinerary
                st.success("Itinerary Generated!")

    # Display the itinerary if it exists
    if "itinerary" in st.session_state:
        st.subheader("Your Itinerary")
        for day, slots in st.session_state.itinerary.items():
            st.markdown(f"### {day}")
            for slot, attraction in slots.items():
                st.write(f"**{slot}**: {attraction['name']}  \n_{attraction['description']}_")


        # Map Integration: Show selected attractions on a Folium map
        st.subheader("Map View")
        folium_map = create_folium_map(st.session_state.selected_attractions)
        st_folium(folium_map, width=700)

        # PDF Download Section
        st.subheader("Download Your Itinerary")
        if st.button("Generate PDF Itinerary"):
            pdf = generate_pdf(st.session_state.itinerary, st.session_state.selected_attractions)
            pdf_bytes = pdf.output(dest="S").encode("latin-1")
            st.download_button(
                label="Download PDF Itinerary",
                data=pdf_bytes,
                file_name="London_Itinerary.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()
