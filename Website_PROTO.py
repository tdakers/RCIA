#%%
import pandas as pd
import numpy as np
import os
from supabase import create_client, Client
import streamlit as st
import streamlit.components.v1 as components
import datetime
#%%
url = "https://dptslvjsbhmxposqarwj.supabase.co"
key = st.secrets["api"]["key"]
supabase: Client = create_client(url, key)


marriage_options = ["Single", "Engaged", "Married", "Separated", "Divorced", "Widow(er)"]
baptism_options = ["No", "Yes", "I am not sure"]

previous_marriage_options = ["This is my first marriage", "I have been married before"]
fiance_previous_marriage_options = ["This is my fiancé(e)’s first marriage", "My fiancé(e) has been married before"]
spouse_previous_marriage_options = ["This is my spouse’s first marriage", "My spouse has been married before"]

# Centered title using HTML
st.set_page_config(page_title="My First Website", layout='wide')

# JavaScript to scroll to the top
scroll_to_top = """
<script>
    window.scrollTo(0, 0);
</script>
"""

# Inject the script at the top of your app layout
components.html(scroll_to_top, height=0)

st.session_state.setdefault("current_page", "Home")

st.session_state.setdefault("first_name_input", None)
st.session_state.setdefault("middle_name_input", None)
st.session_state.setdefault("last_name_input", None)
st.session_state.setdefault("maiden_name_input", None)
st.session_state.setdefault("dob_input", None)
st.session_state.setdefault("religion_input", None)
st.session_state.setdefault("mailing_address_input", None)
st.session_state.setdefault("app_number_input", None)
st.session_state.setdefault("city_input", None)
st.session_state.setdefault("state_input", None)
st.session_state.setdefault("country_input", None)
st.session_state.setdefault("phone_day_input", None)
st.session_state.setdefault("phone_eve_input", None)
st.session_state.setdefault("cell_phone_col", None)
st.session_state.setdefault("email_input", None)
st.session_state.setdefault("other_input", None)
st.session_state.setdefault("occupation_input", None)
st.session_state.setdefault("relationship_input_one", None)
st.session_state.setdefault("name_input_one", None)
st.session_state.setdefault("age_input_one", None)
st.session_state.setdefault("relationship_input_two", None)
st.session_state.setdefault("name_input_two", None)
st.session_state.setdefault("age_input_two", None)
st.session_state.setdefault("relationship_input_three", None)
st.session_state.setdefault("name_input_three", None)
st.session_state.setdefault("age_input_three", None)
st.session_state.setdefault("relationship_input_four", None)
st.session_state.setdefault("name_input_four", None)
st.session_state.setdefault("age_input_four", None)
st.session_state.setdefault("marriage_status", None)
st.session_state.setdefault("marriage_status_index",0)
st.session_state.setdefault("baptism_status", None)
st.session_state.setdefault("baptism_status_index",0)

st.session_state.setdefault("fiance_name_input", None)
st.session_state.setdefault("fiance_religion_input", None)
st.session_state.setdefault("fiance_my_previous_marriage_status")
st.session_state.setdefault("fiance_my_previous_marriage_index")
st.session_state.setdefault("fiance_fiances_previous_marriage_status")
st.session_state.setdefault("fiance_fiances_previous_marriage_index")

st.session_state.setdefault("spouse_name_input")
st.session_state.setdefault("spouse_religion_input")
st.session_state.setdefault("spouse_my_previous_marriage_status")
st.session_state.setdefault("spouse_my_previous_marriage_index", 0)
st.session_state.setdefault("spouse_spouses_previous_marriage_status")
st.session_state.setdefault("spouse_spouses_previous_marriage_index", 0)

st.session_state.setdefault("baptised_denomination_input")
st.session_state.setdefault("baptised_age_input")
st.session_state.setdefault("baptised_location_input")
st.session_state.setdefault("baptised_address_input")
st.session_state.setdefault("baptised_city_input")
st.session_state.setdefault("baptised_state_input")
st.session_state.setdefault("baptised_country_input")
st.session_state.setdefault("sacraments_penance_input")
st.session_state.setdefault("sacraments_eucharist_input")
st.session_state.setdefault("sacraments_confirmation_input")

