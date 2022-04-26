<template>
  <div>
    <div class="content-box-border">
      <div class="section-header">
        <span class="section-name">
          Header name
        </span>
        <span class="logo-dropdown-edit">
          Logo
        </span>
        <div class="seperator"></div>
      </div>
      <div class="fields">
        <ul class="field-list">
          <li>
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
  props: {
  },
};
</script>

<style scoped>

div {
  font-family: "Proxima Nova", sans-serif;
}

.content-box-border {
  width: 1180px;
  height: 284px;
  flex-grow: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 11px;
  padding: 10px;
  border-radius: 20px;
  background-color: #fff;
}

.section-name {
  width: 55px;
  height: 28px;
  margin: 2px 2px 0 0;
  font-family: Arial;
  font-size: 24px;
  font-weight: bold;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
  letter-spacing: normal;
  text-align: left;
  color: #000;
}

.Vector {
  width: 24px;
  height: 24px;
  margin: 0 0 6px;
  background-color: #d9c2ff;
}

.logo-dropdown-edit {
  width: 1160px;
  height: 2px;
  flex-grow: 0;
  background-color: #e7e6e6;
}

.field-label {
  width: 180px;
  height: 22px;
  margin: 0 19px 0.1px 0;
  font-family: ProximaNova;
  font-size: 18px;
  font-weight: 600;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
  letter-spacing: 0.18px;
  text-align: left;
  color: #000;
}

.value {
  height: 54px;
  flex-grow: 1;
  font-family: ProximaNova;
  font-size: 18px;
  font-weight: normal;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
  letter-spacing: normal;
  text-align: left;
  color: #000;
}

</style>
