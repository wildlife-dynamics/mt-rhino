# Mara Triangle Rhino Report Workflow

## Introduction

This workflow helps you to monitor black rhino conservation activity in the Maasai Mara: it combines **rhino monitoring patrols** and **Black Rhino Sighting** events from EarthRanger into maps, summary tables, charts, and a ready-to-share Word report for a chosen reporting period.

**What this workflow does:**
- Downloads rhino monitoring patrols (Foot and Vehicle, for both the **Mara Triangle** and the **National Reserve**) from EarthRanger, along with their **Patrol Information** events to identify the patrol team
- Downloads **Black Rhino Sighting** events and breaks each one down into individual rhino sightings, with the rhino's name and the sighting method (Visual, Camera Trap, Dung, Spoor, or Telemetry)
- Creates two interactive patrol trajectory maps — one for Mara Triangle patrols, one for Reserve patrols — colored by patrol team
- Creates an interactive map of individual rhino sightings, colored by rhino
- Summarizes sightings per rhino with one count column per sighting method plus a total
- Draws a stacked bar chart of sightings per rhino, stacked by sighting method
- Exports patrol trajectories and per-individual sighting records for further analysis
- Generates a Word (DOCX) report containing both patrol maps, the sightings map, the summary table, and the chart

**Who should use this:**
- Conservation managers overseeing rhino monitoring in the Mara Triangle and the National Reserve
- Rhino monitoring teams producing monthly activity reports
- Researchers analyzing individual rhino sighting histories stored in EarthRanger

## Prerequisites

Before using this workflow, you need:

1. **Ecoscope Desktop** installed on your computer
   - If you haven't installed it yet, please follow the installation instructions for Ecoscope Desktop

2. **EarthRanger Data Source** configured in Ecoscope Desktop
   - You must have already set up a connection to your EarthRanger server (for the Mara this is the `mmnr` data source)
   - Your data source should be configured with proper authentication credentials
   - You'll need to know the name of your configured data source (e.g., "mmnr")

3. **Rhino monitoring data** set up in EarthRanger
   - The four rhino monitoring patrol types must exist: Rhino Monitoring - Foot/Vehicle (Triangle) and Rhino Monitoring - Foot/Vehicle (Reserve)
   - The **Black Rhino Sighting** event type must be configured with the per-individual sighting details (Bulls, Cows, and Unsexed Individuals sections)
   - Patrols should have a **Patrol Information** event with the **Team name** filled in — patrols without one appear as "Unknown" on the maps
   - You can review event types at `https://<your-site>.pamdas.org/admin/activity/eventtype/`

## Installation

1. Select "Workflow Templates" tab
2. Click "+ Add Template"
3. Copy and paste this URL https://github.com/wildlife-dynamics/mt-rhino and wait for the workflow template to be downloaded and initialized
4. The template will now appear in your available template list

## Configuration Guide

### Basic Configuration

#### 1. Workflow Details
Give your workflow run a recognizable name.

- **Workflow Name** (required): The title shown on your dashboard
  - Example: `Mara Triangle Rhino Report`
- **Workflow Description** (optional): A short subtitle for the dashboard
  - Example: `Rhino monitoring from EarthRanger (mmnr)`

#### 2. Time Range
The reporting period. Patrols and sightings within this window are included.

- **Since** (required): Start of the period
  - Example: `2026-07-01T00:00:00`
- **Until** (required): End of the period
  - Example: `2026-07-31T23:59:59`
- **Timezone** (required): The timezone your dates are interpreted in
  - Example: `Africa/Nairobi (UTC+03:00)`
  - Note: Use your local timezone so patrol and sighting times display correctly

#### 3. Data Source
The EarthRanger connection to pull data from.

- **Data Source** (required): The name of your configured EarthRanger connection
  - Example: `mmnr`
  - Note: This must match a data source already configured in Ecoscope Desktop

### Advanced Configuration

These optional settings provide additional control over your workflow:

#### Trajectory Filter (Process Patrols)
Controls which patrol track segments are kept when GPS points are converted into trajectories. The defaults are tuned for ranger patrols and rarely need changing.

