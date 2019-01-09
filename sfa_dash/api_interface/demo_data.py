site = {
  "elevation": 595.0,
  "extra_parameters": {
    "net_work_api_abbreviation": "AS",
    "network": "Universit of Oregon SRML",
    "network_api_id": "94040"
  },
  "latitude": 42.19,
  "longitude": -122.7,
  "modeling_parameters": {
    "ac_power": "",
    "axis_azimuth": 45.0,
    "axis_tilt": 45.0,
    "backtrack": True,
    "dc_power": "",
    "gamma_pdc": "",
    "ground_coverage_ratio": 0.5,
    "surface_azimuth": 45.0,
    "surface_tilt": 45.0,
    "tracking_type": "",
  },
  "name": "Ashland OR",
  "provider": "Reference",
  "site_id": "123e4567-e89b-12d3-a456-426655440001",
  "timezone": "Etc/GMT+8"
}
site_1 ={
   "elevation": 786.0,
   "extra_parameters": {
       "network": "NREL MIDC",
   },
   "latitude": 32.22969,
   "longitude": -110.95534,
   "modeling_parameters": {
       "ac_power": "",
       "axis_azimuth": 45.0,
       "axis_tilt": 45.0,
       "backtrack": True,
       "dc_power": "",
       "gamma_pdc": "",
       "ground_coverage_ratio": 0.5,
       "surface_azimuth": 45.0,
       "surface_tilt": 45.0,
       "tracking_type": ""
    },
    "name": "SOLRMAP University of Arizona (OASIS)",
    "provider": "Reference",
    "site_id": "d2018f1d-82b1-422a-8ec4-4e8b3fe92a4a",
    "timezone": "America/Pheonix"
}
site_2 = {
    "elevation": 786.0,
    "extra_parameters": {
        "network": "SURFRAD",
    },
    "latitude": 43.73403,
    "longitude": -96.62328,
    "modeling_parameters": {
        "ac_power": "",
        "axis_azimuth": 45.0,
        "axis_tilt": 45.0,
        "backtrack": True,
        "dc_power": "",
        "gamma_pdc": "",
        "ground_coverage_ratio": 0.5,
        "surface_azimuth": 45.0,
        "surface_tilt": 45.0,
        "tracking_type": ""
    },
    "name": "Sioux Falls, SD",
    "provider": "Reference",
    "site_id": "8594d9a2-a23d-4f62-a410-5dddcba583a7",
    "timezone": "Etc/GMT+6"
}
observation = {
    "extra_parameters": {
      "instrument": "Ascension Technology Rotating Shadowband Pyranometer"
    },
    "name": "Ashland OR, ghi",
    "obs_id": "123e4567-e89b-12d3-a456-426655440000",
    "provider": "UO SRML",
    "site": site,
    "site_id": "123e4567-e89b-12d3-a456-426655440001",
    "variable": "ghi",
    "Value Type": "Interval Mean",
    "Interval Label": "Start"
}
observation_1 = {
    "extra_parameters": {
      "instrument": "Ascension Technology Rotating Shadowband Pyranometer"
    },
    "name": "Ashland OR, dhi",
    "obs_id": "9cfa4aa2-7d0f-4f6f-a1c1-47f75e1d226f",
    "provider": "UO SRML",
    "site": site,
    "site_id": "123e4567-e89b-12d3-a456-426655440001",
    "variable": "dhi",
    "Value Type": "Interval Mean",
    "Interval Label": "Start"
}
observation_2 = {
    "extra_parameters": {
      "instrument": "Ascension Technology Rotating Shadowband Pyranometer"
    },
    "name": "Ashland OR, dni",
    "obs_id": "9ce9715c-bd91-47b7-989f-50bb558f1eb9",
    "provider": "UO SRML",
    "site": site,
    "site_id": "123e4567-e89b-12d3-a456-426655440001",
    "variable": "dni",
    "Value Type": "Interval Mean",
    "Interval Label": "Start"
}
observation_3 = {
    "extra_parameters": {
      "instrument": "Kipp & Zonen CMP 22 Pyranometer"
    },
    "name": "OASIS, ghi",
    "obs_id": "548a6c6e-a685-4690-87a8-ba7aab448bdb",
    "provider": "University of Arizona",
    "site": site_1,
    "site_id": "d2018f1d-82b1-422a-8ec4-4e8b3fe92a4a",
    "variable": "ghi",
    "Value Type": "Interval Mean",
    "Interval Label": "Start"
}
observation_4 = {
    "extra_parameters": {
      "instrument": "Kipp & Zonen CMP 22 Pyranometer"
    },
    "name": "Sioux Falls, ghi",
    "obs_id": "89d0ffa-936f-4d8e-8ad3-4241040e88d8",
    "provider": "NOAA",
    "site": site_2,
    "site_id": "8594d9a2-a23d-4f62-a410-5dddcba583a7",
    "variable": "ghi",
    "Value Type": "Interval Mean",
    "Interval Label": "Start"
}

forecast = {
  "forecast_id": "f79e4f84-e2c3-11e8-9f32-f2801f1b9fd1",
  "name": "Ashland OR, ghi",
  "provider": "University of Arizona",
  "site": {
    "elevation": 595.0,
    "extra_parameters": {
      "net_work_api_abbreviation": "AS",
      "network": "UO SRML",
      "network_api_id": "94040"
    },
    "latitude": 42.19,
    "longitude": -122.7,
    "modeling_parameters": {
      "ac_power": "",
      "axis_azimuth": 45.0,
      "axis_tilt": 45.0,
      "backtrack": True, 
      "dc_power": "",
      "gamma_pdc": "",
      "ground_coverage_ratio": 0.5,
      "surface_azimuth": 45.0,
      "surface_tilt": 45.0,
      "tracking_type": ""
    },
    "name": "Ashland OR",
    "timezone": "Etc/GMT+8"
  },
  "site_id": "123e4567-e89b-12d3-a456-426655440001",
  "variable": "ghi"
}
observations = [ observation, observation_1, observation_2 ]
forecasts = [forecast, forecast, forecast]
sites = [site, site_1, site_2]
