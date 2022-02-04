<template>
  <div class="requiredInputForm" data-test="required-input-form">
    <div style="margin-top: 15px;">
      <label for="name">Name:</label>
      <input type="text" id="name" name="name" v-model="name" data-test="analysis-name">
    </div>
    <div style="margin-top: 15px;">
      <label style="vertical-align: top;" for="description">Description:</label>
      <textarea type="text" id="description" name="description" v-model="description" data-test="description">
      </textarea>
    </div>
    <div style="margin-top: 15px;">
      <button class="addCoordinateButton"
              style="float: left;"
              v-on:click="addGeneticCoords"
              data-test="button-add-coord">
        <img src="../../assets/plus-logo.svg"/>
      </button>
    </div>
    <div style="display: grid; width: 50%; margin-top: 15px;">
      <div style="text-align: center; display: grid; grid-template-columns: repeat(4, 1fr)">
        <label style="" for="chrom">Chromosome:</label>
        <label for="pos">Position:</label>
        <label for="ref">Reference:</label>
        <label for="alt">Alternate:</label>

        <input class="addCoordinateInput"
                v-model="chromosome"
                type="text" id="chrom"
                name="chrom"
                placeholder="8"
                onfocus="this.placeholder=''"
                onblur="this.placeholder='8'"
                data-test="input-coord-chrom">

        <input class="addCoordinateInput"
                v-model="position"
                type="text"
                id="pos"
                name="pos"
                placeholder="19341"
                onfocus="this.placeholder=''"
                onblur="this.placeholder='19341'"
                data-test="input-coord-pos">

        <input class="addCoordinateInput"
                v-model="reference"
                type="text"
                id="ref"
                name="ref"
                placeholder="TGACCAC"
                onfocus="this.placeholder=''"
                onblur="this.placeholder='TGACCAC'"
                data-test="input-coord-ref">

        <input class="addCoordinateInput"
                v-model="alternate"
                type="text"
                id="alt"
                name="alt"
                placeholder="TA"
                onfocus="this.placeholder=''"
                onblur="this.placeholder='TA'"
                data-test="input-coord-alt">
      </div>

      <table data-test="table-coord-list">
      <tbody>
        <tr v-for="(coordinate, index) in coordinates" :key="index" :row="coordinate">
          <td class="coordinateTableRow">{{coordinate.chromosome}}</td>
          <td class="coordinateTableRow">{{coordinate.position}}</td>
          <td class="coordinateTableRow">{{coordinate.reference}}</td>
          <td class="coordinateTableRow">{{coordinate.alternate}}</td>
          <td style="padding-left: 5px; padding-right: 5px;">
              <button class="removeCoordinateButton" v-on:click="deleteRow(index)">
                <img style="height: 20px; width: 20px; " src="../../assets/minus-button.png"/>
              </button>
          </td>
        </tr>
      </tbody>
      </table>
    </div>

    <button v-on:click="createAnalysis" type="button" class="createAnalysisButton" data-test="button-create-analysis">
      Create
    </button>
  </div>
</template>

<script>

export default {
  name: 'analysis-create',
  components: {

  },
  data: function() {
    return {
      name: '',
      description: '',
      coordinates: [],
      chromosome: '',
      position: '',
      reference: '',
      alternate: '',
    };
  },
  methods: {
    addGeneticCoords: function() {
      const coordinate = {
        chromosome: this.chromosome,
        position: this.position,
        reference: this.reference,
        alternate: this.alternate,
      };

      this.chromosome = '';
      this.position = '';
      this.reference = '';
      this.alternate = '';

      this.coordinates.unshift(coordinate);
    },
    createAnalysis: function(event) {
      const formData = {
        name: this.name,
        description: this.description,
        coordinates: this.coordinates,
      };

      this.$emit('create_analysis', formData);
    },
    deleteRow(elem) {
      this.coordinates.splice(elem, 1);
    },
  },
};
</script>

<style scoped>
    @import url("https://use.typekit.net/rgh1osc.css");

    div {
      font-family: "Proxima Nova", sans-serif;
      padding: 0%;
    }

    /* Description Text Area */

    textarea {
      font-family: "Proxima Nova", sans-serif;
      height: 100px;
      width: 400px;
      border-radius: 0.375rem;
      border-style: solid;
      border-width: 1px;
      --tw-border-opacity: 1;
      border-color: rgba(229, 231, 235, var(--tw-border-opacity));
      font-size: 1.125rem;
      line-height: 1.75rem;
    }

    /* Coordinate Input Styling */

    ::placeholder {
      --tw-placeholder-opacity: 1;
      color: rgba(209, 213, 219, var(--tw-placeholder-opacity));
    }

    .addCoordinateInput
    {
      text-align: center;
    }

    input, label {
      margin-right: 15px;
    }

    input {
      border-radius: 0.375rem;
      border-style: solid;
      border-width: 1px;
      --tw-border-opacity: 1;
      border-color: rgba(229, 231, 235, var(--tw-border-opacity));
      font-size: 1rem;
      line-height: 1.35rem;
    }

    .addCoordinateButton
    {
      border: none;
      background-color: white;
      margin-top: 20px;
      margin-right: 5px;
    }

    .removeCoordinateButton
    {
      border: none;
      background: none;
    }

    /* Table Styling */

    table {
      margin-top: 15px;
    }

    tr:nth-child(even) {
        background-color: #f2f2f2;
    }

    .coordinateTableRow {
        width: 25%;
    }

    tbody {
        border: 1px solid black;
        text-align: center;
    }

    /* Create Analysis Button */

    .createAnalysisButton
    {
      width: 10rem;
      height: 2rem;
      margin-top: 15px;
      font-weight: 600;
      font-size: 1rem;
      line-height: 1.75rem;
      --tw-bg-opacity: 1;
      background-color: rgba(39, 174, 96, var(--tw-bg-opacity));
      border-radius: 9999px;
      display: block;
      --tw-border-opacity: 1;
      border-color: rgba(39, 174, 96, var(--tw-border-opacity));
    }
</style>
