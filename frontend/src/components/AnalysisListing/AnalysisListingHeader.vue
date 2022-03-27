<template>
  <header>
    <img src="@/assets/diverGen-logo.svg" class="diverGen-logo">
    <div data-test="primary-content" class="content">
      <span class="title">diverGen</span>
      <div class="search">
        <font-awesome-icon icon="magnifying-glass" size="l" class="search-icon"></font-awesome-icon>
        <input type="search" @input="onSearch" placeholder="Search">
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
  background-color: #F3F5F9;
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
  padding: .5rem;
  border-radius: 10px;
  background-color: white;
}

.title {
  flex: 0;
  font-size: 1.5rem;
  line-height: 2rem;
  font-weight: 700;
}

.search {
  flex: 1 1 auto;
  display: inline-flex;
  align-items: center;
  padding: 0.313rem;
  border: 1px solid transparent;
  border-radius: 10px;
  background-color: #f3f5f9;
}

.search:hover, .search:focus, .search:focus-within{
  border: 1px solid rgb(69 28 137);
  box-shadow:  0px 0 0 4px rgba(69, 28, 137, 0.10);
  background-color: white;
}

.search svg{
  padding:0.25rem;
}


.search input {
  background-color: #f3f5f9;
  border:none;
  outline:none;
  font-size: 1.125rem;
  line-height: 1.75rem;
  flex: 1;
}

.search input:hover,
.search input:focus {
  background-color:white;
}

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
