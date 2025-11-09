<!-- svelte-ignore non_reactive_update -->
<script lang="ts">
  import { MapLibre, GeoJSONSource, NavigationControl, GlobeControl, CircleLayer } from 'svelte-maplibre-gl';
  import { goto } from '$app/navigation';

  let center: [number, number] = [-80, 40];
  let zoom = $state(1.5);
  let microplastics = $state(false);
  let animate = $state(false);

  function goHome() {
    goto('/');
  }

  const frames = [
    "data/forecast_t000h.geojson",
    "data/forecast_t024h.geojson",
    "data/forecast_t048h.geojson",
    "data/forecast_t072h.geojson",
    "data/forecast_t096h.geojson",
    "data/forecast_t120h.geojson",
    "data/forecast_t144h.geojson",
    "data/forecast_t168h.geojson",
    "data/forecast_t192h.geojson",
    "data/forecast_t216h.geojson",
    "data/forecast_t240h.geojson",
    "data/forecast_t264h.geojson",
    "data/forecast_t288h.geojson",
    "data/forecast_t312h.geojson",
    "data/forecast_t336h.geojson",
    "data/forecast_t360h.geojson",
    "data/forecast_t384h.geojson",
    "data/forecast_t408h.geojson",
    "data/forecast_t432h.geojson",
    "data/forecast_t456h.geojson",
    "data/forecast_t480h.geojson",
    "data/forecast_t504h.geojson",
    "data/forecast_t528h.geojson",
    "data/forecast_t552h.geojson",
    "data/forecast_t576h.geojson",
    "data/forecast_t600h.geojson",
    "data/forecast_t624h.geojson",
    "data/forecast_t648h.geojson",
    "data/forecast_t672h.geojson",
    "data/forecast_t696h.geojson",
    "data/forecast_t720h.geojson"
  ];

  let frame = $state(0);

  $effect(() => {
    let interval = setInterval(() => {
      frame = (frame + 1) % frames.length;
    }, 500);
    return () => clearInterval(interval);
  });
</script>

<style>
.layer-panel {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;

  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 1rem;

  background: rgba(255, 255, 255, 0.85);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 0.75rem 1.5rem;
  border-radius: 0 0 0.75rem 0.75rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: #111;
}

.home-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(173, 164, 164, 0.6);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  cursor: pointer;
  backdrop-filter: blur(4px);
  transition: background 0.2s, transform 0.1s;
}

.home-btn:hover {
  background: rgba(150, 161, 184, 0.9);
  transform: scale(1.1);
}

/* Buttons */
.btn {
  display: inline-block;
  text-align: center;
  padding: 0.25rem 0.6rem;
  font-size: 0.8rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.12);
  cursor: pointer;
}

.btn-white {
  background: white;
  border: 1px solid #000;
  color: #000;
}

.btn-white:hover {
  background: #f3f4f6;
}

/* Checkbox row */
.checkbox-label {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.125rem 0;
  user-select: none;
}

.checkbox-input {
  width: 1.05rem;
  height: 1.05rem;
  border-radius: 0.25rem;
  margin: 0;
}


.label-text {
  font-weight: 600;
  color: #111;
}

.mt-2 {
  margin-top: 0.5rem;
}

@media (max-width: 520px) {
  .layer-panel {
    flex-wrap: wrap;
    padding: 0.5rem;
  }
}
</style>

<div class="layer-panel">
  <!-- Home button is now part of the flex row -->
  <button class="home-btn" onclick={goHome} aria-label="Go to Home">🏠︎</button>

  <button
    class="btn btn-white"
    onclick={() => {
      microplastics = false;
      animate = false;
    }}
  >
    Clear All Layers
  </button>

  <!-- Microplastics -->
  <label class="checkbox-label">
    <input
      class="checkbox-input"
      type="checkbox"
      bind:checked={microplastics}
      style="accent-color: #909ce0;"
    />
    <span class="label-text">Microplastics</span>
  </label>

  <!-- Animate -->
  <label class="checkbox-label">
    <input
      class="checkbox-input"
      type="checkbox"
      bind:checked={animate}
      style="accent-color: #909ce0"
    />
    <span class="label-text">Animate</span>
  </label>

  <!-- Shared intensity scale -->
  <div
    class="mt-2 text-sm text-gray-600 pl-1"
    style="font-weight:500; color:#4b5563; margin-left:auto;"
  >
    <div
      class="w-60 h-2 rounded-full mb-1"
      style="background: linear-gradient(to right, rgba(33,102,172,0.1), rgb(33,102,172));"
    ></div>
    <div class="flex justify-between w-60 text-xs" style="color:#6b7280;">
      <span>Low concentration</span>
      <span>High concentration</span>
    </div>
  </div>
</div>

<MapLibre
  class="fixed inset-0 h-screen w-screen"
  style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json"
  bind:zoom
  bind:center
  maxPitch={85}
  attributionControl={false}
>
  <NavigationControl position="bottom-right" />
  <GlobeControl position="bottom-right"/>

  {#if microplastics}
  <GeoJSONSource id="microplastics-source" data="/data/forecast_t720h.geojson">
    <CircleLayer
      id="micro-circles"
      paint={{
        'circle-color': [
          'interpolate',
          ['linear'],
          ['get', 'concentration'],
          0, '#fff87a',      // yellow (low)
          2200, '#FFA500',   // orange (mid)
          3600, '#FF0000'    // red (high)
        ],
        'circle-opacity': 0.8,
        'circle-radius': [
          'interpolate',
          ['linear'],
          ['zoom'],
          0, 0.8,   // at world view (very small)
          5, 1.5,
          10, 2.5,
          18, 4     // still small even when zoomed in
        ]
      }}
    />
  </GeoJSONSource>
{/if}


  {#if animate}
  <GeoJSONSource id="positions" data={frames[frame]}>
    <CircleLayer
      id="animation-circles"
      paint={{
        'circle-color': [
          'interpolate',
          ['linear'],
          ['get', 'concentration'],
          0, '#fff87a',      // yellow (low)
          2000, '#FFA500',   // orange (mid)
          3600, '#FF0000'    // red (high)
        ],
        'circle-opacity': 0.8,
        'circle-radius': [
          'interpolate',
          ['linear'],
          ['zoom'],
          0, 0.8,   // at world view (very small)
          5, 1.5,
          10, 2.5,
          18, 4     // still small even when zoomed in
        ]
      }}
    />
  </GeoJSONSource>
  {/if}
</MapLibre>
