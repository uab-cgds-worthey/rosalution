<template>
  <app-header>
  <RosalutionHeader
    :username="auth.getUsername()"
  >
  <div></div>
  </RosalutionHeader>
</app-header>
<app-content>
  <img :src="imageSrc" :data-test="`rosalution-file-${this.file_id}`"/>
</app-content>
</template>

<script>
import RosalutionHeader from '@/components/RosalutionHeader.vue';

import {authStore} from '@/stores/authStore.js';
import FileRequests from '@/fileRequests.js';

export default {
  name: 'file-view',
  components: {
    RosalutionHeader,
  },
  props: ['file_id'],
  data: function() {
    return {
      auth: authStore,
      imageSrc: new URL('/src/assets/rosalution-logo.svg', import.meta.url),
    };
  },
  created() {
    this.sectionImageUpdate();
  },
  methods: {
    async sectionImageUpdate() {
      const loadingImage = await FileRequests.getImage(this.file_id);
      this.imageSrc = loadingImage;
    },
  },
};
</script>

<style scoped>
  div {
    flex: 1 1 auto;
  }

  img {
    margin: var(--p-10);
  }
</style>
