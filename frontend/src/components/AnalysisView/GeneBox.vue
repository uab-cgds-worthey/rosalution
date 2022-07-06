<template>
  <table class="gene-box-container">
    <tbody>
      <tr class="gene-box-header">
        <router-link :to="{ name: 'annotation', params: { analysis_name: this.name, genomic_unit: this.gene} }">
          <td>
            <h2 class="gene-name" data-test="gene-name">
              {{gene}}
            </h2>
          </td>
        </router-link>
        <td class="link-logo">
          <font-awesome-icon icon="up-right-from-square" size="2xs"/>
        </td>
        <td class="transcript" v-for="transcript in transcripts" :key="transcript">
          {{transcript.transcript}}
        </td>
      </tr>
      <div class="seperator-gene"></div>
      <div v-for="variant in variants" :key="variant">
        <div v-if="variant.c_dot && variant.c_dot.length > 0 || variant.p_dot && variant.p_dot.length > 0">
          <tr class="gene-box-second-line">
            <router-link :to="{ name: 'annotation', params: { analysis_name: this.name, genomic_unit: variant.c_dot}}">
              <td class="c-dot" data-test="c-dot">
                {{variant.c_dot}}
              </td>
            </router-link>
              <td class="link-logo">
                <font-awesome-icon icon="up-right-from-square" size="2xs"/>
              </td>
              <td class="copy">
                <button class="copy-button" @click="copyToClipboard(variant.hgvs_variant)" data-test="copy-button">
                  <font-awesome-icon :icon="['far', 'copy']" size="sm"/>
                </button>
              </td>
              <td class="p-dot">
                ({{variant.p_dot}})
              </td>
              <td class="genomic-build">
                {{getBuild(variant.build)}}
              </td>
              <td class="genome-browser-link-logo">
                <a href="https://www.ncbi.nlm.nih.gov/genome/" class>
                  <img src="@/assets/ncbi-icon.png" class="ncbi-logo"/>
                  Genome Browser
                </a>
              </td>
          </tr>
          <div class="seperator-variant"></div>
        </div>
        <tr class="gene-box-third-line">
          <td class="case-field-value" v-for="caseInfo in variant.case" :key="caseInfo">
            <span class="case-field">
              {{caseInfo.field}}:
            </span>
            <span class="case-value" v-if="caseInfo.value.length > 0">
              {{caseInfo.value.join(', ')}}
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
  components: {
  },
  props: {
    name: {
      type: String,
    },
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
    copyToClipboard(textToCopy) {
      /*
      The below method is the updated way to copy text to clipboard.
      It does not work currently because we have not added HTTPS in traffik.
      This functionality for copying text will be added when HTTPS is added in traffik.
      */
      // navigator.clipboard.writeText(textToCopy);
      console.log(textToCopy);

      /*
      The below method is marked as depreciated
      Link to stack overflow article:
      https://stackoverflow.com/questions/67882865/copy-datatext-to-clipboard-in-vuenuxt-js
      Link to MDN:
      https://developer.mozilla.org/en-US/docs/Web/API/Document/execCommand
      */
      // const tmpTextField = document.createElement('input');
      // tmpTextField.value = textToCopy;
      // tmpTextField.setAttribute('readonly', '');
      // tmpTextField.setAttribute('style', 'position:absolute; right:200%;');
      // document.body.appendChild(tmpTextField);
      // tmpTextField.select();
      // tmpTextField.setSelectionRange(0, 99999);
      // document.execCommand('copy');
      // tmpTextField.remove();
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
  margin: .125rem .1255rem 0 .125rem;
}

.copy {
  height: 1.75rem;
  margin: .125rem .125rem 0 .125rem;
}

.copy-button {
  border: none;
  padding: 0;
  background-color: var(--rosalution-white);
}

.seperator-gene {
  height: .125rem;
  background-color: var(--rosalution-grey-100);
  border: solid .0469rem var(--rosalution-grey-100);
}

.gene-box-second-line {
  line-height: 1.75rem;
  margin: .125rem .125rem 0 .125rem;
  vertical-align: middle;
}

.c-dot {
  font-weight: bold;
  color: var(--rosalution-purple-300);
}

/* Unable to move this to top right of copy-logo */
.genomic-build {
  font-size: .875rem;
  font-weight: 600;
  top: -0.5em;
  position: relative;
}

.ncbi-logo {
  width: .9375rem;
  height: 1.125rem;
  vertical-align: middle;
}

.genome-browser-link-logo {
  float: right;
  right: 3%;
  position: absolute;
  font-weight: bold;
  color: var(--rosalution-purple-300);
}

a {
 color: inherit;
}

.seperator-variant {
  height: .125rem;
  background-color: var(--rosalution-grey-200);
  border: solid .0469rem var(--rosalution-grey-200);
  vertical-align: middle;
}


.gene-box-third-line {
  display: flex;
  flex-direction: row;
  gap: .625rem;
  flex-wrap: wrap;
  line-height: 1.75rem;
  margin: .125rem .125rem 0 .125rem;
  vertical-align: middle;
}

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
