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
          <font-awesome-icon icon="up-right-from-square" size="lg"/>
        </td>
        <td class="transcript" v-for="transcript in transcripts" :key="transcript">
          {{transcript.transcript}}
        </td>
        <td class="copy-logo">
          <font-awesome-icon icon="copy" size="lg"/>
        </td>
      </tr>
      <div class="seperator"></div>
      <div v-for="variant in variants" :key="variant">
        <tr class="gene-box-second-line">
          <span v-if="variant.c_dot && variant.c_dot.length > 0">
            <td class="c-dot">
              {{variant.c_dot}}
            </td>
            <td class="link-logo">
              <font-awesome-icon icon="up-right-from-square" size="lg"/>
            </td>
          </span>
          <span v-if="variant.p_dot && variant.p_dot.length > 0">
            <td class="p-dot">
              ({{variant.p_dot}})
            </td>
            <td class="copy-logo">
              <font-awesome-icon icon="copy" size="lg"/>
            </td>
            <td class="grch-build">
              {{getBuild(variant.build)}}
            </td>
          </span>
          <td class="genome-browser-link-logo">
            Genome Browser
          </td>
        </tr>
        <div class="seperator"></div>
        <tr class="gene-box-third-line" v-for="caseInfo in variant.case" :key="caseInfo">
          <td class="case-field">
            {{caseInfo.field}}
          </td>
          <td class="case-value" v-for="value in caseInfo.value" :key="value">
            {{value}}
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
  background-color: var(--divergen-white);
}

.gene-box-header {
  height: 1.75rem;
  display: flex;
  flex-direction: row;
}

.gene-name {
  height: 1.75rem;
  margin: .125rem .125rem 0 .125rem;
  color: var(--divergen-purple-300);
}

.transcript {
  font-weight: bold;
}

.seperator {
  height: .125rem;
  background-color: var(--divergen-grey-100);
  border: solid .0469rem var(--divergen-grey-100);
}

.gene-box-third-line {
  display: table-row;
  /* flex-direction: column; */
  gap: .625rem;
  flex-wrap: nowrap;
}

</style>
