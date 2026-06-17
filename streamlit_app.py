import streamlit as st
import json
import os
from datetime import datetime

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="Home Budget Tracker",
    page_icon="🏠",
    layout="wide"
)

# ============ LOAD/SAVE DATA ============
DATA_FILE = "budget_data.json"

DEFAULT_DATA = {
    "values": {},
    "fixed_flags": {},
    "transport": {"fuel_price": 0, "civic_liters": 0, "cultus_liters": 0, "bike_liters": 0},
    "meat": {"price": 0, "kg": 0},
    "milk": {"price": 0, "liters_per_day": 0, "days": 30},
    "custom_expenses": {},
    "last_jazib_share": 0,
    "last_updated": None,
}

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                saved = json.load(f)
            data = json.loads(json.dumps(DEFAULT_DATA))
            data.update(saved)
            return data
        except:
            return json.loads(json.dumps(DEFAULT_DATA))
    return json.loads(json.dumps(DEFAULT_DATA))

def save_data(data):
    data["last_updated"] = datetime.now().strftime("%d %b %Y, %I:%M %p")
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

if "data" not in st.session_state:
    st.session_state.data = load_data()

DATA = st.session_state.data

# ============ HEADER ============
st.markdown("""
<div style="background: linear-gradient(135deg, #0f766e 0%, #134e4a 100%); color: white; padding: 30px; border-radius: 12px; margin-bottom: 20px;">
    <h1>🏠 Home Budget Tracker</h1>
    <p>Pakistani Household Expense Manager</p>
</div>
""", unsafe_allow_html=True)

# ============ SIMPLE EXPENSES ============
st.sidebar.title("⚙️ Actions")
if st.sidebar.button("💾 Save Data", use_container_width=True):
    save_data(DATA)
    st.success("✅ Data saved!")

tab1, tab2, tab3 = st.tabs(["👨‍👩‍👧‍👦 Family", "🚗 Transport", "📊 Calculate"])

# ===== TAB 1: FAMILY =====
with tab1:
    st.subheader("Family Expenses")
    
    waliha_pocket = st.number_input("Waliha Pocket Money:", value=float(DATA["values"].get("waliha_pocket", 0)), min_value=0.0, step=50.0)
    DATA["values"]["waliha_pocket"] = waliha_pocket
    
    rahim_pocket = st.number_input("Rahim Pocket Money:", value=float(DATA["values"].get("rahim_pocket", 0)), min_value=0.0, step=50.0)
    DATA["values"]["rahim_pocket"] = rahim_pocket
    
    jazib_pocket = st.number_input("Jazib Pocket Money:", value=float(DATA["values"].get("jazib_pocket", 0)), min_value=0.0, step=50.0)
    DATA["values"]["jazib_pocket"] = jazib_pocket
    
    mother_pocket = st.number_input("Mother Pocket Money:", value=float(DATA["values"].get("mother_pocket", 0)), min_value=0.0, step=50.0)
    DATA["values"]["mother_pocket"] = mother_pocket

# ===== TAB 2: TRANSPORT =====
with tab2:
    st.subheader("🚗 Transport & Other Expenses")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Fuel Price**")
        fuel_price = st.number_input("Rs/Liter:", value=float(DATA["transport"]["fuel_price"]), min_value=0.0, step=1.0, key="fuel_price")
        DATA["transport"]["fuel_price"] = fuel_price
    
    with col2:
        st.write("**Vehicle Liters/Month**")
    
    civic = st.number_input("Civic (Liters):", value=float(DATA["transport"]["civic_liters"]), min_value=0.0, step=5.0)
    DATA["transport"]["civic_liters"] = civic
    
    cultus = st.number_input("Cultus (Liters):", value=float(DATA["transport"]["cultus_liters"]), min_value=0.0, step=5.0)
    DATA["transport"]["cultus_liters"] = cultus
    
    bike = st.number_input("Bike (Liters):", value=float(DATA["transport"]["bike_liters"]), min_value=0.0, step=5.0)
    DATA["transport"]["bike_liters"] = bike
    
    st.divider()
    
    st.write("**Meat & Milk**")
    meat_price = st.number_input("Meat Price (Rs/kg):", value=float(DATA["meat"]["price"]), min_value=0.0, step=50.0)
    DATA["meat"]["price"] = meat_price
    
    meat_kg = st.number_input("Meat (kg/month):", value=float(DATA["meat"]["kg"]), min_value=0.0, step=0.5)
    DATA["meat"]["kg"] = meat_kg
    
    milk_price = st.number_input("Milk Price (Rs/liter):", value=float(DATA["milk"]["price"]), min_value=0.0, step=10.0)
    DATA["milk"]["price"] = milk_price
    
    milk_daily = st.number_input("Milk (liters/day):", value=float(DATA["milk"]["liters_per_day"]), min_value=0.0, step=0.1)
    DATA["milk"]["liters_per_day"] = milk_daily

# ===== TAB 3: CALCULATE =====
with tab3:
    st.subheader("📊 Calculate Total")
    
    if st.button("🔢 CALCULATE", use_container_width=True, type="primary"):
        # Calculate
        total = sum(DATA["values"].values())
        transport_total = DATA["transport"]["fuel_price"] * (DATA["transport"]["civic_liters"] + DATA["transport"]["cultus_liters"] + DATA["transport"]["bike_liters"])
        meat_total = DATA["meat"]["price"] * DATA["meat"]["kg"]
        milk_total = DATA["milk"]["price"] * DATA["milk"]["liters_per_day"] * DATA["milk"]["days"]
        
        total += transport_total + meat_total + milk_total
        
        jazib_share = st.number_input("Your Share (Jazib):", value=float(DATA.get("last_jazib_share", 0)), min_value=0.0, step=100.0)
        DATA["last_jazib_share"] = jazib_share
        
        father_share = max(0, total - jazib_share)
        
        save_data(DATA)
        
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total", f"Rs. {total:,.0f}")
        with col2:
            st.metric("Your Share", f"Rs. {jazib_share:,.0f}")
        with col3:
            st.metric("Father's Share", f"Rs. {father_share:,.0f}")
        
        st.success("✅ Calculation complete!")

st.divider()
st.markdown("**🏠 Home Budget Tracker** | Built with Streamlit")
