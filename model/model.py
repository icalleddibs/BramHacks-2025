import xarray as xr
import numpy as np
from pathlib import Path
from scipy.interpolate import RegularGridInterpolator

class MicroplasticTransportModel:
    def __init__(self, preprocessed_file):
        """Initialize model from preprocessed data"""
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
    
    def run_forecast(self, particles_per_cell=5, dt_hours=3, n_steps=240, 
                     K_h=10, cap_percentile=99, save_interval=8, verbose=True):
        """
        Run forecast simulation (OPTIMIZED)
        
        Args:
            particles_per_cell: Number of particles per grid cell (5 is good balance)
            dt_hours: Time step in hours (3h is stable with RK4)
            n_steps: Number of time steps (240*3h = 30 days)
            K_h: Horizontal diffusivity (m²/s)
            cap_percentile: Cap concentrations at this percentile
            save_interval: Save grid every N steps (8 = every 24h)
            verbose: Print progress updates
        """
        if verbose:
            print(f"\nRunning {n_steps}-step forecast (dt={dt_hours}h, total={n_steps*dt_hours}h)")
        
        # Initialize particles
        positions, weights = self._initialize_particles(particles_per_cell, verbose)
        
        if len(positions) == 0:
            print("  No particles to track!")
            return self.mp_conc, [self.mp_conc], [0]
        
        # Check mass conservation
        initial_mass = self.mp_conc.sum()
        particle_mass = weights.sum()
        if verbose:
            print(f"  Initial grid mass: {initial_mass:.2e}")
            print(f"  Particle mass: {particle_mass:.2e}")
            print(f"  Conservation: {(particle_mass/initial_mass)*100:.1f}%")
        
        # Pre-allocate storage
        n_saves = (n_steps // save_interval) + 2
        timestep_grids = [None] * n_saves
        timestep_hours = [None] * n_saves
        save_idx = 0
        
        # Save initial state
        timestep_grids[save_idx] = self.mp_conc.copy()
        timestep_hours[save_idx] = 0
        save_idx += 1
        
        # Advect particles
        dt_seconds = dt_hours * 3600
        for step in range(n_steps):
            positions = self._advect_rk4(positions, dt_seconds)
            positions = self._add_diffusion(positions, dt_seconds, K_h)
            positions = self._apply_boundaries(positions)
            
            # Save grid at intervals
            if (step + 1) % save_interval == 0:
                step_conc = self._particles_to_grid(positions, weights)
                timestep_grids[save_idx] = step_conc
                timestep_hours[save_idx] = (step + 1) * dt_hours
                save_idx += 1
            
            if verbose and (step + 1) % 20 == 0:
                print(f"  Step {step+1}/{n_steps} ({(step+1)*dt_hours}h)")
        
        # Final concentration
        predicted_conc = self._particles_to_grid(positions, weights)
        
        # Trim unused slots
        timestep_grids = [g for g in timestep_grids[:save_idx] if g is not None]
        timestep_hours = [h for h in timestep_hours[:save_idx] if h is not None]
        
        # Add final if not already saved
        if timestep_hours[-1] != n_steps * dt_hours:
            timestep_grids.append(predicted_conc.copy())
            timestep_hours.append(n_steps * dt_hours)
        else:
            timestep_grids[-1] = predicted_conc
        
        # Check mass conservation
        final_mass = predicted_conc.sum()
        if verbose:
            print(f"  Final grid mass: {final_mass:.2e}")
            print(f"  Mass conservation: {(final_mass/initial_mass)*100:.1f}%")
        
        # Cap outliers
        if cap_percentile is not None:
            predicted_conc, n_capped, cap_value = self._cap_outliers(
                predicted_conc, cap_percentile, verbose
            )
            if verbose:
                print(f"  Capping all timesteps at {cap_value:.2e}")
            timestep_grids = [np.clip(grid, 0, cap_value) for grid in timestep_grids]
        
        if verbose:
            print(f"  Forecast complete: {len(positions)} particles, {len(timestep_grids)} saves")
        
        return predicted_conc, timestep_grids, timestep_hours
    
    def _cap_outliers(self, conc, percentile, verbose=True):
        """Cap concentration values at specified percentile"""
        nonzero = conc[conc > 0]
        
        if len(nonzero) == 0:
            return conc, 0, 0
        
        cap_value = np.percentile(nonzero, percentile)
        original_max = conc.max()
        conc_capped = np.clip(conc, 0, cap_value)
        n_capped = np.sum(conc > cap_value)
        
        if verbose and n_capped > 0:
            print(f"\n  Outlier capping:")
            print(f"    {percentile}th percentile: {cap_value:.2e}")
            print(f"    Original max: {original_max:.2e}")
            print(f"    Cells capped: {n_capped}")
        
        return conc_capped, n_capped, cap_value
    
    def _initialize_particles(self, n_per_cell, verbose=True):
        """Seed particles from initial concentration (VECTORIZED)"""
        nonzero_mask = self.mp_conc > 0
        nonzero_indices = np.argwhere(nonzero_mask)
        n_cells = len(nonzero_indices)
        
        if n_cells == 0:
            return np.array([]).reshape(0, 2), np.array([])
        
        # Pre-allocate
        n_particles = n_cells * n_per_cell
        particles = np.zeros((n_particles, 2))
        weights = np.zeros(n_particles)
        
        dlat = self.lats[1] - self.lats[0] if len(self.lats) > 1 else 0.25
        dlon = self.lons[1] - self.lons[0] if len(self.lons) > 1 else 0.25
        
        # Vectorized generation
        for idx, (i, j) in enumerate(nonzero_indices):
            start = idx * n_per_cell
            end = start + n_per_cell
            
            lat, lon = self.lats[i], self.lons[j]
            conc = self.mp_conc[i, j]
            
            particles[start:end, 0] = np.random.uniform(lat - dlat/2, lat + dlat/2, n_per_cell)
            particles[start:end, 1] = np.random.uniform(lon - dlon/2, lon + dlon/2, n_per_cell)
            weights[start:end] = conc / n_per_cell
        
        if verbose:
            print(f"  Initialized {n_particles} particles from {n_cells} cells")
        
        return particles, weights
    
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
        if self.lons.min() >= 0:
            lons = np.mod(lons, 360)
        else:
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
        
        if self.lons.min() >= 0:
            positions[:, 1] = np.mod(positions[:, 1], 360)
        else:
            positions[:, 1] = np.mod(positions[:, 1] + 180, 360) - 180
        
        return positions
    
    def _particles_to_grid(self, positions, weights):
        """Convert particle positions to gridded concentration (VECTORIZED)"""
        lats_p = positions[:, 0]
        lons_p = positions[:, 1]
        
        # Find grid indices
        lat_indices = np.searchsorted(self.lats, lats_p)
        lon_indices = np.searchsorted(self.lons, lons_p)
        
        # Filter valid
        valid = (lat_indices >= 0) & (lat_indices < len(self.lats)) & \
                (lon_indices >= 0) & (lon_indices < len(self.lons))
        
        conc_map = np.zeros_like(self.mp_conc)
        
        if np.any(valid):
            flat_indices = np.ravel_multi_index(
                (lat_indices[valid], lon_indices[valid]), 
                conc_map.shape
            )
            np.add.at(conc_map.ravel(), flat_indices, weights[valid])
        
        return conc_map
    
    def save_forecast(self, predicted_conc, timestep_grids, timestep_hours, output_file):
        """Save forecast to NetCDF file with all timesteps"""
        conc_timeseries = np.stack(timestep_grids, axis=0)
        
        ds = xr.Dataset(
            {'mp_concentration': (['time', 'lat', 'lon'], conc_timeseries)},
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
        print(f"  Timesteps: {len(timestep_hours)} (0 to {timestep_hours[-1]}h)")
        
        return ds


# === MAIN ===
if __name__ == '__main__':
    model = MicroplasticTransportModel('data/preprocessed/preprocessed_2024-05-13.nc')
    
    # OPTIMIZED: 5 particles/cell, 3h steps, save daily
    predicted, timestep_grids, timestep_hours = model.run_forecast(
        particles_per_cell=5,
        dt_hours=3,
        n_steps=240,  # 30 days
        K_h=10,
        cap_percentile=99,
        save_interval=8  # Every 24h
    )
    
    model.save_forecast(predicted, timestep_grids, timestep_hours, 'forecast_2024-05-13.nc')
    
    print(f"\nPredicted range: {predicted.min():.2e} to {predicted.max():.2e}")