import time
import requests
import streamlit as st


API_URL = "https://oneatlas-trial.onrender.com"


st.set_page_config(
    page_title="OneAtlas AppSpec Generator",
    layout="wide"
)

st.title("OneAtlas Trial — AppSpec Generator")

st.caption(
    "Natural language → AppIntent → DataSchema → AppSpec"
)

prompt = st.text_area(
    "Describe the application you want to build",
    height=180,
    placeholder="Build a CRM for a real estate agency. Agents manage leads, properties, and deals..."
)

if st.button("Generate AppSpec", type="primary"):

    if not prompt.strip():
        st.warning("Please enter a prompt first.")
        st.stop()

    with st.spinner("Starting generation job..."):
        response = requests.post(
            f"{API_URL}/api/generate",
            json={"prompt": prompt}
        )

    if response.status_code != 200:
        st.error("Failed to start generation job.")
        st.write(response.text)
        st.stop()

    job_data = response.json()
    job_id = job_data.get("jobId")

    st.success(f"Job created: {job_id}")

    status_box = st.empty()

    while True:
        job_response = requests.get(
            f"{API_URL}/api/generate/{job_id}"
        )

        if job_response.status_code != 200:
            st.error("Failed to fetch job status.")
            st.write(job_response.text)
            break

        job = job_response.json()

        status_box.info(f"Current Status: {job.get('status')}")

        if job.get("status") in ["completed", "failed", "repair_attempted"]:
            break

        time.sleep(2)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Pipeline Events")
        st.json(job.get("events", []))

    with col2:
        st.subheader("Evaluation Logs")
        result = job.get("result", {})
        st.json(result.get("evaluation_logs", []))

    st.divider()

    if job.get("status") == "failed":
        st.subheader("Errors")
        st.json(job.get("errors"))
        st.stop()

    result = job.get("result", {})

    st.subheader("Generated Output")

    tabs = st.tabs([
        "AppIntent",
        "DataSchema",
        "AppSpec",
        "Repair Logs",
        "Raw Job"
    ])

    with tabs[0]:
        st.json(result.get("intent", {}))

    with tabs[1]:
        st.json(result.get("data_schema", {}))

    with tabs[2]:
        st.json(result.get("appspec", {}))

    with tabs[3]:
        st.json(result.get("repair_logs", []))

    with tabs[4]:
        st.json(job)


with st.sidebar:
    st.header("Backend")

    st.write(API_URL)

    if st.button("Check Integrations"):
        res = requests.get(f"{API_URL}/api/integrations")

        if res.status_code == 200:
            st.success("Integration registry loaded")
            st.json(res.json())
        else:
            st.error("Failed to load integrations")
            st.write(res.text)