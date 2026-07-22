import urllib.parse
import pandas as pd
import streamlit as st
import requests
import io
import google.generativeai as genai

# Streamlit Page Setup
st.set_page_config(page_title="Cambridge Automision", page_icon="🏫", layout="wide")

st.title("🏫 Cambridge Automision")
st.caption("AI-Powered Smart School Management & Automated Parent Communication System")

# Function to Load Sheet directly via Published CSV Link with Request Headers
@st.cache_data(ttl=5)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSnC8YeuGYiEwSFHlusp378ualxbOrrMMYJpH8WxsASpWQ1rWoc2HP-bVwAmpBd2dCMmisRPwZy7sV/pub?gid=0&single=true&output=csv"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text))
            return df
        else:
            st.error(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading Google Sheet: {e}")
        return pd.DataFrame()

df = load_data()

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📋 Attendance & Alerts", "🤖 AI Smart Diary"])

# TAB 1: DASHBOARD
with tab1:
    st.header("System Overview")
    if not df.empty:
        col1, col2 = st.columns(2)
        col1.metric("Total Records", len(df))
        
        st.subheader("Student Master List")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Loading Data from Google Sheet...")

# TAB 2: ATTENDANCE & WHATSAPP
with tab2:
    st.header("Attendance & WhatsApp Notification")
    if not df.empty:
        student_col = df.columns[0]
        for col in df.columns:
            if 'student' in str(col).lower() or 'name' in str(col).lower():
                student_col = col
                break
                
        selected_student = st.selectbox("Select Student:", df[student_col].dropna().unique())
        student_info = df[df[student_col] == selected_student].iloc[0]
        
        status = st.radio("Attendance Status:", ["Present", "Absent"])
        
        if status == "Absent":
            phone_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
            for col in df.columns:
                if 'phone' in str(col).lower() or 'mobile' in str(col).lower() or 'parent' in str(col).lower():
                    phone_col = col
                    break
            
            phone = str(student_info.get(phone_col, '')).replace(".0", "").replace("+", "").strip()
            student_name = str(student_info[student_col])
            
            # Clean WhatsApp Message String
            msg = f"Respected Parent, your child {student_name} is ABSENT today. Please inform the reason. - Cambridge High School"
            encoded_msg = urllib.parse.quote(msg)
            whatsapp_url = f"https://wa.me/{phone}?text={encoded_msg}"
            
            st.warning("Student is Marked ABSENT!")
            st.markdown(f"[📲 Send WhatsApp Message to Parent]({whatsapp_url})", unsafe_allow_html=True)

# TAB 3: AI SMART DIARY
with tab3:
    st.header("🤖 AI Smart Diary Generator")
    st.write("Convert short teacher notes into professional parent messages using Gemini AI.")
    
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        subject = st.selectbox("Subject:", ["Math", "English", "Urdu", "Science", "General Notice"])
        raw_notes = st.text_area("Enter Class Notes / Homework:", placeholder="e.g. Math Exercise 5.1 Q1 to Q5 done. Homework is Q6.")
        
        if st.button("✨ Generate AI Diary Message"):
            if raw_notes:
                system_prompt = f"""
                You are an expert school coordinator. Convert the following teacher's raw daily notes into a polite, professional, and clear WhatsApp message for parents in Roman Urdu / English.
                
                Subject: {subject}
                Raw Note: {raw_notes}
                
                Make it structured with emojis, clear homework instructions, and polite greeting from Cambridge High School.
                """
                
                with st.spinner("AI is generating message..."):
                    response = model.generate_content(system_prompt)
                    st.success("AI Message Ready!")
                    st.code(response.text, language="markdown")
            else:
                st.warning("Please enter some notes first.")
    except Exception as e:
        st.error("Gemini API Key is missing! Please set GEMINI_API_KEY in Streamlit Secrets.")
