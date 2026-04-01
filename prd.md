---
title: 'Mara Triangle Rhino Report'
repo_name: 'mt-rhino'
workflow_id: 'mt_rhino'
created: '2026-03-31'
status: 'ready-for-dev'
stepsCompleted: []
data_sources: [set_smart_connection]
reference_workflows: [mt-patrols, mt-wildlife]
tasks_identified: [set_workflow_details, set_smart_connection, set_time_range, get_timezone_from_time_range, get_patrol_observations_from_smart, get_events_from_smart, convert_values_to_timezone, drop_column_prefix, apply_reloc_coord_filter, relocations_to_trajectory, map_columns, filter_row_values, normalize_json_column, apply_sql_query, apply_color_map, set_base_maps, set_string_var, create_polyline_layer, create_point_layer, draw_ecomap, persist_text, summarize_df, draw_table, draw_bar_chart, persist_df_wrapper, create_map_widget_single_view, create_plot_widget_single_view, create_table_widget_single_view, merge_widget_views, create_docx, gather_dashboard]
---

# PRD: Mara Triangle Rhino Report

**Created:** 2026-03-31
**Repo:** `/Users/yunwu/MEP/wt/mt-rhino/`
**Workflow ID:** `mt_rhino`

## Overview

### Problem Statement

Mara Triangle conservancy needs a consolidated rhino monitoring workflow that combines patrol trajectory visualization with rhino sighting analysis. Currently this is spread across 4+ separate desktop workflows (mt_rhino_map, mt_rhino_patrol, mt_rhino_summary, mt_rhino_bar) plus a download workflow, requiring manual orchestration to produce a monthly report.

### Solution

A single workflow that fetches patrol observations and wildlife events from SMART, filters to rhino-relevant data (Rhino Monitoring mandate patrols + Rhino Direct Observation events), generates a patrol trajectory map, rhino sighting point map, summary table, and bar chart, then assembles everything into a DOCX report and interactive dashboard.

### Scope

**In Scope:**
- Fetch patrol observations from SMART, filter to Rhino Monitoring mandate, convert to trajectories, generate polyline map colored by station
- Fetch SMART events, filter to Rhino Direct Observation, extract Rhino Name, generate point map colored by individual
- Summary table: sighting count by Rhino Name, exported as CSV, displayed as dashboard table widget
- Bar chart: sighting count by Rhino Name
- Data exports: raw patrol trajectories, raw rhino observations, rhino summary CSV
- DOCX report with patrol map, sighting map, summary table, bar chart
- Dashboard with all widgets (patrol map, sighting map, summary table, bar chart)

**Out of Scope:**
- Real-time patrol tracking or rhino monitoring
- Historical trend analysis across months
- Rhino population modeling or density estimation
- Integration with other wildlife species data

## Data Sources & Connections

| Source | Type | Connection | Notes |
| ----- | ---- | ---------- | ----- |
| SMART | Patrol observations | `set_smart_connection` | Mara Triangle conservancy, ca_uuid `735606d2-c34e-49c3-a45b-7496ca834e58`, filtered to Rhino Monitoring mandate downstream |
| SMART | Wildlife events | `set_smart_connection` | Same connection, filtered to `event_type = 'Rhino Direct Observation'` downstream |

## Reference Workflows

| Workflow | Relevance | Patterns Borrowed |
| -------- | --------- | ----------------- |
| mt-patrols | SMART patrol fetch, trajectory processing, polyline map, bar chart, DOCX report | Patrol pipeline: fetch → timezone → drop prefix → coord filter → trajectory → drop prefix → map_columns → colormap. Polyline layer style, trajectory segment filter defaults |
| mt-wildlife | SMART event fetch, sighting processing, point map, summary, DOCX report | Event pipeline: fetch → timezone → coord filter → normalize_json_column → apply_sql_query. Point layer style, colormap, summary pattern |

## Task Pipeline

### Identified Tasks

