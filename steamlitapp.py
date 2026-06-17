import streamlit as st
import json
import os
from datetime import datetime
import re

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="Home Budget Tracker",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
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
            data = json.loads(json.dumps(DEFAULT_DATA))  # deep copy
            data.update(saved)
            return data
        except json.JSONDecodeError:
            return json.loads(json.dumps(DEFAULT_DATA))
    return json.loads(json.dumps(DEFAULT_DATA))

def save_data(data):
    data["last_updated"] = datetime.now().strftime("%d %b %Y, %I:%M %p")
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = load_data()

DATA = st.session_state.data

# ============ EXPENSE SCHEMA ============
SIMPLE_ITEMS = [
    ("family", "waliha_pocket",  "Waliha Pocket Money", "💵"),
    ("family", "waliha_tuition", "Waliha Tuition Fees",  "📚"),
    ("family", "waliha_school",  "Waliha School Fees",   "🏫"),
    ("family", "rahim_pocket",   "Rahim Pocket Money",   "💵"),
    ("family", "jazib_pocket",   "Jazib Pocket Money",   "💵"),
    ("family", "jazib_academy",  "Jazib Academy Fees",   "📖"),
    ("family", "mother_pocket",  "Mother Pocket Money",  "💵"),

    ("food",   "veg_fruit",      "Vegetables & Fruits",  "🥦"),
    ("food",   "grocery",        "Grocery",               "🛒"),

    ("utilities", "electricity", "Electricity Bill",      "💡"),
    ("utilities", "water",       "Water Bill",             "🚰"),
    ("utilities", "sui_gas",     "Sui Gas Bill",           "🔥"),
    ("utilities", "internet",    "Internet Fees",          "🌐"),
    ("utilities", "trash",       "Trash Fees",             "🗑️"),
    ("utilities", "cable",       "Cable Fees",             "📺"),
    ("utilities", "newspaper",   "Newspaper Bill",         "📰"),

    ("staff",  "maid",           "Maid Fees",              "🧹"),
    ("staff",  "gardener",       "Gardener Fees",          "🌳"),
    ("staff",  "guard",          "Guard Fees",             "🛡️"),
    ("staff",  "car_wash",       "Car Wash",               "🚿"),
]

CATEGORY_TITLES = {
    "family":     "👨‍👩‍👧‍👦 Family Pocket Money & Fees",
    "food":       "🍎 Food & Kitchen",
    "utilities":  "💡 Utilities & Bills",
    "staff":      "🧑‍🔧 Staff & Misc",
}

# ============ FETCH FUEL PRICE ============
def fetch_petrol_price():
    try:
        import requests
        r = requests.get(
            "https://www.pakwheels.com/petroleum-prices-in-pakistan",
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        text = r.text
        m = re.search(r'Petrol Price in Pakistan is\s*(?:PKR|Rs\.?)\s*([\d]+\.?\d*)', text, re.IGNORECASE)
        if not m:
            m = re.search(r'Rs\.?\s*([\d]{2,3}\.\d{1,2})\s*/?\s*Ltr', text, re.IGNORECASE)
        if m:
            return float(m.group(1))
    except Exception:
        pass
    return None

# ============ CSS STYLING ============
st.markdown("""
<style>
    .header {
        background: linear-gradient(135deg, #0f766e 0%, #134e4a 100%);
        color: white;
        padding: 30px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .stat-box {
        background: #ecfdf5;
        border: 2px solid #6ee7b7;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .stat-box-jazib {
        background: #eff6ff;
        border: 2px solid #93c5fd;
    }
    .stat-box-father {
        background: #fff7ed;
        border: 2px solid #fdba74;
    }
    .stat-label {
        font-size: 14px;
        color: #666;
        margin-bottom: 8px;
    }
    .stat-value {
        font-size: 28px;
        font-weight: 700;
        color: #111;
    }
</style>
""", unsafe_allow_html=True)

# ============ HEADER ============
st.markdown("""
<div class="header">
    <h1>🏠 Home Budget Tracker</h1>
    <p>Pakistani Household Expense Manager | Track • Calculate • Split</p>
</div>
""", unsafe_allow_html=True)

# ============ SIDEBAR ============
with st.sidebar:
    st.title("⚙️ Quick Actions")
    
    if st.button("💾 Save & Refresh", use_container_width=True):
        save_data(DATA)
        st.success("✅ Data saved!")
        st.rerun()
    
    if st.button("🔄 Load Previous Data", use_container_width=True):
        st.session_state.data = load_data()
        st.success("✅ Previous data loaded!")
        st.rerun()
    
    if st.button("🗑️ Clear All Data", use_container_width=True):
        if st.confirm("Are you sure? This cannot be undone."):
            st.session_state.data = json.loads(json.dumps(DEFAULT_DATA))
            save_data(st.session_state.data)
            st.success("✅ All data cleared!")
            st.rerun()
    
    st.divider()
    st.markdown("### 📊 Data Status")
    if DATA.get("last_updated"):
        st.info(f"💾 Last saved: {DATA['last_updated']}")
    else:
        st.warning("⚠️ No saved data yet")

# ============ TABS ============
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👨‍👩‍👧‍👦 Family",
    "🍎 Food & Kitchen",
    "💡 Utilities",
    "🚗 Transport & More",
    "📊 Calculate & Split"
])

