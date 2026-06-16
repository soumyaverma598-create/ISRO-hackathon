# 🚀 SOLAR SENTINEL AI - COMPLETE STARTUP GUIDE

## 📋 Table of Contents
1. [Quick Start (30 seconds)](#quick-start)
2. [Detailed Installation](#detailed-installation)
3. [Running the Application](#running-the-application)
4. [Accessing the Platform](#accessing-the-platform)
5. [Troubleshooting](#troubleshooting)
6. [Project Structure](#project-structure)
7. [Features Overview](#features-overview)

---

## ⚡ Quick Start (30 seconds)

### For Windows:
```bash
# Option 1: Run setup script
setup.bat

# Option 2: Manual installation
pip install -r requirements.txt
streamlit run app.py
```

### For macOS/Linux:
```bash
# Option 1: Run setup script
bash setup.sh

# Option 2: Manual installation
pip install -r requirements.txt
streamlit run app.py
```

**That's it! The app will open automatically at http://localhost:8501**

---

## 📦 Detailed Installation

### Step 1: Prerequisites Check
```bash
# Check Python version (must be 3.8+)
python --version

# Or on macOS/Linux:
python3 --version
```

If Python is not installed, download from https://www.python.org/

### Step 2: Download Project
- Download the solar-sentinel-ai folder to your local machine
- Or clone from repository if using Git

### Step 3: Navigate to Project
```bash
cd solar-sentinel-ai
```

### Step 4: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 5: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Expected output:
```
Successfully installed streamlit-1.36.0 pandas-2.1.3 numpy-1.24.3 plotly-5.18.0 ...
```

### Step 6: Verify Installation
```bash
# Test imports
python -c "import streamlit; import pandas; import plotly; print('✓ All packages installed!')"
```

---

## ▶️ Running the Application

### Method 1: Direct Streamlit Command (Recommended)
```bash
streamlit run app.py
```

### Method 2: Python Script
```bash
python run.py
```

### Method 3: Batch/Shell Script
```bash
# Windows
setup.bat

# macOS/Linux
bash setup.sh
```

### Expected Output:
```
  You can now view your Streamlit app in your browser.
  
  URL: http://localhost:8501
  
  Press CTRL+C to quit
```

---

## 🌐 Accessing the Platform

### Automatic Opening
- Application automatically opens in your default browser
- If not, manually open: **http://localhost:8501**

### Navigation
1. **Home Page** - Start here for overview
2. **Dashboard** - Real-time solar monitoring
3. **Forecast Center** - Multi-horizon predictions
4. **Explainability** - AI model insights
5. **Alert Center** - Warning system
6. **Analytics** - Historical analysis

### Sidebar Features
- Quick navigation menu
- System status indicators
- Quick stats display
- Last update timestamp

---

## 🔧 Customization Before Running

### 1. Adjust Data Generation Parameters
Edit `utils/data_generator.py`:
```python
# Line ~25: Change base flux range
base_flux = np.ones(n_points) * np.random.uniform(1.0, 2.0)  # Default
# Change to:
base_flux = np.ones(n_points) * np.random.uniform(2.0, 4.0)  # Higher activity

# Line ~35: Change number of flare events
num_events = np.random.randint(2, 5)  # Default (2-5 per day)
# Change to:
num_events = np.random.randint(5, 10)  # More events
```

### 2. Tune Prediction Thresholds
Edit `utils/prediction_engine.py`:
```python
# Line ~120: Adjust prediction sensitivity
probability = probability * horizon_factor
# Add or remove multiplier to change sensitivity
```

### 3. Customize Theme Colors
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#00FF00"      # Change to your color
backgroundColor = "#0a0e27"   # Change to your color
```

### 4. Modify Alert Thresholds
Edit `pages/4_Alerts.py`:
```python
# Line ~25: Change alert thresholds
if prediction_15['risk_level'] == 'CRITICAL':
    # Modify this logic as needed
```

---

## 🐛 Troubleshooting

### Problem: "Module not found" Error
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution:**
```bash
# Reinstall all dependencies
pip install --upgrade -r requirements.txt

# Or specific package
pip install streamlit==1.36.0
```

### Problem: Port 8501 Already in Use
```
ERROR: Address already in use
```
**Solution:**
```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill the process using port 8501
# Windows: netstat -ano | findstr :8501
# macOS/Linux: lsof -i :8501 | kill -9 PID
```

### Problem: Python Not Found
```
'python' is not recognized as an internal or external command
```
**Solution:**
- Reinstall Python and check "Add Python to PATH"
- Use full path: C:\Python39\python.exe app.py
- Or use python3 on macOS/Linux

### Problem: Streamlit Won't Start
```
Command 'streamlit' not found
```
**Solution:**
```bash
# Use Python module syntax
python -m streamlit run app.py

# Or on macOS/Linux
python3 -m streamlit run app.py
```

### Problem: Slow Performance
**Solutions:**
1. Close other applications
2. Increase system RAM
3. Restart Streamlit server
4. Use faster internet connection

### Problem: Plots Not Displaying
**Solutions:**
1. Clear browser cache (Ctrl+Shift+Delete)
2. Try different browser
3. Enable JavaScript
4. Restart Streamlit

### Problem: Data Not Updating
**Solution:**
- Refresh browser (F5 or Ctrl+R)
- Auto-refresh should happen every 60 seconds
- Check browser console for errors (F12)

---

## 📁 Project Structure

```
solar-sentinel-ai/
│
├── 📄 app.py                          ← Main entry point - START HERE
│
├── 📁 pages/                          ← Streamlit page components
│   ├── 1_Dashboard.py                 ← Live monitoring (Real-time data)
│   ├── 2_Forecast.py                  ← Multi-horizon predictions
│   ├── 3_Explainability.py            ← AI model interpretability
│   ├── 4_Alerts.py                    ← Alert management
│   └── 5_Analytics.py                 ← Historical analysis
│
├── 📁 utils/                          ← Core utilities
│   ├── __init__.py                    ← Package initialization
│   ├── data_generator.py              ← SoLEXS/HELIOS data simulator
│   ├── prediction_engine.py           ← Mock AI prediction engine
│   └── visualizations.py              ← Plotly chart functions
│
├── 📁 .streamlit/                     ← Streamlit configuration
│   └── config.toml                    ← Theme and UI settings
│
├── 📁 assets/                         ← Images and resources
│
├── 📄 requirements.txt                ← Python dependencies
├── 📄 README.md                       ← Full documentation
├── 📄 GETTING_STARTED.md              ← Setup instructions
├── 📄 QUICK_REFERENCE.md              ← Cheat sheet
├── 📄 STARTUP_GUIDE.md                ← This file
│
├── 🔧 setup.bat                       ← Windows setup script
├── 🔧 setup.sh                        ← macOS/Linux setup script
├── 🔧 run.py                          ← Python startup script
│
├── 📋 .env.example                    ← Configuration template
├── 🚫 .gitignore                      ← Git ignore rules

```

---

## ✨ Features Overview

### 📊 Dashboard
- **Real-time KPIs**: Flux, Counts, Risk, Probability, Class
- **Live Streams**: SoLEXS and HELIOS time-series charts
- **Combined Analysis**: Dual-axis correlation visualization
- **Auto-refresh**: Every 60 seconds
- **Confidence Metrics**: Model reliability scoring

### 🔮 Forecast Center
- **15-Minute Nowcast**: Immediate threat detection
- **1-Hour Tactical**: Short-term planning
- **6-Hour Strategic**: Contingency preparation
- **Risk Comparison**: Probability matrices
- **Recommendations**: Automated action guidance

### 🧠 Explainability
- **SHAP-Style Analysis**: Feature importance visualization
- **SoLEXS Breakdown**: Soft X-ray feature analysis
- **HELIOS Breakdown**: Hard X-ray feature analysis
- **Derived Metrics**: Ratio and index calculations
- **Model Logic**: Decision-making explanation
- **Confidence Interpretation**: Uncertainty quantification

### 🚨 Alerts
- **Multi-Level System**: GREEN/YELLOW/ORANGE/RED
- **Active Alerts**: Real-time warning display
- **Alert History**: Timestamped log
- **Threshold Configuration**: Customizable limits
- **Operational Guidance**: Action recommendations

### 📈 Analytics
- **30-Day Statistics**: Comprehensive metrics
- **Historical Trends**: Time-series visualization
- **Distribution Analysis**: Histogram and density plots
- **Correlation Study**: Feature relationship analysis
- **Activity Heatmap**: Daily patterns over 7 days
- **Risk Distribution**: Historical alert statistics

---

## 💡 Tips for Best Experience

### Performance
- Run on modern browser (Chrome/Firefox/Safari)
- Use 1920x1080 or higher resolution
- Maintain 1GB+ available RAM
- Stable internet connection

### Navigation
- Use sidebar for quick navigation
- Bookmark frequently visited pages
- Use browser back/forward buttons
- Refresh page if charts don't appear

### Data Understanding
- Dashboard shows latest 1 hour of data
- Forecast Center updates every prediction
- Analytics shows 30 days of history
- Refresh rate: 1 minute auto-update

---

## 🎯 What to Explore First

1. **Home Page (app.py)**
   - Read overview
   - Understand features
   - Check technology stack

2. **Dashboard Page**
   - See real-time data
   - Check current risk level
   - View live charts

3. **Forecast Center**
   - Compare predictions
   - Review risk assessment
   - Understand horizons

4. **Explainability**
   - Learn AI features
   - Check confidence
   - Review logic

5. **Alert Center**
   - See current alerts
   - Review thresholds
   - Understand actions

6. **Analytics**
   - Review trends
   - Check statistics
   - Analyze patterns

---

## 🚀 Next Steps

### For Testing
1. ✓ Install dependencies
2. ✓ Run application
3. ✓ Explore all pages
4. ✓ Test alert triggers
5. ✓ Verify data generation

### For Integration
1. Prepare real data source
2. Create data connector module
3. Replace SolarDataGenerator
4. Test with real data
5. Recalibrate thresholds

### For Deployment
1. Set up CI/CD pipeline
2. Configure Streamlit cloud
3. Set environment variables
4. Deploy application
5. Monitor performance

---

## 📞 Support Resources

- **README.md** - Comprehensive documentation
- **GETTING_STARTED.md** - Setup walkthrough
- **QUICK_REFERENCE.md** - Cheat sheet
- **In-app Help** - Documentation tabs on each page
- **Code Comments** - Detailed docstrings

---

## ✅ Verification Checklist

Before considering setup complete:

- [ ] Python 3.8+ installed and verified
- [ ] Virtual environment created (optional but recommended)
- [ ] All dependencies installed without errors
- [ ] Application starts without errors
- [ ] Browser opens automatically or manually
- [ ] Home page loads with no errors
- [ ] Navigation to all 5 pages works
- [ ] Live data displays in Dashboard
- [ ] Charts render without issues
- [ ] Alerts display correctly

---

## 🌟 You're All Set!

If all verification checks pass, you're ready to use Solar Sentinel AI!

**Start exploring:** http://localhost:8501

**Questions?** Check the README.md or review docstrings in the code.

**Found a bug?** Check troubleshooting section or review logs in browser console (F12).

---

**Solar Sentinel AI v1.0** | Production-Ready Prototype

🌞 Monitoring Solar Activity | 🛡️ Protecting Earth | 🚀 Powered by AI

*Built for ISRO Hackathon | Integration-Ready for Real Data*