# Custom font for the centered title
st.markdown(
    """
    <h1 style='text-align: center; font-family: "Helvetica", sans-serif; font-size: 48px;'>
        Inquirer Information Form
    </h1>
    <h2 style='text-align: center; font-family: "Helvetica", sans-serif; font-size: 24px; font-style: italic;'>
        Diocese of Charlotte
    </h2>
    """,
    unsafe_allow_html=True
)
if st.session_state.current_page == "Home":
    with st.container():
        with st.form("personal_info_form"):
            ##########################
            #--Personal Information--#
            ##########################
            st.markdown(
                """
                <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 32px;'>
                    I. Personal Information
                </h1>
                """,
                unsafe_allow_html=True
            )

            selected_date = st.date_input("Select today's date", value=None)
            
            first_name_col, middle_name_col, last_name_col = st.columns(3)
            with first_name_col:
                st.session_state.first_name_input = st.text_input("Fist Name:", st.session_state.first_name_input)
            with middle_name_col:
                st.session_state.middle_name_input = st.text_input("Middle Name:", st.session_state.middle_name_input)
            with last_name_col:
                st.session_state.last_name_input = st.text_input("Last Name:", st.session_state.last_name_input)

            maiden_name_col, dob_col, empty_col = st.columns(3)
            with maiden_name_col:
                st.session_state.maiden_name_input = st.text_input("Maiden Name (if applicable):", st.session_state.maiden_name_input)
            with dob_col:
                st.session_state.dob_input = st.date_input("Date of Birth", min_value=datetime.date(1800, 1, 1), max_value=datetime.datetime.today(), value = st.session_state.dob_input)
            with empty_col:
                st.empty()

            religion_col, first_empty_col, second_empty_col = st.columns(3)
            with religion_col:
                st.session_state.religion_input = st.text_input("Current Religion (if any)", st.session_state.religion_input)
            with first_empty_col:
                st.empty()
            with second_empty_col:
                st.empty()

            ##################
            #--Contact Info--#
            ##################
            st.markdown(
            """
            <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 32px;'>
                II. Contact Information
            </h1>
            """,
            unsafe_allow_html=True
            )

            mailing_address_col, apt_col = st.columns([2, 1])

            with mailing_address_col:
                st.session_state.mailing_address_input = st.text_input("Mailing Address", st.session_state.mailing_address_input)

            with apt_col:
                st.session_state.app_number_input = st.text_input("App Number", st.session_state.app_number_input)

            city_col, state_col, country_col = st.columns(3)
            with city_col:
                st.session_state.city_input = st.text_input("City", st.session_state.city_input)
            with state_col:
                st.session_state.state_input = st.text_input("State", st.session_state.state_input)
            with country_col:
                st.session_state.country_input = st.text_input("Country (If not USA)", st.session_state.country_input)

            phone_day_col, phone_eve_col, cell_phone_col = st.columns(3)
            with phone_day_col:
                st.session_state.phone_day_input = st.text_input("Phone (Daytime)", st.session_state.phone_day_input)
            with phone_eve_col:
                st.session_state.phone_eve_input = st.text_input("(Evening/Weekend)", st.session_state.phone_eve_input)
            with cell_phone_col:
                st.session_state.cell_phone_col = st.text_input("Cell Phone", st.session_state.cell_phone_col)

            email_col, other_col = st.columns(2)
            with email_col:
                st.session_state.email_input = st.text_input("E-mail (Home)", st.session_state.email_input)
            with other_col:
                st.session_state.other_input = st.text_input("(Other)", st.session_state.other_input)

            occupation_col, first_empty_col, second_empty_col = st.columns(3)
            with occupation_col:
                st.session_state.occupation_input = st.text_input("Occupation", st.session_state.occupation_input)
            with first_empty_col:
                st.empty()
            with second_empty_col:
                st.empty()
        
            ############################
            #--Family Information--#
            ############################
            st.markdown(
                """
                <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 32px; margin-bottom: 0;'>
                    III. Family Information
                </h1>
                <h2 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 18px; font-style: italic; margin-top: 0;'>
                    List the name(s) of any children or other dependents. (e.g. Daughter—Jane; Stepson—John.)
                </h2>
                """,
                unsafe_allow_html=True
            )

            relationship_col_one, family_name_col_one, family_age_col_one = st.columns([2, 2, 1])
            with relationship_col_one:
                st.session_state.relationship_input_one = st.text_input("Relationship", st.session_state.relationship_input_one)
            with family_name_col_one:
                st.session_state.name_input_one = st.text_input("Name", st.session_state.name_input_one)
            with family_age_col_one:
                st.session_state.age_input_one = st.number_input("Age", min_value=0, value=st.session_state.age_input_one)

            relationship_col, family_name_col, family_age_col = st.columns([2, 2, 1])
            with relationship_col:
                st.session_state.relationship_input_two = st.text_input("Relationship ", st.session_state.relationship_input_two)
            with family_name_col:
                st.session_state.name_input_two = st.text_input("Name ", st.session_state.name_input_two)
            with family_age_col:
                st.session_state.age_input_two = st.number_input("Age ", min_value=0, value = st.session_state.age_input_two)

            relationship_col, family_name_col, family_age_col = st.columns([2, 2, 1])
            with relationship_col:
                st.session_state.relationship_input_three = st.text_input("Relationship  ", st.session_state.relationship_input_three)
            with family_name_col:
                st.session_state.name_input_three = st.text_input("Name  ", st.session_state.name_input_three)
            with family_age_col:
                st.session_state.age_input_three = st.number_input("Age  ", min_value=0, value=st.session_state.age_input_three)

            relationship_col, family_name_col, family_age_col = st.columns([2, 2, 1])
            with relationship_col:
                st.session_state.relationship_input_four = st.text_input("Relationship   ", st.session_state.relationship_input_four)
            with family_name_col:
                st.session_state.name_input_four = st.text_input("Name   ", st.session_state.name_input_four)
            with family_age_col:
                st.session_state.age_input_four = st.number_input("Age   ", min_value=0, value=st.session_state.age_input_four)

            ############################
            #--Current Marital Status--#
            ############################
            st.markdown(
            """
            <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 32px;'>
                IV. Current Marital Status
            </h1>
            """,
            unsafe_allow_html=True
            )

            st.session_state.marriage_status = st.radio("Marital Status", marriage_options, horizontal=True, index = st.session_state.marriage_status_index)
            st.session_state.marriage_status_index = marriage_options.index(st.session_state.marriage_status)

            #######################
            #--Religious History--#
            #######################
            st.markdown(
            """
            <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 32px;'>
                V. Religious History
            </h1>
            """,
            unsafe_allow_html=True
            )

            st.session_state.baptism_status = st.radio("Have you ever been baptised?", baptism_options, horizontal=True, index = st.session_state.baptism_status_index)
            st.session_state.baptism_status_index = baptism_options.index(st.session_state.baptism_status)


            # Every form needs a submit button
            submitted = st.form_submit_button("Next")

        # Display results after submission
        if submitted:
            missing_fields = []

            if not selected_date:
                missing_fields.append("Select a date")
            if not st.session_state.first_name_input:
                missing_fields.append("First Name")
            if not st.session_state.last_name_input:
                missing_fields.append("Last Name")
            if not st.session_state.dob_input:
                missing_fields.append("Date of Birth")
            if not st.session_state.mailing_address_input:
                missing_fields.append("Mailing Address")
            if not st.session_state.city_input:
                missing_fields.append("City")
            if not st.session_state.state_input:
                missing_fields.append("State")
            if not st.session_state.email_input:
                missing_fields.append("E-Mail Address")
            if not st.session_state.phone_day_input and not st.session_state.phone_eve_input and not st.session_state.cell_phone_col:
                missing_fields.append("Phone Number")
            if not st.session_state.email_input:
                missing_fields.append("Email Address")
        
            if missing_fields:
                st.write("Missing fields:")
                for field in missing_fields:
                    st.write(f"• {field}")
            else:
                if st.session_state.marriage_status in ["Engaged", "Married"] or st.session_state.baptism_status == "Yes":
                    st.session_state.scroll_top = True
                    st.session_state.current_page = 'Additional Information'
                    st.rerun()

