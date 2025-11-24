<h1 class="title">Scientific Research</h1>

<script lang="ts">
  import { goto } from '$app/navigation'; 

  function goHome() {
    goto('/');
  }
</script>

<button class="home-btn" on:click={goHome} aria-label="Go to Home">
  🏠︎
</button>

<!-- 📦 Your content section -->
<div class="content-section">
  <h2>Background</h2>
  <p>
    Microplastic pollution is a significant concern for human health, wildlife conservation, and ocean chemistry and continues to 
    increase at an alarming rate. Most current market solutions or scientific projects focus on determining where pollution is now. 
    We are instead proposing a system to harness the power of satellite data to predict and intercept future garbage hotspots before they form.
    This allows us to support large-scale clean-up efforts and prevent further environmental damage. Having a predictive model also enables
    strategic deployment of resources to areas that will need it most, improving efficiency and effectiveness in combating plastic pollution.
    In tandem with our predictive model, we have developed a robotic system meant to autonomously navigate towards predicted hotspots and verify 
    the accuracy of our forecasts through computer vision.
  </p>
</div>

<div class="content-section">
  <h2>Mathematical Model</h2>
  <p>
    Our mathematical model breaks pollution into thousands of tiny "particles" and uses physics-based simulation to calculate 
    where ocean currents will push them. The model accounts for both the main current flow and random mixing from waves and turbulence, 
    showing how particles spread out or bunch together in certain areas over time. Project PONTUS is a webapp with a live animation of 
    future movement predictions.
  </p>
  <p>
    Lagrangian particle tracking was used as a quick and effective way to simulate the transport of particules.
    However, we acknowledge that this model can be improved upon as it tends to result in chaotic behaviour over longer timescales. 
    In the future, we would consider further mathematical and AI/ML methods to refine and enhance the accuracy of our predictions.
    Below is a snapshot of the forecasted microplastic concentration map 30 days after intaking satellite data.
  </p>
  <div class="media">
    <!-- svelte-ignore a11y_img_redundant_alt -->
    <img src="images/microplasticsMap.png" alt="Image of Microplastics Map">
  </div>
</div>

<div class="content-section">
  <h2>Interactive Map</h2>
  <p>
    The forecasted microplastic concentration map determines where microplastic “particles” will go after 30 days of ocean movement.
    While this map shows the evolution of a global distribution, this is a particularly useful tool to track down pollution from a point source.
    The varying colours represent different concentrations of microplastics, with red indicating high concentrations and yellow indicating low concentrations.
  </p>
  <p>
    The results of our mathematical model were extracted into GEOJson format, which were then visualized based on location, concentration level, and time stamp.
    These were then overlaid onto an interactive world map, allowing users to zoom in and explore specific regions of interest.
    The map has a static and animated mode, where users can investigate the movement of microplastics over the 30-day period, either as a single snapshot or as a time-lapse animation.
  </p>
  <div class="button-wrapper">
    <button class="map-btn" on:click={() => goto('/map')}>
      Click here to check out the map!
    </button>
  </div>
</div>

<div class="content-section">
  <h2>Datasets</h2>
  <p>
    We leveraged NASA's <a href="https://podaac.jpl.nasa.gov/dataset/CYGNSS_L3_MICROPLASTIC_V3.2" target="_blank" rel="noopener noreferrer" class="blue-link">
CYGNSS L3 Microplastic</a> and <a href="https://podaac.jpl.nasa.gov/dataset/OSCAR_L4_OC_NRT_V2.0" target="_blank" rel="noopener noreferrer" class="blue-link">
OSCAR L4 Ocean Current</a> datasets to inform our mathematical model.  
CYGNSS provided insight into areas with high microplastic concentrations, while OSCAR data helped identify local current patterns influencing debris accumulation. Together, these datasets guided Scrappy’s navigation and sampling to verify predicted plastic hotspots.
The CYGNSS dataset only covers the global oceans within mid-latitude regions in both hemispheres (between 37.4°S and 37.4°N), leading to gaps in the map data near the poles.
  </p>
</div>

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

.blue-link {
  color: #0a4fff;           /* your blue theme */
  text-decoration: none;     /* removes underline */
  font-weight: 500;
  transition: color 0.2s, text-decoration 0.2s;
}

.blue-link:hover {
  color: #0034b6;            /* slightly darker blue on hover */
  text-decoration: underline; /* subtle underline on hover */
}

.media {
  margin: 1.5rem auto;
  width: 100%;
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
