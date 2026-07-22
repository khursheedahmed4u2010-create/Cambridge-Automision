import streamlit as st
import pandas as pd
import google.generativeai as genai
import gspread
from google.oauth2.service_account import Credentials

# Streamlit Page Setup
st.set_page_config(page_title="Cambridge Automision", page_icon="🏫", layout="wide")

# App Header
st.title("🏫 Cambridge Automision")
st.caption("AI-Powered Smart School Management & Automated Parent Communication System")

# Function to Connect to Google Sheets
@st.cache_data(ttl=60)
def load_data():
    try:
        # Load credentials from Streamlit Secrets
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        
        # Open Google Sheet by Name
        sheet = client.open("Cambridge Automision")
        
        # Load Worksheets
        students_df = pd.DataFrame(sheet.worksheet("Students_Master").get_all_records())
        return students_df
    except Exception as e:
        st.error(f"Google Sheet سے کنیکشن میں مسئلہ: {e}")
        return pd.DataFrame()

# Load Data
df = load_data()

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["📊 ڈیش بورڈ (Dashboard)", "📋 اٹینڈنس اور الرٹس (Attendance & Alerts)", "🤖 AI اسمارٹ ڈائری (AI Smart Diary)"])

# TAB 1: DASHBOARD
with tab1:
    st.header("مجموعی جائزہ (System Overview)")
    if not df.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("کل طلباء (Total Students)", len(df))
        
        # Show Student Table
        st.subheader("طلباء کی فہرست (Student Master List)")
        st.dataframe(df[['Student_ID', 'Student_Name', 'Teacher_Name', 'Class_Name', 'Parent_Phone', 'Current_Status']], use_container_width=True)
    else:
        st.info("ڈیٹا لوڈ ہو رہا ہے یا گوگل شیٹ خالی ہے۔")

# TAB 2: ATTENDANCE & WHATSAPP
with tab2:
    st.header("حاضری اور واٹس ایپ نوٹیفکیشن")
    if not df.empty:
        selected_student = st.selectbox("طالب علم منتخب کریں:", df['Student_Name'].tolist())
        student_info = df[df['Student_Name'] == selected_student].iloc[0]
        
        st.write(f"**کلاس:** {student_info.get('Class_Name', 'N/A')}")
        st.write(f"**والد کا فون:** {student_info.get('Parent_Phone', 'N/A')}")
        
        status = st.radio("حاضری کی صورتحال:", ["Present", "Absent"])
        
        if status == "Absent":
            phone = str(student_info.get('Parent_Phone', '')).replace("+", "").strip()
            msg = f"محترم والدین، آپ کا بچہ {student_info['Student_Name']} آج اسکول سے غیر حاضر ہے۔ برائے مہربانی اطلاع دیں۔ - Cambridge High School"
            whatsapp_url = f"https://wa.me/{phone}?text={msg.replace(' ', '%20')}"
            
            st.warning("طالب علم غیر حاضر ہے!")
            st.markdown(f"[📲 والدین کو واٹس ایپ میسج بھیجیں]({whatsapp_url})", unsafe_allow_google_concept=True)

# TAB 3: AI SMART DIARY (REQUIREMENT 3: AI FEATURE)
with tab3:
    st.header("🤖 AI اسمارٹ ڈائری جنریٹر")
    st.write("ٹیچر کا لکھا ہوا شارٹ نوٹ AI کی مدد سے والدین کے لیے ایک بہترین پروفیشنل ڈائری میسج میں تبدیل کریں۔")
    
    # Configure Gemini API
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        subject = st.selectbox("مضمون (Subject):", ["Math", "English", "Urdu", "Science", "General Notice"])
        raw_notes = st.text_area("کلاس نوٹس یا ہوم ورک درج کریں:", placeholder="مثلاً: Math Exercise 5.1 Q1 to Q5 done. Home work is Q6.")
        
        if st.button("✨ AI ڈائری میسج جنریٹ کریں"):
            if raw_notes:
                system_prompt = f"""
                You are an expert school coordinator. Convert the following teacher's raw daily notes into a polite, professional, and clear WhatsApp message for parents in Urdu/English mix (Roman Urdu/Urdu).
                
                Subject: {subject}
                Raw Note: {raw_notes}
                
                Make it structured with emojis, clear homework instructions, and polite greeting from Cambridge High School.
                """
                
                with st.spinner("AI میسج تیار کر رہا ہے..."):
                    response = model.generate_content(system_prompt)
                    st.success("AI ڈائری میسج تیار ہے!")
                    st.code(response.text, language="markdown")
            else:
                st.warning("برائے مہربانی پہلے نوٹس درج کریں۔")
    except Exception as e:
        st.error("Gemini API Key سیٹ نہیں ہے۔ ڈیپلائمنٹ کے وقت کلاؤڈ میں اینٹر کریں۔")
