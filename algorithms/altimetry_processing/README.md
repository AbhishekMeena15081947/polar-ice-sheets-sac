# Altimetry Processing

## Overview
This module contains algorithms and tools for processing satellite altimetry data from various missions including SARAL/AltiKa, ICESat-2, CryoSat-2, and Sentinel-3.

## Key Features
- Multi-mission altimetry data loading and preprocessing
- Waveform retracking algorithms
- Elevation change detection
- Trend analysis and time-series processing
- Data quality control and filtering

## Data Sources
- **SARAL/AltiKa**: Ka-band radar altimeter data
- **ICESat-2**: Laser altimetry (ATL06, ATL08 products)
- **CryoSat-2**: Ku-band radar altimeter (SARIn mode)
- **Sentinel-3**: Dual-frequency altimeter

## Algorithms

### 1. Data Loading
```python
from algorithms.altimetry_processing import load_altimetry

# Load SARAL/AltiKa data
data = load_altimetry('path/to/saral_data.nc', mission='saral')
```

### 2. Waveform Retracking
Implements various retracking algorithms:
- Threshold retracking
- OCOG (Offset Centre of Gravity)
- Ice Sheet retracking
- Sea ice retracking

### 3. Elevation Change Analysis
```python
from algorithms.altimetry_processing import compute_elevation_change

# Compute elevation changes over time
delev = compute_elevation_change(data, method='repeat_track')
```

## Scripts
- `load_data.py`: Data loading utilities
- `retracking.py`: Waveform retracking algorithms
- `preprocessing.py`: Data cleaning and filtering
- `elevation_change.py`: Elevation trend analysis
- `validation.py`: Cross-validation with other datasets

## Requirements
```bash
pip install numpy xarray netCDF4 scipy
```

## Usage Example
```python
import numpy as np
from algorithms.altimetry_processing import AltimetryProcessor

# Initialize processor
processor = AltimetryProcessor(mission='icesat2')

# Load and process data
data = processor.load_data('ATL06_data.h5')
processed = processor.preprocess(data)
elevation_change = processor.compute_trends(processed, period='2018-2024')

print(f"Mean elevation change: {np.mean(elevation_change):.3f} m/year")
```

## References
1. Zwally et al. (2002). "ICESat's laser measurements of polar ice"
2. Aublanc et al. (2018). "SARAL/AltiKa over polar ice"
3. McMillan et al. (2014). "Three-dimensional mapping by CryoSat-2"