| # | Task | ID | Group | Purpose |
|---|------|----|-------|---------|
| 1 | set_workflow_details | workflow_details | — | Dashboard metadata |
| 2 | set_smart_connection | smart_client_name | — | SMART API connection |
| 3 | set_time_range | time_range | — | User time range |
| 4 | get_timezone_from_time_range | get_timezone | — | Extract timezone |
| 5 | get_patrol_observations_from_smart | patrol_obs | — | Fetch patrol relocations |
| 6 | convert_values_to_timezone | convert_patrols_tz | — | Convert fixtime column |
| 7 | drop_column_prefix | drop_prefix_obs | Process Patrols | Remove `extra__` from obs |
| 8 | apply_reloc_coord_filter | filter_patrol_coords | Process Patrols | Filter bad coordinates |
| 9 | relocations_to_trajectory | patrol_traj | Process Patrols | Convert to trajectory segments |
| 10 | drop_column_prefix | drop_prefix_traj | Process Patrols | Remove `extra__` from traj |
| 11 | map_columns | cleanup_traj_cols | Process Patrols | Drop unneeded columns |
| 12 | filter_row_values | filter_rhino_patrols | Process Patrols | Filter to Rhino Monitoring mandate |
| 13 | apply_color_map | patrol_colormap | Process Patrols | Color by station |
| 14 | get_events_from_smart | smart_events | — | Fetch SMART events |
| 15 | convert_values_to_timezone | convert_events_tz | — | Convert time column |
| 16 | apply_reloc_coord_filter | filter_event_coords | Process Sightings | Filter bad coordinates |
| 17 | normalize_json_column | normalize_attrs | Process Sightings | Flatten extracted_attributes |
| 18 | apply_sql_query | process_rhino | Process Sightings | Filter Rhino Direct Observation + extract Rhino Name |
| 19 | apply_color_map | rhino_colormap | Process Sightings | Color by Rhino Name |
| 20 | set_base_maps | base_map_defs | — | Tile layer config |
| 21 | set_string_var | set_patrol_map_title | Patrol Map | Map widget title |
| 22 | map_columns | rename_traj_cols | Patrol Map | Rename for tooltips |
| 23 | create_polyline_layer | patrol_polyline | Patrol Map | Trajectory lines |
| 24 | draw_ecomap | patrol_ecomap | Patrol Map | Render patrol map |
| 25 | persist_text | persist_patrol_ecomap | Patrol Map | Save map HTML |
| 26 | create_map_widget_single_view | patrol_map_widget | Patrol Map | Map widget |
| 27 | merge_widget_views | merged_patrol_map | Patrol Map | Merge views |
| 28 | set_string_var | set_rhino_map_title | Rhino Map | Map widget title |
| 29 | create_point_layer | rhino_point_layer | Rhino Map | Sighting points |
| 30 | draw_ecomap | rhino_ecomap | Rhino Map | Render sighting map |
| 31 | persist_text | persist_rhino_ecomap | Rhino Map | Save map HTML |
| 32 | create_map_widget_single_view | rhino_map_widget | Rhino Map | Map widget |
| 33 | merge_widget_views | merged_rhino_map | Rhino Map | Merge views |
| 34 | persist_df_wrapper | persist_patrol_traj | — | Export raw patrol trajectories |
| 35 | persist_df_wrapper | persist_rhino_obs | — | Export raw rhino observations |
| 36 | summarize_df | rhino_summary | Summary & Chart | Count by Rhino Name |
| 37 | persist_df_wrapper | persist_summary | Summary & Chart | Export summary CSV |
| 38 | set_string_var | set_table_title | Summary & Chart | Table widget title |
| 39 | draw_table | rhino_table | Summary & Chart | Render summary as HTML table |
| 40 | persist_text | persist_table | Summary & Chart | Save table HTML |
| 41 | create_table_widget_single_view | table_widget | Summary & Chart | Table widget |
| 42 | merge_widget_views | merged_table_widget | Summary & Chart | Merge views |
| 43 | set_string_var | set_bar_title | Summary & Chart | Chart widget title |
| 44 | draw_bar_chart | rhino_bar | Summary & Chart | Sighting count bar chart |
| 45 | persist_text | persist_bar | Summary & Chart | Save chart HTML |
| 46 | create_plot_widget_single_view | bar_widget | Summary & Chart | Chart widget |
| 47 | merge_widget_views | merged_bar_widget | Summary & Chart | Merge views |
| 48 | create_docx | rhino_report | — | Generate DOCX report |
| 49 | gather_dashboard | dashboard | — | Dashboard with all widgets |

### Spec.yaml Draft

