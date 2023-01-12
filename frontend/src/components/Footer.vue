<template>
  <footer>
    <a class="footer-link" href="https://github.com/uab-cgds-worthey/rosalution/blob/main/COPYING">
      Copyleft <span class="copy-left">&copy;</span> {{ currentYear }} Center for Computational Genomics and Data
      Science, UAB School of Medicine
    </a>
  </footer>
</template>


<script>
export default {
  computed: {
    currentYear() {
      return new Date().getFullYear()
    }
  }
}
</script>

<style>
footer {
  background-color: var(--primary-background-color);
  padding: 1em;
  text-align: center;
  position: fixed;
  bottom: 0;
  /* stick to the bottom */
  width: 100%;
  /* take up the full width of the parent container */
}

.footer-link {
  font-size: 0.75em;
  /* 25% of the parent font size */
}

.copy-left {
  display: inline-block;
  text-align: right;
  margin: 0px;
  transform: scaleX(-1);
}
</style>
