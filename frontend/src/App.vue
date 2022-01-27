<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import Navigation from "@/components/Navigation.vue";
</script>

<template>
  <section id="page">
    <!-- sidebar -->
    <sidebar>
      <Navigation/>
    </sidebar>

    <!--content-->
      <router-view></router-view>

    <footer>
      Footer
    </footer>
  </section>
</template>

<style>

</style>
