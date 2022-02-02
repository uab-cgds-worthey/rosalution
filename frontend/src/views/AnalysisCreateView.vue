<template>
  <app-content>
    <RequiredInputForm @create_analysis="createUpdateAnalysis" data-test="required-input-form"/>
    <SecondaryInputForm data-test="secondary-input-form"/>
    <SupplementalFormList data-test="supplemental-form-list"/>
  </app-content>
</template>

<script>

import RequiredInputForm from '@/components/FormComponents/RequiredInputForm.vue';
import SecondaryInputForm from '@/components/FormComponents/SecondaryInputForm.vue';
import SupplementalFormList from '@/components/FormComponents/SupplementalFormList.vue';
import analyses from '@/models/analyses.js';

export default {
  name: 'analysis-create-view',
  components: {
    RequiredInputForm,
    SecondaryInputForm,
    SupplementalFormList,
  },
  data: function() {
    return {
    };
  },
  methods: {
    async createUpdateAnalysis(formData) {
      const analysis = {
        name: formData.name,
        description: formData.description,
        samples: [{
          name: formData.name,
          sources: [
            {
              secondaryAnalysis: [
                {
                  annotations: {
                    vcfFileName: `${formData.name}_fakeVCF.vcf`,
                    secondaryPipeline: 'sv',
                  },
                },
              ],
            },
          ],
        }],
        vcfFiles: [
          formData.vcfFile,
        ],
      };
      analyses.saveAnalysis(analysis);
    },
  },
};
</script>
