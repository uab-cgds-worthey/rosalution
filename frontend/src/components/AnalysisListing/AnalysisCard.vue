<template>
  <router-link :to="{ name: 'analysis', params: { analysis_name: this.name } }">
    <div class="analysis-card">
      <div class="analysis-base" :style="cardBorderColorStyle">
        <div class="case-status-section">
          <div class="status-icon">
            <font-awesome-icon :icon="workflowIcon" :style="workflowColorStyle" size="2x"/>
          </div>
          <span>
            <div class="case-name">{{ name }}</div>
            <div class="subection-text">{{ nominated_by }}</div>
          </span>
        </div>
        <div class="dates-section">
            <span class="dates-subsection">
              <div class="subection-text dates-subsection-label">Case Added:</div>
              <div>{{ created_date }}</div>
            </span>
            <span class="middle-separator"></span>
            <span class="dates-subsection">
              <div class="subection-text dates-subsection-label">Last Modified:</div>
              <div>{{ last_modified_date }}</div>
            </span>
        </div>
        <div class="genomic-units-section">
          <ul>
            <li v-for="genomic_unit in genomic_units" :key="genomic_unit">
              <span class="gene-genomic-unit-text">{{ genomic_unit.gene || ""}}</span>
              <ul>
                <li v-for="variant in genomic_unit.variants" :key="variant" class="variant-genomic-unit-text">
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
      </div>
    </div>
  </router-link>
</template>

<script>
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
      if (this.latest_status == 'Annotation') {
        return 'asterisk';
      } else if (this.latest_status == 'Ready') {
        return 'clipboard-check';
      } else if (this.latest_status == 'Active') {
        return 'book-open';
      } else if (this.latest_status == 'Approved') {
        return 'check';
      } else if (this.latest_status == 'On-Hold') {
        return 'pause';
      } else if (this.latest_status == 'Declined') {
        return 'x';
      }

      return 'question';
    },
    workflowColor: function() {
      if (this.latest_status == 'Annotation') {
        return '--rosalution-status-annotation';
      } else if (this.latest_status == 'Ready') {
        return '--rosalution-status-ready';
      } else if (this.latest_status == 'Active') {
        return '--rosalution-status-active';
      } else if (this.latest_status == 'Approved') {
        return '--rosalution-status-approved';
      } else if (this.latest_status == 'On-Hold') {
        return '--rosalution-status-on-hold';
      } else if (this.latest_status == 'Declined') {
        return '--rosalution-status-declined';
      }

      return '--rosalution-white';
    },
    workflowColorStyle: function() {
      return {
        color: `var(${this.workflowColor})`,
      };
    },
    cardBorderColorStyle: function() {
      return {
        'border-color': `var(${this.workflowColor}`,
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

div {
  font-family: "Proxima Nova", sans-serif;
  font-size: 0.75rem; /* 12 px */
  color: var(--rosalution-black)
}

.analysis-card {
  position: relative;
  text-decoration: none;
}

.analysis-base:hover {
  box-shadow: 0 0.5em 0.5em -0.4em;
  transform: translateY(-0.4em);
}

.analysis-base {
  max-width: 11.25rem;
  height: 18.125rem;
  padding: var(--p-8) var(--p-5) var(--p-8) var(--p-5);
  border-radius: 1.25rem;
  border: solid 0.625rem;
  background-color: var(--rosalution-white);
  display: block;
  box-sizing: border-box;
  color: inherit;
  transition: all .2s ease-in-out;
  position: relative;
}

.subection-text {
  font-size: 0.563rem; /* 9px */
  max-width: 22ch;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}

.case-status-section {
  display: flex;
  padding: var(--p-1) 0;
}

.status-icon {
  padding: var(--p-5);
}

.case-name {
  font-weight: bold;
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
  padding: var(--p-1)
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
}

.gene-genomic-unit-text {
  font-weight: bold;
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
  padding: var(--p-1);
  position: absolute;
  bottom: var(--p-1);
  left: 50%;
  transform: translateX(-50%);
}

.logo-link {
  display: inline-block;
  padding: 0 var(--p-1);
  transform: translate(0, 20%);
}

.logo-link img {
  width: 24px;
  height: 24px;
}

</style>
