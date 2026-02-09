import geopandas as gpd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


engine = create_engine('postgresql://YOUR USER AND PASSWORD/geodata')

def plot_both_classifications():
    print("extrage date")
    
    
    query = "SELECT geometry, classification FROM buildings WHERE classification IS NOT NULL"
    
    try:
        gdf = gpd.read_postgis(query, engine, geom_col='geometry')
        
        if gdf.empty:
            print("eroare baza de date")
            return

        
        fig, ax = plt.subplots(figsize=(12, 12))
        
        
        color_dict = {
            'Industrial/Commercial': '#e74c3c', 
            'Residential/Small': '#2ecc71'
        }

        print("Generare hartă...")
        for cls, group in gdf.groupby('classification'):
            group.plot(
                ax=ax, 
                color=color_dict.get(cls, '#95a5a6'), 
                label=cls,
                edgecolor='black',
                linewidth=0.3,
                alpha=0.8
            )

        
        plt.title("Analiza Spațială București\nClasificare bazată pe suprafața clădirilor (ST_Area)", fontsize=14)
        plt.legend(title="Legendă Clasificare", loc='upper right')
        ax.set_axis_off() 

        
        try:
            import contextily as ctx
            gdf_3857 = gdf.to_crs(epsg=3857) 
            
            ax.clear()
            for cls, group in gdf_3857.groupby('classification'):
                group.plot(ax=ax, color=color_dict.get(cls, '#95a5a6'), label=cls, alpha=0.6)
            ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
            ax.set_axis_off()
        except ImportError:
            print(install other")

        
        plt.savefig("analiza_urbana_bucuresti.png", dpi=300, bbox_inches='tight')
        print("harta salvată ca 'analiza_urbana_bucuresti.png'")
        plt.show()

    except Exception as e:
        print(f"eroare vizualizare: {e}")

if __name__ == "__main__":
    plot_both_classifications()
