 # 📍 GrowthMap Romania

An interactive data exploration project for analyzing **Romanian Consistent High-Growth Firms (HGFs)** using structured company data and geographic information.

This project combines company-level business data with regional map data to support analysis, visualization, and insight generation.

---

## 🚀 Features

### 📊 Company Data Analysis
- Explore Romanian high-growth firms using structured company data
- Analyze business descriptions and firm-level attributes
- Support company-level research and comparison

### 🗺️ Geographic Visualization
- Uses regional GeoJSON data for map-based analysis
- Enables location-aware exploration of firms across Romanian regions
- Useful for regional business and market insights

### 🧠 Insight Generation
- Combines firm data with regional structure
- Supports exploratory analytics and business intelligence workflows

---

## 🗂️ Project Structure, Installation, Usage, Dataset, and Tech Stack

```bash
dde_project/
├── vibe_coding.py
├── romania_hgfs.xlsx
├── NUTS_RG_20M_2021_4326_LEVL_2.geojson
├── requirements.txt
└── README.md
```

## 🗂️ Installation, Usage, Dataset, and Tech Stack

### Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/tanu091299/dde_project.git
cd dde_project
pip install -r requirements.txt
```

### Usage

Run the main application:
```
python vibe_coding.py
```

Dataset

The project uses:

romania_hgfs.xlsx for company-level data on Romanian high-growth firms
NUTS_RG_20M_2021_4326_LEVL_2.geojson for regional geographic boundary data

Together, these files support both business analysis and map-based exploration.

Tech Stack
Python
Pandas
GeoJSON / geospatial data
Excel dataset
Data analytics and visualization workflow

💡 Use Cases
Regional market research
High-growth firm analysis
Geographic business intelligence
Startup ecosystem exploration
Interactive company and region-based data analysis

🔮 Future Improvements
Add interactive dashboard support
Improve regional filtering and drill-down analysis
Add richer company comparison features
Integrate advanced visualization layers
Deploy as a web application
