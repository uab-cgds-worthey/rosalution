<template>
  <router-link :to="{ name: 'analysis', params: { analysis_name: this.name } }">
    <div class="analysis-card">
      <div class="analysis-base" :style="`border-color: var(${workflowColor})`">
        <div class="case-status-info">
          <div class="status-icon">
            <font-awesome-icon :icon="workflowIcon" :style="workflowColorStyle" size="lg"/>
          </div>
          <span class="case-info">
            <div class="case-name">
              {{ name }}
            </div>
            <div class="investigator">
              {{ nominated_by }}
            </div>
          </span>
        </div>
        <div class="dates-section">
          <div class="top-border"></div>
          <div class="date-info">
            <span class="case-added-info">
              <div class="case-added-label">Case Added:</div>
              <div class="case-added-date">
                {{ created_date }}
              </div>
            </span>
            <span class="middle-separator"></span>
            <span class="last-modified-info">
              <div class="last-modified-label">Last Modified:</div>
              <div class="last-modified-date">
                {{ last_modified_date }}
              </div>
            </span>
          </div>
          <div class="bottom-border"></div>
        </div>
        <div class="gene-label">Gene:</div>
        <ul class="gene-name">
          <li v-for="genomic_unit in genomic_units" :key="genomic_unit">
            {{ genomic_unit.gene }}
          </li>
        </ul>
        <div class="transcript-label">Transcript:</div>
        <ul class="transcript-name">
          <li v-for="genomic_unit in genomic_units" :key="genomic_unit">
            {{ genomic_unit.transcripts.join(", ") }}
          </li>
        </ul>
        <ul class="coordinates">
          <li v-for="genomic_unit in genomic_units" :key="genomic_unit">
            {{ genomic_unit.variants.join(", ") }}
          </li>
        </ul>
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
        return '--divergen-status-annotation';
      } else if (this.latest_status == 'Ready') {
        return '--divergen-status-ready';
      } else if (this.latest_status == 'Active') {
        return '--divergen-status-active';
      } else if (this.latest_status == 'Approved') {
        return '--divergen-status-approved';
      } else if (this.latest_status == 'On-Hold') {
        return '--divergen-status-on-hold';
      } else if (this.latest_status == 'Declined') {
        return '--divergen-status-declined';
      }

      return '--divergen-white';
    },
    workflowColorStyle: function() {
      return {
        color: `var(${this.workflowColor})`,
      };
    },
  },
};
</script>

<style scoped>

.analysis-card:link{color:inherit}
.analysis-card:active{color:inherit}
.analysis-card:visited{color:inherit}
.analysis-card:hover{color:inherit}

div {
  font-family: "Proxima Nova", sans-serif;
}

.analysis-card {
  position: relative;
  text-decoration: none;
}

.analysis-base {
  max-width: 11.25rem;
  height: 18.125rem;
  flex-grow: 0;
  padding: 0.5rem 0.3125rem 0.875rem 0.3125rem;
  border-radius: 1.25rem;
  border: solid 0.625rem;
  background-color: #fff;
  margin: 1rem;
  margin-right: 1rem;
  position: relative;
  justify-content: center;
  display: block;
  box-sizing: border-box;
  color: inherit;
}

.case-status-info {
  display: flex;
}

.status-icon {
  width: 1.4688rem;
  height: 1.4688rem;
  flex-grow: 0;
  margin: 0.3937rem 0.5313rem 1.075rem 0.1875rem;
  padding: 0.1125rem 0.2562rem 0.275rem 0.2562rem;
  justify-content: center;
}

.case-info {
  align-content: center;
  align-self: stretch;
  flex-grow: 0;
  display: flex;
  flex-direction: column;
  justify-content: left;
  align-items: left;
  margin: 0.3937rem 0.5313rem 1.075rem 0rem;
  padding: 0.1125rem 0.2562rem 0.275rem 0rem;
}

