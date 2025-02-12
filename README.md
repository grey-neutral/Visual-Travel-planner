# 🗺️ London Visual Travel Planner

A **Streamlit-based web application** that helps users create a **custom travel itinerary for London**. Users can select from a list of attractions (with images in the web app), then generate a **multi-day itinerary** (Morning, Afternoon, Evening). The app provides a **map view** of selected attractions and allows users to **download a PDF** with an itinerary.

---

## 🚀 Features

✅ **User Inputs:**  
- Choose **trip duration** (1–3 days).  
- Filter by **activity types** (Museums, Outdoor Spots, Restaurants, Historical Sites, Activities).  
- Adjust **walking tolerance** (currently not functional, placeholder only).  

✅ **Itinerary Generation:**  
- Displays **a list of attractions** (with images and descriptions in-app).  
- Users **select preferred locations** to fill their itinerary.  
- Automatically creates a **day-by-day schedule** (Morning, Afternoon, Evening).  

✅ **Map Integration:**  
- Shows your **selected attractions** on a **Folium map** of London.  
- Markers indicate each chosen location.  

✅ **PDF Export:**  
- The final **itinerary** can be **downloaded** as a PDF.  
- Each day is listed with Morning, Afternoon, and Evening activities.  

---

## 🛠️ Tech Stack

- **Python** (for backend logic)  
- **Streamlit** (for UI)  
- **Folium** (for map visualization)  
- **FPDF** (for PDF generation)  

---

## 📦 Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/your-username/london-travel-planner.git
   cd london-travel-planner
