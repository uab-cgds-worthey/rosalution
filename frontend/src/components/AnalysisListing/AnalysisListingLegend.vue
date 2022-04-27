<template>
  <div class="legend">
    <font-awesome-icon icon="asterisk" size="lg" style="color: var(--divergen-status-annotation);"/>
    <p>Annotating</p>
    <font-awesome-icon icon="clipboard-check" size="lg" style="color: var(--divergen-status-ready);"/>
    <p>Ready</p>
    <font-awesome-icon icon="book-open" size="lg" style="color: var(--divergen-status-active)"/>
    <p>Active</p>
    <font-awesome-icon icon="pause" size="lg" style="color: var(--divergen-status-approved)"/>
    <p>On Hold</p>
    <font-awesome-icon icon="check" size="lg" style="color: var(--divergen-status-on-hold)"/>
    <p>Approved</p>
    <font-awesome-icon icon="x" size="lg" style="color: var(--divergen-status-declined)"/>
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
  padding-right: var(--p-10);
}

</style>


<script>
export default {
  name: 'analysis-listing-legend',
};
</script>