# ============ TAB 1: FAMILY ============
with tab1:
    st.subheader("👨‍👩‍👧‍👦 Family Pocket Money & School Fees")
    
    family_items = [item for item in SIMPLE_ITEMS if item[0] == "family"]
    
    cols = st.columns(2)
    for idx, (cat, key, label, icon) in enumerate(family_items):
        with cols[idx % 2]:
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                st.write(f"{icon}")
            with col2:
                amount = st.number_input(
                    label,
                    value=int(DATA["values"].get(key, 0)),
                    min_value=0,
                    step=50,
                    key=f"family_{key}"
                )
                DATA["values"][key] = amount
            with col3:
                is_fixed = st.checkbox(
                    "Fixed 🔒",
                    value=DATA["fixed_flags"].get(key, False),
                    key=f"fixed_family_{key}"
                )
                DATA["fixed_flags"][key] = is_fixed

# ============ TAB 2: FOOD ============
with tab2:
    st.subheader("🍎 Food & Kitchen Costs")
    
    food_items = [item for item in SIMPLE_ITEMS if item[0] == "food"]
    
    for cat, key, label, icon in food_items:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.write(f"{icon}")
        with col2:
            amount = st.number_input(
                label,
                value=int(DATA["values"].get(key, 0)),
                min_value=0,
                step=50,
                key=f"food_{key}"
            )
            DATA["values"][key] = amount
        with col3:
            is_fixed = st.checkbox(
                "Fixed 🔒",
                value=DATA["fixed_flags"].get(key, False),
                key=f"fixed_food_{key}"
            )
            DATA["fixed_flags"][key] = is_fixed

# ============ TAB 3: UTILITIES ============
with tab3:
    st.subheader("💡 Utilities & Bills")
    
    utilities_items = [item for item in SIMPLE_ITEMS if item[0] == "utilities"]
    
    cols = st.columns(2)
    for idx, (cat, key, label, icon) in enumerate(utilities_items):
        with cols[idx % 2]:
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                st.write(f"{icon}")
            with col2:
                amount = st.number_input(
                    label,
                    value=int(DATA["values"].get(key, 0)),
                    min_value=0,
                    step=50,
                    key=f"util_{key}"
                )
                DATA["values"][key] = amount
            with col3:
                is_fixed = st.checkbox(
                    "Fixed 🔒",
                    value=DATA["fixed_flags"].get(key, False),
                    key=f"fixed_util_{key}"
                )
                DATA["fixed_flags"][key] = is_fixed

