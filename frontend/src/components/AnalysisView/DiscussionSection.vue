<template>
    <div class="rosalution-section-container">
        <input type="checkbox" id="discussion_toggle" />
        <div class="rosalution-section-header">
            <h2 class="rosalution-section-header-text">Discussion</h2>
            <span class="rosalution-section-center" data-test="header-datasets"/>
            <button class="primary-button new-discussion-button">New Discussion</button>
            <label class="collapsable-icon" for="discussion_toggle">
                <font-awesome-icon icon="chevron-down" size="lg"/>
            </label>
        </div>
        <div class="rosalution-section-seperator"></div>
        <div class="section-content">
            Content
        </div>
    </div>
</template>

<script>
export default {
  name: 'discussion-section',
  props: {
    header: {
      type: String,
    },
  },
};

</script>

<style scoped>

.new-discussion-button {
    margin-bottom: 10px;
    margin-right: 10px
}

.collapsable-icon {
    color: var(--rosalution-grey-200);
    cursor: pointer;
}

input[type="checkbox"] {
    display: none;
}

.rosalution-section-container input[type="checkbox"]:checked ~ .section-content {
    display: none;
}

input[type="checkbox"]:checked ~ .rosalution-section-header > span ~ label.collapsable-icon {
    transform: scaleY(-1);
}

</style>
