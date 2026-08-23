"""Streamlit metric ↔ imperial unit converter."""

import streamlit as st

from converter import (
    CATEGORY_LABELS,
    UNIT_LABELS,
    convert,
    convert_to_system,
    units_for,
)

st.set_page_config(page_title="Metric ↔ Imperial Converter", layout="centered")
st.title("Metric ↔ Imperial converter")
st.caption("Length, mass, area, volume, speed, and temperature. Volume has UK imperial and US customary.")

category_keys = list(CATEGORY_LABELS.keys())
category = st.selectbox(
    "Quantity",
    category_keys,
    format_func=lambda key: CATEGORY_LABELS[key],
)

direction = st.radio(
    "Direction",
    ["metric_to_imperial", "imperial_to_metric"],
    format_func=lambda d: (
        "Metric → Imperial" if d == "metric_to_imperial" else "Imperial → Metric"
    ),
    horizontal=True,
)

from_system = "metric" if direction == "metric_to_imperial" else "imperial"
to_system = "imperial" if direction == "metric_to_imperial" else "metric"

from_units = units_for(category, from_system)
to_units = units_for(category, to_system)

col_from, col_to = st.columns(2)
with col_from:
    from_unit = st.selectbox(
        "From",
        from_units,
        format_func=lambda u: UNIT_LABELS[u],
    )
with col_to:
    to_unit = st.selectbox(
        "To",
        to_units,
        format_func=lambda u: UNIT_LABELS[u],
    )

value = st.number_input("Value", value=1.0, format="%.6f")

primary = convert(value, from_unit, to_unit, category)
st.metric(
    label=UNIT_LABELS[to_unit],
    value=f"{primary.value:,.6g}",
)

st.subheader("All units in the target system")
rows = convert_to_system(value, from_unit, category, to_system)
st.dataframe(
    {
        "Unit": [UNIT_LABELS[row.to_unit] for row in rows],
        "Value": [row.value for row in rows],
    },
    hide_index=True,
    use_container_width=True,
)
