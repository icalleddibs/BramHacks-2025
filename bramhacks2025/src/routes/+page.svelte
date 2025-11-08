<script lang="ts">
  // Navigation function
  const goTo = (path: string) => {
    window.location.href = path;
  };
</script>

<h1>MicroMapping</h1>

<button on:click={() => goTo('/map')}>Habitability Map</button>
<button on:click={() => goTo('/animate')}>Animation</button>