```yaml
id: mt_rhino

requirements:
  - name: ecoscope-workflows-core
    version: ">=0.22.17, <0.23.0"
    channel: https://repo.prefix.dev/ecoscope-workflows/
  - name: ecoscope-workflows-ext-ecoscope
    version: ">=0.22.17, <0.23.0"
    channel: https://repo.prefix.dev/ecoscope-workflows/
  - name: ecoscope-workflows-ext-custom
    version: ">=0.0.40, <0.1.0"
    channel: https://repo.prefix.dev/ecoscope-workflows-custom/

rjsf-overrides:
  properties:
    Process Patrols.properties.patrol_traj.properties.trajectory_segment_filter.default:
      min_length_meters: 0.001
      max_length_meters: 10000
      min_time_secs: 1
      max_time_secs: 172800
      min_speed_kmhr: 0.01
      max_speed_kmhr: 500
    persist_summary.properties.filetypes.default: ["csv"]
    persist_summary.properties.filetypes.items.enum: ["csv", "parquet"]
    Patrol Map.properties.base_map_defs.properties.base_maps.default:
      - url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}"
        opacity: 1
    rhino_report.properties.template_path.default: "https://raw.githubusercontent.com/wildlife-dynamics/mt-rhino/main/resources/templates/mt_rhino_report_template.docx"

  uiSchema:
    Process Patrols.filter_patrol_coords.filter_point_coords.items.ui:options.label: false
    Process Sightings.filter_event_coords.filter_point_coords.items.ui:options.label: false

task-instance-defaults:
  skipif:
    conditions:
      - any_is_empty_df
      - any_dependency_skipped

workflow:
  # Setup
  - name: Workflow Details
    id: workflow_details
    task: set_workflow_details

  - name: Time Range
    id: time_range
    task: set_time_range
    partial:
      time_format: '%d %b %Y %H:%M:%S %Z'

  - name: Extract Timezone
    id: get_timezone
    task: get_timezone_from_time_range
    partial:
      time_range: ${{ workflow.time_range.return }}

  - name: Data Source
    id: smart_client_name
    task: set_smart_connection

  # Patrol Data Fetching
  - name: Get Patrol Observations
    id: patrol_obs
    task: ecoscope_workflows_ext_ecoscope.tasks.io.get_patrol_observations_from_smart
    partial:
      client: ${{ workflow.smart_client_name.return }}
      time_range: ${{ workflow.time_range.return }}
      ca_uuid: "735606d2-c34e-49c3-a45b-7496ca834e58"
      language_uuid: "13451893-86af-4ec0-beac-2b8e0c2482b5"
      patrol_mandate: null
      patrol_transport: null

  - name: Convert Patrol Observations to Timezone
    id: convert_patrols_tz
    task: convert_values_to_timezone
    partial:
      df: ${{ workflow.patrol_obs.return }}
      timezone: ${{ workflow.get_timezone.return }}
      columns: ["fixtime"]

  # Process Patrols
  - title: Process Patrols
    type: task-group
    description: "Process patrol observations into rhino monitoring trajectories."
    tasks:
      - name: Remove Column Prefix (Observations)
        id: drop_prefix_obs
        task: drop_column_prefix
        partial:
          df: ${{ workflow.convert_patrols_tz.return }}
          prefix: "extra__"
          duplicate_strategy: "suffix"

      - name: Filter Patrol Coordinates
        id: filter_patrol_coords
        task: apply_reloc_coord_filter
        partial:
          df: ${{ workflow.drop_prefix_obs.return }}
          roi_gdf: null
          roi_name: null
          reset_index: false
          bounding_box:
            min_x: -180.0
            max_x: 180.0
            min_y: -90.0
            max_y: 90.0
          filter_point_coords:
            - {x: 180.0, y: 90.0}
            - {x: 0.0, y: 0.0}
            - {x: 1.0, y: 1.0}

      - name: Convert to Trajectories
        id: patrol_traj
        task: relocations_to_trajectory
        partial:
          relocations: ${{ workflow.filter_patrol_coords.return }}

      - name: Remove Column Prefix (Trajectories)
        id: drop_prefix_traj
        task: drop_column_prefix
        partial:
          df: ${{ workflow.patrol_traj.return }}
          prefix: "extra__"
          duplicate_strategy: "suffix"

      - name: Clean Up Trajectory Columns
        id: cleanup_traj_cols
        task: map_columns
        partial:
          df: ${{ workflow.drop_prefix_traj.return }}
          rename_columns: {}
          drop_columns: ["id", "track"]
          retain_columns: []
          raise_if_not_found: false

      - name: Filter Rhino Monitoring Patrols
        id: filter_rhino_patrols
        task: filter_row_values
        partial:
          df: ${{ workflow.cleanup_traj_cols.return }}
          column: "patrol_mandate"
          values: ["Rhino Monitoring"]

      - name: Patrol Trajectory Colormap
        id: patrol_colormap
        task: apply_color_map
        partial:
          df: ${{ workflow.filter_rhino_patrols.return }}
          input_column_name: "station"
          output_column_name: "patrol_colormap"
          colormap: "Dark2"

  # Event Data Fetching
  - name: Get SMART Events
    id: smart_events
    task: ecoscope_workflows_ext_ecoscope.tasks.io.get_events_from_smart
    partial:
      client: ${{ workflow.smart_client_name.return }}
      time_range: ${{ workflow.time_range.return }}
      ca_uuid: "735606d2-c34e-49c3-a45b-7496ca834e58"
      language_uuid: "13451893-86af-4ec0-beac-2b8e0c2482b5"

  - name: Convert Events to Timezone
    id: convert_events_tz
    task: convert_values_to_timezone
    partial:
      df: ${{ workflow.smart_events.return }}
      timezone: ${{ workflow.get_timezone.return }}
      columns: ["time"]

  # Process Rhino Sightings
  - title: Process Sightings
    type: task-group
    description: "Process SMART events into rhino sighting records."
    tasks:
      - name: Filter Event Coordinates
        id: filter_event_coords
        task: apply_reloc_coord_filter
        partial:
          df: ${{ workflow.convert_events_tz.return }}
          roi_gdf: null
          roi_name: null
          reset_index: false
          bounding_box:
            min_x: -180.0
            max_x: 180.0
            min_y: -90.0
            max_y: 90.0
          filter_point_coords:
            - {x: 180.0, y: 90.0}
            - {x: 0.0, y: 0.0}
            - {x: 1.0, y: 1.0}

      - name: Normalize Extracted Attributes
        id: normalize_attrs
        task: normalize_json_column
        partial:
          df: ${{ workflow.filter_event_coords.return }}
          column: "extracted_attributes"
          skip_if_not_exists: true
          sort_columns: true

      - name: Filter Rhino Sightings
        id: process_rhino
        task: apply_sql_query
        partial:
          df: ${{ workflow.normalize_attrs.return }}
          columns:
            - uuid
            - event_type
            - X
            - Y
            - time
            - geometry
            - "extracted_attributes__Rhino Name"
          query: >-
            SELECT uuid, X, Y, time, geometry,
              "extracted_attributes__Rhino Name" AS "Rhino Name"
            FROM df
            WHERE event_type = 'Rhino Direct Observation'
              AND "extracted_attributes__Rhino Name" IS NOT NULL

      - name: Rhino Sighting Colormap
        id: rhino_colormap
        task: apply_color_map
        partial:
          df: ${{ workflow.process_rhino.return }}
          input_column_name: "Rhino Name"
          output_column_name: "rhino_colormap"
          colormap: "Dark2"

  # Data Exports
  - name: Persist Patrol Trajectories
    id: persist_patrol_traj
    task: persist_df_wrapper
    partial:
      df: ${{ workflow.filter_rhino_patrols.return }}
      root_path: ${{ env.ECOSCOPE_WORKFLOWS_RESULTS }}
      filename_prefix: "rhino_patrol_trajectories"
      filetypes: ["parquet"]
      sanitize: true
    skipif:
      conditions:
        - never

  - name: Persist Rhino Observations
    id: persist_rhino_obs
    task: persist_df_wrapper
    partial:
      df: ${{ workflow.process_rhino.return }}
      root_path: ${{ env.ECOSCOPE_WORKFLOWS_RESULTS }}
      filename_prefix: "rhino_observations"
      filetypes: ["parquet"]
      sanitize: true
    skipif:
      conditions:
        - never

  # Map Settings
  - name: Base Maps
    id: base_map_defs
    task: set_base_maps

  # Patrol Map
  - title: Patrol Map
    type: task-group
    description: "Generate patrol trajectory map."
    tasks:
      - name: Set Patrol Map Title
        id: set_patrol_map_title
        task: set_string_var
        partial:
          var: "Rhino Patrol Trajectories"

      - name: Rename Trajectory Columns for Display
        id: rename_traj_cols
        task: map_columns
        partial:
          df: ${{ workflow.patrol_colormap.return }}
          rename_columns:
            segment_start: "Start Time"
            timespan_seconds: "Duration (s)"
            speed_kmhr: "Speed (kph)"
          drop_columns: []
          retain_columns: []
          raise_if_not_found: false

      - name: Create Patrol Polyline Layer
        id: patrol_polyline
        task: create_polyline_layer
        skipif:
          conditions:
            - any_is_empty_df
            - any_dependency_skipped
            - all_geometry_are_none
        partial:
          geodataframe: ${{ workflow.rename_traj_cols.return }}
          layer_style:
            get_width: 3
            width_units: "pixels"
            color_column: "patrol_colormap"
          legend:
            label_column: "station"
            color_column: "patrol_colormap"
          tooltip_columns: ["Start Time", "Duration (s)", "Speed (kph)"]

      - name: Draw Patrol Ecomap
        id: patrol_ecomap
        task: draw_ecomap
        partial:
          geo_layers: ${{ workflow.patrol_polyline.return }}
          tile_layers: ${{ workflow.base_map_defs.return }}
          north_arrow_style:
            placement: "top-left"
          legend_style:
            title: "Station"
            placement: "bottom-right"
          static: false
          title: null
          max_zoom: 20

      - name: Persist Patrol Ecomap
        id: persist_patrol_ecomap
        task: persist_text
        partial:
          text: ${{ workflow.patrol_ecomap.return }}
          root_path: ${{ env.ECOSCOPE_WORKFLOWS_RESULTS }}
          filename_suffix: "patrol_map"

      - name: Create Patrol Map Widget
        id: patrol_map_widget
        task: create_map_widget_single_view
        skipif:
          conditions:
            - never
        partial:
          title: ${{ workflow.set_patrol_map_title.return }}
          data: ${{ workflow.persist_patrol_ecomap.return }}

      - name: Merge Patrol Map Widget
        id: merged_patrol_map
        task: merge_widget_views
        partial:
          widgets:
            - ${{ workflow.patrol_map_widget.return }}

  # Rhino Sighting Map
  - title: Rhino Map
    type: task-group
    description: "Generate rhino sighting point map."
    tasks:
      - name: Set Rhino Map Title
        id: set_rhino_map_title
        task: set_string_var
        partial:
          var: "Rhino Sightings"

      - name: Create Rhino Point Layer
        id: rhino_point_layer
        task: create_point_layer
        skipif:
          conditions:
            - any_is_empty_df
            - any_dependency_skipped
            - all_geometry_are_none
        partial:
          geodataframe: ${{ workflow.rhino_colormap.return }}
          layer_style:
            get_radius: 5.0
            fill_color_column: "rhino_colormap"
          legend:
            label_column: "Rhino Name"
            color_column: "rhino_colormap"
          tooltip_columns: ["Rhino Name", "time"]

      - name: Draw Rhino Ecomap
        id: rhino_ecomap
        task: draw_ecomap
        partial:
          geo_layers: ${{ workflow.rhino_point_layer.return }}
          tile_layers: ${{ workflow.base_map_defs.return }}
          north_arrow_style:
            placement: "top-left"
          legend_style:
            title: "Rhino Name"
            placement: "bottom-right"
          static: false
          title: null
          max_zoom: 13

      - name: Persist Rhino Ecomap
        id: persist_rhino_ecomap
        task: persist_text
        partial:
          text: ${{ workflow.rhino_ecomap.return }}
          root_path: ${{ env.ECOSCOPE_WORKFLOWS_RESULTS }}
          filename_suffix: "rhino_map"

      - name: Create Rhino Map Widget
        id: rhino_map_widget
        task: create_map_widget_single_view
        skipif:
          conditions:
            - never
        partial:
          title: ${{ workflow.set_rhino_map_title.return }}
          data: ${{ workflow.persist_rhino_ecomap.return }}

      - name: Merge Rhino Map Widget
        id: merged_rhino_map
        task: merge_widget_views
        partial:
          widgets:
            - ${{ workflow.rhino_map_widget.return }}

  # Rhino Summary & Bar Chart
  - title: Summary and Chart
    type: task-group
    description: "Summarize rhino sightings and generate bar chart."
    tasks:
      - name: Summarize Rhino Sightings
        id: rhino_summary
        task: summarize_df
        partial:
          df: ${{ workflow.process_rhino.return }}
          groupby_cols: ["Rhino Name"]
          reset_index: true
          summary_params:
            - display_name: "Count"
              aggregator: count
              column: uuid

      - name: Persist Rhino Summary
        id: persist_summary
        task: persist_df_wrapper
        partial:
          df: ${{ workflow.rhino_summary.return }}
          root_path: ${{ env.ECOSCOPE_WORKFLOWS_RESULTS }}
          filename_prefix: "rhino_summary"
          filetypes: ["csv"]
          sanitize: false
        skipif:
          conditions:
            - never

      - name: Set Summary Table Title
        id: set_table_title
        task: set_string_var
        partial:
          var: "Rhino Sighting Summary"

      - name: Draw Summary Table
        id: rhino_table
        task: draw_table
        partial:
          dataframe: ${{ workflow.rhino_summary.return }}
          columns: ["Rhino Name", "Count"]
          table_config:
            enable_sorting: true
            enable_filtering: true
            enable_download: true
            hide_header: false

      - name: Persist Summary Table
        id: persist_table
        task: persist_text
        partial:
          text: ${{ workflow.rhino_table.return }}
          root_path: ${{ env.ECOSCOPE_WORKFLOWS_RESULTS }}
          filename_suffix: "rhino_summary_table"

      - name: Create Summary Table Widget
        id: table_widget
        task: create_table_widget_single_view
        skipif:
          conditions:
            - never
        partial:
          title: ${{ workflow.set_table_title.return }}
          data: ${{ workflow.persist_table.return }}

      - name: Merge Summary Table Widget
        id: merged_table_widget
        task: merge_widget_views
        partial:
          widgets:
            - ${{ workflow.table_widget.return }}

      - name: Set Bar Chart Title
        id: set_bar_title
        task: set_string_var
        partial:
          var: "Rhino Sighting Counts"

      - name: Draw Rhino Bar Chart
        id: rhino_bar
        task: draw_bar_chart
        partial:
          dataframe: ${{ workflow.rhino_summary.return }}
          category: "Rhino Name"
          layout_kwargs: null
          bar_chart_configs:
            - label: "Count of Sightings"
              column: "Count"
              agg_func: "sum"
              show_label: true
              style:
                marker_color: "#35b779"

      - name: Persist Bar Chart
        id: persist_bar
        task: persist_text
        partial:
          text: ${{ workflow.rhino_bar.return }}
          root_path: ${{ env.ECOSCOPE_WORKFLOWS_RESULTS }}
          filename_suffix: "rhino_bar_chart"

      - name: Create Bar Chart Widget
        id: bar_widget
        task: create_plot_widget_single_view
        skipif:
          conditions:
            - never
        partial:
          title: ${{ workflow.set_bar_title.return }}
          data: ${{ workflow.persist_bar.return }}

      - name: Merge Bar Chart Widget
        id: merged_bar_widget
        task: merge_widget_views
        partial:
          widgets:
            - ${{ workflow.bar_widget.return }}

  # Report
  - name: Create Rhino Report
    id: rhino_report
    task: ecoscope_workflows_ext_custom.tasks.results.create_docx
    partial:
      context:
        items:
          - item_type: timerange
            key: report_date
            value: ${{ workflow.time_range.return }}
            format: "%b %Y"
          - item_type: image
            key: patrol_map
            value: ${{ workflow.persist_patrol_ecomap.return }}
            screenshot_config:
              wait_for_timeout: 20000
              max_concurrent_pages: 2
              device_scale_factor: 1.0
          - item_type: image
            key: rhino_map
            value: ${{ workflow.persist_rhino_ecomap.return }}
            screenshot_config:
              wait_for_timeout: 1000
              max_concurrent_pages: 2
              device_scale_factor: 1.0
          - item_type: table
            key: rhino_summary
            value: ${{ workflow.rhino_summary.return }}
          - item_type: image
            key: bar_chart
            value: ${{ workflow.persist_bar.return }}
            screenshot_config:
              wait_for_timeout: 0
              max_concurrent_pages: 2
      groupers: []
      output_dir: ${{ env.ECOSCOPE_WORKFLOWS_RESULTS }}
      filename_prefix: mt_rhino_report
    skipif:
      conditions:
        - never

  # Dashboard
  - name: Create Dashboard
    id: dashboard
    task: gather_dashboard
    partial:
      details: ${{ workflow.workflow_details.return }}
      widgets:
        - ${{ workflow.merged_patrol_map.return }}
        - ${{ workflow.merged_rhino_map.return }}
        - ${{ workflow.merged_table_widget.return }}
        - ${{ workflow.merged_bar_widget.return }}
      groupers: []
      time_range: ${{ workflow.time_range.return }}
```

