import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


def load_data():
    try:
        data = {
            "group": pd.read_csv("1_group_query_top10_collections.csv"),
            "transform": pd.read_csv("2_transformation_rms_quality.csv"),
            "temporal": pd.read_csv("3_temporal_monthly_trends.csv"),
            "spatial_points": pd.read_csv("4_spatial_clustering_points.csv"),
            "spatial_centroids": pd.read_csv("4_spatial_clustering_centroids.csv")
        }
        return data
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        return None


def create_quality_bar_chart(df):
    fig = px.bar(
        df,
        x='rms_error_quality',
        y='annotation_count',
        title='Distribution of Georeferencing Accuracy',
        labels={'rms_error_quality': 'Accuracy Tier', 'annotation_count': 'Number of Maps'},
        color='rms_error_quality',
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig.update_layout(showlegend=False)
    return fig


def create_quality_pie_chart(df):
    fig = px.pie(
        df,
        names='rms_error_quality',
        values='count',
        title='Proportion of Accuracy Categories',
        hole=0.4
    )
    fig.update_traces(textinfo='percent+label')
    return fig


def create_temporal_line_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['year_month'],
        y=df['annotation_count'],
        mode='lines+markers',
        name='Historical Data',
        line=dict(color='blue')
    ))
    forecast_data = df.dropna(subset=['forecasted_annotations'])
    if not forecast_data.empty:
        fig.add_trace(go.Scatter(
            x=forecast_data['year_month'],
            y=forecast_data['forecasted_annotations'],
            mode='lines+markers',
            name='Forecast (ARIMA)',
            line=dict(color='red', dash='dash')
        ))
    fig.update_layout(
        title='Monthly Annotation Trends & Short-term Forecast',
        xaxis_title='Month',
        yaxis_title='Number of Annotations',
        hovermode="x unified"
    )
    return fig