# ============ TAB 4: TRANSPORT & MORE ============
with tab4:
    # Transport Section
    st.subheader("🚗 Transport (Fuel Consumption)")
    st.info("💡 Enter liters consumed per month for each vehicle. Price fetches automatically.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fuel_price = st.number_input(
            "Fuel Price (Rs/Liter):",
            value=int(DATA["transport"]["fuel_price"]),
            min_value=0,
            step=1,
            key="fuel_price"
        )
        DATA["transport"]["fuel_price"] = fuel_price
    
    with col2:
        if st.button("🔄 Auto-Fetch Petrol Price"):
            fetched = fetch_petrol_price()
            if fetched:
                DATA["transport"]["fuel_price"] = int(fetched)
                st.success(f"✅ Updated to Rs. {int(fetched)}/L")
                st.rerun()
            else:
                st.error("❌ Could not fetch price. Enter manually.")
    
    with col3:
        st.empty()
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        civic = st.number_input(
            "Civic (Liters/month):",
            value=int(DATA["transport"]["civic_liters"]),
            min_value=0,
            step=5,
            key="civic"
        )
        DATA["transport"]["civic_liters"] = civic
    
    with col2:
        cultus = st.number_input(
            "Cultus (Liters/month):",
            value=int(DATA["transport"]["cultus_liters"]),
            min_value=0,
            step=5,
            key="cultus"
        )
        DATA["transport"]["cultus_liters"] = cultus
    
    with col3:
        bike = st.number_input(
            "Bike (Liters/month):",
            value=int(DATA["transport"]["bike_liters"]),
            min_value=0,
            step=5,
            key="bike"
        )
        DATA["transport"]["bike_liters"] = bike
    
    # Meat & Milk Section
    st.divider()
    st.subheader("🥩 Meat & Milk")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Meat**")
        meat_price = st.number_input(
            "Price (Rs/kg):",
            value=int(DATA["meat"]["price"]),
            min_value=0,
            step=50,
            key="meat_price"
        )
        DATA["meat"]["price"] = meat_price
        
        meat_kg = st.number_input(
            "Quantity (kg/month):",
            value=float(DATA["meat"]["kg"]),
            min_value=0.0,
            step=0.5,
            key="meat_kg"
        )
        DATA["meat"]["kg"] = meat_kg
    
    with col2:
        st.write("**Milk**")
        milk_price = st.number_input(
            "Price (Rs/liter):",
            value=int(DATA["milk"]["price"]),
            min_value=0,
            step=10,
            key="milk_price"
        )
        DATA["milk"]["price"] = milk_price
        
        milk_daily = st.number_input(
            "Liters/day:",
            value=float(DATA["milk"]["liters_per_day"]),
            min_value=0.0,
            step=0.1,
            key="milk_daily"
        )
        DATA["milk"]["liters_per_day"] = milk_daily
        
        milk_days = st.slider(
            "Days/month:",
            min_value=1,
            max_value=31,
            value=int(DATA["milk"]["days"]),
            key="milk_days"
        )
        DATA["milk"]["days"] = milk_days
    
    # Staff Section
    st.divider()
    st.subheader("🧑‍🔧 Staff & Miscellaneous")
    
    staff_items = [item for item in SIMPLE_ITEMS if item[0] == "staff"]
    
    cols = st.columns(2)
    for idx, (cat, key, label, icon) in enumerate(staff_items):
        with cols[idx % 2]:
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                st.write(f"{icon}")
            with col2:
                amount = st.number_input(
                    label,
                    value=int(DATA["values"].get(key, 0)),
                    min_value=0,
                    step=50,
                    key=f"staff_{key}"
                )
                DATA["values"][key] = amount
            with col3:
                is_fixed = st.checkbox(
                    "Fixed 🔒",
                    value=DATA["fixed_flags"].get(key, False),
                    key=f"fixed_staff_{key}"
                )
                DATA["fixed_flags"][key] = is_fixed
    
    # Custom Expenses
    st.divider()
    st.subheader("➕ Custom Expenses (Add Your Own)")
    
    if DATA["custom_expenses"]:
        for custom_key, (name, val) in list(DATA["custom_expenses"].items()):
            col1, col2, col3 = st.columns([2, 1, 0.5])
            
            with col1:
                st.write(f"🏷️ {name}")
            with col2:
                new_val = st.number_input(
                    f"{name} amount",
                    value=int(val),
                    min_value=0,
                    step=50,
                    label_visibility="collapsed",
                    key=f"custom_{custom_key}"
                )
                DATA["custom_expenses"][custom_key] = (name, new_val)
            with col3:
                if st.button("❌", key=f"del_{custom_key}"):
                    del DATA["custom_expenses"][custom_key]
                    st.rerun()
    
    st.divider()
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        new_name = st.text_input("New expense name:", placeholder="e.g. Pet Food")
    with col2:
        new_amount = st.number_input("Amount (Rs):", min_value=0, step=50)
    with col3:
        if st.button("➕ Add", use_container_width=True):
            if new_name.strip():
                custom_key = f"custom_{len(DATA['custom_expenses']) + 1}"
                DATA["custom_expenses"][custom_key] = (new_name, int(new_amount))
                st.success(f"✅ Added '{new_name}'")
                st.rerun()

