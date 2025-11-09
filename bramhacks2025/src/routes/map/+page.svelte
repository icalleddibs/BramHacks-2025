<!-- svelte-ignore non_reactive_update -->
<script lang="ts">
  import { MapLibre, GeoJSONSource, NavigationControl, GlobeControl, CircleLayer } from 'svelte-maplibre-gl';
  import { goto } from '$app/navigation';

  let center: [number, number] = [-80, 40];
  let zoom = $state(1.5);
  let temperature = $state(false);
  let animate = $state(false);

  function goHome() {
    goto('/');
  }

  const frames = [
    "/src/lib/data/frame0.geojson",
    "/src/lib/data/frame1.geojson",
    "/src/lib/data/frame2.geojson"
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

.checkbox-dot {
  display: inline-block;
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 9999px;
  flex: 0 0 auto;
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
      temperature = false;
      animate = false;
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
    <span class="label-text">Temperature</span>
  </label>

  <!-- Animate -->
  <label class="checkbox-label">
    <input
      class="checkbox-input"
      type="checkbox"
      bind:checked={animate}
      style="accent-color: rgb(0,255,255);"
    />
    <span class="checkbox-dot" style="background: rgb(0,255,255)"></span>
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

  {#if animate}
    <GeoJSONSource id="positions" data={frames[frame]}>
      <CircleLayer
        paint={{
          "circle-color": "#00ffcc",
          "circle-radius": 6,
          "circle-stroke-width": 1,
          "circle-stroke-color": "#003333"
        }}
      />
    </GeoJSONSource>
  {/if}
</MapLibre>
