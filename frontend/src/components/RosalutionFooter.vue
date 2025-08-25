<template>
  <footer class="footer-text">
    <a href="https://sites.uab.edu/cgds/">
      Center for Computational Genomics and Data Science, University of Alabama at Birmingham, Heersink School of
       Medicine
    </a>
    •
    <a href="https://github.com/uab-cgds-worthey/rosalution">rosalution {{version}}</a>
  </footer>
</template>

<script setup>
const version = import.meta.env.VITE_ROSALUTION_VERSION;
</script>

<style>
footer {
  display: flex;
  background-color: var(--primary-background-color);
  position: fixed;
  bottom: 0;
  width: 100%;
  justify-content: center;
  gap: 1rem;
}

.footer-text {
  font-size: var(--p-14);
}
</style>
