<template>
  <footer>
    <a class="footer-text" href="https://github.com/uab-cgds-worthey/rosalution">
      Center for Computational Genomics and Data Science, University of Alabama at Birmingham, Heersink School of
       Medicine
    </a>
  </footer>
</template>

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
  padding-bottom: var(--p-1);
}

.footer-text {
  font-size: var(--p-14);
}

</style>
