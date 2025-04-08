import streamlit as st
import httpx
import time

# Configuration
API_URL = "http://localhost:8000/match-data"
KNOWN_RULES = ["rule123", "rule456", "performance_test", "integration_check"]

st.set_page_config(page_title="Middleware Tester", layout="centered")
st.title("Middleware Rule Matcher Tester")

st.markdown("#### 1. Choose a rule or type a query:")
query = st.selectbox("Choose a known rule or type your own:", KNOWN_RULES, index=0)
custom_input = st.text_input("Or enter a custom query here:", value=query)

use_custom = custom_input.strip() != query.strip()

# File uploader
st.markdown("#### 2. (Optional) Upload a file to extract query from:")
uploaded_file = st.file_uploader("Upload a rule-related text file", type=["txt"])

file_text = ""
if uploaded_file:
    file_text = uploaded_file.read().decode("utf-8")
    st.text_area("Extracted Text from File", file_text[:1000], height=150)

# Decide final query
final_query = file_text.strip() if file_text else (custom_input if use_custom else query)

if st.button("Send Request"):
    if not final_query:
        st.warning("Please enter a valid query.")
    else:
        st.markdown("#### Sending Request...")
        start_time = time.time()

        try:
            response = httpx.post(API_URL, json={"query": final_query})
            latency = time.time() - start_time
            response.raise_for_status()
            result = response.json()

            st.success(f"Response received in {latency:.2f} seconds")

            st.subheader("Matched Rule:")
            st.code(result.get("matched_rule", "N/A"))

            st.subheader("Endpoints Queried:")
            st.code(result.get("queried_endpoints", []))

            st.subheader("Response Data:")
            st.json(result.get("results", {}))

        except Exception as e:
            st.error(f"Error: {e}")
