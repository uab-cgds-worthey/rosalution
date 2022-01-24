<template>
  <div class="md:w-40 text-gray-700 bg-green-600">
    <div class="px-8 py-4 items-center justify-between">
      <router-link to="/" class="text-lg font-semibold tracking-widest text-gray-900 uppercase rounded-lg focus:outline-none focus:shadow-outline">Delphi</router-link>
      <button class="rounded-lg md:hidden focus:outline-none focus:shadow-outline">
        <svg fill="currentColor" viewBox="0 0 20 20" class="w-6 h-6">
          <path fill-rule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM9 15a1 1 0 011-1h6a1 1 0 110 2h-6a1 1 0 01-1-1z" clip-rule="evenodd"></path>
          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
        </svg>
      </button>
    </div>
    <nav class="px-4 pb-4 md:pb-0 flex flex-wrap">
      <router-link class="" to="/about">About</router-link>
    </nav>
  </div>
</template>