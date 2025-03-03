<template>
  <router-link
    :to="{ name: 'analysis', params: { analysis_name: this.name } }"
    class="analysis-card"
    :style="cardBorderColorStyle"
  >
    <div class="case-status-section ">
      <div class="status-icon case-status-item">
        <font-awesome-icon :icon="workflowIcon" :style="workflowColorStyle" size="2x" data-test="status-icon"/>
      </div>
        <div class="case-name header-text">{{ name }}</div>
        <div class="nominated-text content-text subsection-text">{{ nominated_by }}</div>
    </div>
    <div class="dates-section">
        <span class="dates-subsection">
          <div class="subsection-text small-text dates-subsection-label">Case Added:</div>
          <div class="content-text">{{ created_date }}</div>
        </span>
        <span class="middle-separator"></span>
        <span class="dates-subsection">
          <div class="subsection-text small-text dates-subsection-label">Last Modified:</div>
          <div class="content-text">{{ last_modified_date }}</div>
        </span>
    </div>
    <div class="genomic-units-section">
      <ul>
        <li v-for="genomic_unit in genomic_units" :key="genomic_unit">
          <span class="header-text gene-genomic-unit-text">{{ genomic_unit.gene || ""}}</span>
          <ul>
            <li v-for="variant in genomic_unit.variants" :key="variant" class="variant-genomic-unit-text content-text">
              {{ variant }}
            </li>
          </ul>
        </li>
      </ul>
    </div>
    <div class="logo-links-section">
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
        <img :src="getLogoSrc(link.type)" class="logo-img" />
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
        // 'color': `var(${this.workflowColor})`,
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

.header-text {
  font-size: .8125rem; /** 13px */
  line-height: 1rem;
  font-weight: bold;
}

.content-text {
  font-size: 0.75rem;
  line-height: 1rem;
}

.small-text {
  font-size: 0.625rem;
}

.subsection-text {
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

  font-size: .75rem;

  display: flex;
  align-items: flex-start;
}


.case-name {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nominated-text {
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

.dates-subsection {
  display:flex;
  flex-direction: column;
  padding: var(--p-05)
}

.dates-subsection-label {
  color: var(--rosalution-grey-300)
}

.middle-separator {
  min-width: 1px;
  max-width: 1px;
  background-color: var(--rosalution-grey-300);
}

.genomic-units-section {
  padding: var(--p-1) 0;
  flex-grow: 1;

  font-size: .875rem;

  overflow:auto;
}

.variant-genomic-unit-text {
  background-color: var(--rosalution-grey-50);
  border-radius: var(--input-border-radius);
  padding: var(--p-1) var(--p-1) var(--p-1) var(--p-1);
  word-wrap: break-word;
  margin-bottom: var(--p-1);
}

.logo-links-section {
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo-link img {
  width: 24px;
  height: 24px;
}
</style>
