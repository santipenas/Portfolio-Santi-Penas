"""Comprehensive unit and integration tests for Geospatial RF Planner."""

import pytest
from portfolio_agents.geospatial_rf_planner.agent import root_agent
from portfolio_agents.geospatial_rf_planner.tools import (
    query_rf_cell_sites,
    detect_coverage_dead_zones,
    analyze_inter_cell_interference,
    generate_coverage_geojson,
    optimize_antenna_parameters,
    _haversine_distance,
)


def test_root_agent_configuration():
    assert root_agent.name == "geospatial_rf_planner"
    assert root_agent.model == "gemini-2.5-flash"
    assert len(root_agent.tools) == 5
    tool_names = [getattr(t, "__name__", str(t)) for t in root_agent.tools]
    assert "query_rf_cell_sites" in tool_names
    assert "detect_coverage_dead_zones" in tool_names
    assert "analyze_inter_cell_interference" in tool_names
    assert "generate_coverage_geojson" in tool_names
    assert "optimize_antenna_parameters" in tool_names
    assert "geospatial" in root_agent.description.lower() or "rf" in root_agent.description.lower()


def test_query_rf_cell_sites_all():
    sites = query_rf_cell_sites()
    assert len(sites) >= 6
    for s in sites:
        assert "site_id" in s
        assert "latitude" in s
        assert "longitude" in s
        assert -90 <= s["latitude"] <= 90
        assert -180 <= s["longitude"] <= 180


def test_query_rf_cell_sites_filters():
    manhattan = query_rf_cell_sites(region="Manhattan")
    assert len(manhattan) >= 3
    for s in manhattan:
        assert "Manhattan" in s["region"]

    mmwave = query_rf_cell_sites(band="n258")
    assert len(mmwave) >= 1
    assert "n258" in mmwave[0]["band"]


def test_detect_coverage_dead_zones():
    holes = detect_coverage_dead_zones()
    assert len(holes) >= 1
    for h in holes:
        assert h["estimated_rsrp_dbm"] <= -105.0
        assert h["severity"] in ["CRITICAL", "MODERATE", "LOW"]
        assert "nearest_serving_site" in h


def test_haversine_distance():
    # NYC Manhattan to Brooklyn (~1km - 2km)
    dist = _haversine_distance(40.7075, -74.0090, 40.7033, -73.9890)
    assert 1200 < dist < 2200


def test_analyze_inter_cell_interference():
    analysis = analyze_inter_cell_interference("SITE-NYC-001")
    assert "error" not in analysis
    assert analysis["source_site"] == "SITE-NYC-001"
    assert "interfering_site" in analysis
    assert analysis["separation_distance_m"] > 0
    assert analysis["sinr_penalty_db"] > 0
    assert analysis["collision_risk"] in ["CRITICAL", "MODERATE", "LOW"]


def test_generate_coverage_geojson():
    geojson = generate_coverage_geojson(include_dead_zones=True)
    assert geojson["type"] == "FeatureCollection"
    assert "features" in geojson
    assert len(geojson["features"]) >= 10

    # Validate geometries
    types_found = {f["geometry"]["type"] for f in geojson["features"]}
    assert "Point" in types_found
    assert "Polygon" in types_found

    # Check coordinate values
    point = next(f for f in geojson["features"] if f["geometry"]["type"] == "Point")
    coords = point["geometry"]["coordinates"]
    assert len(coords) == 2  # [lon, lat]
    assert -180 <= coords[0] <= 180
    assert -90 <= coords[1] <= 90


def test_optimize_antenna_parameters():
    plan = optimize_antenna_parameters(site_id="SITE-NYC-001", target_objective="FILL_DEAD_ZONE")
    assert "error" not in plan
    assert plan["site_id"] == "SITE-NYC-001"
    assert plan["recommended_azimuth_deg"] != plan["current_azimuth_deg"]
    assert plan["expected_sinr_gain_db"] > 0
    assert plan["expected_coverage_lift_pct"] > 0
    assert len(plan["rationale"]) > 10
