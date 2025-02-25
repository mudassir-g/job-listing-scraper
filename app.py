import streamlit as st
from jobspy import scrape_jobs

from employee_search import search_employees


def get_jobs(search_term, portals, location, results_wanted=1, days_old=1):
    jobs = scrape_jobs(
        site_name=[p.lower().replace(' ', '_') for p in portals],
        search_term=search_term,
        google_search_term=search_term,
        location=location,
        results_wanted=results_wanted,
        hours_old=days_old * 24,
        country_indeed=location,
    )
    return jobs


def get_employees(company_name, designations, results_wanted=10):
    return search_employees(company_name, designations, results_wanted)


# Set the title of the app
st.title("vSaaS - Job Search Portal")
st.sidebar.title("Search Jobs")

# Create a text box for the search term
search_term = st.sidebar.text_input("Search term")

# Create checkboxes for the portals
portals = st.sidebar.multiselect(
    "Portals",
    options=["Indeed", "LinkedIn", "Zip Recruiter", "Glassdoor", "Google"],
    default=["Indeed", "LinkedIn"]  # You can set a default value if you want
)

# Create a select box for the location
location = st.sidebar.selectbox("Location", options=[
    "Argentina", "Australia", "Austria", "Bahrain", "Belgium", "Brazil",
    "Canada", "Chile", "China", "Colombia", "Costa Rica", "Czech Republic",
    "Czechia", "Denmark", "Ecuador", "Egypt", "Finland", "France",
    "Germany", "Greece", "Hong Kong", "Hungary", "India", "Indonesia",
    "Ireland", "Israel", "Italy", "Japan", "Kuwait", "Luxembourg",
    "Malaysia", "Malta", "Mexico", "Morocco", "Netherlands",
    "New Zealand", "Nigeria", "Norway", "Oman", "Pakistan", "Panama",
    "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania",
    "Saudi Arabia", "Singapore", "South Africa", "South Korea",
    "Spain", "Sweden", "Switzerland", "Taiwan", "Thailand",
    "Türkiye", "Turkey", "Ukraine", "United Arab Emirates",
    "UK", "United Kingdom", "USA", "US", "United States",
    "Uruguay", "Venezuela", "Vietnam", "USA/CA", "Worldwide"
], index=64)

job_results_wanted = st.sidebar.number_input(
    "Results wanted", key="jobs_results_wanted", value=10, min_value=1, max_value=50)
job_post_age = st.sidebar.number_input(
    "Age of job posting (in days)", value=1, min_value=1, max_value=365)

# Create a submit button
if st.sidebar.button("Submit") and search_term:
    # Display the inputs when the button is clicked
    st.write("### Searching for:")
    st.write(f"**Search term:** {search_term}")
    st.write(f"**Selected portals:** {', '.join(portals)}")
    st.write(f"**Location:** {location}")
    st.write(f"**Age of job posting:** {job_post_age} day(s)")

    with st.spinner("Searching..."):
        try:
            jobs = get_jobs(search_term, portals, location,
                            job_results_wanted, job_post_age)
            st.dataframe(jobs)
        except Exception as e:
            st.write("You are searching too fast. Try after sometime..")
            with st.expander("Error Details"):
                st.write(e)

st.sidebar.divider()

st.sidebar.title("Search Employees")
company_name = st.sidebar.text_input("Enter LinkedIn Company name")
designations = st.sidebar.text_area("Enter Designations (comma separated)")
emp_results_wanted = st.sidebar.number_input(
    "Results wanted", key='emp_results_wanted', value=10, min_value=1, max_value=50)
if designations:
    designations = designations.split(",")
if st.sidebar.button("Search Employees") and company_name:
    with st.spinner("Searching..."):
        st.write("### Searching for:")
        st.write(f"**Company:** {company_name}")
        st.write(f"**Designations:** {', '.join(designations)}")
        try:
            employees = get_employees(
                company_name, designations, emp_results_wanted)
            st.write("### Employees:")
            for employee in employees:
                st.write(employee)
        except Exception as e:
            st.write("You are searching too fast. Try after sometime..")
            with st.expander("Error Details"):
                st.write(e)
