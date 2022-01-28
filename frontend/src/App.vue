<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import Navigation from '@/components/Navigation.vue';
</script>

<template>
  <!-- sidebar -->
  <sidebar>
    <Navigation/>
  </sidebar>

  <!-- Putting inside content tag breaks the app -->
  <router-view></router-view>
</template>

<style>

</style>
