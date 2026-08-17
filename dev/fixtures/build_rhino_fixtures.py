"""Build synthetic mock-io fixtures for the mock test case.

Real mmnr rhino data (GPS tracks, individual rhino identities, ranger names)
is sensitive and must never be committed — these fixtures are fully
synthetic: deterministic random-walk patrol tracks inside the Mara Triangle
bounding box, fake rhinos in the 9xxx Kifaru-ID range, and
black_rhino_sighting_v202310 events shaped exactly like the production
payloads (title-mapped event_details keys with the three nested
sighting-details arrays).

Coverage requirements exercised here:
  - all 4 rhino-monitoring patrol slugs (Triangle/Reserve x Foot/Vehicle)
  - >=2 sighting methods (Visual, Camera Trap) so the pivot and stacked bar
    get multiple columns/segments
  - one event with missing class arrays (COALESCE '[]' path in json_each)
  - one item without the named label (Kifaru-ID fallback in the flatten SQL)

Run from any env with geopandas + pyarrow, e.g.:
    pixi run --manifest-path \
      ~/MEP/wt-workflows/mt-patrols/ecoscope-workflows-mt-patrols-workflow/pixi.toml \
      python dev/fixtures/build_rhino_fixtures.py

Fixtures written (consumed via mock_io_overrides in test-cases.yaml):
  - get-patrols-rhino.example-return.parquet
  - patrol-obs-rhino.example-return.parquet
  - get-events-rhino.example-return.parquet
  - process-events-details-rhino.example-return.parquet
"""

import uuid
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Point

OUT_DIR = Path(__file__).resolve().parent
RNG = np.random.default_rng(20260701)
NAMESPACE = uuid.NAMESPACE_URL

# (slug, display, area) — real patrol-type slugs (org config, already public
# in spec.yaml partials); everything else below is synthetic
PATROL_TYPES = [
    ("rhino_monitoring_patrol", "Rhino Monitoring - Foot (Triangle)", "triangle"),
    ("rhino_monitoring_vehicle_patrol", "Rhino Monitoring - Vehicle (Triangle)", "triangle"),
    ("rhino_monitor_patrol_reserve", "Rhino Monitoring - Foot (Reserve)", "reserve"),
    ("rhino_monitoring_veh_patrol_reserve", "Rhino Monitoring - Vehicle (Reserve)", "reserve"),
]
RANGERS = [f"Ranger {i:02d}" for i in range(1, 7)]

# Fully synthetic rhino roster: 9xxx Kifaru IDs, made-up names
BULLS = [("9001", "9001 - BOULDER"), ("9002", "9002 - GRANITE"), ("9003", "9003 - FLINT")]
COWS = [("9101", "9101 - PEBBLE"), ("9102", "9102 - MOSSY"), ("9103", "9103 - RIVER")]
UNSEXED = [("9201", "9201 - JUNIOR"), ("9202", "9202 - DUSTY")]
METHODS = ["Visual", "Visual", "Visual", "Camera Trap", "Camera Trap"]  # weighted

# rough Mara Triangle / Reserve bounding box
LON0, LON1, LAT0, LAT1 = 34.90, 35.30, -1.60, -1.30


def fake_id(name: str) -> str:
    return str(uuid.uuid5(NAMESPACE, f"mt-rhino-fixture/{name}"))


def pick_method() -> str:
    return METHODS[int(RNG.integers(len(METHODS)))]


# ── Patrol fixtures ─────────────────────────────────────────────────────
patrol_rows, obs_frames = [], []
serial = 2000
for rep in range(3):  # 3 patrols per type across Jul 2026
    for k, (slug, display, area) in enumerate(PATROL_TYPES):
        serial += 1
        patrol_id = fake_id(f"patrol/{serial}")
        start = pd.Timestamp("2026-07-02T06:00:00Z") + pd.Timedelta(days=(rep * 9 + k * 2) % 28)
        n_pts = 100
        end = start + pd.Timedelta(seconds=60 * n_pts)
        ranger = RANGERS[serial % len(RANGERS)]
        title = f"{display} {start:%d %b}"

        patrol_rows.append(
            {
                "id": patrol_id,
                "serial_number": serial,
                "title": title,
                "state": "done",
                "patrol_type": slug,
            }
        )

        lon = RNG.uniform(LON0, LON1)
        lat = RNG.uniform(LAT0, LAT1)
        steps = RNG.normal(0, 0.0012, size=(n_pts, 2)).cumsum(axis=0)
        lons = np.clip(lon + steps[:, 0], LON0, LON1)
        lats = np.clip(lat + steps[:, 1], LAT0, LAT1)
        times = pd.date_range(start, periods=n_pts, freq="60s", tz="UTC")
        obs_frames.append(
            gpd.GeoDataFrame(
                {
                    "extra__id": [fake_id(f"obs/{serial}/{i}") for i in range(n_pts)],
                    "extra__created_at": times,
                    "extra__recorded_at": times,
                    "extra__subject_id": fake_id(f"subject/{ranger}"),
                    "groupby_col": patrol_id,
                    "fixtime": times,
                    "junk_status": False,
                    "patrol_id": patrol_id,
                    "patrol_title": title,
                    "patrol_serial_number": serial,
                    "patrol_start_time": start,
                    "patrol_end_time": end,
                    "patrol_type": fake_id(f"patrol-type/{slug}"),
                    "patrol_status": "done",
                    "patrol_subject": ranger,
                    "patrol_type__value": slug,
                    "patrol_type__display": display,
                },
                geometry=[Point(x, y) for x, y in zip(lons, lats)],
                crs=4326,
            )
        )

