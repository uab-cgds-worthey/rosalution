<template>
  <div class="legend">
  <font-awesome-icon icon="asterisk" size="xl" style="color: #feca0f;"/>
  <p>Annotating</p>
  <font-awesome-icon icon="clipboard-check" size="xl" style="color: #0066FF;"/>
  <p>Ready</p>
  <font-awesome-icon icon="book-open" size="xl" style="color: #00c036"/>
  <p>Active</p>
  <font-awesome-icon icon="pause" size="xl" style="color: ced2fe"/>
  <p>On Hold</p>
  <font-awesome-icon icon="check" size="xl" style="color: 13cec3"/>
  <p>Approved</p>
  <font-awesome-icon icon="x" size="xl" style="color: c4c4c4"/>
  <p>Declined</p>
  </div>
</template>

<style>

.legend {
  display: flex;
  flex-grow: 0;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 10px;
  border-radius: 10px;
  padding: 10px;
  background-color: white;
}

.legend p {
  line-height: .245rem;
}

</style>


<script>
export default {
  name: 'analysis-listing-legend',
};
</script>
