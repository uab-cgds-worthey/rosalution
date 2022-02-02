<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import NavigationComponent from '@/components/NavigationComponent.vue';
</script>

<template>
  <router-view></router-view>
  <!-- sidebar -->
  <app-sidebar>
    <NavigationComponent/>
  </app-sidebar>

  <!-- Putting inside content tag breaks the app -->

</template>

<style>

</style>
