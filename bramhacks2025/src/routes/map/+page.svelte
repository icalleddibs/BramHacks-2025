<!-- svelte-ignore non_reactive_update -->
<script lang="ts">
  import { MapLibre, GeoJSONSource, NavigationControl, GlobeControl, CircleLayer } from 'svelte-maplibre-gl';
  import { goto } from '$app/navigation';

  let center: [number, number] = [-80, 40];
  let zoom = $state(1.5);
  let temperature = $state(false);
</script>

<style>
  /* panel */
  .layer-panel {
    position: absolute;
    top: 4rem; /* same as your previous top-16 */
    left: 1rem;
    z-index: 50;
    background: rgba(255, 255, 255, 0.85);
    border-radius: 0.5rem;
    box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    padding: 0.6rem 0.75rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    font-size: 0.95rem;
    font-weight: 600;
    color: #111;
    min-width: 14rem;
  }

  /* buttons */
  .btn {
    display: inline-block;
    text-align: center;
    padding: 0.25rem 0.6rem;
    font-size: 0.75rem;
    border-radius: 0.5rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.12);
    cursor: pointer;
  }

  .btn-white {
    background: white;
    border: 1px solid #000;
    color: #000;
  }

  .btn-white:hover {
    background: #f3f4f6; /* visible hover */
  }

  /* checkbox row */
  .checkbox-label {
    position: relative;           /* for tooltip positioning */
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    padding: 0.125rem 0;
    user-select: none;
  }

  /* keep the native checkbox visible (you can hide it if you prefer a custom dot) */
  .checkbox-input {
    width: 1.05rem;
    height: 1.05rem;
    border-radius: 0.25rem;
    margin: 0;
  }

  .checkbox-dot {
    display: inline-block;
    width: 0.75rem;
    height: 0.75rem;
    border-radius: 9999px;
    flex: 0 0 auto;
  }

  .label-text {
    position: relative; /* contains tooltip */
    display: inline-block;
    line-height: 1;
    font-weight: 600;
    color: #111;
  }

  /* tooltip */
.tooltip {
  position: absolute;
  top: 50%;
  left: 100%;
  transform: translateY(-50%);
  margin-left: 0.5rem;
  background: white;
  color: black;
  border: 1px solid #000;
  border-radius: 8px;
  padding: 6px 8px;
  font-size: 12px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.12);
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  white-space: normal;      /* allow wrapping */
  display: inline-block;    /* allow width constraints to take effect */
  max-width: 600px;         /* adjust width as needed */
  transition: opacity 0.15s ease, transform 0.15s ease;
  z-index: 1000;
}



  /* show tooltip on hover and when label/input has focus (keyboard accessible) */
  .checkbox-label:hover .tooltip,
  .checkbox-label:focus-within .tooltip {
    opacity: 1;
    visibility: visible;
    transform: translateX(-50%) translateY(0);
  }

  /* small screen adjustments */
  @media (max-width: 520px) {
    .layer-panel { left: 0.5rem; right: 0.5rem; min-width: 12rem; }
    .tooltip { font-size: 11px; padding: 5px 7px; }
  }
</style>

<div class="layer-panel">

  <button
    class="btn btn-white"
    onclick={() => {
      temperature = false;
    }}
  >
    Clear All Layers
  </button>

  <!-- Temperature -->
  <label class="checkbox-label">
    <input
      class="checkbox-input"
      type="checkbox"
      bind:checked={temperature}
      style="accent-color: rgb(255,0,255);"
    />
    <span class="checkbox-dot" style="background: rgb(255,0,255)"></span>
    <span class="label-text">
      Sea Surface Temperature
      <span class="tooltip">Temperature (॰C) measures how much heat is in the water. Sharks can often find prey in warm areas, but can be uncomfortable if it is too hot or too cold for them.</span>
    </span>
  </label>

  <!-- Shared intensity scale -->
  <div class="mt-2 text-sm text-gray-600 pl-1" style="font-weight:500; color:#4b5563;">
    <div class="w-60 h-2 rounded-full mb-1" style="background: linear-gradient(to right, rgba(33,102,172,0.1), rgb(33,102,172));"></div>
    <div class="flex justify-between w-60 text-xs" style="color:#6b7280;">
      <span>Low suitability</span>
      <span>High suitability</span>
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
  <NavigationControl />
  <GlobeControl />

  {#if temperature}
    <GeoJSONSource id="temp-source" data="/temperature.geojson">
      <CircleLayer
        id="temp-circles"
        paint={{
          'circle-color': 'rgb(255,0,255)',
          'circle-opacity': ['*', ['get', 'value'], 0.25],
          'circle-radius': ['interpolate', ['linear'], ['zoom'], 0, 4, 18, 10]
        }}
      />
    </GeoJSONSource>
  {/if}

</MapLibre>

<!-- Return Home Button -->
<a
  href="/"
  class="absolute top-4 left-4 bg-white/80 hover:bg-white text-black px-3 py-2 rounded-lg shadow-md text-sm font-semibold transition"
>
  ← Home
</a>

<p
  class="absolute top-4 left-28 bg-black/60 text-white px-3 py-2 rounded-lg shadow-md text-sm font-semibold transition"
>
  Habitat Conditions
</p>