- **Min/Max Length (meters)**: Default `0.001` – `10000`
- **Min/Max Time (seconds)**: Default `1` – `172800`
- **Min/Max Speed (km/h)**: Default `0.01` – `500`
- **Filter Points**: Coordinates to discard as GPS noise (defaults remove common bogus fixes like `0, 0`)

#### Base Maps
The background map tiles used by all three maps.

- **Base Maps**: Default is the ArcGIS World Topo map
  - You can add or replace tile URLs if your organization prefers different basemaps

#### Create Rhino Report
- **Template Path**: The Word template used for the DOCX report
  - Default: the template published with this workflow
  - Note: Only change this if you maintain a customized report template

## Running the Workflow

Once you've configured all the settings:

1. **Review your configuration**
   - Double-check your time range, data source, and timezone

2. **Save and run**
   - Click the "Submit" and the workflow will show up in "My Workflows" table button in Ecoscope Desktop
   - Click on "Run" and the workflow will begin processing

3. **Monitor progress and wait for completion**
   - You'll see status updates as the workflow runs
   - Processing time depends on:
     - The size of your date range
     - The number of patrols in the period
     - The number of rhino sighting events in the period
   - The workflow completes with status "Success" or "Failed"

## Understanding Your Results

After the workflow completes successfully, you'll find your outputs in the designated output folder.

### Data Outputs

#### Patrol Trajectories

- **File format**: GeoParquet (`rhino_patrol_trajectories_*.parquet`)
- **Opens in**: Python/R, QGIS/ArcGIS
- **Best for**: Spatial analysis of patrol coverage
- **Contents**: One row per patrol track segment, for all four rhino monitoring patrol types
  - `patrol_type`: Patrol type slug (e.g., `rhino_monitoring_patrol`)
  - `patrol_type_display`: Readable patrol type (e.g., `Rhino Monitoring - Foot (Triangle)`)
  - `team_name`: The patrol team from the Patrol Information event (`Unknown` when the event is missing)
  - `patrol_title`, `patrol_serial_number`, `patrol_subject`: Patrol identification
  - `segment_start` / `segment_end`, `timespan_seconds`, `speed_kmhr`: Segment movement details

#### Rhino Observations

- **File format**: GeoParquet (`rhino_observations_*.parquet`)
- **Opens in**: Python/R, QGIS/ArcGIS
- **Best for**: Per-individual sighting analysis
- **Contents**: One row per individual rhino per sighting event
  - `Rhino Name`: The named individual (e.g., `1516 - KIOKO`), falling back to the Kifaru ID when no name is recorded
  - `Sighting Method`: How the rhino was recorded (`Visual`, `Camera Trap`, `Dung`, `Spoor`, `Telemetry`)
  - `event_id`, `serial_number`, `time`, `geometry`: The source sighting event details

#### Rhino Summary

- **File format**: CSV (`rhino_summary_*.csv`)
- **Opens in**: Microsoft Excel, Google Sheets
- **Best for**: Quick review of sighting effort per rhino
- **Contents**: One row per rhino with one count column per sighting method present in your data, plus a `Total` column

### Visual Outputs (Dashboard)

The workflow creates an interactive dashboard with 5 visualizations:

