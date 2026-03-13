# Flickr Geodata Analytics Dashboard

An interactive data analytics dashboard built with Python Dash and Plotly, analyzing crowdsourced map georeferencing data from the British Library's Flickr collection.

## Overview

This project performs end-to-end data analysis on 3,000+ georeferenced historical maps, covering data cleaning, statistical analysis, machine learning, and interactive visualization. The dashboard provides actionable insights into data quality, temporal trends, and geographic distribution of annotations.

## Dashboard Features

| Visualization | Method | Insight |
|---|---|---|
| Accuracy Distribution | Group Query + Bar Chart | Quality tier breakdown of georeferencing precision |
| Quality Proportions | Data Transformation + Pie Chart | 90%+ of data falls in Excellent/Good categories |
| Monthly Trends & Forecast | ARIMA Time Series | Historical activity + 2-month forecast |
| Geographic Hotspots | K-Means Clustering + Map | Spatial bias toward Western cultural capitals |

## Tech Stack

- **Dashboard**: Python Dash, Plotly Express, Plotly Graph Objects
- **Data Processing**: Pandas, NumPy, Regex, Unicodedata
- **Machine Learning**: Scikit-learn (K-Means), Statsmodels (ARIMA)
- **Geospatial**: Coordinate parsing, WKT polygon conversion, scatter map

## Project Structure

```
├── Project_4.ipynb                        # Main notebook (cleaning + analysis + dashboard)
├── flickr_geodata.csv                     # Raw dataset (3,137 records, 17 columns)
├── flickr_geodata_final.csv               # Cleaned dataset (3,031 records, 22 columns)
├── 1_group_query_top10_collections.csv    # Indicator 1: Accuracy tier counts
├── 2_transformation_rms_quality.csv       # Indicator 2: Quality distribution
├── 3_temporal_monthly_trends.csv          # Indicator 3: Monthly trends + ARIMA forecast
├── 4_spatial_clustering_points.csv        # Indicator 4: Clustered spatial points
├── 4_spatial_clustering_centroids.csv     # Indicator 4: K-Means cluster centroids
├── indicator_descriptions.txt            # Markdown-ready indicator descriptions
└── validation_plots.png                   # Static validation plots
```

## How to Run

### 1. Install dependencies
```bash
pip install dash plotly pandas numpy scikit-learn statsmodels
```

### 2. Run the notebook
Open `Project_4.ipynb` in Jupyter and run all cells. The Dash app will launch at:
```
http://127.0.0.1:8050/
```

## Data Pipeline

```
Raw Data (flickr_geodata.csv)
    ↓ Data Cleaning (null removal, coordinate parsing, text normalization)
Cleaned Data (flickr_geodata_final.csv)
    ↓ Analysis (group query, transformation, ARIMA, K-Means)
5 Indicator CSVs
    ↓ Visualization (Dash + Plotly)
Interactive Dashboard
```

## Key Findings

- **Data Quality**: Over 90% of georeferenced maps achieve Excellent or Good accuracy (RMS error < 1.0)
- **Temporal Pattern**: Peak annotation activity occurred in August 2014; ARIMA forecasts a low-activity period ahead
- **Geographic Bias**: K-Means clustering reveals a strong concentration of annotations around Western European cities, particularly London — consistent with the British Library's collection origins
- **External Validation**: Cluster centroids align closely with major cultural capitals (London, Paris, New York, Rome, Berlin), confirming the spatial bias hypothesis

## Team

| Member | Role |
|---|---|
| Yuchun Wang | Visualization & Dashboard |
| Elise Fouillet | Data Cleaning |
| Jinxin Zhou | Algorithm Analysis |

## Dashboard Preview

![Validation Plots](validation_plots.png)
