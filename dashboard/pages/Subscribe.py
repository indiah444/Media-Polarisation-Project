"""Page for subscribing, altering subscription, and removing subscription."""

import streamlit as st

from db_functions import get_subscriber_emails, updates_subscriber, add_new_subscriber, remove_subscription


def check_submission(first_name: str, surname: str, email: str, daily: bool, weekly: bool):
    if daily == False and weekly == False:
        st.error("You need to be subscribed to either weekly or daily.")
    else:
        email_list = get_subscriber_emails()
        if email in email_list:
            updates_subscriber(first_name, surname, email, daily, weekly)
            st.success("Subscriber preferences updated!")
        else:
            add_new_subscriber(first_name, surname, email, daily, weekly)
            st.success(
                "Subscription added! (You may get a verification email, please click the link!)")


def check_unsubscribe(email: str):
    email_list = get_subscriber_emails()
    if email in email_list:
        remove_subscription(email)
        st.success("Subscription has been removed!")
    else:
        st.error("You were not subscribed!")


st.title("Subscription Form")
st.write("Subscribe to our newsletters, either daily, weekly, or both!")

with st.form("subscription_form"):
    first_name = st.text_input("Enter your first name")
    surname = st.text_input("Enter your surname")
    email = st.text_input("Enter your email")
    daily = st.checkbox("Daily", value=False)
    weekly = st.checkbox("Weekly", value=False)

    submit_button = st.form_submit_button(label="Submit")

# If the form is submitted, call function_2 with the provided inputs
if submit_button:
    # Call the function with the form inputs
    check_submission(first_name, surname, email, daily, weekly)


with st.form("unsubscribe_form"):
    st.write("If you want to unsubscribe!")
    email2 = st.text_input("Enter your email to unsubscribe")

    unsubscribe_button = st.form_submit_button(label="Unsubscribe")

if unsubscribe_button:
    check_unsubscribe(email2)
