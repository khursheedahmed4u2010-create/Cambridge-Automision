import streamlit as st
import pandas as pd
import google.generativeai as genai

# Streamlit Page Setup
st.set_page_config(page_title="Cambridge Automision", page_icon="🏫", layout="wide")

st.title("🏫 Cambridge Automision")
st.caption("AI-Powered Smart School Management & Automated Parent Communication System")

# Function to Load Sheet Directly via CSV URL
@st.cache_data(ttl=1)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSnC8YeuGYiEwSFHlusp378ualxbOrrMMYJpH8WxsASpWQ1rWoc2HP-bVwAmpBd2dCMmisRPwZy7sV/pub?gid=0&single=true&output=csv"
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"گوگل شیٹ سے ڈیٹا لوڈ نہیں ہو سکا: {e}")
        return pd.DataFrame()

df = load_data()

tab1, tab2, tab3 = st.tabs(["📊 ڈیش بورڈ (Dashboard)", "📋 اٹینڈنس اور الرٹس (Attendance & Alerts)", "🤖 AI اسمارٹ ڈائری (AI Smart Diary)"])

# TAB 1: DASHBOARD
with tab1:
    st.header("مجموعی جائزہ (System Overview)")
    if not df.empty:
        col1, col2 = st.columns(2)
        col1.metric("کل ریکارڈز (Total Records)", len(df))
        
        st.subheader("طلباء کی فہرست (Student Master List)")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("ڈیٹا لوڈ ہو رہا ہے...")

# TAB 2: ATTENDANCE & WHATSAPP
with tab2:
    st.header("حاضری اور واٹس ایپ نوٹیفکیشن")
    if not df.empty:
        student_col = df.columns[0]
        for col in df.columns:
            if 'student' in str(col).lower() or 'name' in str(col).lower():
                student_col = col
                break
                
        selected_student = st.selectbox("طالب علم منتخب کریں:", df[student_col].dropna().unique())
        student_info = df[df[student_col] == selected_student].iloc[0]
        
        status = st.radio("حاضری کی صورتحال:", ["Present", "Absent"])
        
        if status == "Absent":
            phone_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
            for col in df.columns:
                if 'phone' in str(col).lower() or 'mobile' in str(col).lower() or 'parent' in str(col).lower():
                    phone_col = col
                    break
            
            phone = str(student_info.get(phone_col, '')).replace(".0", "").replace("+", "").strip()
            msg = f"محترم والدین، آپ کا بچہ {student_info[student_col]} آج اسکول سے غیر حاضر ہے۔ برائے مہربانی اطلاع دیں۔ - Cambridge High School"
            whatsapp_url = f"https://wa.me/{phone}?text={msg.replace(' ', '%20')}"
            
            st.warning("طالب علم غیر حاضر ہے!")
            st.markdown(f"[📲 والدین کو واٹس ایپ میسج بھیجیں]({whatsapp_url})", unsafe_allow_html=True)

# TAB 3: AI SMART DIARY
with tab3:
    st.header("🤖 AI اسمارٹ ڈائری جنریٹر")
    st.write("ٹیچر کا لکھا ہوا شارٹ نوٹ AI کی مدد سے والدین کے لیے ایک بہترین پروفیشنل ڈائری میسج میں تبدیل کریں۔")
    
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
        st.error("Gemini API Key سیٹ نہیں ہے۔ Streamlit Secrets میں GEMINI_API_KEY اینٹر کریں۔")
