<template>
  <table class="gene-box-container">
    <tbody>
      <tr class="gene-box-header">
        <td>
          <h2 class="gene-name">
            {{gene}}
          </h2>
        </td>
        <td class="link-logo">
          <font-awesome-icon icon="up-right-from-square" size="2xs"/>
        </td>
        <td class="transcript" v-for="transcript in transcripts" :key="transcript">
          {{transcript.transcript}}
        </td>
        <td class="copy-logo">
          <font-awesome-icon :icon="['far', 'copy']" size="sm"/>
        </td>
      </tr>
      <div class="seperator-gene"></div>
      <div v-for="variant in variants" :key="variant">
        <div v-if="variant.c_dot && variant.c_dot.length > 0 || variant.p_dot && variant.p_dot.length > 0">
          <tr class="gene-box-second-line">
            <span v-if="variant.c_dot && variant.c_dot.length > 0">
              <td class="c-dot">
                {{variant.c_dot}}
              </td>
              <td class="link-logo">
                <font-awesome-icon icon="up-right-from-square" size="2xs"/>
              </td>
            </span>
            <span v-if="variant.p_dot && variant.p_dot.length > 0">
              <td class="p-dot">
                ({{variant.p_dot}})
              </td>
              <td class="copy-logo">
                <font-awesome-icon :icon="['far', 'copy']" size="sm"/>
              </td>
              <td class="genomic-build">
                {{getBuild(variant.build)}}
              </td>
              <td class="genome-browser-link-logo">
                Genome Browser
              </td>
            </span>
          </tr>
          <div class="seperator-variant"></div>
        </div>
        <tr class="gene-box-third-line">
          <td class="case-field-value" v-for="caseInfo in variant.case" :key="caseInfo">
            <span class="case-field">
              {{caseInfo.field}}:
            </span>
            <span class="case-value" v-for="value in caseInfo.value" :key="value">
              {{value}},
            </span>
          </td>
        </tr>
      </div>
    </tbody>
  </table>
</template>>

<script>

export default {
  name: 'gene-box',
  props: {
    gene: {
      type: String,
    },
    transcripts: {
      type: Array,
    },
    variants: {
      type: Array,
    },
  },
  methods: {
    getBuild(build) {
      if (build == 'hg19') {
        return 'grch37';
      } else if (build == 'hg38') {
        return 'grch38';
      }
    },
  },
};
</script>

<style scoped>

div {
  font-family: "Proxima Nova", sans-serif;
  padding: var(--p-0);
}

.gene-box-container {
  display: flex;
  flex-direction:column;
  padding: var(--p-10);
  margin: 0.625rem;
  width: 100%;
  border-radius: 1.25rem;
  background-color: var(--rosalution-white);
}

.gene-box-header {
  height: 1.75rem;
  display: flex;
  flex-direction: row;
}

.gene-name {
  height: 1.75rem;
  margin: .125rem .125rem 0 .125rem;
  color: var(--rosalution-purple-300);
}

.link-logo {
  height: 1.75rem;
}

.transcript {
  font-weight: bold;
  height: 1.75rem;
  margin: .125rem .9375rem 0 .9375rem;
  /* padding: 0px .9375rem 0px .9375rem; */
}

.copy-logo {
  height: 1.75rem;
  margin: .125rem .125rem 0 .125rem;
}

.seperator-gene {
  height: .125rem;
  background-color: var(--rosalution-grey-100);
  border: solid .0469rem var(--rosalution-grey-100);
}

.gene-box-second-line {
  display: flex;
  height: 1.75rem;
  margin: .125rem .125rem 0 .125rem;
}

.c-dot {
  font-weight: bold;
  color: var(--rosalution-purple-300);
}

/* Unable to move this to top right of copy-logo */
.genomic-build {
  font-size: .875rem;
  font-weight: 600;
}

.seperator-variant {
  height: .125rem;
  background-color: var(--rosalution-grey-200);
  border: solid .0469rem var(--rosalution-grey-200);
}


.gene-box-third-line {
  display: flex;
  flex-direction: row;
  gap: .625rem;
  flex-wrap: wrap;
}

/* This is making the Genome Broser go into gene-box-third-line */
/* .genome-browser-link-logo {
  float: right;
  right: 3%;
  position: absolute;
} */

.case-field-value {
  display: inline-block;
  flex-wrap: wrap;
  font-size: 1.125rem;
  gap: .625rem;
  color: var(--rosalution-black);
  margin: .125rem .125rem 0 .125rem;
}

.case-field {
  font-weight: 600;
  text-align: left;
}

.case-value {
  text-align: left;
  margin-right: .125rem;
}
</style>
