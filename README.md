# 🌍 GeoFlow: Geospatial Data Engineering Pipeline
### GeoFlow is an end-to-end ETL (Extract, Transform, Load) pipeline designed for large-scale urban data processing and spatial modeling. It demonstrates the transition from raw OpenStreetMap (OSM) data to a structured, classified, and indexed spatial database ready for high-volume production environments.

### Technical Stack
Language: Python 3.14
Database: PostgreSQL 15 + PostGIS (Containerized via Docker)
Core Libraries:
GeoPandas & Pandas (Data manipulation & cleaning)
SQLAlchemy 2.0 (Modern database ORM/Interface)
OSMNX (Overpass API wrapper for geographic data extraction)
Matplotlib & Contextily (Spatial visualization & mapping)
Infrastructure: Docker & Docker Compose (Infrastructure as Code)

### 🏗️ Architecture & Pipeline Steps
#### 1. Data Ingestion (ingest_data.py)
The pipeline extracts real-world building footprints from OpenStreetMap.

Validation: Ensures coordinate reference systems (CRS) are aligned (WGS84 - EPSG:4326).

Database Loading: Uses a robust SQLAlchemy 2.0 connection manager to handle high-volume inserts into PostGIS.

#### 2. Spatial Classification & Modeling (classify_data.py)
This stage implements applied research logic directly into the database layer for maximum efficiency.

Spatial Indexing: Implements GIST Indexes on geometries to optimize query performance for national-scale datasets.

Feature Engineering: Uses PostGIS spatial functions (ST_Area, ST_Transform) to automatically classify urban zones into Industrial/Commercial or Residential/Small based on building footprints.

<img width="1262" height="110" alt="classification in terminal" src="https://github.com/user-attachments/assets/528c5d37-ad40-46d0-8b10-e2129d4c1927" />


#### 3. Analytics & Visualization (visualize_map.py)
Generates high-resolution analytical maps that combine processed vector data with raster basemaps.
Visual Validation: Displays color-coded classifications over real-world street maps to verify model accuracy.

<img width="800" height="800" alt="analiza_urbana_bucuresti" src="https://github.com/user-attachments/assets/05c92d27-a851-4cb4-a4ce-3f9e93d9db4c" />


## 🔧 Troubleshooting & Lessons Learned

During the development of this pipeline, several technical challenges were addressed:

* **Database Connection Issues:** Encountered `Connection Refused` errors due to local port conflicts (default 5432 was occupied). 
    * *Solution:* Remapped the Docker container to port `5433` and updated the SQLAlchemy engine strings accordingly.
* **SQLAlchemy 2.0 Compatibility:** Faced `AttributeError: 'Engine' object has no attribute 'cursor'` and geometry serialization errors with older GeoPandas methods.
    * *Solution:* Migrated to explicit connection management using `with engine.connect()` and ensured all raw SQL commands are wrapped in `text()` for SQLAlchemy 2.0 compliance.
* **Spatial Data Types:** Initial attempts resulted in "geometry not a string" errors.
    * *Solution:* Explicitly defined the geometry column type during the `to_postgis` call and implemented a fallback WKT (Well-Known Text) ingestion method for maximum robustness.
* **Performance:** Large city datasets can be slow to process.
    * *Solution:* Implemented **GIST (Generalized Search Tree)** indexing in PostGIS to speed up spatial area calculations and filtering.
