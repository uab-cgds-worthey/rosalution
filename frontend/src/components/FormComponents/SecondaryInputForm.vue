<template>
  <div style="flex: auto;">
    <title>Secondary Input Form</title>
    <h1>Secondary Input Form</h1>
    <form>
      <div>
        <section>
          <h2>Medical Summary</h2>
          <div class="form-section">
            <div class="multiselect-div">
              <div class="multiselect-field">
                <label class="multiselect-label">Clinical Diagnosis</label>
                <multiselect class="multiselect-input" v-model="clinicalDiagnosisValue"
                tag-placeholder="Add this as new tag" placeholder="Search or add a tag" label="name" track-by="code"
                :options="clinicalDiagnosisOptions" :multiple="true" :taggable="true" @tag="addClinicalDiagnosisTag">
                </multiselect>
              </div>
            </div>
            <div class="input-field">
              <label for="inheritance">Inheritance</label>
              <input type="text" name="inheritance" placeholder="Enter Inheritance" v-model="inheritance">
            </div>
            <div class="input-field">
              <label for="zygosity">Zygosity</label>
              <input type="text" name="zygosity" placeholder="Enter Zygosity" v-model="zygosity">
            </div>
            <div class="input-field">
              <label for="interpretation">Interpretation</label>
              <input type="text" name="interpretation" placeholder="Enter Interpretation" v-model="interpretation">
            </div>
            <div class="input-field">
              <label for="evidence">Evidence</label>
              <input type="text" name="evidence" placeholder="Enter Evidence" v-model="evidence">
            </div>
            <div class="multiselect-div">
              <div class="multiselect-field">
                <label class="multiselect-label">Affected Individuals Identified</label>
                <multiselect class="multiselect-input" v-model="affectedIndividualsValue"
                tag-placeholder="Add this as new tag" placeholder="Search or add a tag" label="name" track-by="code"
                :options="affectedIndivisualsOptions" :multiple="true" :taggable="true" @tag="addAffectedIndividualsTag"
                >
                </multiselect>
              </div>
            </div>
          </div>
        </section>
        <section>
          <h2>Case Information</h2>
          <div class="form-section">
            <div class="input-field">
              <label for="systems">Systems</label>
              <textarea type="text" name="systems" placeholder="Enter Systems" v-model="systems"></textarea>
            </div>
            <div class="input-field">
              <label for="additionalDetails">Additional Details</label>
              <textarea type="text" name="additionalDetails" placeholder="Enter Additional Details"
              v-model="additionalDetails"></textarea>
            </div>
            <div class="multiselect-div">
              <div class="multiselect-field">
                <label for="hpoTerms" class="multiselect-label">HPO Terms</label>
                <multiselect name="hpoTerms" class="multiselect-input" v-model="hpoTermsValue"
                tag-placeholder="Add this as new tag" placeholder="Search or add a tag" label="name" track-by="code"
                :options="hpoTermsOptions" :multiple="true" :taggable="true" @tag="addHpoTermsTag">
                </multiselect>
              </div>
            </div>
          </div>
        </section>
        <section>
          <h2>Additional Testing Information</h2>
          <div class="form-section">
            <div class="input-field">
              <label for="experimentalDesign">Experimental Design</label>
              <textarea type="text" name="experimentalDesign" placeholder="Enter Experimental Design"
              v-model="experimentalDesign"></textarea>
            </div>
            <div class="input-field">
              <label for="priorTesting">Prior Testing</label>
              <textarea type="text" name="priorTesting" placeholder="Enter Prior Testing"
              v-model="priorTesting"></textarea>
            </div>
          </div>
        </section>
        <div class="submit-div">
          <input class="submit" type="submit" value="Add Secondary Information">
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import Multiselect from '@vueform/multiselect';