.case-name {
  width: 3.75rem;
  height: 0.813rem;
  font-size: 0.688rem;
  font-weight: bold;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
  letter-spacing: normal;
  text-align: left;
  color: #000;
}

.investigator {
  width: 4.875rem;
  height: 0.625rem;
  font-size: 0.5625rem;
  font-weight: normal;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
  letter-spacing: normal;
  text-align: left;
  color: #000;
}

.top-border {
  width: 9.375rem;
  height: 0.0625rem;
  flex-grow: 0;
  background-color: #979797;
  justify-content: center;
}

.bottom-border {
  width: 9.375rem;
  height: 0.0625rem;
  flex-grow: 0;
  background-color: #979797;
  border: none;
  justify-content: center;
}

.date-info {
  display: flex;
  width: 9.375rem;
  height: 2.1981rem;
  justify-content: center;
}

.case-added-info {
  align-content: center;
  align-self: stretch;
  flex-grow: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.case-added-label {
  width: 5rem;
  height: 0.625rem;
  flex-grow: 0;
  font-family: Helvetica;
  font-size: 0.5625rem;
  font-weight: normal;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
  letter-spacing: normal;
  text-align: center;
  color: #6f6b6b;
}

.case-added-date {
  width: 4.2687rem;
  height: 0.75rem;
  flex-grow: 0;
  font-family: Helvetica;
  font-size: 0.6375rem;
  font-weight: normal;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
  letter-spacing: normal;
  text-align: center;
  color: #000;
}

.middle-separator {
  width: 0.1062rem;
  height: 2.2rem;
  flex-grow: 0;
  border: solid 0.75px #979797;
  background-color: #979797;
  justify-content: center;
}

.last-modified-info {
  align-content: center;
  align-self: stretch;
  flex-grow: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.last-modified-label {
  width: 4.9375rem;
  height: 0.625rem;
  flex-grow: 0;
  font-family: Helvetica;
  font-size: 0.5625rem;
  font-weight: normal;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
  letter-spacing: normal;
  text-align: center;
  color: #6f6b6b;
}

.last-modified-date {
  width: 4.2687rem;
  height: 0.75rem;
  flex-grow: 0;
  font-family: Helvetica;
  font-size: 0.6375rem;
  font-weight: normal;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
  letter-spacing: normal;
  text-align: center;
  color: #000;
}

.gene-label {
  width: 2.0625rem;
  height: 0.875rem;
  margin: 0.7063rem 1.1875rem 0.4375rem 0.25rem;
  font-family: Helvetica;
  font-size: 0.75rem;
  font-weight: normal;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
  letter-spacing: normal;
  text-align: center;
  color: #6f6b6b;
}

.gene-name {
  width: 1.9375rem;
  height: 0.875rem;
  margin: 0.4375rem 0 0.4375rem 0.25rem;
  font-family: Helvetica;
  font-size: 0.75rem;
  font-weight: normal;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
  letter-spacing: normal;
  text-align: center;
  color: #000;
}

.transcript-label {
  width: 3.5625rem;
  height: 0.875rem;
  margin: 0.4375rem 1.6438rem 0.4375rem 0.1875rem;
  font-family: Helvetica;
  font-size: 0.75rem;
  font-weight: normal;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
  letter-spacing: normal;
  text-align: center;
  color: #6f6b6b;
}

.transcript-name {
  width: 4.75rem;
  height: 0.875rem;
  margin: 0.4375rem 0.3937rem 0.4375rem 0.25rem;
  font-family: Helvetica;
  font-size: 0.75rem;
  font-weight: normal;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
  letter-spacing: normal;
  text-align: center;
  color: #000;
}

.coordinates {
  width: 7.5rem;
  height: 0.875rem;
  margin: 0.4375rem 0.25rem 0.4375rem 0.25rem;
  font-family: Helvetica;
  font-size: 0.75rem;
  font-weight: normal;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
  letter-spacing: normal;
  text-align: left;
  color: #000;
}
</style>
