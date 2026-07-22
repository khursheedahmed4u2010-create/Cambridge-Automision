# Function to Load Sheet Directly via CSV URL
@st.cache_data(ttl=30)
def load_data():
    try:
        # Publish to web والا کاپی کیا ہوا CSV لنک یہاں پیسٹ کریں
        url = "یہاں_اپنا_کاپی_کیا_ہوا_CSV_لنک_پیسٹ_کریں"
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"گوگل شیٹ سے ڈیٹا لوڈ نہیں ہو سکا: {e}")
        return pd.DataFrame()
