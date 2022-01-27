<template>
  <div class="navbar">
    <div>
      <router-link to="/" class="navtitle">diverGen</router-link>
    </div>
    <nav class="navitem">
      <router-link class="" to="/about">About</router-link>
    </nav>
    <nav class="navitem">
      <router-link to="/contact">Contact Us</router-link>
    </nav>
  </div>
</template>

<style>
  .navbar {
    color: rgb(55 65 81);
    background-color: rgb(5 150 105);
    height: 100%;
  }

  .navtitle {
    color: rgb(17 24 39);
    font-size: 1.125rem;
    font-weight: 600;
    line-height: 1.75rem;
    letter-spacing: 0.1em;
  }

  /** Was this intended to be hover? focus:outline-none, focus:shadow-outline */
  .navtitle:focus {
    box-shadow: var(--tw-ring-inset) 0 0 0 calc(3px + var(--tw-ring-offset-width)) var(--tw-ring-color);
    outline: 2px solid transparent;
    outline-offset: 2px;
    border-radius: 0.5rem;
  }

  .navitem {
    padding-top: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
  }
</style>