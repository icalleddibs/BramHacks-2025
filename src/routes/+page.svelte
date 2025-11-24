<script lang="ts">
  import { inview } from 'svelte-inview';
  import { fly, fade } from 'svelte/transition';

  // Track which sections are in view
  let section1InView = false;
  let section2InView = false;
  let section3InView = false;
  let section4InView = false;
  // Navigation function
  const goTo = (path: string) => {
    window.location.href = path;
  };
  // Scrolling function
  const scrollToSection = (id: string) => {
    const el = document.getElementById(id);
    el?.scrollIntoView({ behavior: 'smooth' });
  };
</script>

<style>
  h1 {
      font-size: 3rem;
      color: rgb(219, 236, 255);
      font-weight: bold;
  }
  
  /* Right-aligned vertical button container */
  .section-buttons-vertical {
    position: absolute;
    top: 50%;
    right: 20rem; /* distance from the right edge */
    transform: translateY(-50%);
    display: flex;
    flex-direction: column;
    gap: 1rem; /* spacing between buttons */
    margin-top: 5rem;
  }

  .section-buttons-vertical button {
    padding: 0.75rem 1.5rem;
    font-size: 1.3rem;
    border-radius: 9999px;
    background: rgba(30, 58, 138, 0.7);
    color: white;
    transition: transform 0.2s, background 0.2s;
    text-align: center;
    font-family: 'Epilogue';
  }

  .section-buttons-vertical button:hover {
    transform: scale(1.05);
    background: rgba(37, 99, 235, 0.85);
  }

  home-title {
    font-size: 4rem;
    position: absolute;
    top: 25%; /* adjust vertical position as needed */
    right: 20rem; /* same offset as buttons */
    text-align: right;
    color: #1c2da1;
    font-weight: bold;
    font-family: 'Candal', sans-serif;
  }

  home-desc {
    font-size: 1.2rem;
    position: absolute;
    top: 39%; /* adjust vertical position as needed */
    right: 20rem; /* same offset as buttons */
    text-align: right;
    color: white;
    font-family: 'Candal', sans-serif;
  }

  .blue-link {
  color: #b0defd;           /* your blue theme */
  text-decoration: none;     /* removes underline */
  font-weight: 500;
  transition: color 0.2s, text-decoration 0.2s;
  text-decoration: underline;
}

.blue-link:hover {
  color: #0034b6;            /* slightly darker blue on hover */
  text-decoration: underline; /* subtle underline on hover */
}
</style>


<section
  id="section1"
  use:inview
  on:inview_change={(e) => (section1InView = e.detail.inView)}
  class="relative h-screen flex flex-col justify-center items-center text-white bg-cover bg-center"
  style="background-image: url('/images/homepage.png');"
>
  <home-title>Project PONTUS</home-title>
  <home-desc>(Plastic Observation and Navigation Tracking Using Satellites) |  
    <a href="https://github.com/icalleddibs/BramHacks-2025" target="_blank" rel="noopener noreferrer" class="blue-link">GitHub Repository</a></home-desc> 

  <!-- Right-aligned vertical section buttons -->
  <div class="section-buttons-vertical">
    <button on:click={() => scrollToSection('section2')}>Mission Statement</button>
    <button on:click={() => scrollToSection('section3')}>Functionalities</button>
    <button on:click={() => scrollToSection('section4')}>Meet the Team</button>
  </div>

</section>

<section
  id="section2"
  use:inview
  on:inview_change={(e) => section2InView = e.detail.inView}
  class="relative h-screen flex flex-col justify-center items-center text-white bg-cover bg-center"
  style="background-image: url('/images/homepage2.png');"
>
  <!-- Abstract wavy top of Section 2 -->
  <svg
    class="absolute top-0 left-0 w-full"
    viewBox="0 0 1440 60"
    preserveAspectRatio="none"
    style="height: 40px;"
  >
    <path
      d="M0,20 C360,50 1080,10 1440,30 L1440,0 L0,0 Z"
      fill="#293fc1ff"
    ></path>
  </svg>

  <h1>MISSION STATEMENT</h1>
  <p class="font-bold text-lg">Satellite microplastic concentration data + ocean current models = pollution forecasting. </p>
  <br>
  <p>We identify where microplastics will concentrate before they arrive,</p>
<p>enabling strategic intervention at future hotspots.</p>

</section>

<section
  id="section3"
  use:inview
  on:inview_change={(e) => section3InView = e.detail.inView}
  class="relative h-screen flex flex-col justify-center items-center text-white bg-cover bg-center"
  style="background-image: url('/images/homepage3.png');"
