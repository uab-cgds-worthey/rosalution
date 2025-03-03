<template>
  <div class="rosalution-section-container">
    <div>
      <div class="gene-box-header">
        <router-link class="gene-link" :to="{
            name: 'annotation',
            params: {
              analysis_name: this.name,
            },
            state: {
              gene: this.gene,
              ...(variants.length > 0 ? { variant: getCompleteHgvsVariantName(variants[0]) } : {}),
            }
          }"
          data-test="gene-route"
        >
          <font-awesome-icon icon="angles-right" size="sm" />
          <h2 data-test="gene-name"> {{ gene }} </h2>
        </router-link>
      </div>
      <div class="seperator-gene"></div>
      <div v-for="variant, index in variants" :key="variant">
        <div class="variant-sub-section"
          v-if="variant.c_dot && variant.c_dot.length > 0 || variant.p_dot && variant.p_dot.length > 0">
          <div class="variant-name-line">
            <router-link class="variant" :to="{
                name: 'annotation',
                params: {
                  analysis_name: this.name,
                },
                state: {
                  gene: this.gene,
                  variant: getCompleteHgvsVariantName(variant),
                },
              }"
:data-test="`variant-route-${index}`">
              <font-awesome-icon icon="angles-right" size="sm" />
              <span class="variant-transcript">{{ variant.hgvs_variant.split(':')[0] }}:</span>
              <span>{{ variant.c_dot }}</span>
              <span v-if="variant.p_dot">({{ variant.p_dot }})</span>
            </router-link>
            <font-awesome-icon :icon="['far', 'copy']" class="copy-icon"
@click="copyToClipboard(variant.hgvs_variant)"
              data-test="copy-button" />
            <span class="genomic-build"> {{ getBuild(variant.build) }} </span>
          </div>
          <div class="seperator-variant"></div>
          <div class="variant-case-information">
            <div v-for="caseInfo in variant.case" :key="caseInfo">
              <span class="case-field">
                {{ caseInfo.field }}:
              </span>
              <span v-if="caseInfo.value.length > 0">
                {{ caseInfo.value.join(', ') }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
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
    async copyToClipboard(textToCopy) {
      /** Needed to add a try/catch to can an error that occurs in Cypress, which causes the test to fail.  */
      try {
        await navigator.clipboard.writeText(textToCopy);
      } catch (error) {
        console.error(error.message);
      }

      this.$emit('clipboard-copy', textToCopy);
    },
    getCompleteHgvsVariantName(variant) {
      if (variant.p_dot) {
        return `${variant.hgvs_variant}(${variant.p_dot})`;
      }

      return variant.hgvs_variant;
    },
  },
};
</script>

<style scoped>
.gene-box-header {
  padding-left: var(--p-05);
}

.gene-link {
  display: inline-flex;
  align-items: center;
  gap: var(--p-5)
}

.seperator-gene {
  height: var(--p-005);
  background-color: var(--rosalution-grey-100);
  border: solid var(--p-005) var(--rosalution-grey-100);
}

.variant-sub-section {
  margin-top: var(--p-10);
}

.variant-name-line {
  display: inline-flex;
  align-items: center;
  padding: var(--p-05);
  gap: var(--p-5);
}

.variant {
  font-weight: bold;
}

.variant-transcript {
  font-weight: normal;
  padding-left: var(--p-5)
}

.copy-icon {
  padding-bottom: var(--p-1)
}

.copy-icon:hover {
  cursor: pointer;
}

.copy-icon:active {
  color: var(--rosalution-purple-200)
}

.genomic-build {
  font-size: .875rem;
  font-weight: 600;
}

.seperator-variant {
  height: var(--p-005);
  background-color: var(--rosalution-grey-200);
  border: solid var(--p-005) var(--rosalution-grey-200);
}


.variant-case-information {
  display: flex;
  gap: var(--p-16);
  flex-wrap: wrap;
  margin: var(--p-1) var(--p-1) var(--p-05) var(--p-1);
}

.case-field {
  font-weight: 600;
}
</style>
