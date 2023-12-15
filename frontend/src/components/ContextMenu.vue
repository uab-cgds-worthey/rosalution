<template>
    <li>
        <label :for="context_id">
            <slot></slot>
        </label>
        <input type="checkbox" :id="context_id" />
        <ul class="grey-rounded-menu drop-down-content">
            <li v-for="action in actions" :key="action.text" @click="action.operation()">
                <span> {{ action.text }} </span>
                <font-awesome-icon v-if="action.icon" :icon="action.icon" size="lg" class="right-side-icon" />
            </li>
        </ul>
    </li>
</template>

<script>
export default {
    name: 'context-menu',
    props: {
        actions: {
            type: Array,
            validator: (prop) => prop.every(
                (action) => action.text !== undefined || action.divider,
            )
        },
        context_id: String,
    },
    computed: {
        context_toggle() {
            return this.context_id.toLowerCase() + '_menu'
        }
    }
};
</script>

<style scoped>
hr {
    border: 1px solid var(--rosalution-grey-100);
}

.grey-rounded-menu {
    border-radius: var(--content-border-radius);
    background-color: var(--rosalution-white);
    border: 3px solid var(--rosalution-grey-000);
    width: 230px;
    padding: .75rem;
}

.drop-down-content {
    text-align: right;
}

.right-side-icon {
    margin-left: var(--p-8);
    margin-bottom: 0.12rem;
}

ul li ul {
  visibility: hidden;
  opacity: 0;
  position: absolute;
  transition: all 0.5s ease;
  right: 0;
  display: none;
}

ul li ul:hover li:hover {
  color: var(--rosalution-purple-300);
  background-color: var(--rosalution-purple-100);
}

label {
    cursor: pointer;
}

input[type="checkbox"] {
    display: none;
}

/* li input[type=checkbox]:checked ~ ul {
    visibility: visible;
    opacity: 1;
    display: block;
} */

input[type=checkbox]:checked + ul {
    visibility: visible;
    opacity: 1;
    display: block;
}
</style>