def create_spatial_map(points_df, centroids_df):
    fig = px.scatter_map(
        points_df,
        lat="center_latitude",
        lon="center_longitude",
        color="cluster_label",
        size_max=10,
        zoom=1,
        opacity=0.5,
        title="Geographic Hotspots vs. Major Cultural Capitals (External Data)"
    )
    fig.add_trace(go.Scattermap(
        lat=centroids_df['centroid_latitude'],
        lon=centroids_df['centroid_longitude'],
        mode='markers',
        marker=go.scattermap.Marker(size=18, color='red', symbol='circle'),
        text=centroids_df['cluster_name'],
        name='Cluster Centers (Analysis)'
    ))
    external_data = pd.DataFrame({
        'City': ['London (British Library)', 'Paris', 'New York', 'Rome', 'Berlin'],
        'lat': [51.5074, 48.8566, 40.7128, 41.9028, 52.5200],
        'lon': [-0.1278, 2.3522, -74.0060, 12.4964, 13.4050]
    })
    fig.add_trace(go.Scattermap(
        lat=external_data['lat'],
        lon=external_data['lon'],
        mode='markers+text',
        marker=go.scattermap.Marker(size=12, color='black', symbol='star'),
        text=external_data['City'],
        textposition="top right",
        name='External Data: Major Cities'
    ))
    fig.update_layout(map_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
    return fig


# --- App initialization (module-level, required for gunicorn) ---
data = load_data()

app = dash.Dash(__name__)
server = app.server  # gunicorn entry point

desc_group = """
#### 1. A Health Check on Data Accuracy: Georeferencing Precision
We began by assessing the overall accuracy of the dataset using a **Group Query**. We categorized the RMS error (a metric for map alignment precision) into four distinct tiers.

**Key Insight**:
As the bar chart clearly illustrates, **maps in the "Excellent" tier (RMS ≤ 0.5) dominate the dataset**, accounting for over 2,600 entries. This indicates that the crowdsourced data from the British Library is of exceptionally high quality.
"""

desc_transform = """
#### 2. Overview of Data Usability: Quality Distribution
To visualize the "purity" of the dataset, we applied **Data Transformation** techniques to convert continuous error values into a percentage-based pie chart.

**Key Insight**:
The chart reveals that **over 90% of the data falls within the "Excellent" or "Good" categories**. This suggests that future users can confidently utilize the bulk of this dataset.
"""

desc_temporal = """
#### 3. Activity Review & Forecast: Temporal Analysis
We tracked the monthly volume of annotations (blue line) throughout 2014 and used an **ARIMA Model** to forecast trends for the upcoming two months (red dashed line).

**Key Insight**:
The data highlights **August 2014** as a breakout month with peak user activity, followed by a gradual cooling off. Our model predicts that activity will likely **remain at a relatively low level** for February and March 2015.
"""

desc_spatial = """
#### 4. Uncovering Geographical Bias: Hotspots & External Validation
This map performs a comparative validation:
1. **Red Dots**: High-density data centers identified by our **K-Means Clustering** algorithm.
2. **Black Stars**: [External Data] Coordinates of major global cultural capitals.

**Key Insight**:
There is a **striking alignment** between our calculated hotspots and major Western cities, confirming a clear geographical bias in the digitized collection.
"""

app.layout = html.Div(
    style={'fontFamily': 'Arial, sans-serif', 'padding': '20px', 'backgroundColor': '#f4f4f4'},
    children=[
        html.H1("Project 4: Programming in Data Science Dashboard",
                style={'textAlign': 'center', 'color': '#2c3e50'}),

        html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px',
                        'marginBottom': '30px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}, children=[
            html.H4("Project Metadata", style={'marginTop': '0', 'color': '#34495e'}),
            html.P([html.Strong("Group Members: "),
                    "Elise Fouillet (Cleaning), Jinxin zhou (Analysis), Yuchun wang (Visualization)"]),
            html.P([html.Strong("Dataset Name: "), "Flickr Geodata (British Library)"]),
            html.P([html.Strong("Project Goal: "),
                    "To analyze the quality, temporal trends, and spatial distribution of crowdsourced map georeferencing data."])
        ]),

        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between'}, children=[
            html.Div(style={'width': '48%', 'backgroundColor': 'white', 'padding': '15px',
                            'borderRadius': '8px', 'marginBottom': '20px',
                            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}, children=[
                html.H3("1. Accuracy Count (Group Query)", style={'fontSize': '18px'}),
                dcc.Graph(figure=create_quality_bar_chart(data['group']), style={'height': '400px'}),
                dcc.Markdown(desc_group, style={'backgroundColor': '#f8f9fa', 'padding': '10px',
                                                'fontSize': '14px', 'marginTop': '10px'})
            ]),
            html.Div(style={'width': '48%', 'backgroundColor': 'white', 'padding': '15px',
                            'borderRadius': '8px', 'marginBottom': '20px',
                            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}, children=[
                html.H3("2. Quality Distribution (Transformation)", style={'fontSize': '18px'}),
                dcc.Graph(figure=create_quality_pie_chart(data['transform']), style={'height': '400px'}),
                dcc.Markdown(desc_transform, style={'backgroundColor': '#f8f9fa', 'padding': '10px',
                                                    'fontSize': '14px', 'marginTop': '10px'})
            ])
        ]),

        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between'}, children=[
            html.Div(style={'width': '48%', 'backgroundColor': 'white', 'padding': '15px',
                            'borderRadius': '8px', 'marginBottom': '20px',
                            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}, children=[
                html.H3("3. Monthly Activity & Forecast (Temporal)", style={'fontSize': '18px'}),
                dcc.Graph(figure=create_temporal_line_chart(data['temporal']), style={'height': '400px'}),
                dcc.Markdown(desc_temporal, style={'backgroundColor': '#f8f9fa', 'padding': '10px',
                                                   'fontSize': '14px', 'marginTop': '10px'})
            ]),
            html.Div(style={'width': '48%', 'backgroundColor': 'white', 'padding': '15px',
                            'borderRadius': '8px', 'marginBottom': '20px',
                            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}, children=[
                html.H3("4. Geographic Hotspots (Spatial Clustering)", style={'fontSize': '18px'}),
                dcc.Graph(figure=create_spatial_map(data['spatial_points'], data['spatial_centroids']),
                          style={'height': '400px'}),
                dcc.Markdown(desc_spatial, style={'backgroundColor': '#f8f9fa', 'padding': '10px',
                                                  'fontSize': '14px', 'marginTop': '10px'})
            ])
        ])
    ]
)

if __name__ == '__main__':
    app.run(debug=False)
