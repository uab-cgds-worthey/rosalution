<template>
    <li tabindex="1" ref="contextRef">
        <slot></slot>
        <ul class="grey-rounded-menu drop-down-content">
            <li v-for="action in actions" :key="action.text" @click="this.runAction(action.operation)">
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
      ),
    },
    context_id: String,
  },
  methods: {
    runAction(actionOperation) {
      actionOperation();
      this.closeContext();
    },
    closeContext() {
      this.$refs.contextRef.blur();
    },
  },
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
    width: 175px;
    padding: .75rem;
    margin-right: var(--p-16)
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

ul li ul li {
  clear: both;
  width: 100%;
  line-height: 2rem;
}

li:focus ul {
    visibility: visible;
    opacity: 1;
    display: block;
}

.drop-down-content {
    text-align: right;
}

.right-side-icon {
    margin-left: var(--p-8);
    margin-bottom: 0.12rem;
}
</style>
