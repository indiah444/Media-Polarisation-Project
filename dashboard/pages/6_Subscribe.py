# pylint: disable=C0103, E0401, R0801

"""Page for subscribing, altering subscription, and removing subscription."""

import streamlit as st

from db_functions import (get_subscriber_emails, updates_subscriber,
                          add_new_subscriber, remove_subscription)


def check_submission(first_name: str, surname: str, email: str, daily: bool, weekly: bool):
    """Check if email is already registered and then return appropriate response for
    their selections"""

    if daily is False and weekly is False:
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
    """Check if user is already """

    email_list = get_subscriber_emails()
    if email in email_list:
        remove_subscription(email)
        st.success("Subscription has been removed!")
    else:
        st.error("You were not subscribed!")


if __name__ == "__main__":

    st.set_page_config(
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Subscription Form")
    st.write("""Subscribe to our newsletters, either daily, weekly, or both!
             A daily newsletter sends you an email at 9am containing a
            table with the average sentiment per topic for each source
             for the previous day. A weekly newsletter sends you an email
             at 9am on a Monday with a sentiment distribution and bar chat.""")

    with st.form("subscription_form"):
        first_name_inp = st.text_input("Enter your first name")
        surname_inp = st.text_input("Enter your surname")
        email_inp = st.text_input("Enter your email")
        daily_inp = st.checkbox("Daily", value=False)
        weekly_inp = st.checkbox("Weekly", value=False)

        submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        check_submission(first_name_inp, surname_inp,
                         email_inp, daily_inp, weekly_inp)

    with st.form("unsubscribe_form"):
        st.write("If you want to unsubscribe")
        email2 = st.text_input("Enter your email to unsubscribe")

        unsubscribe_button = st.form_submit_button(label="Unsubscribe")

    if unsubscribe_button:
        check_unsubscribe(email2)