elif st.session_state.current_page == "Additional Information":
    with st.form("Engagement_Form"):
        if st.session_state.marriage_status == "Engaged":
            #####################
            #--Engagement Info--#
            #####################
            st.markdown(
            """
            <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 32px;'>
                Fiancé(e) Information
            </h1>
            """,
            unsafe_allow_html=True
            )
            fiance_name_col, fiance_empty_one, fiance_empty_two = st.columns(3)
            with fiance_name_col:
                st.session_state.fiance_name_input = st.text_input("Fiancé(e)’s Name")
            with fiance_empty_one:
                st.empty()
            with fiance_empty_two:
                st.empty()
            
            fiance_religion_col, fiance_religion_empty_one, fiance_religion_empty_two = st.columns(3)
            with fiance_religion_col:
                st.session_state.fiance_religion_input = st.text_input("Your Fiancé(e)’s Current Religious Affiliation (if any)")
            with fiance_religion_empty_one:
                st.empty()
            with fiance_religion_empty_two:
                st.empty()

            st.session_state.fiance_my_previous_marriage_status = st.radio("Have YOU ever been married before?", previous_marriage_options, horizontal=True)
            st.session_state.fiance_my_previous_marriage_index = previous_marriage_options.index(st.session_state.fiance_my_previous_marriage_status)

            st.session_state.fiance_fiances_previous_marriage_status = st.radio("Has your FIANCÉ(E) ever been married before?", fiance_previous_marriage_options, horizontal=True)
            st.session_state.fiance_fiances_previous_marriage_index = fiance_previous_marriage_options.index(st.session_state.fiance_fiances_previous_marriage_status)

        if st.session_state.marriage_status == "Married":
            ##################
            #--Married Info--#
            ##################
            st.markdown(
            """
            <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 32px;'>
                Married Information
            </h1>
            """,
            unsafe_allow_html=True
            )

            spouse_name_col, spouse_empty_one, spouse_empty_two = st.columns(3)
            with spouse_name_col:
                st.session_state.spouse_name_input = st.text_input("Your Spouse’s Name")
            with spouse_empty_one:
                st.empty()
            with spouse_empty_two:
                st.empty()

            spouse_religion_col, spouse_religion_empty_one, spouse_religion_empty_two = st.columns(3)
            with spouse_religion_col:
                st.session_state.spouse_religion_input = st.text_input("Your Spouse’s Current Religious Affiliation (if any)")
            with spouse_religion_empty_one:
                st.empty()
            with spouse_religion_empty_two:
                st.empty()

            st.session_state.spouse_my_previous_marriage_status = st.radio("Have YOU ever been married before?", previous_marriage_options, horizontal=True)
            st.session_state.spouse_my_previous_marriage_index = previous_marriage_options.index(st.session_state.spouse_my_previous_marriage_status)

            st.session_state.spouse_spouses_previous_marriage_status = st.radio("Has your SPOUSE ever been married before?", spouse_previous_marriage_options, horizontal=True)
            st.session_state.spouse_spouses_previous_marriage_index = spouse_previous_marriage_options.index(st.session_state.spouse_spouses_previous_marriage_status)

        ##################
        #--Baptism Info--#
        ##################
        if st.session_state.baptism_status == "Yes":
            st.markdown(
            """
            <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 32px;'>
                Baptism Information
            </h1>
            """,
            unsafe_allow_html=True
            )
                    
            baptised_denomination_col, baptised_age_col, baptised_empty_one = st.columns(3)
            with baptised_denomination_col:
                st.session_state.baptised_denomination_input = st.text_input("In what denomination were you baptized?")
            with baptised_age_col:
                st.session_state.baptised_age_input = st.number_input("Approximate age when you were baptized:", min_value=0)
            with baptised_empty_one:
                st.empty()

            baptised_location_col, baptised_address_col = st.columns([1, 2])
            with baptised_location_col:
                st.session_state.baptised_location_input = st.text_input("Place of Baptism (Name of church)")
            with baptised_address_col:
                st.session_state.baptised_address_input = st.text_input("Mailing Address, if known")

            baptised_city_col, baptised_state_col, baptised_country_col = st.columns(3)
            with baptised_city_col:
                st.session_state.baptised_city_input = st.text_input("City")
            with baptised_state_col:
                st.session_state.baptised_state_input = st.text_input("State")
            with baptised_country_col:
                st.session_state.baptised_country_input = st.text_input("Country (if not USA)")

            st.write("If you were baptized as a Catholic, check those sacraments you have already received:")
            sacraments_penance_col, sacraments_eucharist_col, sacraments_confirmation_col = st.columns(3)
            with sacraments_penance_col:
                st.session_state.sacraments_penance_input = st.checkbox("Penance (Confession)")
            with sacraments_eucharist_col:
                st.session_state.sacraments_eucharist_input = st.checkbox("Eucharist (First Communion)")
            with sacraments_confirmation_col:
                st.session_state.sacraments_confirmation_input = st.checkbox("Confirmation")

        button_cols = st.columns(10)
        with button_cols[0]:
            review_form = st.form_submit_button("Next")
        with button_cols[1]:
            previous_form = st.form_submit_button("Home")

        if previous_form:
            st.session_state.current_page = 'Home'
            st.session_state.scroll_top = True
            st.rerun()

        if review_form:
            missing_fields = []

            if st.session_state.marriage_status == "Married":
                if not st.session_state.spouse_name_input:                    
                    missing_fields.append("Enter Spouse's Name")

            if st.session_state.marriage_status == "Engaged":
                if not st.session_state.fiance_name_input:                    
                    missing_fields.append("Enter Spouse's Name")

            if st.session_state.baptism_status == "Yes":
                if not st.session_state.baptised_denomination_input:
                    missing_fields.append("Please Enter Baptism Denomination")
                if not st.session_state.baptised_age_input:
                    missing_fields.append("Please enter approximate age of baptism")
                if not st.session_state.baptised_location_input:
                    missing_fields.append("Please enter church name of baptism")
                if not st.session_state.baptised_city_input:
                    missing_fields.append("Please enter church state of baptism")

            if missing_fields:
                st.write("Missing fields:")
                for field in missing_fields:
                    st.write(f"• {field}")
            else:                    
                st.session_state.current_page = 'Review'
                st.session_state.scroll_top = True
                st.rerun()

