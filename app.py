import streamlit as st

# Set up Streamlit page configuration
st.set_page_config(page_title="E-Waste Detection", page_icon="🗑️", layout="wide")

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "home"

# Navigation function
def navigate_to(page):
    st.session_state.page = page

# Home Page Layout
if st.session_state.page == "home":
    st.title("🔋 E-Waste Detection")
    st.write("Select an option below to start detecting e-waste.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📷 Real-Time Detection", use_container_width=True):
            navigate_to("real_time")

    with col2:
        if st.button("🖼️ Upload an Image", use_container_width=True):
            navigate_to("upload_image")

# Navigate to other pages
elif st.session_state.page == "real_time":
    from pages.real_time import real_time_detection
    real_time_detection()

elif st.session_state.page == "upload_image":
    from pages.upload_image import upload_image_detection
    upload_image_detection()
