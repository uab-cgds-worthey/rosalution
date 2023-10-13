<template>
  <div class="rosalution-section-container">
      <div class="rosalution-section-header">
      <h2 class="rosalution-section-header-text">
          Animal Models
      </h2>
      </div>
      <div class="rosalution-section-seperator"></div>
      <div class="section-content">
          <br>
          <textarea style="width: 400px; height: 100px;" v-model="modelText"/>
          <p  v-html="convertToTable"></p>
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
        if (this.modelText == '')
            return
        
        var data = this.modelText
        var lines = data.split("\n"), output = [], i;
        
        for (i = 0; i < lines.length; i++)
            output.push(
                "<tr><td>"
                + lines[i].split(",").join("</td><td>")
                + "</td></tr>"
            );

        return `<table>` + output.join("") + `</table>`;
      }
    }
}
</script>

<!--
    The styling doesn't appear to work if it's scoped,
    which means anything with this class will be affected
    within Rosalution
-->
<style>

table, th, td {
  border: 1px solid;
}

</style>