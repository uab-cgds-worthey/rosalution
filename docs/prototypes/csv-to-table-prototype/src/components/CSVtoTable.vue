<template>
  <div class="rosalution-section-container">

      <div class="rosalution-section-header">
      <h2 class="rosalution-section-header-text">
          Animal Models
      </h2>
      <span class="rosalution-section-center" data-test="header-datasets">
          <slot name="headerDatasets"></slot>
      </span>

      <label class="collapsable-icon" v-bind:for="section_toggle">
          <font-awesome-icon icon="chevron-down" size="lg"/>
      </label>
      </div>
      <div class="rosalution-section-seperator"></div>
      <div class="section-content">
          <br>
          <textarea style="width: 400px; height: 100px;" v-model="modelText"/>
          <span  v-html="convertToTable"></span>
      </div>
  </div>
</template>

<script>
export default {
  name: 'csv-to-table',
  data() {
      return {
          section_toggle: 'animal models' + '_collapse',
          modelText: ''
      }
  },
  computed: {
      convertToTable() {
        var data = this.modelText
        console.log(data)
        
        var lines = data.split("\n"), output = [], i;
        
        for (i = 0; i < lines.length; i++)
            output.push(
                "<tr><td>"
                + lines[i].split(",").join("</td><td>")
                + "</td></tr>"
            );

        output = `<table class="new-table">` + output.join("") + `</table>`;

        return output
      }
  }
}
</script>

<!--
    The styling doesn't appear to work if it's scoped,
    which might affect anything within
-->
<style>
.new-table {
  border-collapse: collapse;
  border: 2px black solid;
  font: 12px sans-serif;
}
</style>