<template>
  <!--Header-->
  <app-header>Header Box - Analysis Listing</app-header>
  <!--Content-->
  <app-content>
    <!-- Implicit -->
    <font-awesome-icon icon="user" />
    <font-awesome-icon icon="users" />
    <font-awesome-icon icon="user-group" />
    <font-awesome-icon icon="calendar" />
    <font-awesome-icon icon="book-open" />
    <font-awesome-icon icon="list" />
    <font-awesome-icon icon="layer-group" />
    <font-awesome-icon icon="box-archive" />
    <font-awesome-icon icon="question" />
    <font-awesome-icon icon="clock" />
    <font-awesome-icon icon="clipboard-check" />

    <br>

    <!-- Explicit -->
    <font-awesome-icon :icon="['fas', 'user']" />
    <font-awesome-icon :icon="['fas', 'users']" />
    <font-awesome-icon :icon="['fas', 'user-group']" />
    <font-awesome-icon :icon="['fas', 'calendar']" />
    <font-awesome-icon :icon="['fas', 'book-open']" />
    <font-awesome-icon :icon="['fas', 'list']" />
    <font-awesome-icon :icon="['fas', 'layer-group']" />
    <font-awesome-icon :icon="['fas', 'box-archive']" />
    <font-awesome-icon :icon="['fas', 'question']" />
    <font-awesome-icon :icon="['fas', 'clock']" />
    <font-awesome-icon :icon="['fas', 'clipboard-check']" />
  </app-content>
</template>

<script>
import Analyses from '@/models/analyses.js';
import AppIconsVue from '../components/icons/AppIcons.vue';

export default {
  name: 'analysis-listing-view',
  components: {
    AppIconsVue
  },
  data: function() {
    return {
      analysisList: [],
    };
  },
  created() {
    this.getListing();
  },
  methods: {
    async getListing() {
      this.analysisList.length = 0;
      this.analysisList.push(...await Analyses.all());
    },
  },
};
</script>