### Task Gaps

None — all tasks exist in core/ecoscope/custom libraries. Uses fully-qualified task names for SMART-specific tasks (`ecoscope_workflows_ext_ecoscope.tasks.io.get_patrol_observations_from_smart`, `ecoscope_workflows_ext_ecoscope.tasks.io.get_events_from_smart`) and custom tasks (`ecoscope_workflows_ext_custom.tasks.results.create_docx`).

## Development Strategy

### Data Source Approach

3-phase approach — both data sources are remote SMART APIs.

### Phase 1 — Bootstrap Data

**Download workflows:** Use existing `wt-download-patrols` and `wt-download-events` in `/Users/yunwu/MEP/wt/`.

| Data | Source Task | Output Format | Output Path |
| ---- | ----------- | ------------- | ----------- |
| Patrol observations | get_patrol_observations_from_smart | Parquet | `resources/mock-data/mock_patrol_reloc.parquet` |
| SMART events | get_events_from_smart | Parquet | `resources/mock-data/mock_smart_events.parquet` |

### Phase 2 — Develop with Local Data

**load_df stand-in configuration:**

```yaml
# Replace patrol fetch with:
- name: Load Patrol Observations
  id: patrol_obs
  task: ecoscope_workflows_ext_custom.tasks.io.load_df
  partial:
    deserialize_json: false

# Replace event fetch with:
- name: Load SMART Events
  id: smart_events
  task: ecoscope_workflows_ext_custom.tasks.io.load_df
  partial:
    deserialize_json: false
```