elif st.session_state.current_page == "Review":
    st.markdown(
        """
        <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 32px;'>
            I. Personal Information
        </h1>
        """,
        unsafe_allow_html=True
    )
    first_name_col, middle_name_col, last_name_col = st.columns(3)
    with first_name_col:
        st.text_input("Fist Name:", st.session_state.first_name_input, disabled=True)
    with middle_name_col:
        st.text_input("Middle Name:", st.session_state.middle_name_input, disabled=True)
    with last_name_col:
        st.text_input("Last Name:", st.session_state.last_name_input, disabled=True)

    maiden_name_col, dob_col, empty_col = st.columns(3)
    with maiden_name_col:
        st.text_input("Maiden Name (if applicable):", st.session_state.maiden_name_input, disabled=True)
    with dob_col:
        st.date_input("Date of Birth", st.session_state.dob_input, disabled=True)
    with empty_col:
        st.empty()

    religion_col, first_empty_col, second_empty_col = st.columns(3)
    with religion_col:
        st.text_input("Current Religion (if any)", st.session_state.religion_input, disabled=True)
    with first_empty_col:
        st.empty()
    with second_empty_col:
        st.empty()

    ##################
    #--Contact Info--#
    ##################
    st.markdown(
    """
    <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 32px;'>
        II. Contact Information
    </h1>
    """,
    unsafe_allow_html=True
    )

    mailing_address_col, apt_col = st.columns([2, 1])

    with mailing_address_col:
        st.text_input("Mailing Address", st.session_state.mailing_address_input, disabled=True)

    with apt_col:
        st.text_input("App Number", st.session_state.app_number_input, disabled=True)

    city_col, state_col, country_col = st.columns(3)
    with city_col:
        st.text_input("City", st.session_state.city_input, disabled=True)
    with state_col:
        st.text_input("State", st.session_state.state_input, disabled=True)
    with country_col:
        st.text_input("Country (If not USA)", st.session_state.country_input, disabled=True)

    phone_day_col, phone_eve_col, cell_phone_col = st.columns(3)
    with phone_day_col:
        st.text_input("Phone (Daytime)", st.session_state.phone_day_input, disabled=True)
    with phone_eve_col:
        st.text_input("(Evening/Weekend)", st.session_state.phone_eve_input, disabled=True)
    with cell_phone_col:
        st.text_input("Cell Phone", st.session_state.cell_phone_col, disabled=True)

    email_col, other_col = st.columns(2)
    with email_col:
        st.text_input("E-mail (Home)", st.session_state.email_input, disabled=True)
    with other_col:
        st.text_input("(Other)", st.session_state.other_input, disabled=True)

    occupation_col, first_empty_col, second_empty_col = st.columns(3)
    with occupation_col:
        st.text_input("Occupation", st.session_state.occupation_input, disabled=True)
    with first_empty_col:
        st.empty()
    with second_empty_col:
        st.empty()

    ############################
    #--Family Information--#
    ############################
    st.markdown(
        """
        <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 32px; margin-bottom: 0;'>
            III. Family Information
        </h1>
        <h2 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 18px; font-style: italic; margin-top: 0;'>
            List the name(s) of any children or other dependents. (e.g. Daughter—Jane; Stepson—John.)
        </h2>
        """,
        unsafe_allow_html=True
    )

    relationship_col_one, family_name_col_one, family_age_col_one = st.columns([2, 2, 1])
    with relationship_col_one:
        st.text_input("Relationship", st.session_state.relationship_input_one, disabled=True)
    with family_name_col_one:
        st.text_input("Name", st.session_state.name_input_one, disabled=True)
    with family_age_col_one:
        st.number_input("Age", st.session_state.age_input_one, disabled=True)

    relationship_col, family_name_col, family_age_col = st.columns([2, 2, 1])
    with relationship_col:
        st.text_input("Relationship ", st.session_state.relationship_input_two, disabled=True)
    with family_name_col:
        st.text_input("Name ", st.session_state.name_input_two, disabled=True)
    with family_age_col:
        st.number_input("Age ", st.session_state.age_input_two, disabled=True)

    relationship_col, family_name_col, family_age_col = st.columns([2, 2, 1])
    with relationship_col:
        st.text_input("Relationship  ", st.session_state.relationship_input_three, disabled=True)
    with family_name_col:
        st.text_input("Name  ", st.session_state.name_input_three, disabled=True)
    with family_age_col:
        st.number_input("Age  ", st.session_state.age_input_three, disabled=True)

    relationship_col, family_name_col, family_age_col = st.columns([2, 2, 1])
    with relationship_col:
        st.text_input("Relationship   ", st.session_state.relationship_input_four, disabled=True)
    with family_name_col:
        st.text_input("Name   ", st.session_state.name_input_four, disabled=True)
    with family_age_col:
        st.number_input("Age   ", st.session_state.age_input_four, disabled=True)

    st.radio("Marital Status", marriage_options, horizontal=True, index=st.session_state.marriage_status_index, disabled=True)
    st.radio("Have you ever been baptised?", baptism_options, horizontal=True, index=st.session_state.baptism_status_index, disabled=True)

    #####################
    #--Engagement Info--#
    #####################
    if st.session_state.marriage_status == "Engaged":
            st.markdown(
            """
            <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 32px;'>
                Fiancé(e) Information
            </h1>
            """,
            unsafe_allow_html=True
            )
            fiance_name_col, fiance_empty_one, fiance_empty_two = st.columns(3)
            with fiance_name_col:
                st.text_input("Fiancé(e)’s Name", value = st.session_state.fiance_name_input)
            with fiance_empty_one:
                st.empty()
            with fiance_empty_two:
                st.empty()
            
            fiance_religion_col, fiance_religion_empty_one, fiance_religion_empty_two = st.columns(3)
            with fiance_religion_col:
                st.text_input("Your Fiancé(e)’s Current Religious Affiliation (if any)", value = st.session_state.fiance_religion_input)
            with fiance_religion_empty_one:
                st.empty()
            with fiance_religion_empty_two:
                st.empty()

            st.radio("Have YOU ever been married before?", previous_marriage_options, horizontal=True, index = st.session_state.fiance_my_previous_marriage_index, disabled=True)

            st.radio("Has your FIANCÉ(E) ever been married before?", fiance_previous_marriage_options, horizontal=True, index = st.session_state.fiance_fiances_previous_marriage_index, disabled=True)

    ##################
    #--Married Info--#
    ##################
    if st.session_state.marriage_status == "Married":
        st.markdown(
        """
        <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 32px;'>
            Married Information
        </h1>
        """,
        unsafe_allow_html=True
        )

        spouse_name_col, spouse_empty_one, spouse_empty_two = st.columns(3)
        with spouse_name_col:
            st.text_input("Your Spouse’s Name", value = st.session_state.spouse_name_input, disabled=True)
        with spouse_empty_one:
            st.empty()
        with spouse_empty_two:
            st.empty()

        spouse_religion_col, spouse_religion_empty_one, spouse_religion_empty_two = st.columns(3)
        with spouse_religion_col:
            st.text_input("Your Spouse’s Current Religious Affiliation (if any)", value=st.session_state.spouse_religion_input, disabled=True)
        with spouse_religion_empty_one:
            st.empty()
        with spouse_religion_empty_two:
            st.empty()

        st.radio("Have YOU ever been married before?", previous_marriage_options, horizontal=True, index = st.session_state.spouse_my_previous_marriage_index, disabled=True)

        st.radio("Has your SPOUSE ever been married before?", spouse_previous_marriage_options, horizontal=True, index = st.session_state.spouse_spouses_previous_marriage_index, disabled=True)
    ##################
    #--Baptism Info--#
    ##################
    if st.session_state.baptism_status == "Yes":
        st.markdown(
        """
        <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 32px;'>
            Baptism Information
        </h1>
        """,
        unsafe_allow_html=True
        )
                
        baptised_denomination_col, baptised_age_col, baptised_empty_one = st.columns(3)
        with baptised_denomination_col:
            st.text_input("In what denomination were you baptized?", value = st.session_state.baptised_denomination_input, disabled=True)
        with baptised_age_col:
            st.number_input("Approximate age when you were baptized:", value = st.session_state.baptised_age_input, disabled=True)
        with baptised_empty_one:
            st.empty()

        baptised_location_col, baptised_address_col = st.columns([1, 2])
        with baptised_location_col:
            st.text_input("Place of Baptism (Name of church)", value=st.session_state.baptised_location_input, disabled=True)
        with baptised_address_col:
            st.text_input("Mailing Address, if known", value=st.session_state.baptised_address_input, disabled=True)

        baptised_city_col, baptised_state_col, baptised_country_col = st.columns(3)
        with baptised_city_col:
            st.text_input("City ", value=st.session_state.baptised_city_input, disabled=True)
        with baptised_state_col:
            st.text_input("State ", value=st.session_state.baptised_state_input, disabled=True)
        with baptised_country_col:
            st.text_input("Country (if not USA) ", value=st.session_state.baptised_country_input, disabled=True)

        st.write("If you were baptized as a Catholic, check those sacraments you have already received:")
        sacraments_penance_col, sacraments_eucharist_col, sacraments_confirmation_col = st.columns(3)
        with sacraments_penance_col:
            st.checkbox("Penance (Confession)", value=st.session_state.sacraments_penance_input, disabled=True)
        with sacraments_eucharist_col:
            st.checkbox("Eucharist (First Communion)", value=st.session_state.sacraments_eucharist_input, disabled=True)
        with sacraments_confirmation_col:
            st.checkbox("Confirmation", value=st.session_state.sacraments_confirmation_input, disabled=True)

    if st.session_state.marriage_status in ["Engaged", "Married"] or st.session_state.baptism_status == "Yes":
        button_cols = st.columns(10)
        with button_cols[0]:
            home_from_review_button = st.button("Home")
        with button_cols[1]:
            additional_information_from_review_button = st.button("Previous")
        with button_cols[2]:
            final_submit_button = st.button("Submit")
    else:
        button_cols = st.columns(10)
        with button_cols[0]:
            home_from_review_button = st.button("Home")
        with button_cols[1]:
            final_submit_button = st.button("Submit")

    if home_from_review_button:
        st.session_state.current_page = 'Home'
        st.session_state.scroll_top = True
        st.rerun()

    if additional_information_from_review_button:
        st.session_state.current_page = 'Additional Information'
        st.session_state.scroll_top = True
        st.rerun()