#### Mara Triangle Rhino Patrols (map)
- **Format**: Interactive trajectory map
- **Features**:
  - Patrol tracks for the two Triangle patrol types, colored by **patrol team** (from each patrol's Patrol Information event)
  - Legend (bottom right) and north arrow (top left)
  - Interactive hover: Team, Start Time, Duration (s), Speed (kph) per segment

#### Reserve Rhino Patrols (map)
- **Format**: Interactive trajectory map
- **Features**: Same as the Triangle map, for the two Reserve patrol types — team colors are consistent across both maps

#### Rhino Sightings (map)
- **Format**: Interactive point map
- **Features**:
  - One point per individual rhino sighting, colored by rhino
  - Interactive hover: Rhino Name, Sighting Method, and time

#### Rhino Sighting Summary (table)
- **Format**: Interactive table with sorting, filtering, and download enabled
- **Features**: One row per rhino; one column per sighting method plus Total

#### Rhino Sightings by Method (chart)
- **Format**: Interactive stacked bar chart
- **Features**:
  - X-axis: Rhino name
  - Y-axis: Number of sightings
  - One stacked segment per sighting method, with legend
  - Interactive hover: Shows exact counts when you mouse over bars

### DOCX Report

A Word report (`mt_rhino_report_*.docx`) containing the reporting period, both patrol maps, the rhino sightings map, the summary table, and the stacked bar chart — ready to circulate.

## Common Use Cases & Examples

Here are some typical scenarios and how to configure the workflow for each:

### Example 1: Monthly Rhino Report
**Goal**: Produce the standard monthly report for July 2026

**Configuration**:
- **Time Range**:
  - Since: `2026-07-01T00:00:00`
  - Until: `2026-07-31T23:59:59`
  - Timezone: `Africa/Nairobi (UTC+03:00)`
- **Data Source**: `mmnr`

**Result**:
- Two patrol maps covering all July rhino monitoring patrols in the Triangle and the Reserve
- Sightings map, per-rhino summary table, stacked bar chart, and the DOCX report for July

---

### Example 2: Quarterly Review
**Goal**: Review rhino monitoring effort across a full quarter

**Configuration**:
- **Time Range**:
  - Since: `2026-04-01T00:00:00`
  - Until: `2026-06-30T23:59:59`
  - Timezone: `Africa/Nairobi (UTC+03:00)`
- **Data Source**: `mmnr`

**Result**:
- The same outputs aggregated over three months — useful for spotting rhinos with few sightings and comparing method mix (e.g., how much monitoring relies on camera traps)

---

### Example 3: Custom Report Template
**Goal**: Produce the monthly report using your organization's customized Word template

**Configuration**:
- **Time Range**: as in Example 1
- **Data Source**: `mmnr`
- **Create Rhino Report → Template Path**: URL or path to your customized template
  - Note: Your template must keep the placeholder names (`patrol_map_triangle`, `patrol_map_reserve`, `rhino_map`, `rhino_summary`, `bar_chart`, `report_date`)

**Result**:
- The same data rendered into your organization's report layout

## Troubleshooting

### Common Issues and Solutions

#### Workflow fails to start
**Problem**: The workflow fails immediately with a connection or authentication error

**Solutions**:
- Verify your EarthRanger data source is configured in Ecoscope Desktop and the credentials are current
- Confirm the data source name in your configuration matches exactly (e.g., `mmnr`)
- If you receive repeated `402` or `502` errors from the server, try switching your VPN server before further debugging

#### No patrols on the maps
**Problem**: The workflow succeeds but one or both patrol maps are empty

**Solutions**:
- Check that patrols of the rhino monitoring types exist in EarthRanger for your time range
- Only patrols with status **Done** are included — patrols still open or cancelled are excluded
- Widen your time range to confirm data appears

#### No rhino sightings
**Problem**: The sightings map, table, and chart are empty

**Solutions**:
- Confirm **Black Rhino Sighting** events exist within your time range
- Check that the events have the individual sighting details filled in (Bulls / Cows / Unsexed Individuals sections) — events without any individuals recorded cannot be broken down
- Verify events have a location; events without coordinates are excluded from the maps

#### A report section is blank
**Problem**: The generated report has an empty spot where a map, table, or chart should be — for example no Mara Triangle map for a month with no Triangle rhino patrols

**Solutions**:
- This is expected when the period has no data for that section: the report still generates, with the missing section left blank
- Check in EarthRanger that the missing area's patrols were closed out (status Done) for the period

#### Workflow runs very slowly
**Problem**: The workflow takes a long time to finish

**Solutions**:
- The first run after installation includes a one-time warm-up; later runs are faster
- Large time ranges with many patrols increase download time — try a single month
- Report screenshots of the maps take up to 20 seconds each by design; this is normal

#### A rhino appears twice in the table
**Problem**: The same animal shows up under two names (e.g., once by name and once by ID)

**Solutions**:
- This happens when some sightings record only the Kifaru ID without selecting the named individual — the workflow falls back to the bare ID
- Correct the affected events in EarthRanger so the named individual is selected, then re-run
