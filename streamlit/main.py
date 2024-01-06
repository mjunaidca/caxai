import streamlit as st
import requests
import json
from streamlit_lottie import st_lottie

BASE_URL = "http://127.0.0.1:8000"

# Page Configuration 
st.set_page_config(
    page_title= "Cal AI",
    page_icon= "🤖"
)

# Import Downloaded JSON
def import_json(path):
    with open(path, "r", encoding="utf8", errors="ignore") as file:
        url = json.load(file)
        return url
    
data_oracle = import_json(r"robo_brain.json")
st_lottie(data_oracle, height = 400, key = "oracle")

# Initialize session state
if 'access_token' not in st.session_state:
    st.session_state['access_token'] = None

st.title("Cal AI")

def user_signup():
    with st.form("User Signup"):
        fullname = st.text_input("Fullname", key="signup_fullname")
        username = st.text_input("Username", key="signup_username")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        submit_button = st.form_submit_button("Signup")

        if submit_button:
            # Check if all fields are filled
            if not all([fullname, username, email, password]):
                st.warning("Please fill in all fields.")
                st.toast("Please fill in all fields.")
            else:
                response = requests.post(
                    f"{BASE_URL}/api/auth/users/signup/",
                    json={"username": username, "email": email, "password": password, "full_name": fullname}
                )
                if response.status_code == 200:
                    st.success("Signup successful. Please login.")
                    st.toast("Signup successful. Please login.")
                else:
                    st.error("Signup failed")
                    st.toast(response.json()["detail"])

def user_login():
    with st.form("User Login"):
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        submit_button = st.form_submit_button("Login")
        if submit_button:
            response = requests.post(
                f"{BASE_URL}/api/auth/login",
                data={"username": username, "password": password}
            )
            if response.status_code == 200:
                st.session_state['access_token'] = response.json()["access_token"]
                st.success("Logged in successfully")
                st.toast(f"Welcome {response.json()['user']['full_name']}")
                st.rerun()
            else:
                st.error("Login failed")
                # Display the 'detail' field from the response
                print('response.json()', response.json())
                print('response.status_code', response.status_code)
                st.toast(response.json()["detail"])

def create_todo():
    with st.form("Create Todo"):
        title = st.text_input("Enter Todo Title")
        description = st.text_area("Enter Todo Description")
        submit_button = st.form_submit_button("Add Todo")
        if submit_button and 'access_token' in st.session_state:
            response = requests.post(
                f"{BASE_URL}/api/todos/",
                json={"title": title, "description": description},
                headers={"Authorization": f"Bearer {st.session_state['access_token']}"}
            )
            if response.status_code == 200:
                st.toast("Todo added successfully")
                # Clear the output after success
                st.empty()
            elif response.status_code == 401:
                st.error("Unauthorized. Please log in again.")
                st.session_state['access_token'] = None  # Reset access token
            else:
                st.error("Failed to add todo")
            st.rerun()

def delete_todo():
    with st.form("Delete Todo"):
        todo_id = st.text_input("Enter Todo ID to delete")
        submit_button = st.form_submit_button("Delete Todo")
        if submit_button and 'access_token' in st.session_state:
            response = requests.delete(f"{BASE_URL}/api/todos/{todo_id}",
                headers={"Authorization": f"Bearer {st.session_state['access_token']}"})
            if response.status_code == 200:
                st.success("Todo deleted successfully")
            elif response.status_code == 401:
                st.error("Unauthorized. Please log in again.")
                st.session_state['access_token'] = None  # Reset access token
            else:
                st.error("Failed to delete todo")
            st.rerun()

if not st.session_state['access_token']:
    tab1, tab2 = st.tabs(["Login", "Signup"])
    with tab1:
        st.subheader("Login")
        user_login()
    with tab2:
        st.subheader("Signup")
        user_signup()

if st.session_state['access_token']:
    create_todo()
    delete_todo()

    # Show all todos
    response = requests.get(f"{BASE_URL}/api/todos/",
                            headers={"Authorization": f"Bearer {st.session_state['access_token']}"})
    if response.status_code == 200:
        todos = response.json()
        st.write("Todos:", todos)
    else:
        st.error("Failed to fetch todos")