export default {
  name: 'input-form',
  components: {
    Multiselect,
  },
  data() {
    return {
      clinicalDiagnosisValue: [
      ],
      clinicalDiagnosisOptions: [
      ],
      inheritance: '',
      zygosity: '',
      interpretation: '',
      evidence: '',
      affectedIndividualsValue: [
      ],
      affectedIndivisualsOptions: [
      ],
      systems: '',
      additionalDetails: '',
      hpoTermsValue: [
      ],
      hpoTermsOptions: [
      ],
      experimentalDesign: '',
      priorTesting: '',
    };
  },
  methods: {
    addClinicalDiagnosisTag(newTag) {
      const tag = {
        name: newTag,
        code: newTag.substring(0, 2) + Math.floor((Math.random() * 10000000)),
      };
      this.clinicalDiagnosisOptions.push(tag);
      this.clinicalDiagnosisValue.push(tag);
    },
    addAffectedIndividualsTag(newTag) {
      const tag = {
        name: newTag,
        code: newTag.substring(0, 2) + Math.floor((Math.random() * 10000000)),
      };
      this.affectedIndivisualsOptions.push(tag);
      this.affectedIndividualsValue.push(tag);
    },
    addHpoTermsTag(newTag) {
      const tag = {
        name: newTag,
        code: newTag.substring(0, 2) + Math.floor((Math.random() * 10000000)),
      };
      this.hpoTermsOptions.push(tag);
      this.hpoTermsValue.push(tag);
    },
  },
};
</script>

<style src="@vueform/multiselect/themes/default.css"></style>

<style>

.multiselect {
  width: 57rem;
}

.multiselect__input {
  height: 4rem;
  font-size: 1.125rem;
  width: 57rem;
}

.multiselect__tags {
  min-height: 4rem;
  width: 57rem;
  font-size: 1.125rem;
  --tw-border-opacity: 1;
  border-color: rgba(229, 231, 235, var(--tw-border-opacity));
  border-style: solid;
  border-radius: 0.375rem;
  border-width: 1px;
}

.multiselect__tag {
  background: #27AE60;
}

.multiselect__placeholder {
  --tw-placeholder-opacity: 1;
  color: rgba(209, 213, 219, var(--tw-placeholder-opacity));
}

</style>

<style scoped>
@import url("https://use.typekit.net/rgh1osc.css");

div {
  font-family: "Proxima Nova", sans-serif;
  padding: 0%;
}

.form-section {
  padding-left: 1rem;
}

h1 {
  text-align: left;
}

h3 {
  margin-block-start: 0em;
  margin-block-end: 0em;
}

TextInput {
  height: 1.125rem;
}

input, label {
  display: block;
  font-size: 1.125rem;
  line-height: 1.75rem;
}

label {
  height: 1.5rem;
}

input {
  --tw-border-opacity: 1;
  border-color: rgba(229, 231, 235, var(--tw-border-opacity));
  border-style: solid;
  border-radius: 0.375rem;
  border-width: 1px;
  width: 28rem;
  height: 2rem;
}

.input-field {
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
}

.multiselect-field {
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  display: block;
}

.multiselect-label {
  font-size: 1.125rem;
}

.submit-div {
  padding: 1rem;
  position: relative;
  display: flex;
}

.submit {
  width: 18rem;
  height: 3rem;
  font-weight: 600;
  font-size: 1.125rem;
  line-height: 1.75rem;
  --tw-bg-opacity: 1;
  background-color: rgba(39, 174, 96, var(--tw-bg-opacity));
  border-radius: 9999px;
  display: block;
  --tw-border-opacity: 1;
  border-color: rgba(39, 174, 96, var(--tw-border-opacity));
}

textarea {
  font-family: "Proxima Nova", sans-serif;
  width: 57rem;
  height: 4rem;
  border-radius: 0.375rem;
  border-style: solid;
  border-width: 1px;
  --tw-border-opacity: 1;
  border-color: rgba(229, 231, 235, var(--tw-border-opacity));
  font-size: 1.125rem;
  line-height: 1.75rem;
}

::-webkit-input-placeholder { /* Chrome/Opera/Safari */
  --tw-placeholder-opacity: 1;
  color: rgba(209, 213, 219, var(--tw-placeholder-opacity));
}

::-moz-placeholder { /* Firefox 19+ */
  --tw-placeholder-opacity: 1;
  color: rgba(209, 213, 219, var(--tw-placeholder-opacity));
}

:-ms-input-placeholder { /* IE 10+ */
  --tw-placeholder-opacity: 1;
  color: rgba(209, 213, 219, var(--tw-placeholder-opacity));
}

:-moz-placeholder { /* Firefox 18- */
  --tw-placeholder-opacity: 1;
  color: rgba(209, 213, 219, var(--tw-placeholder-opacity));
}

</style>