patrols_df = pd.DataFrame(patrol_rows)
patrols_df.to_parquet(OUT_DIR / "get-patrols-rhino.example-return.parquet")

obs = gpd.GeoDataFrame(pd.concat(obs_frames, ignore_index=True), crs=4326)
obs.to_parquet(OUT_DIR / "patrol-obs-rhino.example-return.parquet")

# ── Sighting event fixtures ─────────────────────────────────────────────
reporter = {
    "content_type": "observations.subject",
    "id": fake_id("reporter-1"),
    "name": "Ranger 01",
    "subject_subtype": "er_mobile",
    "subject_type": "person",
}

N_EVENTS = 24
event_rows, details = [], []
for i in range(N_EVENTS):
    bulls, cows, nk = [], [], []
    # 1-3 individuals per event, drawn across the three classes
    for _ in range(int(RNG.integers(1, 4))):
        cls = int(RNG.integers(3))
        if cls == 0:
            kid, name = BULLS[int(RNG.integers(len(BULLS)))]
            bulls.append({"Bull": name, "Kifaru ID": kid, "Sighting": pick_method()})
        elif cls == 1:
            kid, name = COWS[int(RNG.integers(len(COWS)))]
            cows.append({"Known Cows": name, "Kifaru ID": kid, "Sighting": pick_method()})
        else:
            kid, name = UNSEXED[int(RNG.integers(len(UNSEXED)))]
            nk.append({"Unsexed Individual(s)": name, "Kifaru ID": kid, "Sighting": pick_method()})

    detail = {}
    if bulls:
        detail["Sighting Details - Bulls"] = bulls
    if cows:
        detail["Sighting Details - Cows"] = cows
    if nk:
        detail["Sighting Details - Unsexed Individuals"] = nk

    # every event misses at least one class array naturally (1-3 individuals
    # across 3 classes); force one event to have ONLY bulls and one item with
    # no named label (Kifaru-ID fallback)
    if i == 0:
        detail = {"Sighting Details - Bulls": [{"Kifaru ID": "9003", "Sighting": "Visual"}]}

    details.append(detail)
    event_rows.append(
        {
            "id": fake_id(f"event/{i}"),
            "time": pd.Timestamp("2026-07-01T06:00:00Z")
            + pd.Timedelta(minutes=int(RNG.integers(0, 30 * 24 * 60))),
            "event_type": "black_rhino_sighting_v202310",
            "event_category": "rhino_mgmt",
            "title": "Black Rhino Sighting",
            "priority": 0,
            "priority_label": "Gray",
            "state": "active",
            "reported_by": reporter,
            "geometry": Point(
                round(float(RNG.uniform(LON0, LON1)), 6),
                round(float(RNG.uniform(LAT0, LAT1)), 6),
            ),
            "serial_number": 91000 + i,
            "event_type_display": "Black Rhino Sighting",
        }
    )

events_df = pd.DataFrame(event_rows).sort_values("time")
details = [details[j] for j in events_df.index]  # keep details aligned after sort
events_df = events_df.reset_index(drop=True)

events = gpd.GeoDataFrame(events_df, geometry="geometry", crs="EPSG:4326")
events.to_parquet(OUT_DIR / "get-events-rhino.example-return.parquet", index=False)

# process_events_details mock: same rows, drop `reported_by`, add the columns
# this task contributes (title-mapped event_details, reported_by_name)
processed = events.drop(columns=["reported_by"]).copy()
processed["event_details"] = details
processed["reported_by_name"] = "Ranger 01"
processed.to_parquet(OUT_DIR / "process-events-details-rhino.example-return.parquet", index=False)

n_individuals = sum(len(v) for d in details for v in d.values())
print(f"patrols: {len(patrols_df)}, obs: {len(obs)}, events: {len(events)}, individuals: {n_individuals}")
print(f"wrote fixtures to {OUT_DIR}")
