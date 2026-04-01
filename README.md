# Mara Triangle Rhino Report Workflow

## Introduction

This workflow generates a comprehensive rhino monitoring report for the Mara Triangle conservancy by combining patrol trajectory data with rhino sighting observations.

**What this workflow does:**
- Fetches patrol observations from **SMART** and filters to **Rhino Monitoring** mandate patrols
- Fetches wildlife events from **SMART** and filters to **Rhino Direct Observation** sightings
- Generates an interactive patrol trajectory map colored by station
- Generates an interactive rhino sighting map colored by individual rhino
- Summarizes sighting counts by individual rhino name
- Creates a bar chart of sighting statistics
- Exports patrol trajectories, rhino observations, and summary data
- Assembles a DOCX report with maps, charts, and summary tables
- Creates a dashboard with all 4 visualizations

**Who should use this:**
- Conservation managers monitoring rhino populations in the Mara Triangle
- Patrol coordinators reviewing rhino monitoring patrol coverage
- Researchers analyzing individual rhino sighting patterns

## Prerequisites

Before using this workflow, you need:

1. **Ecoscope Desktop** installed on your computer
   - If you haven't installed it yet, please follow the installation instructions for Ecoscope Desktop

2. **SMART Data Source** configured in Ecoscope Desktop
   - You must have already set up a connection to your SMART server (Mara Triangle)
   - Your data source should be configured with proper authentication credentials
   - You'll need to know the name of your configured data source (e.g., `"mara_triangle"`)

3. **SMART Patrol and Event Data** available
   - Patrol observations with Rhino Monitoring mandate must exist for your selected time range
   - Rhino Direct Observation events must be recorded in SMART

## Installation

1. Select "Workflow Templates" tab
2. Click "+ Add Template"
3. Copy and paste this URL https://github.com/wildlife-dynamics/mt-rhino and wait for the workflow template to be downloaded and initialized
4. The template will now appear in your available template list

## Configuration Guide

### Basic Configuration

#### 1. Workflow Details
Give your workflow run a descriptive name.

- **Workflow Name** (required): A name to identify this run
  - Example: `"Mara Triangle Rhino Report"`

#### 2. Time Range
Select the period of time to analyze.

- **Since** (required): Start date and time
  - Example: `2026-02-01T00:00:00`
- **Until** (required): End date and time
  - Example: `2026-02-28T23:59:59`
- **Timezone** (optional): Your local timezone
  - Example: `Africa/Nairobi (UTC+03:00)`

#### 3. Data Source
Select your SMART connection.

- **Data Source Name** (required): The name of your configured SMART data source
  - Example: `"mara_triangle"`

#### 4. Base Maps
Choose the background map tile layer.

- **Base Maps** (optional): Map tile URL and opacity
  - Default: ArcGIS World Topo Map

#### 5. Report Template
Path or URL to the DOCX template for report generation.

- **Template Path** (optional): URL to the Word template
  - Default: GitHub-hosted template

### Advanced Configuration

These optional settings provide additional control over your workflow:

#### Trajectory Segment Filter
Control how patrol relocations are converted to trajectory segments. Segments outside these bounds are removed.

- **Min/Max Length (meters)**: Filter by segment distance (default: 0.001 - 10,000 m)
- **Min/Max Time (seconds)**: Filter by segment duration (default: 1 - 172,800 s)
- **Min/Max Speed (km/hr)**: Filter by segment speed (default: 0.01 - 500 km/hr)

#### Coordinate Filters
Remove known bad coordinates (e.g., 0,0 or 180,90).

## Running the Workflow

Once you've configured all the settings:

1. **Review your configuration**
   - Double-check your time range, data source, and other settings

2. **Save and run**
   - Click "Submit" and the workflow will show up in the "My Workflows" table
   - Click on "Run" and the workflow will begin processing

3. **Monitor progress and wait for completion**
   - You'll see status updates as the workflow runs
   - Processing time depends on:
     - The size of your date range
     - Number of patrol observations and rhino sightings
     - SMART server response time
   - The workflow completes with status "Success" or "Failed"

## Understanding Your Results

After the workflow completes successfully, you'll find your outputs in the designated output folder.

### Data Outputs

#### Patrol Trajectories
- **File format**: GeoParquet
- **Contents**: Rhino Monitoring patrol trajectory segments with columns including:
  - `station`: Patrol station name
  - `patrol_mandate`: Always "Rhino Monitoring"
  - `segment_start`: Start time of trajectory segment
  - `speed_kmhr`: Speed in km/h
  - `dist_meters`: Distance in meters
  - `geometry`: LineString trajectory geometry

