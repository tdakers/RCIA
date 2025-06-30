from supabase import create_client, Client
import streamlit as st
import streamlit.components.v1 as components
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

url = "https://dptslvjsbhmxposqarwj.supabase.co"
key = st.secrets["api"]["key"]
from_email = st.secrets["api"]["from_email"]
from_password = st.secrets["api"]["email_app_password"]
supabase: Client = create_client(url, key)

def send_html_email(to_email, subject, html_content):
    msg = MIMEMultipart("alternative")
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    # Attach HTML version
    html_part = MIMEText(html_content, "html")
    msg.attach(html_part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(from_email, from_password)
            server.sendmail(from_email, to_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False



def former_spouse_form(prefix: str, title: str, annulment_options: list):
    st.write(title)

    # Name
    first_col, middle_col, last_col = st.columns(3)
    with first_col:
        st.session_state[f"{prefix}_first_name_input"] = st.text_input("First", key=f"{prefix}_first")
    with middle_col:
        st.session_state[f"{prefix}_middle_name_input"] = st.text_input("Middle", key=f"{prefix}_middle")
    with last_col:
        st.session_state[f"{prefix}_last_name_input"] = st.text_input("Last", key=f"{prefix}_last")

    # Date of Marriage
    date_col_1, _, _ = st.columns(3)
    with date_col_1:
        default_date = st.session_state.get(f"{prefix}_date_of_marriage_input", datetime.date(2000, 1, 1))
        st.session_state[f"{prefix}_date_of_marriage_input"] = st.date_input(
            "Date of Marriage",
            min_value=datetime.date(1800, 1, 1),
            max_value=datetime.datetime.today(),
            value=default_date,
            key=f"{prefix}_marriage_date"
        )

    # Annulment radio
    st.session_state[f"{prefix}_annulment_petition_status"] = st.radio(
        'Was there ever a petitioned for an annulment from a Church Tribunal?',
        annulment_options,
        horizontal=True,
        key=f"{prefix}_annulment_radio"
    )
    status_index = annulment_options.index(st.session_state[f"{prefix}_annulment_petition_status"])
    st.session_state[f"{prefix}_annulment_petition_index"] = status_index

    if status_index == 1:
        # Annulment Case Details
        case_col, date_col, _ = st.columns(3)
        with case_col:
            st.session_state[f"{prefix}_annulment_case_nbr_input"] = st.text_input("Annulment Case Number", key=f"{prefix}_case_num")
        with date_col:
            default_annulment_date = st.session_state.get(f"{prefix}_annulment_case_date_input", datetime.date(2000, 1, 1))
            st.session_state[f"{prefix}_annulment_case_date_input"] = st.date_input(
                "Date Granted",
                min_value=datetime.date(1800, 1, 1),
                max_value=datetime.datetime.today(),
                value=default_annulment_date,
                key=f"{prefix}_case_date"
            )

        # Diocese Info
        city_col, state_col, country_col = st.columns(3)
        with city_col:
            st.session_state[f"{prefix}_annulment_diocese_city_input"] = st.text_input("Diocese/City", key=f"{prefix}_city")
        with state_col:
            st.session_state[f"{prefix}_annulment_diocese_state_input"] = st.text_input("State", key=f"{prefix}_state")
        with country_col:
            st.session_state[f"{prefix}_annulment_diocese_country_input"] = st.text_input("Country (if not USA)", key=f"{prefix}_country")

        # Nullity Info
        nullity_col, date_nullity_col = st.columns(2)
        with nullity_col:
            st.session_state[f"{prefix}_annulment_nullity_verification_input"] = st.text_input("Nullity Verification (if applicable)", key=f"{prefix}_nullity_verif")
        with date_nullity_col:
            default_nullity_date = st.session_state.get(f"{prefix}_annulment_nullity_date_input", datetime.date(2000, 1, 1))
            st.session_state[f"{prefix}_annulment_nullity_date_input"] = st.date_input(
                "Date of Verification",
                min_value=datetime.date(1800, 1, 1),
                max_value=datetime.datetime.today(),
                value=default_nullity_date,
                key=f"{prefix}_nullity_date"
            )

def family_member_input(family_current_count):
    relationship_key = f"relationship_input_{family_current_count}"
    name_key = f"name_input_{family_current_count}"
    age_key = f"age_input_{family_current_count}"

    indent  = " " * family_current_count

    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        st.session_state[relationship_key] = st.text_input(f"Relationship{indent}")
    with col2:
        st.session_state[name_key] = st.text_input(f"Name{indent}")
    with col3:
        st.session_state[age_key] = st.number_input(f"Age{indent}", min_value=0)

marriage_options = ["Single", "Engaged", "Married", "Separated", "Divorced", "Widow(er)"]
baptism_options = ["No", "Yes", "I am not sure"]

previous_marriage_options = ["This is my first marriage", "I have been married before"]
fiance_previous_marriage_options = ["This is my fiancé(e)’s first marriage", "My fiancé(e) has been married before"]
spouse_previous_marriage_options = ["This is my spouse’s first marriage", "My spouse has been married before"]

previous_marriage_annulment_options = ["Not, to my knowledge", "Yes", "An annulment is currently in process"]
previous_marriage_annulment_status = ["No", "Yes", "I do not know"]

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
st.session_state.setdefault("current_relationship_count", 0)
st.session_state.setdefault("relationship_input_1", None)
st.session_state.setdefault("name_input_1", None)
st.session_state.setdefault("age_input_1", None)
st.session_state.setdefault("relationship_input_2", None)
st.session_state.setdefault("name_input_2", None)
st.session_state.setdefault("age_input_2", None)
st.session_state.setdefault("relationship_input_3", None)
st.session_state.setdefault("name_input_3", None)
st.session_state.setdefault("age_input_3", None)
st.session_state.setdefault("relationship_input_4", None)
st.session_state.setdefault("name_input_4", None)
st.session_state.setdefault("age_input4", None)
st.session_state.setdefault("marriage_status", None)
st.session_state.setdefault("marriage_status_index",0)
st.session_state.setdefault("baptism_status", None)
st.session_state.setdefault("baptism_status_index",0)

st.session_state.setdefault("fiance_name_input", None)
st.session_state.setdefault("fiance_religion_input", None)
st.session_state.setdefault("fiance_my_previous_marriage_status")
st.session_state.setdefault("fiance_my_previous_marriage_index", 0)
st.session_state.setdefault("fiance_fiances_previous_marriage_status")
st.session_state.setdefault("fiance_fiances_previous_marriage_index", 0)

st.session_state.setdefault("spouse_name_input")
st.session_state.setdefault("spouse_baptised_catholic_input")
st.session_state.setdefault("spouse_witnessed_by_ordination_input")
st.session_state.setdefault("spouse_dispensation_for_ordination_input")
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

st.session_state.setdefault("my_first_former_spouse_first_name_input")
st.session_state.setdefault("my_first_former_spouse_middle_name_input")
st.session_state.setdefault("my_first_former_spouse_last_name_input")
st.session_state.setdefault("my_first_former_spouse_date_of_marriage_input", None)
st.session_state.setdefault("my_first_former_spouse_annulment_input")
st.session_state.setdefault("my_first_former_spouse_annulment_petition_status")
st.session_state.setdefault("my_first_former_spouse_annulment_petition_index", 0)
st.session_state.setdefault("my_first_former_spouse_annulment_case_nbr_input")
st.session_state.setdefault("my_first_former_spouse_annulment_case_date_input", None)
st.session_state.setdefault("my_first_former_spouse_annulment_diocese_city_input")
st.session_state.setdefault("my_first_former_spouse_annulment_diocese_state_input")
st.session_state.setdefault("my_first_former_spouse_annulment_diocese_country_input")
st.session_state.setdefault("my_first_former_spouse_annulment_nullity_verification_input")
st.session_state.setdefault("my_first_former_spouse_annulment_nullity_date_input", None)
st.session_state.setdefault("my_first_former_spouse_annulment_additional_marriage_boolean", False)
st.session_state.setdefault("my_second_former_spouse_first_name_input")
st.session_state.setdefault("my_second_former_spouse_middle_name_input")
st.session_state.setdefault("my_second_former_spouse_last_name_input")
st.session_state.setdefault("my_second_former_spouse_date_of_marriage_input", None)
st.session_state.setdefault("my_second_former_spouse_annulment_input")
st.session_state.setdefault("my_second_former_spouse_annulment_petition_status")
st.session_state.setdefault("my_second_former_spouse_annulment_petition_index", 0)
st.session_state.setdefault("my_second_former_spouse_annulment_case_nbr_input")
st.session_state.setdefault("my_second_former_spouse_annulment_case_date_input", None)
st.session_state.setdefault("my_second_former_spouse_annulment_diocese_city_input")
st.session_state.setdefault("my_second_former_spouse_annulment_diocese_state_input")
st.session_state.setdefault("my_second_former_spouse_annulment_diocese_country_input")
st.session_state.setdefault("my_second_former_spouse_annulment_nullity_verification_input")
st.session_state.setdefault("my_second_former_spouse_annulment_nullity_date_input", None)
st.session_state.setdefault("my_second_former_spouse_annulment_additional_marriage_boolean")
st.session_state.setdefault("my_third_former_spouse_first_name_input")
st.session_state.setdefault("my_third_former_spouse_middle_name_input")
st.session_state.setdefault("my_third_former_spouse_last_name_input")
st.session_state.setdefault("my_third_former_spouse_date_of_marriage_input", None)
st.session_state.setdefault("my_third_former_spouse_annulment_input")
st.session_state.setdefault("my_third_former_spouse_annulment_petition_status")
st.session_state.setdefault("my_third_former_spouse_annulment_petition_index", 0)
st.session_state.setdefault("my_third_former_spouse_annulment_case_nbr_input")
st.session_state.setdefault("my_third_former_spouse_annulment_case_date_input", None)
st.session_state.setdefault("my_third_former_spouse_annulment_diocese_city_input")
st.session_state.setdefault("my_third_former_spouse_annulment_diocese_state_input")
st.session_state.setdefault("my_third_former_spouse_annulment_diocese_country_input")
st.session_state.setdefault("my_third_former_spouse_annulment_nullity_verification_input")
st.session_state.setdefault("my_third_former_spouse_annulment_nullity_date_input", None)
st.session_state.setdefault("my_third_former_spouse_annulment_additional_marriage_boolean", False)

st.session_state.setdefault("so_first_former_spouse_first_name_input")
st.session_state.setdefault("so_first_former_spouse_middle_name_input")
st.session_state.setdefault("so_first_former_spouse_last_name_input")
st.session_state.setdefault("so_first_former_spouse_date_of_marriage_input", None)
st.session_state.setdefault("so_first_former_spouse_annulment_input")
st.session_state.setdefault("so_first_former_spouse_annulment_petition_status")
st.session_state.setdefault("so_first_former_spouse_annulment_petition_index", 0)
st.session_state.setdefault("so_first_former_spouse_annulment_case_nbr_input")
st.session_state.setdefault("so_first_former_spouse_annulment_case_date_input", None)
st.session_state.setdefault("so_first_former_spouse_annulment_diocese_city_input")
st.session_state.setdefault("so_first_former_spouse_annulment_diocese_state_input")
st.session_state.setdefault("so_first_former_spouse_annulment_diocese_country_input")
st.session_state.setdefault("so_first_former_spouse_annulment_nullity_verification_input")
st.session_state.setdefault("so_first_former_spouse_annulment_nullity_date_input", None)
st.session_state.setdefault("so_first_former_spouse_annulment_additional_marriage_boolean", False)
st.session_state.setdefault("so_second_former_spouse_first_name_input")
st.session_state.setdefault("so_second_former_spouse_middle_name_input")
st.session_state.setdefault("so_second_former_spouse_last_name_input")
st.session_state.setdefault("so_second_former_spouse_date_of_marriage_input", None)
st.session_state.setdefault("so_second_former_spouse_annulment_input")
st.session_state.setdefault("so_second_former_spouse_annulment_petition_status")
st.session_state.setdefault("so_second_former_spouse_annulment_petition_index", 0)
st.session_state.setdefault("so_second_former_spouse_annulment_case_nbr_input")
st.session_state.setdefault("so_second_former_spouse_annulment_case_date_input", None)
st.session_state.setdefault("so_second_former_spouse_annulment_diocese_city_input")
st.session_state.setdefault("so_second_former_spouse_annulment_diocese_state_input")
st.session_state.setdefault("so_second_former_spouse_annulment_diocese_country_input")
st.session_state.setdefault("so_second_former_spouse_annulment_nullity_verification_input")
st.session_state.setdefault("so_second_former_spouse_annulment_nullity_date_input", None)
st.session_state.setdefault("so_second_former_spouse_annulment_additional_marriage_boolean")
st.session_state.setdefault("so_third_former_spouse_first_name_input")
st.session_state.setdefault("so_third_former_spouse_middle_name_input")
st.session_state.setdefault("so_third_former_spouse_last_name_input")
st.session_state.setdefault("so_third_former_spouse_date_of_marriage_input", None)
st.session_state.setdefault("so_third_former_spouse_annulment_input")
st.session_state.setdefault("so_third_former_spouse_annulment_petition_status")
st.session_state.setdefault("so_third_former_spouse_annulment_petition_index", 0)
st.session_state.setdefault("so_third_former_spouse_annulment_case_nbr_input")
st.session_state.setdefault("so_third_former_spouse_annulment_case_date_input", None)
st.session_state.setdefault("so_third_former_spouse_annulment_diocese_city_input")
st.session_state.setdefault("so_third_former_spouse_annulment_diocese_state_input")
st.session_state.setdefault("so_third_former_spouse_annulment_diocese_country_input")
st.session_state.setdefault("so_third_former_spouse_annulment_nullity_verification_input")
st.session_state.setdefault("so_third_former_spouse_annulment_nullity_date_input", None)
st.session_state.setdefault("so_third_former_spouse_annulment_additional_marriage_boolean", False)

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

    date_col = st.columns(5)
    with date_col[0]:
        selected_date = st.write(f'Date: {datetime.datetime.now().strftime("%B %d, %Y")}')
    
    first_name_col, middle_name_col, last_name_col = st.columns(3)
    with first_name_col:
        st.session_state.first_name_input = st.text_input("Fist Name:", st.session_state.first_name_input)
    with middle_name_col:
        st.session_state.middle_name_input = st.text_input("Middle Name", st.session_state.middle_name_input)
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

    if(st.session_state.current_relationship_count > 0 and st.session_state.current_relationship_count < 5):
        for x in range(1, st.session_state.current_relationship_count + 1):
            family_member_input(x)
    
    if st.session_state.current_relationship_count < 4:
        if st.button("Add Family Member") and st.session_state.current_relationship_count < 4:
            st.session_state.current_relationship_count += 1
            st.rerun()
    
    if st.session_state.current_relationship_count > 0:
        if st.button("Remove Family Member") and st.session_state.current_relationship_count > 0:
            st.session_state.current_relationship_count -= 1
            st.rerun()

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

    st.markdown(
            """
            <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 22px; margin-bottom: -100px;'>
                Marital Status
            </h1>
            """,
            unsafe_allow_html=True
            )
    st.session_state.marriage_status = st.radio("", marriage_options, horizontal=True)
    st.session_state.marriage_status_index = marriage_options.index(st.session_state.marriage_status)

    if st.session_state.marriage_status == "Married":
        ##################
        #--Married Info--#
        ##################
        st.markdown("""
            <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 22px; margin-bottom: -100px;'>
                Have YOU ever been married before?
            </h1>
        """, unsafe_allow_html=True)

        st.session_state.spouse_my_previous_marriage_status = st.radio("", previous_marriage_options, horizontal=True)
        st.session_state.spouse_my_previous_marriage_index = previous_marriage_options.index(st.session_state.spouse_my_previous_marriage_status)

        if st.session_state.marriage_status in ["Engaged", "Married"] and (st.session_state.spouse_my_previous_marriage_status == "I have been married before" or st.session_state.spouse_my_previous_marriage_status == "I have been married before"):
            st.markdown(
                """
                <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 22px;'>
                    My Previous Marriage Information
                </h1>
                """,
                unsafe_allow_html=True
            )
            
            # First spouse
            former_spouse_form("my_first_former_spouse", "Former Spouse’s Current Name:", previous_marriage_annulment_options)

            if not st.session_state.my_second_former_spouse_annulment_additional_marriage_boolean:
                if st.button("Add Another Former Spouse"):
                    st.session_state.my_second_former_spouse_annulment_additional_marriage_boolean = True
                    st.rerun()

            if st.session_state.my_second_former_spouse_annulment_additional_marriage_boolean:
                # Second spouse
                former_spouse_form("my_second_former_spouse", "Second Former Spouse’s Current Name:", previous_marriage_annulment_options)

                if not  st.session_state.my_third_former_spouse_annulment_additional_marriage_boolean:
                    if st.button("Remove previous spouse"):
                        st.session_state.my_second_former_spouse_annulment_additional_marriage_boolean = False
                        st.rerun()
                    if st.button("Add Another Former Spouse "):
                        st.session_state.my_third_former_spouse_annulment_additional_marriage_boolean = True
                        st.rerun()

            if st.session_state.my_third_former_spouse_annulment_additional_marriage_boolean:
                # Third spouse
                former_spouse_form("my_third_former_spouse", "Third Former Spouse’s Current Name:", previous_marriage_annulment_options)
                if st.button("Remove previous spouse "):
                    st.session_state.my_third_former_spouse_annulment_additional_marriage_boolean = False
                    st.rerun()

        st.markdown(
        """
        <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 22px;'>
            Spouse’s Information
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

        st.session_state.spouse_baptised_catholic_input = st.checkbox("My spouse baptized as a Catholic?")

        if st.session_state.spouse_baptised_catholic_input:
            st.session_state.spouse_witnessed_by_ordination_input = st.radio("Our Marriage was witnessed by a Catholic priest or deacon?", ["Yes", "No"], horizontal=True)

        if st.session_state.spouse_baptised_catholic_input and st.session_state.spouse_witnessed_by_ordination_input == "No":
            st.session_state.spouse_dispensation_for_ordination_input = st.radio("Did you receive a dispensation for ordination?", ["Yes", "No"], horizontal=True)
            

    elif st.session_state.marriage_status == "Engaged":
        #####################
        #--Engagement Info--#
        #####################
        # Now render your heading and radio
        st.markdown("""
            <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 22px; margin-bottom: -100px;'>
                Have YOU ever been married before?
            </h1>
        """, unsafe_allow_html=True)
        st.session_state.fiance_my_previous_marriage_status = st.radio("", previous_marriage_options, horizontal=True)
        st.session_state.fiance_my_previous_marriage_index = previous_marriage_options.index(st.session_state.fiance_my_previous_marriage_status)

        if st.session_state.marriage_status in ["Engaged", "Married"] and (st.session_state.fiance_my_previous_marriage_status == "I have been married before" or st.session_state.fiance_my_previous_marriage_status == "I have been married before"):
            st.markdown(
                """
                <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 22px;'>
                    My Previous Marriage Information
                </h1>
                """,
                unsafe_allow_html=True
            )
            
            # First spouse
            former_spouse_form("my_first_former_spouse", "Former Spouse’s Current Name:", previous_marriage_annulment_options)

            if not st.session_state.my_second_former_spouse_annulment_additional_marriage_boolean:
                if st.button("Add Another Former Spouse"):
                    st.session_state.my_second_former_spouse_annulment_additional_marriage_boolean = True
                    st.rerun()

            if st.session_state.my_second_former_spouse_annulment_additional_marriage_boolean:
                # Second spouse
                former_spouse_form("my_second_former_spouse", "Second Former Spouse’s Current Name:", previous_marriage_annulment_options)

                if not  st.session_state.my_third_former_spouse_annulment_additional_marriage_boolean:
                    if st.button("Remove previous spouse"):
                        st.session_state.my_second_former_spouse_annulment_additional_marriage_boolean = False
                        st.rerun()
                    if st.button("Add Another Former Spouse "):
                        st.session_state.my_third_former_spouse_annulment_additional_marriage_boolean = True
                        st.rerun()

            if st.session_state.my_third_former_spouse_annulment_additional_marriage_boolean:
                # Third spouse
                former_spouse_form("my_third_former_spouse", "Third Former Spouse’s Current Name:", previous_marriage_annulment_options)
                if st.button("Remove previous spouse "):
                    st.session_state.my_third_former_spouse_annulment_additional_marriage_boolean = False
                    st.rerun()
        
        st.markdown(
        """
        <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 22px;'>
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

    if st.session_state.marriage_status == "Married":
        st.markdown(
                """
                <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 22px; margin-bottom: -100px;'>
                    Has your SPOUSE ever been married before?
                </h1>
                """,
                unsafe_allow_html=True
            )
        st.session_state.spouse_spouses_previous_marriage_status = st.radio("", spouse_previous_marriage_options, horizontal=True)
        st.session_state.spouse_spouses_previous_marriage_index = spouse_previous_marriage_options.index(st.session_state.spouse_spouses_previous_marriage_status)

    elif st.session_state.marriage_status == "Engaged":
        st.markdown(
                """
                <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 22px; margin-bottom: -100px;'>
                    Fiancé(e) Previous Marriage Information
                </h1>
                """,
                unsafe_allow_html=True
            )
        st.session_state.fiance_fiances_previous_marriage_status = st.radio("", fiance_previous_marriage_options, horizontal=True)
        st.session_state.fiance_fiances_previous_marriage_index = fiance_previous_marriage_options.index(st.session_state.fiance_fiances_previous_marriage_status)  

    if st.session_state.marriage_status in ["Engaged", "Married"] and (st.session_state.spouse_spouses_previous_marriage_status == "My spouse has been married before" or st.session_state.fiance_fiances_previous_marriage_status == "My fiancé(e) has been married before"):
        if st.session_state.marriage_status == "Engaged": 
            st.markdown(
                """
                <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 22px;'>
                    Fiancé(e) Previous Marriage Information
                </h1>
                """,
                unsafe_allow_html=True
            )
        elif st.session_state.marriage_status == "Married":
            st.markdown(
                """
                <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 32px;'>
                    Spouse Previous Marriage Information
                </h1>
                """,
                unsafe_allow_html=True
            )

        # First spouse
        former_spouse_form("so_first_former_spouse", "Former Spouse’s Current Name:", previous_marriage_annulment_options)

        if not st.session_state.so_second_former_spouse_annulment_additional_marriage_boolean:
            if st.button("Add Another Former Spouse  "):
                st.session_state.so_second_former_spouse_annulment_additional_marriage_boolean = True
                st.rerun()

        if st.session_state.so_second_former_spouse_annulment_additional_marriage_boolean:
            # Second spouse
            former_spouse_form("so_second_former_spouse", "Second Former Spouse’s Current Name:", previous_marriage_annulment_options)

            if not  st.session_state.so_third_former_spouse_annulment_additional_marriage_boolean:
                if st.button("Remove previous spouse  "):
                    st.session_state.so_second_former_spouse_annulment_additional_marriage_boolean = False
                    st.rerun()
                if st.button("Add Another Former Spouse   "):
                    st.session_state.so_third_former_spouse_annulment_additional_marriage_boolean = True
                    st.rerun()

        if st.session_state.so_third_former_spouse_annulment_additional_marriage_boolean:
            # Third spouse
            former_spouse_form("so_third_former_spouse", "Third Former Spouse’s Current Name:", previous_marriage_annulment_options)
            if st.button("Remove previous spouse    "):
                st.session_state.so_third_former_spouse_annulment_additional_marriage_boolean = False
                st.rerun()
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

    st.markdown(
                """
                <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 22px; margin-bottom: -100px;'>
                    Have you ever been baptised?
                </h1>
                """,
                unsafe_allow_html=True
            )
    st.session_state.baptism_status = st.radio("", baptism_options, horizontal=True)
    st.session_state.baptism_status_index = baptism_options.index(st.session_state.baptism_status)

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
                    st.session_state.baptised_age_input = st.number_input("Approximate age when you were baptized:", min_value=0, value=0)
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

    if st.button("Submit"):

        missing_fields = []
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
        if st.session_state.marriage_status == "Engaged":
            if not st.session_state.fiance_name_input:                    
                missing_fields.append("Enter Fiance's Name")
        if st.session_state.marriage_status == "Married":
            if not st.session_state.spouse_name_input:                    
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
            try:
                response = supabase.table("Candidates").insert({
                "first_name" : st.session_state.first_name_input,
                "middle_name" : st.session_state.middle_name_input,
                "last_name" : st.session_state.last_name_input,
                "maiden_name" : st.session_state.maiden_name_input,
                "dob" : str(st.session_state.dob_input),
                "religion" : st.session_state.religion_input,
                "mailing_address" : st.session_state.mailing_address_input,
                "app_number" : st.session_state.app_number_input,
                "city" : st.session_state.city_input,
                "state" : st.session_state.state_input,
                "country" : st.session_state.country_input,
                "phone_day" : st.session_state.phone_day_input,
                "phone_evening" : st.session_state.phone_eve_input,
                "cell_phone" : st.session_state.cell_phone_col,
                "email" : st.session_state.email_input,
                "other" : st.session_state.other_input,
                "occupation" : st.session_state.occupation_input,
                "relationship_type_one" : st.session_state.relationship_input_1,
                "relationship_name_one" : st.session_state.name_input_1,
                "relationship_age_one" : st.session_state.age_input_1,
                "relationship_type_two" : st.session_state.relationship_input_2,
                "relationship_name_two" : st.session_state.name_input_2,
                "relationship_age_two" : st.session_state.age_input_2,
                "relationship_type_three" : st.session_state.relationship_input_3,
                "relationship_name_three" : st.session_state.name_input_3,
                "relationship_age_three" : st.session_state.age_input_3,
                "relationship_type_four" : st.session_state.relationship_input_4,
                "relationship_name_four" : st.session_state.name_input_4,
                "relationship_age_four" : st.session_state.age_input4,
                "marriage_status" : st.session_state.marriage_status,
                "baptism_status" : st.session_state.baptism_status,
                "fiance_name" : st.session_state.fiance_name_input,
                "fiance_religion" : st.session_state.fiance_religion_input,
                "fiance_my_previous_mariage" : st.session_state.fiance_my_previous_marriage_status,
                "fiance_fiance_previous_mariage" : st.session_state.fiance_fiances_previous_marriage_status,
                "spouse_name" : st.session_state.spouse_name_input,
                "spouse_baptised_catholic" : st.session_state.spouse_baptised_catholic_input,
                "spouse_witnessed_by_ordination" : st.session_state.spouse_witnessed_by_ordination_input,
                "spouse_dispensation_for_ordination" : st.session_state.spouse_dispensation_for_ordination_input,
                "spouse_religion" : st.session_state.spouse_religion_input,
                "spouse_my_previous_marriage_status" : st.session_state.spouse_my_previous_marriage_status,
                "spouse_spouses_previous_marriage_status" : st.session_state.spouse_spouses_previous_marriage_status,
                "baptised_denomination" : st.session_state.baptised_denomination_input,
                "baptised_age" : st.session_state.baptised_age_input,
                "baptised_location" : st.session_state.baptised_location_input,
                "baptised_address" : st.session_state.baptised_address_input,
                "baptised_city" : st.session_state.baptised_city_input,
                "baptised_state" : st.session_state.baptised_state_input,
                "baptised_country" : st.session_state.baptised_country_input,
                "sacraments_penance" : st.session_state.sacraments_penance_input,
                "sacraments_eucharist" : st.session_state.sacraments_eucharist_input,
                "sacraments_confirmation" : st.session_state.sacraments_confirmation_input,
                "my_first_former_spouse_first_name" : st.session_state.my_first_former_spouse_first_name_input,
                "my_first_former_spouse_middle_name" : st.session_state.my_first_former_spouse_middle_name_input,
                "my_first_former_spouse_last_name" : st.session_state.my_first_former_spouse_last_name_input,
                "my_first_former_spouse_date_of_marriage" : str(st.session_state.my_first_former_spouse_date_of_marriage_input),
                "my_first_former_spouse_annulment" : st.session_state.my_first_former_spouse_annulment_input,
                "my_first_former_spouse_annulment_petition_" : st.session_state.my_first_former_spouse_annulment_petition_status,
                "my_first_former_spouse_annulment_case_nbr" : st.session_state.my_first_former_spouse_annulment_case_nbr_input,
                "my_first_former_spouse_annulment_case_date" : str(st.session_state.my_first_former_spouse_annulment_case_date_input),
                "my_first_former_spouse_annulment_diocese_city" : st.session_state.my_first_former_spouse_annulment_diocese_city_input,
                "my_first_former_spouse_annulment_diocese_state" : st.session_state.my_first_former_spouse_annulment_diocese_state_input,
                "my_first_former_spouse_annulment_diocese_country" : st.session_state.my_first_former_spouse_annulment_diocese_country_input,
                "my_first_former_spouse_annulment_nullity_verification" : st.session_state.my_first_former_spouse_annulment_nullity_verification_input,
                "my_first_former_spouse_annulment_nullity_date" : str(st.session_state.my_first_former_spouse_annulment_nullity_date_input),
                "my_second_former_spouse_first_name" : st.session_state.my_second_former_spouse_first_name_input,
                "my_second_former_spouse_middle_name" : st.session_state.my_second_former_spouse_middle_name_input,
                "my_second_former_spouse_last_name" : st.session_state.my_second_former_spouse_last_name_input,
                "my_second_former_spouse_date_of_marriage" : str(st.session_state.my_second_former_spouse_date_of_marriage_input),
                "my_second_former_spouse_annulment" : st.session_state.my_second_former_spouse_annulment_input,
                "my_second_former_spouse_annulment_petition_" : st.session_state.my_second_former_spouse_annulment_petition_status,
                "my_second_former_spouse_annulment_case_nbr" : st.session_state.my_second_former_spouse_annulment_case_nbr_input,
                "my_second_former_spouse_annulment_case_date" : str(st.session_state.my_second_former_spouse_annulment_case_date_input),
                "my_second_former_spouse_annulment_diocese_city" : st.session_state.my_second_former_spouse_annulment_diocese_city_input,
                "my_second_former_spouse_annulment_diocese_state" : st.session_state.my_second_former_spouse_annulment_diocese_state_input,
                "my_second_former_spouse_annulment_diocese_country" : st.session_state.my_second_former_spouse_annulment_diocese_country_input,
                "my_second_former_spouse_annulment_nullity_verification" : st.session_state.my_second_former_spouse_annulment_nullity_verification_input,
                "my_second_former_spouse_annulment_nullity_date" : str(st.session_state.my_second_former_spouse_annulment_nullity_date_input),
                "my_third_former_spouse_first_name" : st.session_state.my_third_former_spouse_first_name_input,
                "my_third_former_spouse_middle_name" : st.session_state.my_third_former_spouse_middle_name_input,
                "my_third_former_spouse_last_name" : st.session_state.my_third_former_spouse_last_name_input,
                "my_third_former_spouse_date_of_marriage" : str(st.session_state.my_third_former_spouse_date_of_marriage_input),
                "my_third_former_spouse_annulment" : st.session_state.my_third_former_spouse_annulment_input,
                "my_third_former_spouse_annulment_petition_" : st.session_state.my_third_former_spouse_annulment_petition_status,
                "my_third_former_spouse_annulment_case_nbr" : st.session_state.my_third_former_spouse_annulment_case_nbr_input,
                "my_third_former_spouse_annulment_case_date" : str(st.session_state.my_third_former_spouse_annulment_case_date_input),
                "my_third_former_spouse_annulment_diocese_city" : st.session_state.my_third_former_spouse_annulment_diocese_city_input,
                "my_third_former_spouse_annulment_diocese_state" : st.session_state.my_third_former_spouse_annulment_diocese_state_input,
                "my_third_former_spouse_annulment_diocese_country" : st.session_state.my_third_former_spouse_annulment_diocese_country_input,
                "my_third_former_spouse_annulment_nullity_verification" : st.session_state.my_third_former_spouse_annulment_nullity_verification_input,
                "my_third_former_spouse_annulment_nullity_date" : str(st.session_state.my_third_former_spouse_annulment_nullity_date_input),
                "so_first_former_spouse_first_name" : st.session_state.so_first_former_spouse_first_name_input,
                "so_first_former_spouse_middle_name" : st.session_state.so_first_former_spouse_middle_name_input,
                "so_first_former_spouse_last_name" : st.session_state.so_first_former_spouse_last_name_input,
                "so_first_former_spouse_date_of_marriage" : str(st.session_state.so_first_former_spouse_date_of_marriage_input),
                "so_first_former_spouse_annulment" : st.session_state.so_first_former_spouse_annulment_input,
                "so_first_former_spouse_annulment_petition_" : st.session_state.so_first_former_spouse_annulment_petition_status,
                "so_first_former_spouse_annulment_case_nbr" : st.session_state.so_first_former_spouse_annulment_case_nbr_input,
                "so_first_former_spouse_annulment_case_date" : str(st.session_state.so_first_former_spouse_annulment_case_date_input),
                "so_first_former_spouse_annulment_diocese_city" : st.session_state.so_first_former_spouse_annulment_diocese_city_input,
                "so_first_former_spouse_annulment_diocese_state" : st.session_state.so_first_former_spouse_annulment_diocese_state_input,
                "so_first_former_spouse_annulment_diocese_country" : st.session_state.so_first_former_spouse_annulment_diocese_country_input,
                "so_first_former_spouse_annulment_nullity_verification" : st.session_state.so_first_former_spouse_annulment_nullity_verification_input,
                "so_first_former_spouse_annulment_nullity_date" : str(st.session_state.so_first_former_spouse_annulment_nullity_date_input),
                "so_second_former_spouse_first_name" : st.session_state.so_second_former_spouse_first_name_input,
                "so_second_former_spouse_middle_name" : st.session_state.so_second_former_spouse_middle_name_input,
                "so_second_former_spouse_last_name" : st.session_state.so_second_former_spouse_last_name_input,
                "so_second_former_spouse_date_of_marriage" : str(st.session_state.so_second_former_spouse_date_of_marriage_input),
                "so_second_former_spouse_annulment" : st.session_state.so_second_former_spouse_annulment_input,
                "so_second_former_spouse_annulment_petition_" : st.session_state.so_second_former_spouse_annulment_petition_status,
                "so_second_former_spouse_annulment_case_nbr" : st.session_state.so_second_former_spouse_annulment_case_nbr_input,
                "so_second_former_spouse_annulment_case_date" : str(st.session_state.so_second_former_spouse_annulment_case_date_input),
                "so_second_former_spouse_annulment_diocese_city" : st.session_state.so_second_former_spouse_annulment_diocese_city_input,
                "so_second_former_spouse_annulment_diocese_state" : st.session_state.so_second_former_spouse_annulment_diocese_state_input,
                "so_second_former_spouse_annulment_diocese_country" : st.session_state.so_second_former_spouse_annulment_diocese_country_input,
                "so_second_former_spouse_annulment_nullity_verification" : st.session_state.so_second_former_spouse_annulment_nullity_verification_input,
                "so_second_former_spouse_annulment_nullity_date" : str(st.session_state.so_second_former_spouse_annulment_nullity_date_input),
                "so_third_former_spouse_first_name" : st.session_state.so_third_former_spouse_first_name_input,
                "so_third_former_spouse_middle_name" : st.session_state.so_third_former_spouse_middle_name_input,
                "so_third_former_spouse_last_name" : st.session_state.so_third_former_spouse_last_name_input,
                "so_third_former_spouse_date_of_marriage" : str(st.session_state.so_third_former_spouse_date_of_marriage_input),
                "so_third_former_spouse_annulment" : st.session_state.so_third_former_spouse_annulment_input,
                "so_third_former_spouse_annulment_petition_" : st.session_state.so_third_former_spouse_annulment_petition_status,
                "so_third_former_spouse_annulment_case_nbr" : st.session_state.so_third_former_spouse_annulment_case_nbr_input,
                "so_third_former_spouse_annulment_case_date" : str(st.session_state.so_third_former_spouse_annulment_case_date_input),
                "so_third_former_spouse_annulment_diocese_city" : st.session_state.so_third_former_spouse_annulment_diocese_city_input,
                "so_third_former_spouse_annulment_diocese_state" : st.session_state.so_third_former_spouse_annulment_diocese_state_input,
                "so_third_former_spouse_annulment_diocese_country" : st.session_state.so_third_former_spouse_annulment_diocese_country_input,
                "so_third_former_spouse_annulment_nullity_verification" : st.session_state.so_third_former_spouse_annulment_nullity_verification_input,
                "so_third_former_spouse_annulment_nullity_date" : str(st.session_state.so_third_former_spouse_annulment_nullity_date_input)
                }).execute()

                st.success("Candidate information submitted successfully!")
                st.session_state.current_page = "Home"
            except Exception as e:
                st.error(f"An error occurred while submitting the data: {e}")

            try:
                recipient = "tdakers0113@gmail.com"
                subject = "Fancy HTML Email"
                html_body = st.text_area("HTML Body", value="""
                <h2 style='color:blue;'>Hello from Streamlit!</h2>
                <p>This is an <b>HTML-formatted</b> email sent using <i>Python</i>.</p>
                """, height=200)

                success = send_html_email(recipient, subject, html_body)
                if success:
                    st.success("HTML email sent successfully!")
            except Exception as e:
                st.write(f"An error occurred while preparing the email: {e}")
# %%
