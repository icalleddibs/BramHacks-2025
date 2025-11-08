<script lang="ts">
  import CameraFeed from '$lib/camerafeed.svelte';
  let movingForward = false;
  let movingBackward = false;
  let turningLeft = false;
  let turningRight = false;
  let lightsOn = false;
  let sensorsActive = false;

  function toggleLights() {
    lightsOn = !lightsOn;
  }

  function toggleSensors() {
    sensorsActive = !sensorsActive;
  }
</script>



<div class="flex h-screen w-screen bg-gray-100">
  <!-- Left panel: Controls -->
  <div class="flex-[0_0_12rem] bg-white shadow-md p-4 flex flex-col gap-4">
    <h2 class="text-xl font-bold mb-2">Robot Controls</h2>

    <!-- Toggles -->
    <div class="flex flex-col gap-2 mt-4">
      <label class="flex items-center gap-2">
        <input type="checkbox" bind:checked={lightsOn} class="w-5 h-5" />
        <span>Lights</span>
      </label>
      <label class="flex items-center gap-2">
        <input type="checkbox" bind:checked={sensorsActive} class="w-5 h-5" />
        <span>Sensors</span>
      </label>
    </div>

    <!-- Status -->
    <div class="mt-4">
      <h3 class="font-semibold mb-2">Status</h3>
      <ul class="text-sm">
        <li>Forward: {movingForward ? "✅" : "❌"}</li>
        <li>Backward: {movingBackward ? "✅" : "❌"}</li>
        <li>Left: {turningLeft ? "✅" : "❌"}</li>
        <li>Right: {turningRight ? "✅" : "❌"}</li>
        <li>Lights: {lightsOn ? "✅" : "❌"}</li>
        <li>Sensors: {sensorsActive ? "✅" : "❌"}</li>
      </ul>
    </div>
  </div>

  <!-- Right panel: Camera feed -->
  <div class="flex-1 relative flex items-center justify-center bg-gray-200">
    <CameraFeed />

    <!-- Directional buttons (now relative to camera feed) -->
    <div class="absolute bottom-6 left-6 bg-white/20 backdrop-blur-md p-4 rounded-2xl shadow-lg border border-white/30 flex flex-col items-center gap-2">
      <button
        class="w-13 h-13 bg-blue-600 text-white text-3xl rounded-full hover:bg-blue-700"
        on:mousedown={() => (movingForward = true)}
        on:mouseup={() => (movingForward = false)}
      >
      ▴
      </button>

      <div class="flex gap-2">
        <button
          class="w-13 h-13 bg-blue-600 text-white text-3xl rounded-full hover:bg-blue-700"
          on:mousedown={() => (turningLeft = true)}
          on:mouseup={() => (turningLeft = false)}
        >
        ◂
        </button>

        <button
          class="ml-13 w-13 h-13 bg-blue-600 text-white text-3xl rounded-full hover:bg-blue-700"
          on:mousedown={() => (turningRight = true)}
          on:mouseup={() => (turningRight = false)}
        >
        ▸
        </button>
      </div>

      <button
        class="w-13 h-13 bg-blue-600 text-white text-3xl rounded-full hover:bg-blue-700"
        on:mousedown={() => (movingBackward = true)}
        on:mouseup={() => (movingBackward = false)}
      >
      ▾
      </button>
    </div>
  </div>
</div>
