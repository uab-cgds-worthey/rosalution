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
      return new Date().getFullYear();
    },
  },
};
</script>

<style>
footer {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  background-color: var(--primary-background-color);
  text-align: center;
  position: fixed;
  bottom: 0;
  width: 100%;
}

.footer-link {
  font-size: 0.75em;
}

.copy-left {
  display: inline-block;
  text-align: right;
  margin: 0px;
  transform: scaleX(-1);
}
</style>
