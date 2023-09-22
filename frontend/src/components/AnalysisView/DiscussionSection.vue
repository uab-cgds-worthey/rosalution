<template>
    <div class="rosalution-section-container">
        <input type="checkbox" v-bind:id="section_toggle" />
        <div class="rosalution-section-header">
            <h2 class="rosalution-section-header-text">Discussion</h2>
            <span class="rosalution-section-center" data-test="header-datasets"/>
            <button class="primary-button new-discussion-button">New Discussion</button>
            <label class="collapsable-icon" v-bind:for="section_toggle">
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
    name: "",
    props: {
        header: {
            type: String,
        },
    },
    data() {
        return
    }
}

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

</style>