# streamlit_app.py

import streamlit as st
import pandas as pd
import urllib.parse

# App title
st.title("🍽️ Restaurant Recommender")

# Upload CSV
uploaded_file = st.file_uploader("Upload the Zomato CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, encoding='latin1')

    # Clean data
    data['Cuisines'].fillna(data['Cuisines'].mode()[0], inplace=True)
    data['Cuisines'] = data['Cuisines'].str.lower()
    data['Average Cost for two'] = pd.to_numeric(data['Average Cost for two'].astype(str).str.replace(',', ''), errors='coerce')
    data['Aggregate rating'] = pd.to_numeric(data['Aggregate rating'], errors='coerce')
    data['Votes'] = pd.to_numeric(data['Votes'], errors='coerce').fillna(0).astype(int)

    # Sidebar filters
    st.sidebar.header("Filter Preferences")

    cuisines = data['Cuisines'].dropna().unique().tolist()
    selected_cuisine = st.sidebar.selectbox("Cuisine", sorted(set(cuisines)))

    min_cost, max_cost = st.sidebar.slider("Average Cost for Two", 0, int(data['Average Cost for two'].max()), (100, 500))
    min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.5)

    # Filtered data
    filtered = data[
        (data['Cuisines'].str.contains(selected_cuisine, case=False)) &
        (data['Average Cost for two'].between(min_cost, max_cost)) &
        (data['Aggregate rating'] >= min_rating)
    ]

    st.subheader(f"🍴 {len(filtered)} Restaurants Found")

    if filtered.empty:
        st.warning("No restaurants match your criteria.")
    else:
        for _, row in filtered.iterrows():
            st.markdown("----")
            st.markdown(f"### {row['Restaurant Name']}")
            st.markdown(f"**Cuisine**: {row['Cuisines'].title()}")
            st.markdown(f"**Cost for Two**: ₹{int(row['Average Cost for two'])}")
            st.markdown(f"**Rating**: {row['Aggregate rating']} ⭐")
            query = urllib.parse.quote_plus(row['Restaurant Name'] + " restaurant")
            map_link = f"https://www.google.com/maps/search/?api=1&query={query}"
            st.markdown(f"[📍 View on Google Maps]({map_link})", unsafe_allow_html=True)
else:
    st.info("Please upload a CSV file to get started.")

# --- Evaluation Section ---
st.markdown("## 📝 Evaluation")

# A/B Testing Option
ab_version = st.radio("Which recommendation strategy are you using?", ("Strategy A: Basic Filtering", "Strategy B: Alternate Ranking"))

# Likert Scale Feedback
satisfaction = st.slider("How satisfied are you with the recommendations?", 1, 5, 3)

# Relevance Feedback
relevance = st.radio("Did the recommendations seem relevant to your preferences?", ("Yes", "No"))

# Usability Feedback
usability = st.text_area("Any feedback about the app's usability or suggestions for improvement?")

# Submit Button
if st.button("Submit Feedback"):
    # Collect feedback in a dictionary (could be saved to a file or database in a real app)
    feedback = {
        "version": ab_version,
        "satisfaction_score": satisfaction,
        "relevance": relevance,
        "usability_feedback": usability
    }

    st.success("✅ Thank you for your feedback!")
    st.json(feedback)  # For demonstration; you can save to a CSV or DB instead


