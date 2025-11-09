<script lang="ts">
  // Movement / robot controls
  let movingForward = false;
  let movingBackward = false;
  let turningLeft = false;
  let turningRight = false;
  let grapple = false;
  let ungrapple = false;
  let blueLightOn = false;
  let greenLightOn = false;

  function toggleBlueLights() {
    blueLightOn = !blueLightOn;
  }

  function toggleGreenLights() {
    greenLightOn = !greenLightOn;
  }

  import { goto } from '$app/navigation'; // SvelteKit navigation

  function goHome() {
    goto('/'); // replace '/' with your actual home route if different
  }

  // Camera feed / ESP32
  let esp32Ip = '192.168.4.1';
  let streamUrl = `http://${esp32Ip}:81/stream`;
  let streamError = false;
  let controlUrl = `http://${esp32Ip}/control`;

  const resolutions = [
    { value: 0, label: 'QQVGA (160x120)' },
    { value: 1, label: 'QCIF (176x144)' },
    { value: 2, label: 'HQVGA (240x176)' },
    { value: 3, label: 'QVGA (320x240)' },
    { value: 4, label: 'CIF (400x296)' },
    { value: 5, label: 'VGA (640x480)' },
    { value: 6, label: 'SVGA (800x600)' },
    { value: 7, label: 'XGA (1024x768)' },
    { value: 8, label: 'SXGA (1280x1024)' },
    { value: 9, label: 'UXGA (1600x1200)' }
  ];

  let selectedResolution = 5;
  let vflipEnabled = false;
  let statusMessage = '';

  const handleStreamLoad = () => {
    streamError = false;
  };

  const sendControlCommand = async (variable: string, value: number) => {
    try {
      const response = await fetch(`${controlUrl}?var=${variable}&val=${value}`);
      if (response.ok) {
        statusMessage = `${variable} set to ${value}`;
        setTimeout(() => (statusMessage = ''), 2000);
      } else {
        statusMessage = 'Failed to send command';
      }
    } catch (error) {
      console.error('Control error:', error);
      statusMessage = 'Error: Cannot connect to ESP32';
    }
  };

  const sendRobotCommand = async (cmd: string) => {
  try {
    const response = await fetch(`http://${esp32Ip}/control?cmd=${cmd}`);
    if (!response.ok) throw new Error("Failed to send command");
  } catch (error) {
    console.error("Robot command error:", error);
  }
};

  const changeResolution = async () => {
    await sendControlCommand('framesize', selectedResolution);
    streamUrl = `${streamUrl}?t=${Date.now()}`;
  };

  const toggleVFlip = async () => {
    vflipEnabled = !vflipEnabled;
    await sendControlCommand('vflip', vflipEnabled ? 1 : 0);
  };

  $: if (blueLightOn) {
    sendRobotCommand('A');   // Replace with your ESP32 command for Blue Light ON
  } else {
    sendRobotCommand('C');  // Replace with your ESP32 command for Blue Light OFF
  }

  $: if (greenLightOn) {
    sendRobotCommand('D');   // Replace with your ESP32 command for Green Light ON
  } else {
    sendRobotCommand('C');  // Replace with your ESP32 command for Green Light OFF
  }  
</script>

