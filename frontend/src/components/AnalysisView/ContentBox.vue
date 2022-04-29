<template>
  <div class="content-box" @wheel.prevent @touchmove.prevent @scroll.prevent>
    <div class="content-box-border">
      <div class="section-header">
        <span class="section-name">
          Header {{section_name}}
        </span>
        <span class="logo-dropdown-edit" >
          <font-awesome-icon icon="chevron-down" size="lg"/>
        </span>
        <div class="seperator"></div>
      </div>
      <div class="fields">
        <ul class="field-list">
          <li class="field-value-row">
            <label class="field-label">
              Field
            </label>
            <span class="field-value">
              Value
            </span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'content-box',
  components: {
  },
  props: ['section_name'],
  data: function() {
    return {
      fieldsList: [],
    };
  },
  methods: {
    dropDown() {
      return 0;
    },
  },
};
</script>

<style scoped>

div {
  font-family: "Proxima Nova", sans-serif;
  padding: 0%;
  display: inline-block;
}

.content-box {
  text-decoration: none;
  display: flex;
  flex-wrap: wrap;
  flex: 1;
  flex-grow: 0;
  width: 100%;
}

.content-box-border {
  width: 71.5rem;
  min-height: 10rem;
  height: auto;
  flex-grow: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  gap: .6875rem;
  padding: .625rem;
  border-radius: 1.25rem;
  background-color: #fff;
}

.section-header {
  height: 1.75rem;;
  gap: 66.5rem;
  align-self: stretch;
  flex-grow: 0;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 0;
}

.section-name {
  width: 3.4375rem;
  height: 1.75rem;
  margin: .125rem .125rem 0 0;
  font-family: Arial;
  font-size: 1.5rem;
  font-weight: bold;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
  letter-spacing: normal;
  text-align: left;
  color: #000;
}

.logo-dropdown-edit {
  width: 1.875rem;
  height: 1.875rem;
  flex-grow: 0;
  object-fit: contain;
  color: #c4c4c4;
  float: right;
}

.field-value-row {
  height: 3.375rem;
  align-self: stretch;
  flex-grow: 0;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
  gap: .625rem;
  padding: 0;
}

.field-label {
  width: 11.25rem;
  height: 1.375rem;
  margin: 0 1.1875rem .0063rem 0;
  font-size: 1.125rem;
  font-weight: 600;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
  letter-spacing: .0112rem;
  text-align: left;
  color: #000;
}

.value {
  height: 3.375rem;
  flex-grow: 1;
  font-size: 1.125rem;
  font-weight: normal;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
  letter-spacing: normal;
  text-align: left;
  color: #000;
}

</style>
