<template>
  <header>
    <img src="@/assets/diverGen-logo.svg" class="diverGen-logo">
    <div data-test="primary-content" class="content">
      <span class="title left-content">diverGen</span>
      <div class="search">
        <font-awesome-icon icon="magnifying-glass" size="l" class="search-icon"></font-awesome-icon>
        <input data-test="analysis-search" type="search" @input="onSearch" placeholder="Search">
      </div>
      <span class="login">LOGIN</span>
    </div>
  </header>
</template>

<style>

header {
  display: flex;
  flex-direction: row;
  gap: 15px;
  background-color: var(--primary-background-color);
}

img.diverGen-logo {
  width: 55px;
  height: 45px;
  flex: 0 0 auto;
}

header .content {
  display: flex;
  flex: 1 1 auto;
  align-items: center;
  gap: 12px;
  padding: var(--p-8);
  border-radius: var(--content-border-radius);
  background-color: var(--secondary-background-color);
}

header .left-content {
  flex: 0;
}

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
  border: 1px solid var(--divergen-purple-300);
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
}

.search input:hover,
.search input:focus {
  background-color:var(--secondary-background-color);
}

/** todo: need to figure out what this style ought to be */
.login {
  font-size: 1.125rem;
  line-height: 2rem;
}

</style>


<script>
export default {
  name: 'header-component',
  methods: {
    onSearch(event) {
      this.$emit('search', event.target.value);
    },
  },
};
</script>
