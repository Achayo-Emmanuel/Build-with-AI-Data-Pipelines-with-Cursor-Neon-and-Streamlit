import math

import pytest

from converter import convert, convert_to_system, units_for


def test_metre_to_inch_exact():
    result = convert(1.0, "m", "in", "length")
    assert result.value == pytest.approx(1.0 / 0.0254)


def test_kilogram_to_pound_nist():
    result = convert(1.0, "kg", "lb", "mass")
    assert result.value == pytest.approx(1.0 / 0.45359237)


def test_celsius_to_fahrenheit():
    assert convert(0.0, "C", "F", "temperature").value == pytest.approx(32.0)
    assert convert(100.0, "C", "F", "temperature").value == pytest.approx(212.0)
    assert convert(32.0, "F", "C", "temperature").value == pytest.approx(0.0)


def test_kelvin_round_trip():
    celsius = convert(300.0, "K", "C", "temperature").value
    kelvin = convert(celsius, "C", "K", "temperature").value
    assert kelvin == pytest.approx(300.0)


def test_uk_gallon_to_litre():
    result = convert(1.0, "gal_uk", "L", "volume_uk")
    assert result.value == pytest.approx(4.54609)


def test_us_gallon_to_litre():
    result = convert(1.0, "gal_us", "L", "volume_us")
    assert result.value == pytest.approx(3.785411784)


def test_kmh_to_mph():
    result = convert(160.9344, "km/h", "mph", "speed")
    assert result.value == pytest.approx(100.0)


def test_hectare_to_acre():
    result = convert(1.0, "ha", "acre", "area")
    assert result.value == pytest.approx(2.4710538147, rel=1e-9)


def test_unknown_category():
    with pytest.raises(ValueError):
        convert(1.0, "m", "ft", "energy")


def test_convert_to_system_lists_imperial_length():
    rows = convert_to_system(1.0, "m", "length", "imperial")
    codes = [row.to_unit for row in rows]
    assert codes == ["in", "ft", "yd", "mi"]
    assert all(math.isfinite(row.value) for row in rows)


def test_units_for_filters_system():
    assert "m" in units_for("length", "metric")
    assert "ft" not in units_for("length", "metric")
    assert "ft" in units_for("length", "imperial")
