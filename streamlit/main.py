import streamlit as st
import requests
import json
from streamlit_lottie import st_lottie
import os
from dotenv import load_dotenv, find_dotenv

_: bool = load_dotenv(find_dotenv())

BASE_URL = os.environ.get("BASE_URL")

if not BASE_URL:
    raise ValueError("Contact Developer ~ Base URL not found")

# Page Configuration
st.set_page_config(
    page_title="Cal AI",
    page_icon="🤖"
)

# Import Downloaded JSON
def import_json(path):
    with open(path, "r", encoding="utf8", errors="ignore") as file:
        url = json.load(file)
        return url


data_oracle = import_json(r"./robo_brain.json")
st_lottie(data_oracle, height=400, key="oracle")

st.title("Cal AI")

# Initialize session state
if 'access_token' not in st.session_state:
    st.session_state['access_token'] = None

if 'edit_todo_id' not in st.session_state:
    st.session_state.edit_todo_id = None
    st.session_state.edit_todo_title = ''
    st.session_state.edit_todo_description = ''

def signout():
    st.session_state['access_token'] = None
    st.rerun()



def user_signup():
    with st.form("User Signup"):
        fullname = st.text_input("Fullname", key="signup_fullname")
        username = st.text_input("Username", key="signup_username")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input(
            "Password", type="password", key="signup_password")
        submit_button = st.form_submit_button("Signup")

        if submit_button:
            # Check if all fields are filled
            if not all([fullname, username, email, password]):
                st.warning("Please fill in all fields.")
                st.toast("Please fill in all fields.")
            else:
                response = requests.post(
                    f"{BASE_URL}/api/auth/users/signup/",
                    json={"username": username, "email": email,
                          "password": password, "full_name": fullname}
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
            # Check if username or password is empty
            if not username.strip() or not password.strip():
                st.error("Username and password cannot be empty")
            else:
                response = requests.post(f"{BASE_URL}/api/auth/login", data={"username": username, "password": password})
                if response.status_code == 200:
                    st.session_state['access_token'] = response.json()["access_token"]
                    st.toast(f"Welcome {response.json()['user']['full_name']}")
                    st.rerun()
                else:
                    st.error("Login failed")
                    print('response.json()', response.json())
                    print('response.status_code', response.status_code)
                    st.toast(response.json()["detail"])



def create_todo():
    with st.form("Create Todo"):
        title = st.text_input("Enter Todo Title")
        description = st.text_area("Enter Todo Description")
        submit_button = st.form_submit_button("Add Todo")
        if submit_button and 'access_token' in st.session_state:
            response = requests.post(f"{BASE_URL}/api/todos/", json={"title": title, "description": description}, headers={"Authorization": f"Bearer {st.session_state['access_token']}"})
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

    # Display the signout button when the user is logged in
    if st.button('Sign Out'):
        signout()

    # Show all todos
    response = requests.get(f"{BASE_URL}/api/todos/", headers={"Authorization": f"Bearer {st.session_state['access_token']}"})
    if response.status_code == 200:
        todos = response.json()

        if todos:
            st.subheader("Your Work List :D")
            for todo in todos:
                with st.expander(f"**Task Name: {todo['title']}** (Created: {todo['created_at'][:10]})"):
                    st.markdown(f"**Description:** {todo['description']}")
                    st.markdown(f"**Completed:** {'Yes' if todo['completed'] else 'No'}")
                    st.markdown(f"**Last Updated:** {todo['updated_at'][:10]}")

                    # Interactive buttons for each todo
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col1:
                        if st.button("Update Status", key=f"complete_{todo['id']}"):
                            # Logic to toggle the completion status of the todo
                            new_status = not todo['completed']
                            patch_response = requests.patch(f"{BASE_URL}/api/todos/{todo['id']}", json={"title": todo['title'], "completed": new_status}, headers={"Authorization": f"Bearer {st.session_state['access_token']}"})
                            if patch_response.status_code == 200:
                                st.toast("Updated todo status")
                            elif patch_response.status_code == 401:
                                st.error("Unauthorized. Please log in again.")
                                st.session_state['access_token'] = None
                            else:
                                st.error("Failed to update todo")
                            st.rerun()

                    with col2:
                        if st.button("Delete", key=f"delete_{todo['id']}") and 'access_token' in st.session_state:
                            response = requests.delete(f"{BASE_URL}/api/todos/{todo['id']}", headers={"Authorization": f"Bearer {st.session_state['access_token']}"})
                            if response.status_code == 200:
                                st.toast("Todo deleted successfully")
                            elif response.status_code == 401:
                                st.error("Unauthorized. Please log in again.")
                                st.session_state['access_token'] = None  # Reset access token
                            else:
                                st.error("Failed to delete todo")
                            st.rerun()
                    with col3:
                        if st.button("Edit", key=f"edit_{todo['id']}"):
                            st.session_state.edit_todo_id = todo['id']
                            st.session_state.edit_todo_title = todo['title']
                            st.session_state.edit_todo_description = todo['description']

                    # Edit form
            if st.session_state.edit_todo_id:
                with st.form("Edit Todo"):
                    new_title = st.text_input("Title", value=st.session_state.edit_todo_title)
                    new_description = st.text_area("Description", value=st.session_state.edit_todo_description)
                    
                    # Layout for Update and Cancel buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        submit_button = st.form_submit_button("Update Todo")
                    with col2:
                        cancel_button = st.form_submit_button("Cancel")

                    if submit_button:
                        update_response = requests.put(f"{BASE_URL}/api/todos/{st.session_state.edit_todo_id}", json={"title": new_title, "description": new_description}, headers={"Authorization": f"Bearer {st.session_state['access_token']}"})
                        if update_response.status_code == 200:
                            st.toast("Todo updated successfully")
                            st.session_state.edit_todo_id = None  # Reset edit mode
                        else:
                            st.error("Failed to update todo")
                        st.rerun()

                    if cancel_button:
                        st.session_state.edit_todo_id = None  # Reset edit mode
                        st.rerun()


        else:
            st.write("No todos found. Start by adding a new todo.")
    else:
        st.error("Failed to fetch todos. Please try again later.")
