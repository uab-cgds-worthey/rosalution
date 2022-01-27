<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import Navigation from "@/components/Navigation.vue";
</script>

<template>



  <!-- sidebar -->
  <Navigation class="sidebar"/>

  <!--content-->
  <router-view></router-view>

  <div class="content">Content Box</div>
  <div class="footer">Footer Box</div>

</template>

<style>

</style>
