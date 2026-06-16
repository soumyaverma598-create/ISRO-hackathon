# Quick Reference Card

## 🚀 ONE-LINE START
```bash
pip install -r requirements.txt && streamlit run app.py
```

## 📊 PAGES & FEATURES

| Page | Purpose | Key Metrics |
|------|---------|------------|
| **Dashboard** | Real-time monitoring | Flux, Counts, Risk, Probability, Class |
| **Forecast** | Multi-horizon predictions | 15min/1hr/6hr horizons, Risk levels |
| **Explainability** | AI interpretability | Feature importance, Confidence |
| **Alerts** | Warning system | Alert levels, Severity, Actions |
| **Analytics** | Historical analysis | 30-day trends, Statistics, Correlations |

## 🤖 PREDICTION MODEL

**Weighted Ensemble:**
- Soft X-ray (35%) - Corona heating indicator
- Hard X-ray (35%) - Particle acceleration detector
- Trends (20%) - Rate of change detection
- Volatility (10%) - Magnetic destabilization

## 🎨 ALERT LEVELS

| Level | Color | Threshold | Action |
|-------|-------|-----------|--------|
| CRITICAL | 🔴 RED | Prob > 75% | Emergency |
| WARNING | 🟠 ORANGE | Prob 50-75% | High alert |
| ADVISORY | 🟡 YELLOW | Prob 25-50% | Ready |
| NORMAL | 🟢 GREEN | Prob < 25% | Monitor |

## 📈 FLARE CLASSIFICATION (GOES Scale)

| Class | Soft X-ray | Description |
|-------|-----------|-------------|
| A | < 1e-7 | Sub-flare |
| B | 1e-7 to 1e-6 | Small |
| C | 1e-6 to 1e-5 | Medium |
| M | 1e-5 to 1e-4 | Major |
| X | > 1e-4 | Extreme |

## 🔧 CUSTOMIZATION FILES

- **Data**: `utils/data_generator.py`
- **AI Engine**: `utils/prediction_engine.py`
- **Visualizations**: `utils/visualizations.py`
- **Theme**: `.streamlit/config.toml`

## 🌐 DATA COLUMNS

```python
DataFrame columns: [
    'timestamp',           # datetime
    'soft_xray_flux',     # W/m²
    'hard_xray_counts',   # counts/sec
]
```

## 📊 KEY FEATURES EXPLAINED

**SoLEXS (Soft X-ray)**
- Range: 1-12 Angstroms
- Baseline: 1-2 W/m²
- Flare peaks: 5-10+ W/m²
- Indicates: Corona heating

**HELIOS (Hard X-ray)**
- Range: 4-25 keV
- Baseline: 50-100 counts/sec
- Flare peaks: 200-500+ counts/sec
- Indicates: Particle acceleration

## 🎯 QUICK TASKS

**Want to...** | **Do this...**
---|---
See live data | → Go to Dashboard
Get predictions | → Go to Forecast Center
Understand AI | → Go to Explainability
Check warnings | → Go to Alert Center
Analyze trends | → Go to Analytics
Learn system | → Read README.md

## 📱 BROWSER OPTIMIZATION

- **Best**: Chrome, Firefox (latest)
- **Screen**: 1920x1080+ recommended
- **Resolution**: Optimized for 16:9
- **JavaScript**: Must be enabled

## 💾 FILE STRUCTURE

```
solar-sentinel-ai/
├── app.py (main)
├── pages/ (5 Streamlit pages)
├── utils/ (data, AI, viz)
├── .streamlit/config.toml
├── requirements.txt
├── README.md (full docs)
├── GETTING_STARTED.md
└── QUICK_REFERENCE.md (this file)
```

## ⚙️ SYSTEM REQUIREMENTS

- Python 3.8+
- RAM: 512MB minimum (1GB recommended)
- Disk: 500MB
- Network: For Streamlit cloud deployment
- Browser: Modern (Chrome/Firefox/Safari)

## 🔄 REAL DATA INTEGRATION CHECKLIST

- [ ] Replace `SolarDataGenerator` class
- [ ] Update `make_prediction()` function
- [ ] Maintain DataFrame column names
- [ ] Test on Dashboard first
- [ ] Verify Forecast Center works
- [ ] Check Alert Center thresholds
- [ ] Validate Analytics calculations

## 🐛 TROUBLESHOOTING QUICK FIXES

```bash
# Port conflict
streamlit run app.py --server.port 8502

# Module errors
pip install --upgrade -r requirements.txt

# Cache issues
rm -rf ~/.streamlit/cache

# Force refresh
Ctrl+R (in browser)
```

## 📞 RESOURCES

- **Main Docs**: README.md
- **Setup Guide**: GETTING_STARTED.md
- **Streamlit Docs**: https://docs.streamlit.io
- **Plotly Docs**: https://plotly.com/python
- **GitHub**: [Repository URL]

## ⭐ MUST KNOW

1. **Entry Point**: `streamlit run app.py`
2. **Port**: http://localhost:8501
3. **Pages**: Automatically loaded from `/pages` folder
4. **Config**: `.streamlit/config.toml`
5. **Data**: Real-time simulated, ready for real data
6. **Mock AI**: Weighted ensemble (no ML training needed)

---

**Solar Sentinel AI v1.0** | ISRO Hackathon | Production-Ready

🌞 Questions? See README.md | 🚀 Ready to deploy? Follow GETTING_STARTED.md
