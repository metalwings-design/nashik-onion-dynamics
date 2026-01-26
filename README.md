**Analysis of Agricultural Intensification & Market Dynamics: Nashik District (2017-2025)**
This research project presents a comprehensive spatio-temporal analysis of the agricultural landscape in Nashik, Maharashtra, specifically focusing on the relationship between onion market economics and land-use transitions. By integrating multi-temporal satellite imagery with econometric modeling, this study quantifies how intensified cropping patterns—such as Double and Triple cropping—respond to previous year price signals and proximity to market infrastructure (Mandis). I would like to extend my sincere gratitude to the CoRE Stack team for providing the comprehensive data—including multi-temporal LULC rasters that made this deep-dive analysis of the Nashik agricultural landscape possible.

#Project Context
This project was developed as part of the CoRE Stack Innovation Challenge on Geospatial Programming (1st Edition), held from December 2025 to January 2026. This challenge focused on leveraging the CoRE Stack platform to drive innovation in sustainable land and water management through advanced data science.

Official Challenge Information: core-stack.org/innovation-challenge-1st-edition

Live Interactive Dashboard: nashik-onion-dynamics.streamlit.app

#Technical Highlights
Geospatial Processing: Analyzed LULC rasters from 2017–2025 to map land-use intensification hotspots using hexagonal binning and coordinate transformation.

Spatial Econometrics: Utilized cKDTree algorithms for high-speed proximity analysis, establishing the "Market Decay Effect" between intensification zones and Mandi locations.

Economic Modeling: Calculated Spearman Correlation and Supply Elasticity for 15 Talukas to determine the sensitivity of different cropping patterns (Kharif, Double, Triple) to market price volatility.

Deployment: Developed a multi-page Streamlit application to visualize district-wide trends and taluka-specific temporal transitions.