#### Rhino Observations
- **File format**: GeoParquet
- **Contents**: Individual rhino sighting records with columns including:
  - `Rhino Name`: Name/ID of the individual rhino
  - `time`: Observation timestamp
  - `X`, `Y`: Coordinates
  - `geometry`: Point geometry

#### Rhino Summary
- **File format**: CSV
- **Opens in**: Microsoft Excel, Google Sheets
- **Contents**: Sighting count per individual rhino
  - `Rhino Name`: Individual rhino identifier
  - `Count`: Number of sightings

### Visual Outputs (Dashboard)

The workflow creates an interactive dashboard with 4 visualizations:

#### Rhino Patrol Trajectories Map
- **Format**: Interactive map with polyline layers
- **Features**:
  - Patrol routes colored by station (Dark2 colormap)
  - Legend showing station names
  - Tooltips: Start Time, Duration (s), Speed (kph)
  - North arrow (top-left), legend (bottom-right)

#### Rhino Sightings Map
- **Format**: Interactive map with point layers
- **Features**:
  - Sighting locations colored by individual Rhino Name (Dark2 colormap)
  - Legend showing rhino names
  - Tooltips: Rhino Name, time
  - North arrow (top-left), legend (bottom-right)

#### Rhino Sighting Summary Table
- **Format**: Interactive HTML table
- **Features**:
  - Sortable and filterable columns
  - Downloadable data
  - Shows Rhino Name and Count

#### Rhino Sighting Counts Bar Chart
- **Format**: Interactive bar chart
- **Features**:
  - X-axis: Individual rhino names
  - Y-axis: Count of sightings
  - Hover: Shows exact count values

### DOCX Report

A Word document containing all visualizations and data:
- Report date header
- Patrol trajectory map (screenshot)
- Rhino sighting map (screenshot)
- Summary table
- Bar chart (screenshot)

## Common Use Cases & Examples

### Example 1: Monthly Rhino Report
**Goal**: Generate the standard monthly rhino monitoring report

**Configuration**:
- **Time Range**:
  - Since: `2026-02-01T00:00:00`
  - Until: `2026-02-28T23:59:59`
  - Timezone: `Africa/Nairobi (UTC+03:00)`
- **Data Source**: `"mara_triangle"`

**Result**:
- Maps showing February patrol routes and sighting locations
- Summary of individual rhino sightings for February
- DOCX report ready for stakeholder distribution

---

### Example 2: Quarterly Review
**Goal**: Analyze rhino monitoring over a 3-month period

**Configuration**:
- **Time Range**:
  - Since: `2026-01-01T00:00:00`
  - Until: `2026-03-31T23:59:59`
  - Timezone: `Africa/Nairobi (UTC+03:00)`
- **Data Source**: `"mara_triangle"`

**Result**:
- Comprehensive patrol coverage map for Q1
- Aggregated sighting counts per rhino over 3 months
- Useful for identifying trends in individual rhino activity

---

### Example 3: Specific Incident Period
**Goal**: Review rhino activity during a specific week

**Configuration**:
- **Time Range**:
  - Since: `2026-02-10T00:00:00`
  - Until: `2026-02-17T23:59:59`
  - Timezone: `Africa/Nairobi (UTC+03:00)`
- **Data Source**: `"mara_triangle"`

**Result**:
- Focused patrol and sighting data for one week
- Useful for incident response review or targeted analysis

## Troubleshooting

### Common Issues and Solutions

#### Workflow fails to connect to SMART
**Problem**: Error message about connection or authentication failure

**Solutions**:
- Verify your SMART data source is correctly configured in Ecoscope Desktop
- Check that your SMART server is accessible
- Confirm your credentials are valid

#### No patrol data returned
**Problem**: Patrol trajectory map is empty

**Solutions**:
- Check that your time range contains patrol data
- Verify that "Rhino Monitoring" mandate patrols exist for the selected period
- Try a wider time range to confirm data availability

#### No rhino sightings returned
**Problem**: Sighting map and summary are empty

**Solutions**:
- Confirm that "Rhino Direct Observation" events exist in SMART for your time range
- Check that events have a valid "Rhino Name" attribute filled in
- Try a wider time range

#### SMART API returns 502 error
**Problem**: Intermittent server error during data fetch

**Solutions**:
- This is a transient SMART server issue
- Wait a few minutes and retry the workflow
- If persistent, check SMART server status

#### Report template not found
**Problem**: DOCX report generation fails with template error

**Solutions**:
- Ensure the template URL is accessible (the default points to the GitHub repository)
- If using a custom template, verify the file path or URL is correct
- For local testing, use an absolute file path to your template

#### Empty or missing charts
**Problem**: Bar chart or summary table shows no data

**Solutions**:
- This usually means no rhino sightings matched the filters
- Verify that events have the "Rhino Name" field populated in SMART
- Check the raw rhino observations export to see what data was fetched
