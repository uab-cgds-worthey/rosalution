<template>
  <div>
    <table class="gene-box-container">
      <tbody>
        <tr class="gene-box-header">
        <td class="gene-name">
          {{gene}}
        </td>
        <td class="transcript" v-if="transcript.transcript">
          {{transcript.transcript}}
        </td>
        <td class="reference-logo">
          logo here
        </td>
        <td class="logo-dropdown-edit">
          <font-awesome-icon icon="chevron-down" size="lg"/>
        </td>
      </tr>
      <div class="seperator"></div>
      <tr class="gene-box-second-line">
        <td class="c-dot">
          {{variants.c_dot}}
        </td>
        <td class="p-dot">
          {{variants.p_dot}}
        </td>
        <td class="reference-logo">
          logo here
        </td>
        <td class="grch-build">
          grch38
        </td>
        <td class="genome-browser-link-logo">
          Genome Browser
        </td>
      </tr>
      <div class="seperator"></div>
      <tr class="gene-box-third-line">
        <td class="case-evidence">
          {{variants.case.evidence}}
        </td>
        <td class="case-interpretation">
          {{variants.case.interpretation}}
        </td>
        <td class="case-inheritance">
          {{variants.case.inheritance}}
        </td>
      </tr>
      </tbody>
    </table>
  </div>
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
};
</script>

<style scoped>

div {
  font-family: "Proxima Nova", sans-serif;
  padding: var(--p-0);
}

.gene-box-container {
  display: flex;
  flex-direction: column;
  padding: var(--p-10);
  margin: 0.625rem;
  width: 100%;
  gap: .625rem;
  border-radius: 1.25rem;
  background-color: var(--divergen-white);
}

.gene-box-header {
  height: 1.75rem;
  display: flex;
  flex-direction: row;
}

.gene-box-name {
  height: 1.75rem;
  margin: .125rem .125rem 0 .125rem;
}

.logo-dropdown-edit {
  color: var(--divergen-grey-200);
  float: right;
  right: 3%;
  position: absolute;
}

.seperator {
  height: .125rem;
  background-color: var(--divergen-grey-100);
  border: solid .0469rem var(--divergen-grey-100);
}

</style>