Comment out `set_smart_connection` task as well.

**What to complete in Phase 2:**
- [ ] Full patrol pipeline (relocations -> trajectories -> filter Rhino Monitoring -> polyline map)
- [ ] Full sighting pipeline (events -> filter Rhino Direct Observation -> point map)
- [ ] Summary table and bar chart validated
- [ ] All CSV exports generated
- [ ] DOCX report renders correctly with all sections
- [ ] Dashboard renders with 3 widgets
- [ ] rjsf form configured and validated
- [ ] Base test case passing with local data

### Phase 3 — Reconnect Live Data Source

Uncomment `set_smart_connection`, `get_patrol_observations_from_smart`, and `get_events_from_smart`. Remove `load_df` stand-ins. Update test-cases.yaml to use `mock_io: false` with real mara_triangle connection.

**Final data source configuration:**

```yaml
# Restore patrol fetch:
- name: Get Patrol Observations
  id: patrol_obs
  task: ecoscope_workflows_ext_ecoscope.tasks.io.get_patrol_observations_from_smart
  partial:
    client: ${{ workflow.smart_client_name.return }}
    time_range: ${{ workflow.time_range.return }}
    ca_uuid: "735606d2-c34e-49c3-a45b-7496ca834e58"
    language_uuid: "13451893-86af-4ec0-beac-2b8e0c2482b5"
    patrol_mandate: null
    patrol_transport: null

# Restore event fetch:
- name: Get SMART Events
  id: smart_events
  task: ecoscope_workflows_ext_ecoscope.tasks.io.get_events_from_smart
  partial:
    client: ${{ workflow.smart_client_name.return }}
    time_range: ${{ workflow.time_range.return }}
    ca_uuid: "735606d2-c34e-49c3-a45b-7496ca834e58"
    language_uuid: "13451893-86af-4ec0-beac-2b8e0c2482b5"
```

