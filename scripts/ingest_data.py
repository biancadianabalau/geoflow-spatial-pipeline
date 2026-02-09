import osmnx as ox
from sqlalchemy import create_engine, text
import geopandas as gpd

engine = create_engine('postgresql://YOUR_USER_AND_PASSWORD/geodata')

def fetch_and_store_city(city_name):
    print(f"Fetching data for {city_name}...")
    
    
    buildings = ox.features_from_place(city_name, tags={'building': True})
    
   
    buildings = buildings[['geometry', 'building']].reset_index().head(1000)
    
   
    buildings = buildings.to_crs(epsg=4326)

    print("Uploading to PostGIS via SQLAlchemy Engine...")
    
 
    with engine.connect() as connection:
        
        connection.execute(text("DROP TABLE IF EXISTS buildings CASCADE;"))
        connection.commit()
        
        # Upload
        buildings.to_postgis(
            name='buildings', 
            con=connection, 
            if_exists='replace', 
            index=False
        )
    
    print("Done")

if __name__ == "__main__":
    fetch_and_store_city("Bucharest, Romania")
