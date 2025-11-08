<script lang="ts">
  import { MapLibre, GeoJSONSource, CircleLayer, GlobeControl } from "svelte-maplibre-gl";

  const frames = [
    "/src/lib/data/frame0.geojson",
    "/src/lib/data/frame1.geojson",
    "/src/lib/data/frame2.geojson"
  ];

  let frame = $state(0);

  // Loop through frames
  $effect(() => {
    let interval = setInterval(() => {
      frame = (frame + 1) % frames.length;
    }, 500); // update every 0.5s
    return () => clearInterval(interval);
  });
</script>

<MapLibre
  class="h-[70vh] w-full"
  style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"
  center={[0, 10]}
  zoom={2}
>
  <GlobeControl />
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
</MapLibre>
