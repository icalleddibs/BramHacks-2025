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
    font-size: 1.6rem;
    border-radius: 9999px;
    background: rgba(30, 58, 138, 0.7);
    color: white;
    font-weight: bold;
    transition: transform 0.2s, background 0.2s;
    text-align: center;
  }

  .section-buttons-vertical button:hover {
    transform: scale(1.05);
    background: rgba(37, 99, 235, 0.85);
  }

  home-title {
    font-size: 4rem;
    position: absolute;
    top: 30%; /* adjust vertical position as needed */
    right: 20rem; /* same offset as buttons */
    text-align: right;
    color: white;
  }
</style>


<section
  id="section1"
  use:inview
  on:inview_change={(e) => (section1InView = e.detail.inView)}
  class="relative h-screen flex flex-col justify-center items-center text-white bg-cover bg-center"
  style="background-image: url('/images/homepage.png');"
>
  <home-title>MicroMapping</home-title>
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

      <!-- make 5 colums for all 5 people, a little image and a short bio -->
        <div class="grid-container mt-8">
            <div class="column-item">
                <h3 class="text-2xl font-bold mb-2">Adara Hagman</h3>
                <p class="text-sm">Digital Media Arts student at York University. Interested in mechatronics, space science, and assistive devices.</p>
            <a
                href="https://www.linkedin.com/in/adarahagman/"
                target="_blank"
                class="hover:decoration-orange-500 underline transition-all duration-200"
                style="color: #fe8080ff"
            >LinkedIn</a>
            <span class="text-orange-400">|</span>
            <a
                href="https://www.zenithpathways.ca/adara-hagman"
                target="_blank"
                class="hover:decoration-orange-500 underline transition-all duration-200"
                style="color: #fe8080ff"
            >Zenith Fellow '24</a>
            </div>

            <div class="column-item">
                <h3 class="text-2xl font-bold mb-2">Adithi Balaji</h3>
                <p class="text-sm">Master's candidate in Physics at the University of Toronto, with research interests in Earth Observation and planetary science.</p>
                <a
                    href="https://www.linkedin.com/in/adithi-balaji-00483827b/"
                    target="_blank"
                    class="hover:decoration-orange-500 underline transition-all duration-200"
                    style="color: #fe8080ff"
                >LinkedIn</a>
                <span class="text-orange-400">|</span>
                <a
                    href="https://www.zenithpathways.ca/adithi-balaji"
                    target="_blank"
                    class="hover:decoration-orange-500 underline transition-all duration-200"
                    style="color: #fe8080ff"
                >Zenith Fellow '25</a>
            </div>

            <div class="column-item">
                <h3 class="text-2xl font-bold mb-2">Diba Alam</h3>
                <p class="text-sm">Engineering Science (Machine Intelligence & Robotics) student at the University of Toronto. Passionate about leveraging AI & robotics to support space exploration.
                </p>
                <a
                    href="https://www.linkedin.com/in/diba-alam/"
                    target="_blank"
                    class="hover:decoration-orange-500 underline transition-all duration-200"
                    style="color: #fe8080ff"
                >LinkedIn</a>
                <span class="text-orange-400">|</span>
                <a
                    href="https://www.zenithpathways.ca/diba-alam"
                    target="_blank"
                    class="hover:decoration-orange-500 underline transition-all duration-200"
                    style="color: #fe8080ff"
                >Zenith Fellow '24</a>
            </div>

            <div class="column-item">
                <h3 class="text-2xl font-bold mb-2">Kartik Jassal</h3>
                <p class="text-sm">desc.</p>
                <a
                    href="https://www.linkedin.com/in/kartikjassal/"
                    target="_blank"
                    class="hover:decoration-orange-500 underline transition-all duration-200"
                    style="color: #fe8080ff"
                >LinkedIn</a>
            </div>

            <div class="column-item">
                <h3 class="text-2xl font-bold mb-2">Umar Shabbir</h3>
                <p class="text-sm">Aerospace engineering graduate from Toronto Metropolitan University with an interest in rockets, rovers, and robotics.</p>
                <a
                    href="https://www.linkedin.com/in/umaremshabbir/"
                    target="_blank"
                    class="hover:decoration-orange-500 underline transition-all duration-200"
                    style="color: #fe8080ff"
                >LinkedIn</a>
                <span class="text-orange-400">|</span>
                <a
                    href="https://www.zenithpathways.ca/umar-shabbir"
                    target="_blank"
                    class="hover:decoration-orange-500 underline transition-all duration-200"
                    style="color: #fe8080ff"
                >Zenith Fellow '25</a>
            </div>
        </div>
    </div>
  {/if}
</section>
