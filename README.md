# 🏠 Home Budget Tracker
**Pakistani Household Expense Manager**

A smart budgeting app to track all home expenses, lock fixed costs, and split bills between family members.

---

## ✨ Features

✅ **Auto-fetch petrol prices** from web (or enter manually)  
✅ **Lock fixed expenses** — they stay the same each month  
✅ **Calculate fuel costs** by vehicle (Civic, Cultus, Bike)  
✅ **Track meat & milk** by quantity (price × kg/liters)  
✅ **Add custom expenses** anytime (Pet food, Charity, etc.)  
✅ **Split bills** between you and your father  
✅ **Data saves locally** — survives app restart  
✅ **Clean interface** — organized by category  

---

## 📊 What You Can Track

| Category | Items |
|---|---|
| 👨‍👩‍👧‍👦 **Family** | Waliha (pocket, tuition, school), Rahim, Jazib, Mother |
| 🍎 **Food** | Vegetables, fruits, grocery |
| 💡 **Utilities** | Electricity, water, gas, internet, trash, cable, newspaper |
| 🧑‍🔧 **Staff** | Maid, gardener, guard, car wash |
| 🚗 **Transport** | Civic, Cultus, Bike (by liters × price) |
| 🥩 **Meat & Milk** | Quantity-based calculation |
| ➕ **Custom** | Add anything you want |

---

## 🚀 How to Run Locally

### **Option 1: Quick Start (No installation needed)**

If you have Python 3.8+ installed:

```bash
# Clone this repository
git clone https://github.com/YOUR_USERNAME/home-budget-tracker
cd home-budget-tracker

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app opens at: **http://localhost:8501**

### **Option 2: Using Python venv (Recommended)**

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run
streamlit run app.py
```

---

## ☁️ Deploy to Streamlit Cloud (FREE)

### **Step 1: Push to GitHub**

1. Go to your GitHub repository
2. Upload these 3 files:
   - `app.py` (the main app)
   - `requirements.txt` (dependencies)
   - `README.md` (this file)

3. Commit and push

### **Step 2: Deploy on Streamlit Cloud**

1. Go to **streamlit.io/cloud**
2. Click **"New app"**
3. Select:
   - **Repository:** your GitHub repo
   - **Branch:** main
   - **Main file path:** `app.py`
4. Click **"Deploy"**

✅ Your app is now **live on the web** — share the link with anyone!

**Example link:** `https://home-budget-tracker.streamlit.app`

---

## 🎯 How to Use

### **1. Fill Your Expenses**

- Go to each tab (Family, Food, Utilities, etc.)
- Enter the amount for each expense
- Check **"Fixed 🔒"** if it doesn't change monthly

### **2. Transport & Special Items**

- **Transport:** Enter liters/month for each vehicle
  - Click **"🔄 Auto-Fetch"** to get today's petrol price
  - Or enter the price manually
  
- **Meat:** Enter price/kg + quantity
- **Milk:** Enter price/liter + liters/day + days/month

### **3. Add Custom Expenses**

- In the Transport tab, scroll to **"Custom Expenses"**
- Enter name (e.g., "Pet Food") and amount
- Click **"➕ Add"**

### **4. Calculate & Split**

- Go to **"Calculate & Split"** tab
- Enter your share (amount you paid)
- Click **"🔢 CALCULATE TOTAL"**
- See:
  - 💰 Total monthly expense
  - 👤 Your share
  - 👨 Father's share

### **5. Save Your Data**

- Click **"💾 Save & Refresh"** in the sidebar
- Data is saved locally
- Next time you open, click **"🔄 Load Previous Data"**

---

## 🔄 What Changed From Google Colab?

| Feature | Colab Notebook | Streamlit App |
|---|---|---|
| **Interface** | Jupyter widgets | Web interface |
| **Data Storage** | Google Drive | Local JSON file |
| **Running** | Browser (Colab cloud) | Local computer OR Streamlit Cloud |
| **Sharing** | Colab link + Drive access | One Streamlit URL |
| **Updates** | Edit notebook, rerun cells | Edit file, redeploy |
| **Cost** | Free (Google) | Free (Streamlit Cloud) |

---

## 📱 Mobile Friendly?

Yes! The app works on phones and tablets. Open the Streamlit Cloud link on your phone's browser.

---

## 🛠️ Troubleshooting

### **"ModuleNotFoundError: No module named 'streamlit'"**
```bash
pip install -r requirements.txt
```

### **App not starting?**
```bash
# Make sure you're in the right folder
cd home-budget-tracker

# Check app.py name is correct
streamlit run app.py
```

### **Data not saving?**
- Make sure you click **"💾 Save & Refresh"**
- Check you have write permission in the folder

### **Petrol price not fetching?**
- Website may have changed structure
- Just enter the price manually (it changes every 15 days)

---

## 💡 Smart Usage Tips

1. **Lock fixed expenses:** School fees, salaries, subscriptions
2. **Update transport monthly:** As fuel prices change
3. **Track peaks:** Which months are expensive?
4. **Export data:** Download `budget_data.json` for records
5. **Share with father:** Show him the split breakdown

---

## 🎓 Learning Value

Building this tracker teaches:
- ✅ **Expense classification** (grouping by type)
- ✅ **Variable vs. fixed costs** (locked amounts)
- ✅ **Quantity-based math** (price × quantity)
- ✅ **Data persistence** (saving to files)
- ✅ **Web app building** (Streamlit basics)

This is **real accounting logic** used in business budgets and CA exams.

---

## 📄 License

Free to use, modify, and share.

---

## 👤 Created By

**Jazib Ali** | CA Student, Pakistan  
Building tools to simplify finance & accounting.

---

**Questions?** Check the code comments or reach out!
