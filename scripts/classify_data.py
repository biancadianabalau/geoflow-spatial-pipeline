from sqlalchemy import create_engine, text


engine = create_engine('postgresql://YOUR USER AND PASSWORD/geodata')

def run_classification():
    print("Running spatial classification logic...")
    
    with engine.connect() as conn:
        
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_buildings_geometry ON buildings USING GIST (geometry);"))
        
        
        conn.execute(text("ALTER TABLE buildings DROP COLUMN IF EXISTS classification;"))
        conn.execute(text("ALTER TABLE buildings ADD COLUMN classification TEXT;"))
        
       
        query = """
        UPDATE buildings 
        SET classification = CASE 
            WHEN ST_Area(ST_Transform(geometry, 3857)) > 500 THEN 'Industrial/Commercial'
            ELSE 'Residential/Small'
        END;
        """
        conn.execute(text(query))
        conn.commit()
        print("Classification complete!")

if __name__ == "__main__":
    run_classification()
