<script lang="ts">
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

  const changeResolution = async () => {
    await sendControlCommand('framesize', selectedResolution);
    streamUrl = `${streamUrl}?t=${Date.now()}`;
  };

  const toggleVFlip = async () => {
    vflipEnabled = !vflipEnabled;
    await sendControlCommand('vflip', vflipEnabled ? 1 : 0);
  };
</script>

<!-- Wrapper fills the full screen -->
<div class="camera-page">
  <!-- Controls bar (fixed to top) -->
  <div class="controls">
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

  <!-- Camera Stream fills the rest -->
  <div class="stream-container">
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
  </div>
</div>

<style>
  .camera-page {
    display: flex;
    flex-direction: column;
    height: 100vh;
    width: 100vw;
    overflow: hidden;
    background: #000;
  }

  .controls {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 20px;
    background: #1e1e2f;
    color: white;
    padding: 10px 20px;
    position: sticky;
    top: 0;
    z-index: 10;
  }

  .control-group {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  label {
    font-weight: bold;
  }

  select {
    padding: 6px 10px;
    border-radius: 4px;
    border: none;
    outline: none;
    background: #2d2d3d;
    color: white;
  }

  button {
    padding: 8px 16px;
    border-radius: 9999px;
    border: none;
    background: #4a90e2;
    color: white;
    font-weight: bold;
    cursor: pointer;
    transition: background 0.2s;
  }

  button:hover {
    background: #357ab7;
  }

  button.active {
    background: #4caf50;
  }

  .status {
    font-weight: bold;
    color: #4caf50;
  }

  .stream-container {
  flex: 1 1 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
}

.camera-stream {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain; /* keeps aspect ratio and fits within container */
}

  .error {
    color: red;
    font-weight: bold;
  }
</style>
