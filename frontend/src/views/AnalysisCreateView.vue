<template>
  <app-content>
    <RequiredInputForm @create_analysis="createUpdateAnalysis" data-test="required-input-form"/>
    <SupplementalFormList data-test="supplemental-form-list"/>
  </app-content>
</template>

<script>
import RequiredInputForm from '@/components/FormComponents/RequiredInputForm.vue';
import SupplementalFormList from '@/components/AnalysisView/SupplementalFormList.vue';
import analyses from '@/models/analyses.js';

export default {
  name: 'analysis-create-view',
  components: {
    RequiredInputForm,
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
                    coordinateList: formData.coordinates,
                    secondaryPipeline: 'sv',
                  },
                },
              ],
            },
          ],
        }],
      };
      analyses.saveAnalysis(analysis);
    },
  },
};
</script>
