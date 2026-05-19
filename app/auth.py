import streamlit as st

# =========================================
# LOGIN SYSTEM
# =========================================

def login():

    st.title("🔐 VisionGuard AI Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    login_button = st.button("Login")

    if login_button:

        if (
            username == "houssam"
            and
            password == "houssam200"
        ):

            st.session_state["authenticated"] = True

            st.success("Login successful")

            st.rerun()

        else:

            st.error("Invalid credentials")