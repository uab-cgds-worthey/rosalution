<template>
  <router-link
    :to="{ name: 'analysis', params: { analysis_name: this.name } }"
    class="analysis-card"
    :style="cardBorderColorStyle"
  >
    <div class="case-status-section">
      <div class="status-icon">
        <font-awesome-icon :icon="workflowIcon" :style="workflowColorStyle" size="2x" data-test="status-icon"/>
      </div>
      <div class="case-name card-header-text">{{ name }}</div>
      <div class="nominated content-text hide-overflow-text">{{ nominated_by }}</div>
    </div>
    <div class="dates-section">
      <span class="dates-item">
        <div class="dates-label small-text">Case Added:</div>
        <div class="content-text">{{ created_date }}</div>
      </span>
      <span class="middle-separator"></span>
      <span class="dates-item">
        <div class="dates-label small-text">Last Modified:</div>
        <div class="content-text">{{ last_modified_date }}</div>
      </span>
    </div>
    <div class="genomic-units-section">
      <dl class="genomic-units-list">
        <template v-for="genomic_unit in genomic_units" :key="genomic_unit">
          <dt class="card-header-text">{{ genomic_unit.gene || ""}}</dt>
          <dd v-for="variant in genomic_unit.variants" :key="variant" class="variant content-text">
            {{ variant }}
          </dd>
        </template>
      </dl>
    </div>
    <div class="linkout-section" data-test="linkout-section">
      <a
        v-for="link in third_party_links"
        :key="link.type"
        :href="link.link"
        target="_blank"
        class="logo-link"
        data-test="third-party-link"
        rel="noopener noreferrer"
        @click.stop
      >
        <img :src="getLogoSrc(link.type)"/>
      </a>
    </div>
  </router-link>
</template>

<script>
import {StatusType} from '@/config.js';

export default {
  name: 'analysis-card',
  components: {},
  props: {
    status_icon: {
      type: String,
    },
    latest_status: {
      type: String,
    },
    name: {
      type: String,
    },
    description: {
      type: String,
    },
    nominated_by: {
      type: String,
      required: true,
    },
    created_date: {
      type: String,
    },
    last_modified_date: {
      type: String,
    },
    genomic_units: {
      type: Array,
    },
    third_party_links: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    workflowIcon: function() {
      if ( !(this.latest_status in StatusType) ) {
        return 'question';
      }

      return StatusType[this.latest_status].icon;
    },
    workflowColor: function() {
      if ( !(this.latest_status in StatusType) ) {
        return '--rosalution-white';
      }

      return StatusType[this.latest_status].color;
    },
    workflowColorStyle: function() {
      return {
        color: `var(${this.workflowColor})`,
      };
    },
    cardBorderColorStyle: function() {
      return {
        'border-color': `var(${this.workflowColor})`,
        'color': `var(${this.workflowColor})`,
      };
    },
  },
  methods: {
    getLogoSrc(type) {
      switch (type) {
        case 'monday_com':
          return new URL('/src/assets/monday-avatar-logo.svg', import.meta.url);
        case 'phenotips_com':
          return new URL('/src/assets/phenotips-favicon-96x96.png', import.meta.url);
        default:
          return '';
      }
    },
  },
};
</script>

<style scoped>

.analysis-card div {
  color: var(--rosalution-black);
}

.card-header-text {
  font-size: var(--p-14);
  line-height: 1rem;
  font-weight: bold;
}

.content-text {
  font-size: var(--p-12);
  line-height: 1rem;
}

.small-text {
  font-size: var(--p-10);
}

.hide-overflow-text {
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}

.case-status-section {
  display: grid;
  grid-template-columns: min-content 1fr;
  grid-template-rows: repeat(3,min-content);

  column-gap: var(--p-5);
  grid-auto-flow: dense;
}

.status-icon {
  grid-column: 1;
  grid-row: 1;

  font-size: var(--p-12);

  display: flex;
  align-items: flex-start;
}

.case-name {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nominated {
  grid-row: -1;
  grid-column: 1 / -1;
}

.dates-section {
  display:flex;
  flex-direction: row;
  justify-content: center;
  text-align: center;
  padding: var(--p-1);
  border-top: 1px solid var(--rosalution-grey-300);
  border-bottom: 1px solid var(--rosalution-grey-300);
}

.dates-item {
  display:flex;
  flex-direction: column;
  padding: var(--p-05)
}

.dates-label {
  color: var(--rosalution-grey-300) !important;
}

.middle-separator {
  min-width: 1px;
  max-width: 1px;
  background-color: var(--rosalution-grey-300);
}

.genomic-units-section {
  padding: var(--p-1) 0;
  flex-grow: 1;

  overflow:auto;
}

.genomic-units-list {
  margin-block-end: 0px;
  margin-block-start: 0px;
}

.variant {
  background-color: var(--rosalution-grey-50);
  border-radius: var(--input-border-radius);
  padding: var(--p-1) var(--p-1) var(--p-1) var(--p-1);
  word-wrap: break-word;

  margin-bottom: var(--p-1);
  margin-inline-start: 0px;
}

.linkout-section {
  display: flex;
  justify-content: center;
  align-items: center;
}

.linkout-section img {
  width: 24px;
  height: 24px;
}
</style>