**Test case updates:**
- Update `base` case: `mock_io: true` (mocked API)
- Add `integration` case: `mock_io: false` with real SMART API credentials and time range
- Verify data shape from live source matches Phase 2 development data

## Output Configuration

### Maps

| Map | Layer Type | Style Config | Legend | Notes |
| --- | ---------- | ------------ | ------ | ----- |
| Rhino Patrol Trajectories | `create_polyline_layer` | `get_width: 3`, `color_column: patrol_colormap` | label: station, color: patrol_colormap, bottom-right | Interactive, north arrow top-left |
| Rhino Sightings | `create_point_layer` | `get_radius: 5.0`, `fill_color_column: rhino_colormap` | label: Rhino Name, color: rhino_colormap, bottom-right | Interactive, north arrow top-left, max_zoom: 13 |

**Patrol Polyline Layer Style:**
```yaml
layer_style:
  get_width: 3
  width_units: "pixels"
  color_column: "patrol_colormap"
legend:
  label_column: "station"
  color_column: "patrol_colormap"
tooltip_columns: ["Start Time", "Duration (s)", "Speed (kph)"]
```

**Rhino Point Layer Style:**
```yaml
layer_style:
  get_radius: 5.0
  fill_color_column: "rhino_colormap"
legend:
  label_column: "Rhino Name"
  color_column: "rhino_colormap"
tooltip_columns: ["Rhino Name", "time"]
```

**Colormaps:** Both use `Dark2` matplotlib colormap (consistent with desktop workflows).

### Charts

