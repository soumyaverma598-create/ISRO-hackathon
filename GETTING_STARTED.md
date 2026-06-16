# Solar Sentinel AI - Getting Started Guide

This file provides quick instructions to get the application running.

## 🚀 Installation & Setup

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
streamlit run app.py
```

### Step 3: Open in Browser
- Automatically opens at http://localhost:8501
- Or manually navigate to that URL

## 📊 First Time Users

1. **Start on Home Page** - Overview of all features
2. **Visit Dashboard** - See live simulated data
3. **Check Forecast** - View multi-horizon predictions
4. **Explore Explainability** - Understand AI decisions
5. **Review Alerts** - See alert system in action
6. **Analyze Trends** - Review 30-day historical data

## 🎮 Interactive Features

- **Clickable Buttons**: Navigate between pages using quick-start buttons
- **Expandable Sections**: Click expanders for detailed information
- **Interactive Charts**: Hover over plots for data values, zoom/pan with Plotly tools
- **Data Tables**: Sort and filter tables by clicking column headers
- **Dropdowns**: Select different timeframes and metrics

## 💡 Key Areas to Explore

### Dashboard
- Current solar activity metrics
- Live data streams from SoLEXS and HELIOS
- Real-time flare probability

### Forecast Center
- Compare predictions at different time horizons
- Understand risk assessment
- Get operational recommendations

### Explainability
- See how AI makes predictions
- Feature importance breakdown
- Model confidence scoring

### Alert Center
- Active alerts and their severity
- Alert thresholds and configuration
- Recommended actions for each alert level

### Analytics
- 30-day historical trends
- Statistical analysis
- Distribution and correlation patterns

## 🔧 Customization Tips

1. **Change Data Generation**: Edit `utils/data_generator.py`
   - Adjust flux ranges
   - Modify flare frequency
   - Change noise levels

2. **Tune Predictions**: Edit `utils/prediction_engine.py`
   - Modify feature weights
   - Adjust risk thresholds
   - Change alert triggers

3. **Update Theme**: Edit `.streamlit/config.toml`
   - Change colors
   - Modify fonts
   - Adjust layout

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| Port 8501 already in use | `streamlit run app.py --server.port 8502` |
| Module not found errors | `pip install --upgrade -r requirements.txt` |
| Slow performance | Close other applications, restart Streamlit |
| Charts not displaying | Clear browser cache, try different browser |

## 📚 File Structure Quick Reference

```
app.py                    ← Main entry point (run this!)
utils/
  ├── data_generator.py   ← Data simulation
  ├── prediction_engine.py ← AI predictions
  └── visualizations.py   ← Chart utilities
pages/
  ├── 1_Dashboard.py      ← Live monitoring
  ├── 2_Forecast.py       ← Predictions
  ├── 3_Explainability.py ← AI insights
  ├── 4_Alerts.py         ← Warnings
  └── 5_Analytics.py      ← Historical analysis
```

## ⚡ Advanced Usage

### Increase Data Update Frequency
Edit any page file and change:
```python
st.set_page_config(..., initial_sidebar_state="expanded")
```

### Modify Simulated Data Characteristics
In `utils/data_generator.py`:
```python
# More realistic: increase event frequency
num_events = np.random.randint(5, 10)

# Larger peaks: increase magnitude
event_magnitude = np.random.uniform(5, 15)
```

### Add Custom Metrics
In dashboard pages, add new KPI cards:
```python
st.metric("Custom Metric", value)
```

## 🎯 Integration for Real Data

When connecting to real Aditya-L1 data:

1. **Replace data_generator.py**:
   - Keep same DataFrame format
   - Maintain column names: 'timestamp', 'soft_xray_flux', 'hard_xray_counts'

2. **Update prediction_engine.py**:
   - Replace with trained model
   - Maintain same output dictionary structure
   - Keep feature names consistent

3. **No other code changes needed!**
   - All visualizations work automatically
   - All pages update seamlessly
   - Alerts recalibrate automatically

## 📞 Need Help?

- Check README.md for detailed documentation
- Review in-app help tabs on each page
- Examine docstrings in Python files
- Check Streamlit documentation: https://docs.streamlit.io

---

**Happy exploring! 🌞**

For questions or updates, see the main README.md file.