if final_submit_button: 
    response = supabase.table("Candidates").insert({
        "First_Name" : st.session_state.first_name_input,
        "Middle_Name" : st.session_state.middle_name_input,
        "Last_Name" : st.session_state.last_name_input,
        "Maiden_Name" : st.session_state.maiden_name_input,
        "DOB" : str(st.session_state.dob_input),
        "Religion" : st.session_state.religion_input,
        "Mailing_Address" : st.session_state.mailing_address_input,
        "App_Number" : st.session_state.app_number_input,
        "Mailing_City" : st.session_state.city_input,
        "Mailing_State" : st.session_state.state_input,
        "Mailing_Country" : st.session_state.country_input,
        "Phone_Day" : st.session_state.phone_day_input,
        "Phone_Eve" : st.session_state.phone_eve_input,
        "Phone_Other" : st.session_state.cell_phone_col,
        "Email" : st.session_state.email_input,
        "Notes" : st.session_state.other_input,
        "Occupation" : st.session_state.occupation_input,
        "Relationship_Type_One" : st.session_state.relationship_input_one,
        "Relationship_Name_One" : st.session_state.name_input_one,
        "Relationship_Age_One" : st.session_state.age_input_one,
        "Relationship_Type_Two" : st.session_state.relationship_input_two,
        "Relationship_Name_Two": st.session_state.name_input_two,
        "Relationship_Age_Two" : st.session_state.age_input_two,
        "Relationship_Type_Three" : st.session_state.relationship_input_three,
        "Relationship_Name_Three" : st.session_state.name_input_three,
        "Relationship_Age_Three" : st.session_state.age_input_three,
        "Relationship_Type_Four" : st.session_state.relationship_input_four,
        "Relationship_Name_Four" : st.session_state.name_input_four,
        "Relationship_Age_Four" : st.session_state.age_input_four,
        "Marriage_Status" : st.session_state.marriage_status,
        "Baptism_Status" : st.session_state.baptism_status,

        "Fiance_Name" : st.session_state.fiance_name_input,
        "Fiance_Religion" : st.session_state.fiance_religion_input,
        "Fiance_My_Prev_Marriage_Status" : st.session_state.fiance_my_previous_marriage_status,
        "Fiance_fiances_Prev_Marriage_Status" : st.session_state.fiance_fiances_previous_marriage_status,

        "Spouse_Name" : st.session_state.spouse_name_input,
        "Spouse_Religion" : st.session_state.spouse_religion_input,
        "Spouse_My_Prev_Marriage_Status" : st.session_state.spouse_my_previous_marriage_status,
        "Spouse_Spouse_Prev_Marriage_Status" : st.session_state.spouse_spouses_previous_marriage_status,

        "Baptised_Denomination" : st.session_state.baptised_denomination_input,
        "Baptised_Age" : st.session_state.baptised_age_input,
        "Baptised_Church_Name" : st.session_state.baptised_location_input,
        "Baptised_Mailing_Address" : st.session_state.baptised_address_input,
        "Baptised_Mailing_City" : st.session_state.baptised_city_input,
        "Baptised_Mailing_State" : st.session_state.baptised_state_input,
        "Baptised_Mailing_Country" : st.session_state.baptised_country_input,
        "Sacraments_Penance" : st.session_state.sacraments_penance_input,
        "Sacraments_Eucharist" : st.session_state.sacraments_eucharist_input,
        "Sacraments_Confirmation" : st.session_state.sacraments_confirmation_input
    }).execute()