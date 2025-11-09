import xarray as xr
import numpy as np
from pathlib import Path
from scipy.interpolate import RegularGridInterpolator

class MicroplasticTransportModel:
    def __init__(self, preprocessed_file):
        """
        Initialize model from preprocessed data
        
        Args:
            preprocessed_file: Path to preprocessed NetCDF file
        """
        print(f"\nLoading preprocessed data from {preprocessed_file}")
        
        self.data = xr.open_dataset(preprocessed_file)
        self.date = self.data.attrs.get('date', 'unknown')
        
        # Extract arrays
        self.mp_conc = self.data['mp_concentration'].values
        self.u = self.data['u_current'].values
        self.v = self.data['v_current'].values
        self.lats = self.data['lat'].values
        self.lons = self.data['lon'].values
        
        # Handle NaN
        self.mp_conc = np.nan_to_num(self.mp_conc, nan=0.0)
        self.u = np.nan_to_num(self.u, nan=0.0)
        self.v = np.nan_to_num(self.v, nan=0.0)
        
        # Check and fix array shapes
        self._align_array_shapes()
        
        # Create velocity interpolators
        self.u_interp = RegularGridInterpolator(
            (self.lats, self.lons), self.u, bounds_error=False, fill_value=0
        )
        self.v_interp = RegularGridInterpolator(
            (self.lats, self.lons), self.v, bounds_error=False, fill_value=0
        )
        
        print(f"  Date: {self.date}")
        print(f"  Grid: {len(self.lats)} lats x {len(self.lons)} lons")
        print(f"  MP range: {self.mp_conc[self.mp_conc>0].min():.2e} to {self.mp_conc.max():.2e}")
        print(f"  Model ready!")
    
    def _align_array_shapes(self):
        """Ensure all arrays match (lats, lons) ordering"""
        expected_shape = (len(self.lats), len(self.lons))
        
        if self.mp_conc.shape != expected_shape:
            print(f"  Transposing mp_conc from {self.mp_conc.shape}")
            self.mp_conc = self.mp_conc.T
        if self.u.shape != expected_shape:
            print(f"  Transposing u from {self.u.shape}")
            self.u = self.u.T
        if self.v.shape != expected_shape:
            print(f"  Transposing v from {self.v.shape}")
            self.v = self.v.T
    
    def run_forecast(self, particles_per_cell=10, dt_hours=1, n_steps=24*30, 
                     K_h=10, cap_percentile=99, save_interval=24, verbose=True):
        """
        Run forecast simulation
        
        Args:
            particles_per_cell: Number of particles per grid cell
            dt_hours: Time step in hours
            n_steps: Number of time steps (24 = 1 day)
            K_h: Horizontal diffusivity (m²/s)
            cap_percentile: Cap concentrations at this percentile (99 recommended)
            save_interval: Save grid every N steps (1 = every step)
            verbose: Print progress updates
        
        Returns:
            predicted_conc: Final concentration map
            timestep_grids: List of concentration grids at each save_interval
            timestep_hours: List of hours corresponding to saved grids
        """
        if verbose:
            print(f"\nRunning {n_steps}-step forecast (dt={dt_hours}h)")
        
        # Initialize particles
        positions, weights = self._initialize_particles(particles_per_cell, verbose)
        
        # Check mass conservation
        initial_mass = self.mp_conc.sum()
        particle_mass = weights.sum()
        if verbose:
            print(f"  Initial grid mass: {initial_mass:.2e}")
            print(f"  Particle mass: {particle_mass:.2e}")
            print(f"  Conservation check: {(particle_mass/initial_mass)*100:.1f}%")
        
        # Storage for timesteps
        timestep_grids = []
        timestep_hours = []
        
        # Save initial state
        timestep_grids.append(self.mp_conc.copy())
        timestep_hours.append(0)
        
        # Advect particles
        for step in range(n_steps):
            positions = self._advect_rk4(positions, dt_hours * 3600)
            positions = self._add_diffusion(positions, dt_hours * 3600, K_h)
            positions = self._apply_boundaries(positions)
            
            # Save grid at intervals
            if (step + 1) % save_interval == 0:
                step_conc = self._particles_to_grid(positions, weights)
                timestep_grids.append(step_conc.copy())
                timestep_hours.append((step + 1) * dt_hours)
            
            if verbose and (step + 1) % 6 == 0:
                print(f"  Step {step+1}/{n_steps} ({(step+1)*dt_hours}h)")
        
        # Final concentration
        predicted_conc = self._particles_to_grid(positions, weights)
        
        # Update last timestep if not already saved
        if timestep_hours[-1] != n_steps * dt_hours:
            timestep_grids.append(predicted_conc.copy())
            timestep_hours.append(n_steps * dt_hours)
        else:
            timestep_grids[-1] = predicted_conc.copy()
        
        # Check mass conservation after
        final_mass = predicted_conc.sum()
        if verbose:
            print(f"  Final grid mass: {final_mass:.2e}")
            print(f"  Mass conservation: {(final_mass/initial_mass)*100:.1f}%")
        
        # Cap outliers at percentile
        if cap_percentile is not None:
            predicted_conc, n_capped, cap_value = self._cap_outliers(
                predicted_conc, cap_percentile, verbose
            )
            
            # Also cap all timesteps
            if verbose:
                print(f"  Capping all timesteps at {cap_value:.2e}")
            timestep_grids = [np.clip(grid, 0, cap_value) for grid in timestep_grids]
        
        if verbose:
            print(f"  Forecast complete: {len(positions)} particles tracked")
            print(f"  Saved {len(timestep_grids)} timesteps")
        
        return predicted_conc, timestep_grids, timestep_hours
    
    def _cap_outliers(self, conc, percentile, verbose=True):
        """Cap concentration values at specified percentile"""
        nonzero = conc[conc > 0]
        
        if len(nonzero) == 0:
            return conc, 0, 0
        
        cap_value = np.percentile(nonzero, percentile)
        original_max = conc.max()
        
        # Cap values
        conc_capped = np.clip(conc, 0, cap_value)
        n_capped = np.sum(conc > cap_value)
        
        if verbose and n_capped > 0:
            print(f"\n  Outlier capping:")
            print(f"    Threshold ({percentile}th percentile): {cap_value:.2e}")
            print(f"    Original max: {original_max:.2e}")
            print(f"    Cells capped: {n_capped}")
            mass_removed = conc.sum() - conc_capped.sum()
            print(f"    Mass removed: {mass_removed:.2e} ({mass_removed/conc.sum()*100:.2f}%)")
        
        return conc_capped, n_capped, cap_value
    
    def _initialize_particles(self, n_per_cell, verbose=True):
        """Seed particles from initial concentration"""
        particles = []
        weights = []
        
        dlat = self.lats[1] - self.lats[0] if len(self.lats) > 1 else 0.25
        dlon = self.lons[1] - self.lons[0] if len(self.lons) > 1 else 0.25
        
        for i, lat in enumerate(self.lats):
            for j, lon in enumerate(self.lons):
                conc = self.mp_conc[i, j]
                
                if conc <= 0:
                    continue
                
                cell_lats = np.random.uniform(lat - dlat/2, lat + dlat/2, n_per_cell)
                cell_lons = np.random.uniform(lon - dlon/2, lon + dlon/2, n_per_cell)
                
                particles.extend(np.column_stack([cell_lats, cell_lons]))
                weights.extend([conc / n_per_cell] * n_per_cell)
        
        if verbose:
            print(f"  Initialized {len(particles)} particles")
        
        return np.array(particles), np.array(weights)
    
    def _advect_rk4(self, positions, dt_seconds):
        """4th-order Runge-Kutta advection"""
        k1 = self._velocity_at(positions) * dt_seconds
        k2 = self._velocity_at(positions + 0.5*k1) * dt_seconds
        k3 = self._velocity_at(positions + 0.5*k2) * dt_seconds
        k4 = self._velocity_at(positions + k3) * dt_seconds
        return positions + (k1 + 2*k2 + 2*k3 + k4) / 6
    
    def _velocity_at(self, positions):
        """Get velocity at particle positions (degrees/second)"""
        lats = positions[:, 0]
        lons = positions[:, 1]
        
        # Match longitude convention to grid
        if self.lons.min() >= 0:  # Grid uses [0, 360]
            # Ensure longitudes are in [0, 360]
            lons = np.mod(lons, 360)
        else:  # Grid uses [-180, 180]
            # Ensure longitudes are in [-180, 180]
            lons = np.mod(lons + 180, 360) - 180
        
        points = np.column_stack([lats, lons])
        
        u_ms = self.u_interp(points)
        v_ms = self.v_interp(points)
        
        # Convert m/s to degrees/second
        dlat_dt = v_ms / 111000.0
        dlon_dt = u_ms / (111000.0 * np.cos(np.radians(lats)))
        return np.column_stack([dlat_dt, dlon_dt])
    
    def _add_diffusion(self, positions, dt_seconds, K_h):
        """Horizontal turbulent diffusion"""
        std_lat = np.sqrt(2 * K_h * dt_seconds) / 111000.0
        std_lon = std_lat / np.cos(np.radians(positions[:, 0]))
        
        positions[:, 0] += np.random.normal(0, std_lat, len(positions))
        positions[:, 1] += np.random.normal(0, std_lon, len(positions))
        return positions
    
    def _apply_boundaries(self, positions):
        """Enforce lat/lon bounds"""
        positions[:, 0] = np.clip(positions[:, 0], -90, 90)
        
        # Match longitude convention to grid
        if self.lons.min() >= 0:  # Grid uses [0, 360]
            positions[:, 1] = np.mod(positions[:, 1], 360)
        else:  # Grid uses [-180, 180]
            positions[:, 1] = np.mod(positions[:, 1] + 180, 360) - 180
        
        return positions
    
    def _particles_to_grid(self, positions, weights):
        """Convert particle positions to gridded concentration"""
        conc_map = np.zeros_like(self.mp_conc)
        
        for (lat, lon), weight in zip(positions, weights):
            i = np.searchsorted(self.lats, lat)
            j = np.searchsorted(self.lons, lon)
            
            if 0 <= i < len(self.lats) and 0 <= j < len(self.lons):
                conc_map[i, j] += weight
        
        return conc_map
    
    def save_forecast(self, predicted_conc, timestep_grids, timestep_hours, output_file):
        """
        Save forecast to NetCDF file with all timesteps
        
        Args:
            predicted_conc: Final concentration (for backward compatibility)
            timestep_grids: List of concentration grids at each timestep
            timestep_hours: List of hours for each timestep
            output_file: Output filename
        """
        # Stack timesteps into 3D array (time, lat, lon)
        conc_timeseries = np.stack(timestep_grids, axis=0)
        
        ds = xr.Dataset(
            {
                'mp_concentration': (['time', 'lat', 'lon'], conc_timeseries),
            },
            coords={
                'time': timestep_hours,
                'lat': self.lats,
                'lon': self.lons
            },
            attrs={
                'description': f'Microplastic forecast from {self.date}',
                'forecast_method': 'Lagrangian particle tracking (RK4)',
                'source_date': self.date,
                'time_units': 'hours since start',
                'forecast_duration_hours': timestep_hours[-1]
            }
        )
        
        ds.to_netcdf(output_file)
        print(f"\n✓ Saved forecast to {output_file}")
        print(f"  Time dimension: {len(timestep_hours)} steps (0 to {timestep_hours[-1]} hours)")
        
        return ds


# === MAIN ===
if __name__ == '__main__':
    # Load preprocessed data
    model = MicroplasticTransportModel('data/preprocessed/preprocessed_2024-05-13.nc')
    
    # Run forecast with capping and timestep saving
    predicted, timestep_grids, timestep_hours = model.run_forecast(
        particles_per_cell=10,
        dt_hours=1,
        n_steps=24*30,
        K_h=10,
        cap_percentile=99,  # Cap at 99th percentile
        save_interval=24     # Save every hour (change to 6 for every 6 hours)
    )
    
    # Save results
    model.save_forecast(predicted, timestep_grids, timestep_hours, 'forecast_2024-05-13.nc')
    
    print(f"\nPredicted concentration range: {predicted.min():.2e} to {predicted.max():.2e}")