# ============ TAB 5: CALCULATE & SPLIT ============
with tab5:
    st.subheader("📊 Calculate Total & Settlement")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("**If you pay some expenses but your father covers the rest, enter what you paid here.**")
        jazib_share = st.number_input(
            "Your Share (Jazib) - Rs:",
            value=int(DATA.get("last_jazib_share", 0)),
            min_value=0,
            step=100,
            key="jazib_share_input"
        )
        DATA["last_jazib_share"] = jazib_share
    
    with col2:
        st.empty()
    
    # CALCULATE BUTTON
    if st.button("🔢 CALCULATE TOTAL", use_container_width=True, type="primary"):
        # Calculate all totals
        total = sum(DATA["values"].values())
        
        # Transport
        transport_total = (
            DATA["transport"]["fuel_price"] * 
            (DATA["transport"]["civic_liters"] + 
             DATA["transport"]["cultus_liters"] + 
             DATA["transport"]["bike_liters"])
        )
        total += transport_total
        
        # Meat
        meat_total = DATA["meat"]["price"] * DATA["meat"]["kg"]
        total += meat_total
        
        # Milk
        milk_total = (DATA["milk"]["price"] * 
                      DATA["milk"]["liters_per_day"] * 
                      DATA["milk"]["days"])
        total += milk_total
        
        # Custom
        custom_total = sum(v for _, v in DATA["custom_expenses"].values())
        total += custom_total
        
        # Calculate split
        jazib_share_val = DATA["last_jazib_share"]
        father_share = max(0, total - jazib_share_val)
        
        # Save to file
        save_data(DATA)
        
        # ===== DISPLAY RESULTS =====
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-label">💰 TOTAL MONTHLY EXPENSE</div>
                <div class="stat-value">Rs. {total:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-box stat-box-jazib">
                <div class="stat-label">👤 Your Share (Jazib)</div>
                <div class="stat-value">Rs. {jazib_share_val:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-box stat-box-father">
                <div class="stat-label">👨 Father's Share</div>
                <div class="stat-value">Rs. {father_share:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Breakdown
        st.markdown("### 📋 Expense Breakdown")
        
        breakdown = []
        
        for (cat, key, label, icon) in SIMPLE_ITEMS:
            val = DATA["values"].get(key, 0)
            if val > 0:
                breakdown.append((f"{icon} {label}", val))
        
        if transport_total > 0:
            breakdown.append(("🚗 Transport (Fuel)", transport_total))
        if meat_total > 0:
            breakdown.append(("🥩 Meat", meat_total))
        if milk_total > 0:
            breakdown.append(("🥛 Milk", milk_total))
        
        for _, (name, val) in DATA["custom_expenses"].items():
            if val > 0:
                breakdown.append((f"🏷️ {name}", val))
        
        breakdown.sort(key=lambda x: x[1], reverse=True)
        
        # Display as table
        df_data = {"Item": [], "Amount (Rs)": []}
        for label, amt in breakdown:
            df_data["Item"].append(label)
            df_data["Amount (Rs)"].append(f"{amt:,.0f}")
        
        st.dataframe(
            {"Item": df_data["Item"], "Amount (Rs)": df_data["Amount (Rs)"]},
            use_container_width=True,
            hide_index=True
        )
        
        # Summary statistics
        st.divider()
        st.markdown("### 📈 Quick Stats")
        
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        
        with stat_col1:
            st.metric("Total Expenses", f"Rs. {total:,.0f}")
        with stat_col2:
            st.metric("Your Payment", f"Rs. {jazib_share_val:,.0f}")
        with stat_col3:
            percentage = (jazib_share_val / total * 100) if total > 0 else 0
            st.metric("Your % of Total", f"{percentage:.1f}%")
        
        st.success("✅ Calculation complete & data saved!")

# ============ FOOTER ============
st.divider()
st.markdown("""
---
**🏠 Home Budget Tracker** | Built by Jazib Ali  
📊 Track expenses • 🔒 Lock fixed costs • 📱 Split bills  
💾 Data saved locally | 🌐 Run on Streamlit Cloud
""")
