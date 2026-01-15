import streamlit as st
import os
import pandas as pd
from PIL import Image

# --- Config ---
st.set_page_config(layout="wide", page_title="Nashik Geospatial Analysis (2017-25)")

# --- Paths ---
# Use relative paths assuming app is run from /webapp/ folder or root
# We'll normalize to root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
FINDINGS_DIR = os.path.join(ROOT_DIR, "findings")
ASSETS_DIR = os.path.join(ROOT_DIR, "nsk_dist_plt")

# --- Helper Functions ---
def load_image(path):
    if os.path.exists(path):
        return Image.open(path)
    else:
        return None

def get_taluka_list():
    if os.path.exists(FINDINGS_DIR):
        # List folders that are not 'onion_price'
        dirs = [d for d in os.listdir(FINDINGS_DIR) 
                if os.path.isdir(os.path.join(FINDINGS_DIR, d)) and d != "onion_price"]
        return sorted(dirs)
    return []

# --- Sidebar ---
st.sidebar.title("Navigation")
talukas = get_taluka_list()
if not talukas:
    st.sidebar.warning("No Taluka data found in /findings/")

options = ["Overview"] + talukas
selection = st.sidebar.radio("Go to taluka:", options)

# --- Main Page : Overview ---
if selection == "Overview":
    col_title, col_about = st.columns([0.9, 0.1])
    with col_title:
        st.markdown("# **Analysis of Agricultural Intensification & Market Dynamics: Nashik District (2017-2025)**")
        st.markdown("Evaluating the responsiveness of cropping patterns to market price signals and mandi proximity.")
    with col_about:
        if st.button("About Me"):
            st.session_state['show_about'] = True
    
    if st.session_state.get('show_about', False):
        st.markdown("## About Me")
        st.markdown("""
        **Project By**: Sanket G.
        """)
        st.markdown("**Sanket G.** | *Passionate Researcher in field of economics*")
        st.markdown("""
        Passionate about bridging the gap between raw data and actionable insights. With a strong background in 
        analyzing complex datasets in field of seconomics, I focus on developing innovative, data-driven solutions to 
        understand real-world economic challenges with keen interst in spatial econometrics.

        This project reflects my enthusiasm for exploring the interaction between **geospatial 
        market proximity** and **crop pattern change**. 
        """)

        st.markdown("#### **Connect & Explore**")
        st.markdown("- [**Blog: infoaccess.wordpress.com**](https://infoaccess.wordpress.com)")
        st.markdown("- [**GitHub: metalwings-design**](https://github.com/metalwings-design)")
        st.markdown("- [**LinkedIn**](https://www.linkedin.com/in/23f87u6ytreszdxc)")

        st.markdown("---")

        st.markdown("#### **Acknowledgment**")
        st.markdown("""
        This dashboard was developed as part of the **CoRE Stack Innovation Challenge on Geospatial Programming – 1st Edition** (December 2025).
        I would like to extend my sincere gratitude to the **CoRE Stack team** for providing the comprehensive data—including multi-temporal LULC rasters that made this deep-dive analysis of the Nashik agricultural landscape possible. Thanks!
        """)

        st.markdown("---")
        if st.button("Back to Dashboard"):
            st.session_state['show_about'] = False
            st.rerun()
        st.markdown("---")
        st.stop() # key: stop execution here so it acts like a separate page
    
    # Intro Section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("District Context")
        img_intro = load_image(os.path.join(ASSETS_DIR, "Figure_10_intro_loc.jpeg"))
        if img_intro:
            st.image(img_intro, caption="Market & Trader Locations", use_container_width=True)
        else:
            st.warning("Intro Image (Figure_10) not found.")

    with col2:
        st.subheader("Agricultural Profile")
        st.markdown("""
        **Nashik District** is agricultural hub in India, characterized by:
        - **Semi-arid Climate**: Moderate temperatures conducive to onions/grapes.
        - **Soil**: Rich loamy soils offering excellent drainage.
        - **Seasonality**: Distinct Kharif (Monsoon), Late Kharif, and Rabi seasons.
        
        """)

    st.markdown("---")
    
    # Market Trends
    st.subheader("Market Price Dynamics")
    img_heat = load_image(os.path.join(ASSETS_DIR, "Figure_8_heat_map.jpeg"))
    if img_heat:
        st.image(img_heat, caption="Monthly Onion Price Heatmap", use_container_width=True)
    else:
        st.warning("Heatmap Image (Figure_8) not found.")

    st.markdown("---")

    # Stats Section
    st.subheader("Statistical Analysis")
    
    st.markdown("### Correlation Matrix")
    st.markdown("""
    **Variable Breakdown**:
    - **Price T-1 vs Single_Kharif**: Impact on traditional monsoon farming.
    - **Price T-1 vs Single_Non_Kharif**: Specialized single-season farming.
    - **Price T-1 vs Double_Crop**: Response via Rabi adoption.
    - **Price T-1 vs Triple_Crop**: Sensitivity of year-round farming.
    """)
    csv_pearson = os.path.join(ASSETS_DIR, "pearson.csv")
    if os.path.exists(csv_pearson):
        df_p = pd.read_csv(csv_pearson)
        st.dataframe(df_p)
    else:
        st.info("pearson.csv not found in assets directory.")

    st.markdown("---")

    st.markdown("### Elasticity Matrix")
    st.markdown("""
    **Interpretation Benchmarks**:
    - **> 1.0 / < -1.0 (Elastic)**: High sensitivity to profit.
    - **-1.0 to 1.0 (Inelastic)**: Resistance (subsistence/infrastructure).
    - **Negative**: Opportunity cost / crop switching.
    """)
    csv_elast = os.path.join(ASSETS_DIR, "elasticity.csv")
    if os.path.exists(csv_elast):
        df_e = pd.read_csv(csv_elast)
        st.dataframe(df_e)
    else:
        st.info("elasticity.csv not found in assets directory.")

