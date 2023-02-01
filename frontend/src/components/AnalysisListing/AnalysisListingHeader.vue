<template>
  <RosalutionHeader :username="username">
      <div class="search">
        <font-awesome-icon icon="magnifying-glass" size="lg" class="search-icon"></font-awesome-icon>
        <input
          data-test="analysis-search"
          type="search"
          v-model="searchInput"
          placeholder="Search"
        >
      </div>
  </RosalutionHeader>
</template>

<script>
import RosalutionHeader from '@/components/RosalutionHeader.vue';

export default {
  name: 'analysis-listing-header-component',
  components: {
    RosalutionHeader,
  },
  props: {
    username: {
      type: String,
      default: undefined,
      required: false,
    },
    searchText: {
      type: String,
      required: false,
      default: '',
    },
  },
  emits: ['update:searchText'],
  computed: {
    searchInput: {
      get() {
        return this.searchText;
      },
      set(value) {
        this.$emit('update:searchText', value);
      },
    },
  },
};
</script>

<style scoped>

.search {
  flex: 1 1 auto;
  display: inline-flex;
  align-items: center;
  padding: var(--p-5);
  border: 1px solid transparent;
  border-radius: var(--content-border-radius);
  background-color: var(--primary-background-color);
}

.search:hover, .search:focus, .search:focus-within{
  border: 1px solid var(--rosalution-purple-300);
  box-shadow:  0px 0 0 4px rgba(69, 28, 137, 0.10);
  background-color: var(--secondary-background-color);
}

.search svg{
  padding:var(--p-5);
}

.search input {
  background-color: var(--primary-background-color);
  border:none;
  outline:none;
  flex: 1;
  padding: 0;
  box-shadow: none;
}

.search input:hover,
.search input:focus {
  background-color:var(--secondary-background-color);
}

</style>