| Chart | Type | X Column | Y Column | Category | Notes |
| ----- | ---- | -------- | -------- | -------- | ----- |
| Rhino Sighting Counts | `draw_bar_chart` | — | Count | Rhino Name | Single bar series, green (#35b779) |

### Data Exports

| Export | Format | Sanitize | Notes |
| ------ | ------ | -------- | ----- |
| Patrol trajectories | Parquet | true | Raw Rhino Monitoring patrol trajectories, skipif: never |
| Rhino observations | Parquet | true | Raw rhino sighting events, skipif: never |
| Rhino sighting summary | CSV | false | Count by Rhino Name, skipif: never |

### DOCX Report

| Item | Type | Source | Notes |
| ---- | ---- | ------ | ----- |
| Report date | timerange | time_range | Format: "%b %Y" |
| Patrol map | image | persist_patrol_ecomap | Screenshot with 20s wait (map tiles) |
| Rhino sighting map | image | persist_rhino_ecomap | Screenshot with 1s wait |
| Rhino summary | table | rhino_summary | DataFrame rendered as table |
| Bar chart | image | persist_bar | Screenshot, no wait |

No report groupers — single report section with all content.

### Widget & Dashboard Assembly

| Widget | Type | Title Source | Content Source |
| ------ | ---- | ------------ | -------------- |
| Patrol Trajectories Map | `create_map_widget_single_view` | set_patrol_map_title | persist_patrol_ecomap |
| Rhino Sightings Map | `create_map_widget_single_view` | set_rhino_map_title | persist_rhino_ecomap |
| Rhino Sighting Summary | `create_table_widget_single_view` | set_table_title | persist_table |
| Sighting Count Bar Chart | `create_plot_widget_single_view` | set_bar_title | persist_bar |

No grouping — widgets are created as direct calls (no mapvalues), wrapped via merge_widget_views.

**gather_dashboard:**
```yaml
details: ${{ workflow.workflow_details.return }}
widgets:
  - ${{ workflow.merged_patrol_map.return }}
  - ${{ workflow.merged_rhino_map.return }}
  - ${{ workflow.merged_table_widget.return }}
  - ${{ workflow.merged_bar_widget.return }}
groupers: []
time_range: ${{ workflow.time_range.return }}
```

## Form Configuration (rjsf)

### Parameter Visibility

| Parameter | Basic / Advanced | Default | Notes |
| --------- | ---------------- | ------- | ----- |
| workflow_details | Basic | — | Name and description |
| smart_client_name | Basic | — | SMART connection |
| time_range | Basic | — | Since/until |
| patrol_obs (ca_uuid, language_uuid) | Advanced (partial) | Mara Triangle UUIDs | Hardcoded in spec |
| patrol_traj.trajectory_segment_filter | Advanced | Sensible defaults via rjsf-overrides | Filter thresholds |
| filter_patrol_coords.filter_point_coords | Advanced | Bad coord filter | Labels hidden via uiSchema |
| filter_event_coords.filter_point_coords | Advanced | Bad coord filter | Labels hidden via uiSchema |
| process_rhino.query | Advanced | SQL filter | Default query set in spec |
| persist_summary.filetypes | Advanced | ["csv"] | Constrained to csv/parquet |
| base_map_defs | Advanced | ArcGIS World Topo | Default map tiles |
| rhino_report.template_path | Advanced | GitHub-hosted template | DOCX template URL |

### rjsf-overrides Draft

```yaml
rjsf-overrides:
  properties:
    Process Patrols.properties.patrol_traj.properties.trajectory_segment_filter.default:
      min_length_meters: 0.001
      max_length_meters: 10000
      min_time_secs: 1
      max_time_secs: 172800
      min_speed_kmhr: 0.01
      max_speed_kmhr: 500
    persist_summary.properties.filetypes.default: ["csv"]
    persist_summary.properties.filetypes.items.enum: ["csv", "parquet"]
    Patrol Map.properties.base_map_defs.properties.base_maps.default:
      - url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}"
        opacity: 1
    rhino_report.properties.template_path.default: "https://raw.githubusercontent.com/wildlife-dynamics/mt-rhino/main/resources/templates/mt_rhino_report_template.docx"

  uiSchema:
    Process Patrols.filter_patrol_coords.filter_point_coords.items.ui:options.label: false
    Process Sightings.filter_event_coords.filter_point_coords.items.ui:options.label: false
```

### Validation Checklist

- [x] Trajectory filter defaults are sensible for patrol data
- [x] Export filetypes constrained to csv/parquet
- [x] Base map defaults to ArcGIS World Topo (good for Africa)
- [x] DOCX template URL defaults to main branch
- [x] Coordinate filter point labels hidden (technical, not user-facing)

## Test Strategy

### Test Cases

| Case Name | mock_io | Purpose |
| --------- | ------- | ------- |
| base | false | Full integration test against real SMART API |

### test-cases.yaml Draft

```yaml
base:
  name: Mara Triangle Rhino Report
  mock_io: false
  params:
    workflow_details:
      name: "Mara Triangle Rhino Report"
    time_range:
      since: "2026-02-01T00:00:00+03:00"
      until: "2026-02-28T23:59:59+03:00"
      time_zone: "Africa/Nairobi"
    smart_client_name:
      data_source:
        name: "mara_triangle"
    base_map_defs:
      base_maps:
        - url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}"
          opacity: 1
```

### Data Source Testing

| Data Source | mock_io: false requirements |
| ----------- | --------------------------- |
| SMART Patrols | Real SMART API with mara_triangle connection |
| SMART Events | Real SMART API with mara_triangle connection |

### skipif Conditions

| Task | Conditions | Rationale |
| ---- | ---------- | --------- |
| (all tasks) | any_is_empty_df, any_dependency_skipped | Global default |
| patrol_polyline | + all_geometry_are_none | Skip if no valid geometries |
| rhino_point_layer | + all_geometry_are_none | Skip if no valid geometries |
| patrol_map_widget | never | Always create widget placeholder |
| rhino_map_widget | never | Always create widget placeholder |
| table_widget | never | Always create widget placeholder |
| bar_widget | never | Always create widget placeholder |
| persist_patrol_traj | never | Always export |
| persist_rhino_obs | never | Always export |
| persist_summary | never | Always export |
| rhino_report | never | Always generate report |

### Validation Approach

- Integration test: verify SMART API returns data for the specified time range
- Verify trajectory conversion produces valid LineString geometries
- Verify patrol mandate filter correctly isolates "Rhino Monitoring" patrols
- Verify rhino sighting SQL extracts Rhino Name and filters nulls
- Verify summary has expected columns (Rhino Name, Count)
- Verify bar chart renders with correct categories
- Verify DOCX report renders with all sections (patrol map, sighting map, summary table, bar chart)
- Verify dashboard displays 3 widgets

## Dashboard Layout

### layout.json Draft

```json
[
    {
        "i": "0",
        "x": 0, "y": 0,
        "w": 5, "h": 12,
        "minW": 5, "minH": 10,
        "widget_id": 0,
        "static": false
    },
    {
        "i": "1",
        "x": 5, "y": 0,
        "w": 5, "h": 12,
        "minW": 5, "minH": 10,
        "widget_id": 1,
        "static": false
    },
    {
        "i": "2",
        "x": 0, "y": 12,
        "w": 5, "h": 10,
        "minW": 4, "minH": 8,
        "widget_id": 2,
        "static": false
    },
    {
        "i": "3",
        "x": 5, "y": 12,
        "w": 5, "h": 10,
        "minW": 4, "minH": 8,
        "widget_id": 3,
        "static": false
    }
]
```

Widget 0: Patrol trajectory map (top-left), Widget 1: Rhino sighting map (top-right), Widget 2: Summary table (bottom-left), Widget 3: Bar chart (bottom-right).

## Implementation Plan

### Tasks

- [ ] Task 1: Bootstrap data from SMART API
  - Action: Run wt-download-patrols and wt-download-events to get `mock_patrol_reloc.parquet` and `mock_smart_events.parquet`

- [ ] Task 2: Scaffold repo and create spec.yaml with Phase 2 load_df
  - File: `spec.yaml`
  - Action: Full pipeline from load_df through DOCX report and dashboard

- [ ] Task 3: Create DOCX report template
  - File: `resources/templates/mt_rhino_report_template.docx`
  - Action: Design template with placeholders for patrol_map, rhino_map, rhino_summary, bar_chart, report_date

- [ ] Task 4: Create test-cases.yaml
  - File: `test-cases.yaml`
  - Action: Base test case with mocked I/O

- [ ] Task 5: Compile, test, validate outputs
  - Action: Compile, run tests, visually inspect maps/chart/report/dashboard

- [ ] Task 6: Configure rjsf-overrides and layout.json
  - File: `spec.yaml` (rjsf-overrides section), `layout.json`
  - Action: Set defaults, validate form rendering, configure dashboard layout

- [ ] Task 7: Reconnect SMART API (Phase 3)
  - File: `spec.yaml`, `test-cases.yaml`
  - Action: Restore SMART fetch tasks, add integration test case

### Acceptance Criteria

- [ ] AC 1: Given SMART patrol data, when the workflow runs, then only "Rhino Monitoring" mandate patrols are shown on the trajectory map colored by station
- [ ] AC 2: Given SMART event data, when filtered for rhino sightings, then point map shows sighting locations colored by individual Rhino Name
- [ ] AC 3: Given rhino sightings, when summarized, then CSV export contains sighting count per Rhino Name
- [ ] AC 4: Given rhino summary data, when bar chart is drawn, then chart shows count per Rhino Name
- [ ] AC 5: Given all outputs, when DOCX report is generated, then report contains patrol map, sighting map, summary table, and bar chart
- [ ] AC 6: Given all outputs, when dashboard is rendered, then 4 widgets display (patrol map, sighting map, summary table, bar chart)
- [ ] AC 7: Given no patrol or sighting data for the time range, when the workflow runs, then skipif conditions prevent errors and report/exports are still generated
- [ ] AC 8: Given the rjsf form, when rendered, then trajectory filter has sensible defaults, filetypes are constrained, and coordinate filter labels are hidden

## Additional Context

### Dependencies

- ecoscope-workflows-core >= 0.22.17
- ecoscope-workflows-ext-ecoscope >= 0.22.17
- ecoscope-workflows-ext-custom >= 0.0.40
- DOCX template hosted on GitHub (wildlife-dynamics/mt-rhino)

### Notes

- SMART tasks use fully-qualified names because they are conservancy-specific
- Patrol mandate filtering is done downstream via `filter_row_values` (not at API level) because the SMART API `patrol_mandate` param may require a UUID
- Polyline layer uses `color_column` (not `get_color_column`) — matches mt-patrols convention
- Both colormaps use Dark2, matching the existing desktop workflow styling
- No grouping/splitting — all data is processed as a single group, dashboard shows widgets directly without filter dropdowns
- The `load_df` stand-in is kept as a comment in spec.yaml for easy Phase 2/3 switching
