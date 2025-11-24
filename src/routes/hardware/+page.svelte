<h1 class="title">Hardware Overview</h1>

<script lang="ts">
  import { goto } from '$app/navigation'; 

  function goHome() {
    goto('/');
  }
</script>

<button class="home-btn" on:click={goHome} aria-label="Go to Home">
  🏠︎
</button>

<!-- Content section -->
<div class="content-section">
  <h2>Meet Scrappy!</h2>
  <p>
    Scrappy is our on-shore validation robot and proof of concept for a future ocean-deployable system.
    Controlled remotely by this webapp, scrappy lays the groundwork for a 
    scalable fleet of robots that can verify satellite predictions and support large-scale cleanup efforts like 
    The Ocean Cleanup and 4Ocean. By combining machine learning, robotics, and satellite data, we’re creating a smarter, 
    scalable way to protect our oceans.
  </p>
  <div class="media">
    <!-- svelte-ignore a11y_img_redundant_alt -->
    <img src="images/robotPhoto.jpg" alt="Image of Scrappy Robot">
  </div>
  <p class="caption">Scrappy's Final Version</p>
</div>

<div class="content-section">
  <h2>Specifications</h2>
  <p>
    Powered by an ESP32, Scrappy navigates shorelines to confirm garbage piles, as predicted by our mathematical model.
    It features:
  </p>
  <ul class="list">
      <li>Onboard camera for visual verification</li>
      <li>Steering and grappling mechanism through remote control</li>
      <li>Green LEDs to enhance plastic detection underwater</li>
      <li>YOLOv8-based object recognition</li>
  </ul>
  <div class="media">
    <!-- svelte-ignore a11y_media_has_caption -->
    <video controls>
      <source src="images/robotVideo.MOV" type="video/mp4">
      Your browser does not support the video tag.
    </video>
  </div>
  <p class="caption">Scrappy Demo Video</p>
</div>

<div class="content-section">
  <h2>Hardware Development</h2>
  <p>
    The hardware developed for Scrappy was done during the Hackathon, using the tools available by a hardware sponsor, Make Stuff Move.
    They provided microcontrollers, motors, wooden pieces, tools, and other components that allowed us to rapidly prototype and build Scrappy.
    Short on time, we focused on creating a functional moving prototype capable of grasping pieces of trash, with a camera for visual feedback.
  </p>
  <div class="media">
    <img src="images/robotWiringDiagram.jpeg" alt="Wiring Diagram">
  </div>
  <p class="caption">Wiring Diagram</p>
  <p>
    The ESP32 microcontroller's onboard webserver and WiFi capabilities made it an ideal choice for remote operation via our webapp.
    We developed buttons on the web interface that would write to the ESP32's webserver, and the microcontroller would read these commands to control the motors and servos accordingly.
    The camera feed was also streamed to the webapp, providing real-time visual feedback for precise navigation and trash collection.
  </p>
  <div class="video-media">
    <!-- svelte-ignore a11y_media_has_caption -->
    <video controls>
      <source src="images/grapple video (1).mp4" type="video/mp4">
      Your browser does not support the video tag.
    </video>
  </div>
  <p class="caption">Scrappy Demo Video</p>
  <div class="button-wrapper">
    <button class="map-btn" on:click={() => goto('/controls')}>
      Click here to check out the remote controls!
    </button>
  </div>
</div>

<div class="content-section">
  <h2>Future Improvements</h2>
  <p>
    In future iterations, we plan to enhance Scrappy's capabilities by adding waterproofing to allow for water deployment, improving the gripping mechanism for better trash collection, and integrating more advanced sensors for environmental monitoring.
    Additionally, we aim to optimize the power consumption for longer operational periods and explore swarm robotics to enable multiple units to work collaboratively in larger areas.
  </p>
</div>

<!-- Style setup to make the background appealing and minimal -->

<style>

:global(body) {
  background-color: #a2c5e1; /* soft light blue */
  margin: 0;
  padding: 0;
}

/* --- Title --- */
.title {
  text-align: center;
  margin-top: 2rem;
  font-size: 2.3rem;
  color: #0034b6;
  font-weight: 700;
}

/* --- Section Container --- */
.content-section {
  max-width: 900px;
  margin: 2rem auto;
  padding: 1.8rem;
  background: white;
  border-radius: 14px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
  border-left: 18px solid #0034b6;
}

.content-section h2 {
  margin-top: 0;
  color: #0a4fff;
  font-size: 1.7rem;
  border-bottom: 2px solid #d7e4ff;
  padding-bottom: 0.3rem;
  font-weight: bold;
}

.content-section p {
  font-size: 1.05rem;
  line-height: 1.65;
  margin-top: 1rem;
}

/* --- Home Button --- */
.home-btn {
  position: fixed;
  top: 12px;
  left: 12px;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.6);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  cursor: pointer;
  backdrop-filter: blur(4px);
  z-index: 1000;
  transition: background 0.2s, transform 0.1s;
}

.home-btn:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: scale(1.1);
}

.list {
  margin-top: 0.5rem;
  padding-left: 1.5rem;
  line-height: 1;
}

.list li {
  margin-bottom: 0.5rem;
  padding-left: 0.3rem;
}

:global(.list li::marker) {
  color: #0a4fff;
  font-size: 2rem;
}

:global(ul.list) {
  list-style: disc;
}

.media {
  margin: 1.5rem auto;
  width: 50%;
  text-align: center;
}

.video-media {
  margin: 1.5rem auto;
  width: 100%;
  text-align: center;
}

.media img,
.media video {
  max-width: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.caption {
  font-size: 0.9rem;
  color: #4a4a4a;
  margin-top: 0.4rem;
  text-align: center;
}

.button-wrapper {
  display: flex;
  justify-content: center; /* centers horizontally */
  margin: 1.5rem 0;       /* optional spacing above/below */
}

.map-btn {
  background-color: #0a4fff;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s, transform 0.1s;
}

.map-btn:hover {
  background-color: #0034b6;
  transform: scale(1.05);
}

</style>
