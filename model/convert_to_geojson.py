import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pathlib import Path
import json
from datetime import datetime, timedelta

class ForecastVisualizer:
    def __init__(self, forecast_file):
        """
        Initialize visualizer with forecast NetCDF file
        
        Args:
            forecast_file: Path to forecast NetCDF file
        """
        print(f"Loading forecast from {forecast_file}")
        self.ds = xr.open_dataset(forecast_file)
        self.source_date = self.ds.attrs.get('source_date', 'unknown')
        
        print(f"  Source date: {self.source_date}")
        print(f"  Time steps: {len(self.ds.time)}")
        print(f"  Grid shape: {len(self.ds.lat)} x {len(self.ds.lon)}")
    
    def plot_all_timesteps(self, output_dir='plots', vmin=None, vmax=None, 
                          cmap='YlOrRd', dpi=150):
        """
        Create map plots for all timesteps
        
        Args:
            output_dir: Directory to save plots
            vmin, vmax: Color scale limits (None for auto)
            cmap: Colormap name
            dpi: Plot resolution
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Auto-scale if not provided
        if vmin is None or vmax is None:
            all_data = self.ds['mp_concentration'].values
            nonzero = all_data[all_data > 0]
            if len(nonzero) > 0:
                vmin = vmin or np.percentile(nonzero, 1)
                vmax = vmax or np.percentile(nonzero, 99)
            else:
                vmin, vmax = 0, 1
        
        print(f"\nPlotting {len(self.ds.time)} timesteps...")
        print(f"  Color scale: {vmin:.2e} to {vmax:.2e}")
        
        for t_idx, time_val in enumerate(self.ds.time.values):
            hours = int(time_val)
            
            # Extract data
            conc = self.ds['mp_concentration'].isel(time=t_idx).values
            lats = self.ds.lat.values
            lons = self.ds.lon.values
            
            # Create figure
            fig = plt.figure(figsize=(16, 8), dpi=dpi)
            ax = plt.axes(projection=ccrs.PlateCarree())
            
            # Plot data
            im = ax.pcolormesh(lons, lats, conc, 
                              transform=ccrs.PlateCarree(),
                              cmap=cmap, vmin=vmin, vmax=vmax,
                              shading='auto')
            
            # Add features
            ax.add_feature(cfeature.LAND, facecolor='lightgray', edgecolor='black', linewidth=0.5)
            ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
            ax.add_feature(cfeature.BORDERS, linewidth=0.3, linestyle=':')
            ax.gridlines(draw_labels=True, linewidth=0.5, alpha=0.5)
            
            # Title and colorbar
            date_str = self._format_forecast_time(hours)
            ax.set_title(f'Microplastic Concentration - {date_str}\n(T+{hours}h from {self.source_date})',
                        fontsize=12, fontweight='bold')
            
            cbar = plt.colorbar(im, ax=ax, orientation='horizontal', 
                               pad=0.05, aspect=50, shrink=0.8)
            cbar.set_label('Concentration', fontsize=10)
            
            # Save
            output_file = output_dir / f'forecast_t{hours:03d}h.png'
            plt.savefig(output_file, bbox_inches='tight', dpi=dpi)
            plt.close()
            
            if (t_idx + 1) % 5 == 0:
                print(f"  Plotted {t_idx + 1}/{len(self.ds.time)} timesteps")
        
        print(f"\n✓ All plots saved to {output_dir}/")
        
        # Create index HTML for easy viewing
        self._create_plot_index(output_dir)
    
    def _format_forecast_time(self, hours):
        """Format forecast time as readable string"""
        try:
            base_date = datetime.strptime(self.source_date, '%Y-%m-%d')
            forecast_date = base_date + timedelta(hours=hours)
            return forecast_date.strftime('%Y-%m-%d %H:%M UTC')
        except:
            return f'{hours} hours'
    
    def _create_plot_index(self, output_dir):
        """Create HTML index file for viewing plots"""
        html = ['<!DOCTYPE html>',
                '<html><head><title>Forecast Plots</title></head>',
                '<body style="font-family: Arial; margin: 20px;">',
                f'<h1>Microplastic Forecast - {self.source_date}</h1>']
        
        png_files = sorted(output_dir.glob('forecast_t*.png'))
        for png in png_files:
            html.append(f'<div style="margin: 20px 0;">')
            html.append(f'<h3>{png.stem}</h3>')
            html.append(f'<img src="{png.name}" style="max-width: 100%; height: auto;">')
            html.append('</div>')
        
        html.extend(['</body>', '</html>'])
        
        index_file = output_dir / 'index.html'
        index_file.write_text('\n'.join(html))
        print(f"  Created {index_file} for easy viewing")
    
    def export_to_geojson(self, output_dir='geojson', threshold=None, 
                         max_features_per_file=50000):
        """
        Export each timestep to separate GeoJSON file
        
        Args:
            output_dir: Directory to save GeoJSON files
            threshold: Minimum concentration to include (None = include all non-zero)
            max_features_per_file: Limit features to prevent huge files
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\nExporting {len(self.ds.time)} timesteps to GeoJSON...")
        
        for t_idx, time_val in enumerate(self.ds.time.values):
            hours = int(time_val)
            
            # Extract data
            conc = self.ds['mp_concentration'].isel(time=t_idx).values
            lats = self.ds.lat.values
            lons = self.ds.lon.values
            
            # Convert to GeoJSON
            geojson = self._create_geojson(conc, lats, lons, hours, 
                                          threshold, max_features_per_file)
            
            # Save
            output_file = output_dir / f'forecast_t{hours:03d}h.geojson'
            with open(output_file, 'w') as f:
                json.dump(geojson, f)
            
            n_features = len(geojson['features'])
            if (t_idx + 1) % 5 == 0:
                print(f"  Exported {t_idx + 1}/{len(self.ds.time)} timesteps ({n_features} features)")
        
        print(f"\n✓ All GeoJSON files saved to {output_dir}/")
        print(f"  Note: Files contain point features for each non-zero grid cell")
    
    def _create_geojson(self, conc, lats, lons, hours, threshold, max_features):
        """Create GeoJSON FeatureCollection from gridded data"""
        features = []
        
        # Apply threshold
        if threshold is None:
            threshold = 0
        
        # Collect all non-zero points
        points = []
        for i, lat in enumerate(lats):
            for j, lon in enumerate(lons):
                value = conc[i, j]
                if value > threshold:
                    points.append({
                        'lat': float(lat),
                        'lon': float(lon),
                        'value': float(value)
                    })
        
        # Subsample if too many features
        if len(points) > max_features:
            print(f"    Warning: {len(points)} points, subsampling to {max_features}")
            # Sort by value and take top N
            points.sort(key=lambda p: p['value'], reverse=True)
            points = points[:max_features]
        
        # Create features
        for point in points:
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [point['lon'], point['lat']]
                },
                'properties': {
                    'concentration': point['value'],
                    'time_hours': hours,
                    'source_date': self.source_date,
                    'forecast_time': self._format_forecast_time(hours)
                }
            }
            features.append(feature)
        
        geojson = {
            'type': 'FeatureCollection',
            'features': features,
            'metadata': {
                'source_date': self.source_date,
                'time_hours': hours,
                'n_features': len(features),
                'concentration_range': [
                    float(min(p['value'] for p in points)) if points else 0,
                    float(max(p['value'] for p in points)) if points else 0
                ]
            }
        }
        
        return geojson
    
    def export_grid_geojson(self, output_dir='geojson_grid', decimate=10):
        """
        Export as gridded polygons (cells) instead of points
        Warning: Creates very large files!
        
        Args:
            output_dir: Directory to save GeoJSON files
            decimate: Only export every Nth cell to reduce file size
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\nExporting {len(self.ds.time)} timesteps as grid polygons...")
        print(f"  Decimation factor: {decimate} (every {decimate}th cell)")
        
        lats = self.ds.lat.values
        lons = self.ds.lon.values
        
        # Calculate cell boundaries
        dlat = lats[1] - lats[0] if len(lats) > 1 else 0.25
        dlon = lons[1] - lons[0] if len(lons) > 1 else 0.25
        
        for t_idx, time_val in enumerate(self.ds.time.values):
            hours = int(time_val)
            conc = self.ds['mp_concentration'].isel(time=t_idx).values
            
            features = []
            
            for i in range(0, len(lats), decimate):
                for j in range(0, len(lons), decimate):
                    value = conc[i, j]
                    
                    if value <= 0:
                        continue
                    
                    lat = lats[i]
                    lon = lons[j]
                    
                    # Create cell polygon
                    cell_polygon = [
                        [lon - dlon/2, lat - dlat/2],
                        [lon + dlon/2, lat - dlat/2],
                        [lon + dlon/2, lat + dlat/2],
                        [lon - dlon/2, lat + dlat/2],
                        [lon - dlon/2, lat - dlat/2]
                    ]
                    
                    feature = {
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Polygon',
                            'coordinates': [cell_polygon]
                        },
                        'properties': {
                            'concentration': float(value),
                            'time_hours': hours
                        }
                    }
                    features.append(feature)
            
            geojson = {
                'type': 'FeatureCollection',
                'features': features
            }
            
            output_file = output_dir / f'forecast_grid_t{hours:03d}h.geojson'
            with open(output_file, 'w') as f:
                json.dump(geojson, f)
            
            print(f"  Exported t+{hours}h: {len(features)} cells")
        
        print(f"\n✓ Grid GeoJSON files saved to {output_dir}/")


# === MAIN ===
if __name__ == '__main__':
    # Load forecast
    viz = ForecastVisualizer('forecast_2024-05-13.nc')
    
    # 1. Plot all timesteps as maps
    viz.plot_all_timesteps(
        output_dir='plots',
        cmap='YlOrRd',  # Yellow-Orange-Red colormap
        dpi=150
    )
    
    # 2. Export each timestep to GeoJSON (point features)
    viz.export_to_geojson(
        output_dir='geojson',
        threshold=1e-10,  # Only include concentrations above this
        max_features_per_file=50000  # Limit to prevent huge files
    )
    
    # 3. Optional: Export as grid polygons (WARNING: creates large files!)
    # viz.export_grid_geojson(
    #     output_dir='geojson_grid',
    #     decimate=20  # Every 20th cell to reduce file size
    # )
    
    print("\n=== Visualization Complete ===")
    print("View plots: open plots/index.html in browser")
    print("GeoJSON files: geojson/forecast_t*h.geojson")