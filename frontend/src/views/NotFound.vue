
<template>
  <!--Header-->
  <app-header>rosalution</app-header>
  <!--Content-->
  <app-content>
    <h1>404 Not Found</h1>
  </app-content>
</template>

<script>

export default {
  name: 'not-found-view',
  created: function() {
    const currentUrl = window.location.pathname;
    console.error(currentUrl);
    console.error(this.$route);
  },
};

</script>

