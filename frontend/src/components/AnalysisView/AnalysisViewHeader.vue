<template>
  <RosalutionHeader :username="this.username" :titleText="this.titleText" :actions="this.actions">
    <a
      v-for="link in third_party_links"
      :key="link.type"
      :href="link.link"
      target="_blank"
      class="logo-link"
      :data-test="`${link.type.toLowerCase().replace('_com', '')}-link`"
    >
      <img :src="getIconSrc(link.type)" :class="getIconClass(link.type)" />
    </a>
    <div>
      <a v-for="anchorLink in this.sectionAnchors" :href="this.toAnchorId(anchorLink)" :key="anchorLink">
        {{ anchorLink }}
      </a>
    </div>
  </RosalutionHeader>
</template>

<script>
import RosalutionHeader from '@/components/RosalutionHeader.vue';

export default {
  name: 'analysis-view-header-component',
  components: {
    RosalutionHeader,
  },
  props: {
    username: {
      type: String,
      default: undefined,
      required: false,
    },
    titleText: {
      type: String,
      required: true,
    },
    sectionAnchors: {
      type: Array,
      required: true,
    },
    actions: {
      type: Array,
      required: true,
    }, 
    third_party_links: {
      type: Array,
      default: () => [],
    },
  },
  methods: {
    toAnchorId(anchorText) {
      return `#${anchorText.replace(' ', '_')}`;
    },
    getIconSrc(linkType) {
      if (linkType === 'monday_com') {
        return '/src/assets/monday-avatar-logo.svg';
      } else if (linkType === 'phenotips_com') {
        return '/src/assets/phenotips-favicon-96x96.png';
      }
    },
    getIconClass(linkType) {
      if (linkType === 'monday_com') {
        return 'monday-icon';
      } else if (linkType === 'phenotips_com') {
        return 'phenotips-icon';
      }
    },
  },
};
</script>

<style scoped>

div {
  flex: 1 1 auto;
  display: inline-flex;
  justify-content: center;
}

div a {
  border-radius: var(--content-border-radius);
  background-color: var(--primary-background-color);
  color: var(--rosalution-purple-200);
  padding: var(--p-5);
  margin-left: var(--p-5);
  margin-right: var(--p-5);
  font-size: 1.125rem; /* 18px */
  font-weight: 700;
}

.logo-link {
  background-color: transparent;
  padding: 0;
  transform: translate(0, 4px);
}

img {
  margin-left: var(--p-5);
  margin-right: var(--p-5);
}

.monday-icon {
  width: 1.875rem; /* 30px */
  height: 1.875rem; /* 30px */
  transform: translate(-8px, 0);
}

.phenotips-icon {
  width: 1.25rem; /* 20px */
  height: 1.25rem; /* 20px */
  transform: translate(-16px, 0);
}
</style>