>
  <!-- Abstract wavy top of Section 3 -->
  <svg
    class="absolute top-0 left-0 w-full"
    viewBox="0 0 1440 60"
    preserveAspectRatio="none"
    style="height: 40px;"
  >
    <path
      d="M0,20 C360,50 1080,0 1440,25 L1440,0 L0,0 Z"
      fill="#293fc1ff"
    ></path>
  </svg>

  <h1>Functionalities</h1>
  <p>Explore the various functionalities of our platform.</p>
  <!-- 2-column container -->
  <div class="grid grid-cols-1 md:grid-cols-2 gap-12 w-full max-w-4xl px-4 mt-20">
    <!-- Column 1 -->
    <div class="flex flex-col items-center text-center">
      <img src="/images/truck-icon.png" alt="Truck Icon" class="w-38 h-30 mb-4" />
      <h2 class="text-2xl font-bold mb-2">Robot Controller</h2>
      <button 
        class="mt-4 px-6 py-3 rounded-full bg-gradient-to-r from-[#1e3a8a] via-[#2563eb] to-[#2771e8] text-white text-lg hover:scale-105 transition-transform"
        on:click={() => goTo('/controls')}
      >
        Explore Controls
      </button>
      <button 
        class="mt-4 px-6 py-3 rounded-full bg-gradient-to-r from-[#1e3a8a] via-[#2563eb] to-[#2771e8] text-white text-lg hover:scale-105 transition-transform"
        on:click={() => goTo('/hardware')}
      >
        Hardware Information
      </button>
    </div>

    <!-- Column 2 -->
    <div class="flex flex-col items-center text-center">
      <img src="/images/globe-icon.png" alt="Globe Icon" class="w-33 h-28 mb-4" />
      <h2 class="mt-2 text-2xl font-bold mb-2">Oceanographic Map</h2>
      <button 
        class="mt-4 px-6 py-3 rounded-full bg-gradient-to-r from-[#1e3a8a] via-[#2563eb] to-[#2771e8] text-white text-lg hover:scale-105 transition-transform"
        on:click={() => goTo('/map')}
      >
        Explore Map
      </button>
      <button 
        class="mt-4 px-6 py-3 rounded-full bg-gradient-to-r from-[#1e3a8a] via-[#2563eb] to-[#2771e8] text-white text-lg hover:scale-105 transition-transform"
        on:click={() => goTo('/science')}
      >
        Scientific Datasets
      </button>
    </div>
  </div>
</section>

<section
  id="section4"
  use:inview
  on:inview_change={(e) => section4InView = e.detail.inView}
  class="relative h-screen flex flex-col justify-center items-center text-white bg-cover bg-center"
  style="background-image: url('/images/homepage4.png');"
>

  {#if section4InView}
    <div transition:fly={{ y: 50, duration: 800 }}>
      <h1>Meet the Team</h1>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8 max-w-6xl mx-auto">
        <!-- First row: 3 cards -->
        <div class="bg-white/10 p-6 rounded-2xl flex flex-col items-center text-center w-90 h-50">
          <h3 class="text-2xl font-bold mb-2">Adara Hagman</h3>
          <p class="text-sm mb-4">Digital Media Arts student at York University. Interested in mechatronics, space science, and assistive devices.</p>
          <div class="flex gap-2">
            <a href="https://www.linkedin.com/in/adarahagman/" target="_blank" class="underline text-blue-800 hover:text-blue-300">LinkedIn</a>
          </div>
        </div>

        <div class="bg-white/10 p-6 rounded-2xl flex flex-col items-center text-center w-90 h-50">
          <h3 class="text-2xl font-bold mb-2">Adithi Balaji</h3>
          <p class="text-sm mb-4">Master's candidate in Physics at the University of Toronto, with research interests in Earth Observation and planetary science.</p>
          <div class="flex gap-2">
            <a href="https://www.linkedin.com/in/adithi-balaji-00483827b/" target="_blank" class="underline text-blue-800 hover:text-blue-300">LinkedIn</a>
          </div>
        </div>

        <div class="bg-white/10 p-6 rounded-2xl flex flex-col items-center text-center w-90 h-50">
          <h3 class="text-2xl font-bold mb-2">Diba Alam</h3>
          <p class="text-sm mb-4">Engineering Science (Machine Intelligence & Robotics) student at the University of Toronto. Passionate about leveraging AI & robotics to support space exploration.</p>
          <div class="flex gap-2">
            <a href="https://www.linkedin.com/in/diba-alam/" target="_blank" class="underline text-blue-800 hover:text-blue-300">LinkedIn</a>
          </div>
        </div>

        <!-- Second row: 2 cards, centered -->
        <div class="md:col-span-3 flex justify-center gap-4 mt-4">
          <div class="bg-white/10 p-6 rounded-2xl flex flex-col items-center text-center w-90 h-50">
            <h3 class="text-2xl font-bold mb-2">Kartik Jassal</h3>
            <p class="text-sm mb-4">Space Engineering student at York University. Passionate about space robotics and GNC for space debris collection and on-orbit assembly.</p>
            <div class="flex gap-2">
              <a href="https://www.linkedin.com/in/kartikjassal/" target="_blank" class="underline text-blue-800 hover:text-blue-300">LinkedIn</a>
            </div>
          </div>

          <div class="bg-white/10 p-6 rounded-2xl flex flex-col items-center text-center w-90 h-50">
            <h3 class="text-2xl font-bold mb-2">Umar Shabbir</h3>
            <p class="text-sm mb-4">Aerospace engineering graduate from Toronto Metropolitan University with an interest in rockets, rovers, and robotics.</p>
            <div class="flex gap-2">
              <a href="https://www.linkedin.com/in/umaremshabbir/" target="_blank" class="underline text-blue-800 hover:text-blue-300">LinkedIn</a>
            </div>
          </div>
        </div>
      </div>
    </div>
    <button
      class="absolute bottom-6 px-4 py-3 rounded-2xl text-sm bg-[#3951d4] text-white text-lg hover:scale-105 transition-transform"
      on:click={() => scrollToSection('section1')}
    >
      Home
    </button>
  {/if}
</section>

