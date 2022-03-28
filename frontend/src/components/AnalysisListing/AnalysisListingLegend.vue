<template>
  <div class="legend">
  <font-awesome-icon icon="asterisk" size="xl" style="color: var(--divergen-yellow-200);"/>
  <p>Annotating</p>
  <font-awesome-icon icon="clipboard-check" size="xl" style="color: var(--divergen-blue-200);"/>
  <p>Ready</p>
  <font-awesome-icon icon="book-open" size="xl" style="color: var(--divergen-green-200)"/>
  <p>Active</p>
  <font-awesome-icon icon="pause" size="xl" style="color: var(--cgds-blue-100)"/>
  <p>On Hold</p>
  <font-awesome-icon icon="check" size="xl" style="color: var(--divergen-teal-200)"/>
  <p>Approved</p>
  <font-awesome-icon icon="x" size="xl" style="color: var(--divergen-grey-200)"/>
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
  border-radius: var(--content-border-radius);
  padding: var(--p-8);
  background-color: var(--secondary-background-color);
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
