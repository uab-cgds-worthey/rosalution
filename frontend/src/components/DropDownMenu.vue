<template>
  <li>
    <slot></slot>
    <ul class="grey-rounded-menu drop-down-content">
      <li v-for="action in actions" :key="action.text" @click="action.operation()">
        <span> {{ action.text }} </span>
        <font-awesome-icon v-if="action.icon" :icon="action.icon" size="lg" class="right-side-icon"></font-awesome-icon>
        <hr style="margin-top: .25rem;" v-if="action.divider" />
      </li>
    </ul>
  </li>
</template>

<script>
export default {
  name: 'drop-down-menu',
  props: {
    actions: {
      type: Array,
      validator: (prop) => prop.every(
          (action) => action.text !== undefined || action.divider,
      ),
    },
  },
};

</script>

<style scoped>
hr {
  border: 1px solid var(--rosalution-grey-100);
}

li {
  display: block;
  transition-duration: 0.5s;
}

li:hover {
  cursor: pointer;
}

ul li ul {
  visibility: hidden;
  opacity: 0;
  position: absolute;
  transition: all 0.5s ease;
  right: 0;
  display: none;
}

ul li:hover > ul,
ul li ul:hover {
  visibility: visible;
  opacity: 1;
  display: block;
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

.grey-rounded-menu {
  border-radius: var(--content-border-radius);
  background-color: var(--rosalution-white);
  border: 3px solid var(--rosalution-grey-000);
  width: 230px;
  padding: .75rem;
  color: var(--rosalution-black)
}

.drop-down-content {
  text-align: right;
}

.right-side-icon {
  margin-left: var(--p-8);
  margin-bottom: 0.12rem;
}

</style>
