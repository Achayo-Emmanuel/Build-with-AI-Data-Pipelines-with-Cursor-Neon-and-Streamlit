"""Metric ↔ imperial (and US customary) unit conversion.

Length and mass use international yard/pound definitions (NIST).
Volume is split: UK imperial vs US customary, because they differ.
Temperature uses the linear Celsius–Fahrenheit relation.
"""

from __future__ import annotations

from dataclasses import dataclass

# Base unit per category. Factors are "how many base units in 1 of this unit".
CATEGORIES: dict[str, dict[str, float]] = {
    "length": {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1.0,
        "km": 1000.0,
        "in": 0.0254,
        "ft": 0.3048,
        "yd": 0.9144,
        "mi": 1609.344,
    },
    "mass": {
        "mg": 1e-6,
        "g": 0.001,
        "kg": 1.0,
        "t": 1000.0,
        "oz": 0.028349523125,
        "lb": 0.45359237,
        "st": 6.35029318,
    },
    "area": {
        "cm2": 1e-4,
        "m2": 1.0,
        "ha": 10_000.0,
        "km2": 1_000_000.0,
        "in2": 0.00064516,
        "ft2": 0.09290304,
        "yd2": 0.83612736,
        "acre": 4046.8564224,
        "mi2": 2_589_988.110336,
    },
    "volume_uk": {
        "ml": 0.001,
        "L": 1.0,
        "m3": 1000.0,
        "fl_oz_uk": 0.0284130625,
        "pt_uk": 0.56826125,
        "qt_uk": 1.1365225,
        "gal_uk": 4.54609,
    },
    "volume_us": {
        "ml": 0.001,
        "L": 1.0,
        "m3": 1000.0,
        "fl_oz_us": 0.0295735295625,
        "cup_us": 0.2365882365,
        "pt_us": 0.473176473,
        "qt_us": 0.946352946,
        "gal_us": 3.785411784,
    },
    "speed": {
        "m/s": 1.0,
        "km/h": 1 / 3.6,
        "ft/s": 0.3048,
        "mph": 0.44704,
        "kn": 0.514444,
    },
}

METRIC_UNITS: dict[str, set[str]] = {
    "length": {"mm", "cm", "m", "km"},
    "mass": {"mg", "g", "kg", "t"},
    "area": {"cm2", "m2", "ha", "km2"},
    "volume_uk": {"ml", "L", "m3"},
    "volume_us": {"ml", "L", "m3"},
    "speed": {"m/s", "km/h"},
    "temperature": {"C", "K"},
}

IMPERIAL_UNITS: dict[str, set[str]] = {
    "length": {"in", "ft", "yd", "mi"},
    "mass": {"oz", "lb", "st"},
    "area": {"in2", "ft2", "yd2", "acre", "mi2"},
    "volume_uk": {"fl_oz_uk", "pt_uk", "qt_uk", "gal_uk"},
    "volume_us": {"fl_oz_us", "cup_us", "pt_us", "qt_us", "gal_us"},
    "speed": {"ft/s", "mph", "kn"},
    "temperature": {"F"},
}

UNIT_LABELS: dict[str, str] = {
    "mm": "millimetre (mm)",
    "cm": "centimetre (cm)",
    "m": "metre (m)",
    "km": "kilometre (km)",
    "in": "inch (in)",
    "ft": "foot (ft)",
    "yd": "yard (yd)",
    "mi": "mile (mi)",
    "mg": "milligram (mg)",
    "g": "gram (g)",
    "kg": "kilogram (kg)",
    "t": "tonne (t)",
    "oz": "ounce (oz)",
    "lb": "pound (lb)",
    "st": "stone (st)",
    "cm2": "square centimetre (cm²)",
    "m2": "square metre (m²)",
    "ha": "hectare (ha)",
    "km2": "square kilometre (km²)",
    "in2": "square inch (in²)",
    "ft2": "square foot (ft²)",
    "yd2": "square yard (yd²)",
    "acre": "acre",
    "mi2": "square mile (mi²)",
    "ml": "millilitre (mL)",
    "L": "litre (L)",
    "m3": "cubic metre (m³)",
    "fl_oz_uk": "UK fluid ounce",
    "pt_uk": "UK pint",
    "qt_uk": "UK quart",
    "gal_uk": "UK gallon",
    "fl_oz_us": "US fluid ounce",
    "cup_us": "US cup",
    "pt_us": "US pint",
    "qt_us": "US quart",
    "gal_us": "US gallon",
    "m/s": "metre per second (m/s)",
    "km/h": "kilometre per hour (km/h)",
    "ft/s": "foot per second (ft/s)",
    "mph": "mile per hour (mph)",
    "kn": "knot (kn)",
    "C": "Celsius (°C)",
    "F": "Fahrenheit (°F)",
    "K": "Kelvin (K)",
}

CATEGORY_LABELS: dict[str, str] = {
    "length": "Length",
    "mass": "Mass",
    "area": "Area",
    "volume_uk": "Volume (UK imperial)",
    "volume_us": "Volume (US customary)",
    "speed": "Speed",
    "temperature": "Temperature",
}


@dataclass(frozen=True)
class ConversionResult:
    value: float
    from_unit: str
    to_unit: str
    category: str


def _to_celsius(value: float, unit: str) -> float:
    if unit == "C":
        return value
    if unit == "F":
        return (value - 32.0) * 5.0 / 9.0
    if unit == "K":
        return value - 273.15
    raise ValueError(f"Unknown temperature unit: {unit}")


def _from_celsius(celsius: float, unit: str) -> float:
    if unit == "C":
        return celsius
    if unit == "F":
        return celsius * 9.0 / 5.0 + 32.0
    if unit == "K":
        return celsius + 273.15
    raise ValueError(f"Unknown temperature unit: {unit}")


def convert(value: float, from_unit: str, to_unit: str, category: str) -> ConversionResult:
    if category == "temperature":
        valid = {"C", "F", "K"}
        if from_unit not in valid or to_unit not in valid:
            raise ValueError("Temperature units must be C, F, or K.")
        result = _from_celsius(_to_celsius(value, from_unit), to_unit)
        return ConversionResult(result, from_unit, to_unit, category)

    table = CATEGORIES.get(category)
    if table is None:
        raise ValueError(f"Unknown category: {category}")
    if from_unit not in table:
        raise ValueError(f"Unknown unit {from_unit!r} for {category}")
    if to_unit not in table:
        raise ValueError(f"Unknown unit {to_unit!r} for {category}")

    base = value * table[from_unit]
    result = base / table[to_unit]
    return ConversionResult(result, from_unit, to_unit, category)


def units_for(category: str, system: str | None = None) -> list[str]:
    """Return unit codes. system is 'metric', 'imperial', or None for all."""
    if category == "temperature":
        all_units = ["C", "K", "F"]
    else:
        all_units = list(CATEGORIES[category].keys())

    if system is None:
        return all_units
    if system == "metric":
        allowed = METRIC_UNITS[category]
    elif system == "imperial":
        allowed = IMPERIAL_UNITS[category]
    else:
        raise ValueError(f"Unknown system: {system}")
    return [u for u in all_units if u in allowed]


def convert_to_system(value: float, from_unit: str, category: str, to_system: str) -> list[ConversionResult]:
    """Convert one value into every unit of the target system in this category."""
    targets = units_for(category, to_system)
    return [convert(value, from_unit, target, category) for target in targets]