<div class="camera-container">
  <!-- Camera Stream -->
  {#if streamError}
    <p class="error">Unable to load stream. Check ESP32 connection at {esp32Ip}</p>
  {:else}
    <img
      src={streamUrl}
      alt="ESP32 Camera Stream"
      on:load={handleStreamLoad}
      on:error={() => (streamError = true)}
      class="camera-stream"
    />
  {/if}

  <!-- Top camera controls (resolution + V-flip) -->
  <div class="overlay top-controls">
    <div class="control-group">
      <label for="resolution">Resolution:</label>
      <select id="resolution" bind:value={selectedResolution} on:change={changeResolution}>
        {#each resolutions as resolution}
          <option value={resolution.value}>{resolution.label}</option>
        {/each}
      </select>
    </div>

    <div class="control-group">
      <button on:click={toggleVFlip} class:active={vflipEnabled}>
        V-Flip: {vflipEnabled ? 'ON' : 'OFF'}
      </button>
    </div>

    {#if statusMessage}
      <div class="status">{statusMessage}</div>
    {/if}
  </div>

  <!-- Robot toggles overlay -->
  <div class="overlay robot-toggles top-left">
    <button class="home-btn" on:click={goHome} aria-label="Go to Home">🏠︎</button>

    <label class="flex items-center gap-2">
      <input type="checkbox" bind:checked={blueLightOn} />
      Blue Lights
    </label>
    <label class="flex items-center gap-2 ml-4">
      <input type="checkbox" bind:checked={greenLightOn} />
      Green Lights
    </label>
  </div>

  <!-- Status overlay -->
  <div class="overlay status-panel top-right">
    <ul>
      <li>Forward: {movingForward ? "✅" : "❌"}</li>
      <li>Backward: {movingBackward ? "✅" : "❌"}</li>
      <li>Left: {turningLeft ? "✅" : "❌"}</li>
      <li>Right: {turningRight ? "✅" : "❌"}</li>
      <li>Grapple: {grapple ? "✅" : "❌"}</li>
      <li>Ungrapple: {ungrapple ? "✅" : "❌"}</li>
      <li>Blue Lights: {blueLightOn ? "✅" : "❌"}</li>
      <li>Green Lights: {greenLightOn ? "✅" : "❌"}</li>
    </ul>
  </div>

  <!-- Directional buttons (now relative to camera feed) -->
    <div class="absolute bottom-6 left-6 bg-white/20 backdrop-blur-md p-4 rounded-2xl shadow-lg border border-white/30 flex flex-col items-center gap-2">
      <button
        class="w-13 h-13 bg-blue-600 text-white text-3xl rounded-full hover:bg-blue-700"
        on:mousedown={() => { movingForward = true; sendRobotCommand('F'); }}
        on:mouseup={() => { movingForward = false; sendRobotCommand('S'); }}
      >
      ▴
      </button>

      <div class="flex gap-2">
        <button
          class="w-13 h-13 bg-blue-600 text-white text-3xl rounded-full hover:bg-blue-700"
          on:mousedown={() => { turningLeft = true; sendRobotCommand('L'); }}
          on:mouseup={() => { turningLeft = false; sendRobotCommand('S'); }}
        >
        ◂
        </button>

        <button
          class="ml-13 w-13 h-13 bg-blue-600 text-white text-3xl rounded-full hover:bg-blue-700"
          on:mousedown={() => { turningRight = true; sendRobotCommand('R'); }}
          on:mouseup={() => { turningRight = false; sendRobotCommand('S'); }}
        >
        ▸
        </button>
      </div>

      <button
        class="w-13 h-13 bg-blue-600 text-white text-3xl rounded-full hover:bg-blue-700"
          on:mousedown={() => { movingBackward = true; sendRobotCommand('B'); }}
          on:mouseup={() => { movingBackward = false; sendRobotCommand('S'); }}
      >
      ▾
      </button>
    </div>
    <!-- Grapple Controls (next to direction pad) -->
  <div class="absolute bottom-6 left-56 bg-white/20 backdrop-blur-md p-4 rounded-2xl shadow-lg border border-white/30 flex flex-col items-start gap-19 ml-5">

  <div class="flex items-center gap-3 justify-start">
    <button class="w-12 h-12 bg-green-600 text-white text-lg rounded-full hover:bg-green-700"
      on:mousedown={() => { grapple = true; sendRobotCommand('G'); }}
      on:mouseup={() => { grapple = false; sendRobotCommand('S'); }}
    >
      X
    </button>
    <span class="text-white font-semibold text-sm">Grapple</span>
  </div>

  <div class="flex items-center gap-3">
    <button class="w-12 h-12 bg-red-600 text-white text-lg rounded-full hover:bg-red-700"
    on:mousedown={() => { ungrapple = true; sendRobotCommand('U'); }}
      on:mouseup={() => { ungrapple = false; sendRobotCommand('S'); }}
    >
      Y
    </button>
    <span class="text-white font-semibold text-sm">Ungrapple</span>
  </div>
</div>
</div>

<style>
.camera-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: black;
}

.camera-stream {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

/* Shared overlay style */
.overlay {
  position: absolute;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(4px);
  padding: 12px;
  border-radius: 12px;
  color: white;
}

/* Top camera controls */
.top-controls {
  top: 12px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 12px;
}

/* Robot toggles overlay */
.robot-toggles.top-left {
  top: 12px;
  left: 12px;
  display: flex;
  align-items: center;
}

/* Status panel */
.status-panel.top-right {
  top: 12px;
  right: 12px;
  font-weight: bold;
}

.error {
  color: red;
  font-weight: bold;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

/* Button active state */
button.active {
  background: #4caf50;
}

.robot-toggles.top-left {
  top: 12px;
  left: 12px;
  display: flex;
  align-items: center;
  gap: 8px; /* spacing between home button and checkboxes */
}

.home-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.6);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  cursor: pointer;
  backdrop-filter: blur(4px);
  transition: background 0.2s, transform 0.1s;
  margin-right: 10px; /* <- adds space to the right */
}

.home-btn:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: scale(1.1);
}

</style>
