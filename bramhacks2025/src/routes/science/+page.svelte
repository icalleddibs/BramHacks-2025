<h1>empty science</h1>

<script lang="ts">
  import { goto } from '$app/navigation';

  function goHome() {
    goto('/');
  }
</script>

<button class="home-btn" on:click={goHome} aria-label="Go to Home">
  🏠︎
</button>

<style>
.home-btn {
  position: fixed;
  top: 12px;
  left: 12px;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.6); /* slightly translucent */
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  cursor: pointer;
  backdrop-filter: blur(4px);
  z-index: 1000; /* ensure it’s above other elements */
  transition: background 0.2s, transform 0.1s;
}

.home-btn:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: scale(1.1);
}
</style>
