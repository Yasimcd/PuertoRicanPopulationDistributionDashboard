import pandas as pd
import plotly.express as px
import numpy as np
import streamlit as st

st.set_page_config(page_title="Puerto Rican Population Dashboard", layout="wide")

st.title("🇵🇷 Puerto Rican Population Distribution Dashboard")

# Load data
df = pd.read_csv("puerto_rican_population.csv")

df = df.set_index("Label (Grouping)").T
df.columns = df.columns.astype(str).str.strip()

df = df.reset_index().rename(columns={"index": "State"})
df["State"] = df["State"].astype(str).str.strip()
df = df[~df["State"].str.contains("Margin of Error", na=False)]

df = df[["State", "Puerto Rican"]].rename(columns={"Puerto Rican": "Population"})
df["Population"] = pd.to_numeric(df["Population"].astype(str).str.replace(",", ""), errors="coerce")
df["State"] = df["State"].str.replace("!!Estimate", "", regex=False).str.strip()

# Mapping
us_state_abbrev = {
    "Florida": "FL", "New York": "NY", "Pennsylvania": "PA", "California": "CA",
    "Texas": "TX", "New Jersey": "NJ", "Massachusetts": "MA", "Connecticut": "CT"
}

df["State_Full"] = df["State"]
df["State"] = df["State"].map(us_state_abbrev)

df = df.dropna()
df["log_pop"] = np.log10(df["Population"])

# Metrics
total = int(df["Population"].sum())
top_state = df.sort_values("Population", ascending=False).iloc[0]

col1, col2 = st.columns(2)
col1.metric("Total Population", f"{total:,}")
col2.metric("Top State", f"{top_state['State_Full']} ({int(top_state['Population']):,})")

# Map
fig = px.choropleth(
    df,
    locations="State",
    locationmode="USA-states",
    color="log_pop",
    scope="usa",
    hover_name="State_Full",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig, use_container_width=True)

# Bar chart
top10 = df.sort_values("Population", ascending=False).head(10)

fig_bar = px.bar(
    top10,
    x="Population",
    y="State_Full",
    orientation="h",
    color="Population",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig_bar, use_container_width=True)