# --- Taluka Page ---
else:
    taluka_name = selection
    taluka_path = os.path.join(FINDINGS_DIR, taluka_name)
    
    st.markdown(f"# **{taluka_name}**")
    
    # 1. Price Model
    st.markdown("### 1. Onion Price")
    # Try to find a price plot that matches the Taluka name (approx) or show available
    price_dir = os.path.join(FINDINGS_DIR, "onion_price")
    price_plot_found = False
    
    if os.path.exists(price_dir):
        # Simple match: check if Taluka name is part of filename
        price_files = [f for f in os.listdir(price_dir) if f.endswith(".jpg")]
        # Fuzzy match logic could go here. For now, strict containment.
        matches = [f for f in price_files if taluka_name.lower() in f.lower()]
        
        if matches:
            # Display first match
            img_price = load_image(os.path.join(price_dir, matches[0]))
            st.image(img_price, caption=f"Price Trend: {matches[0]}", use_container_width=True)
            price_plot_found = True
        else:
            # Fallback: List generic or all if small
            pass
            
    if not price_plot_found:
        st.info(f"No specific price plot found matching '{taluka_name}' in findings/onion_price/. Local Mandi data might be missing.")

    st.markdown("---")

    # 2. Multi-Temporal Visuals
    st.markdown("### 2. Multi-Temporal Analysis (2017 - 2025)")
    
    # Year Slider
    years = [f"{y}-{y+1}" for y in range(2017, 2025)] # 2017-2018 to 2024-2025
    selected_year_label = st.select_slider("Select Academic Year:", options=years)
    
    # Safe year string for filenames (remove - if your script uses different format)
    # Based on taluka.py: filenames are like 'combined_crops_20172018.jpg' or '2017-2018.jpg'
    # taluka.py uses: safe_year = year_label.replace(' ', '').replace(':', '') -> "2017-2018"
    # Actually taluka.py line: safe_year = year_label.replace(' ', '').replace(':', '') 
    # If label is "2017 - 2018", safe is "2017-2018".
    
    safe_year_str = selected_year_label # "2017-2018" matches
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("**Combined Crop Layers**")
        fname = f"combined_crops_{safe_year_str}.jpg"
        img = load_image(os.path.join(taluka_path, fname))
        if img:
            st.image(img, caption=f"Crop Patterns ({selected_year_label})", use_container_width=True)
        else:
            st.warning(f"File not found: {fname}")

    with c2:
        st.markdown("**Intensification Hotspots**")
        fname = f"hotspots_{safe_year_str}.jpg"
        img = load_image(os.path.join(taluka_path, fname))
        if img:
            st.image(img, caption=f"Hotspots ({selected_year_label})", use_container_width=True)
        else:
            st.warning(f"File not found: {fname}")

    st.markdown("#### Distance Analysis")
    fname = f"dist_distrib_{safe_year_str}.jpg"
    img = load_image(os.path.join(taluka_path, fname))
    if img:
        st.image(img, caption=f"Distance Distribution ({selected_year_label})", width=600)
    else:
        st.warning(f"File not found: {fname}")

    st.markdown("---")

    # 3. Static Analysis
    st.markdown("### 3. Change & Transition Analysis")
    
    st.markdown("**Year-on-Year (YoY) Change**")
    cols = st.columns(4)
    crops = ["Single_Kharif", "Single_Non_Kharif", "Double_Crop", "Triple_Crop"]
    
    for idx, crop in enumerate(crops):
        fname = f"YoY_{crop}.jpg"
        img = load_image(os.path.join(taluka_path, fname))
        with cols[idx]:
            if img:
                st.image(img, caption=crop.replace('_', ' '), use_container_width=True)
            else:
                st.caption(f"No YoY data for {crop}")

    st.markdown("**Land Use Transition Map**")
    fname = "transition_map.jpg"
    img = load_image(os.path.join(taluka_path, fname))
    if img:
         st.image(img, caption=f"Transition Map (2017-2025)", use_container_width=True)
    else:
         st.warning("Transition map not found.")

