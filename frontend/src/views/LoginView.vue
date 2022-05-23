<template>
    <div class="center">
        <h1 v-if="username != ''">Welcome, {{ this.username }}</h1>
        <h1 v-else>Authentication</h1>
          <input v-model="username" placeholder="username"/>
          <br />
          <br />
          <input v-model="password" placeholder="password" type="password"/>
          <br />
          <br />
          <button @click="loginTemp" type="submit">Login</button>
          <br />
          <br />
          <button @click="verify" type="submit">Verify</button>   
          <br />
          <br />
          <button @click="logout" type="submit">Logout</button>          
    </div>
</template>

<script>

export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async loginTemp() {
      const loginParams = new URLSearchParams({
        'username': this.username,
        'password': this.password,
        'scope': 'read'
      });

      console.log(loginParams.values)
      
      const response = await fetch("http://local.divergen.cgds/divergen/api/auth/token", {
          method: 'POST',
          headers: {
              "accept": "application/json",
              "Content-Type": "application/x-www-form-urlencoded",
          },
          mode: 'cors',
          cache: 'no-cache',
          body: 'grant_type=password&scope=read+write&username=' + this.username + '&password=' + this.password,
      });

      //grant_type=password&scope=me+items&username=johndoe&password=secret

      console.log(await response.json());
    },
    async verify() {
      const verifyURL = '/divergen/api/auth/verify';
      const newURL = await fetch(verifyURL, {
        method: 'GET',
        mode: 'cors',
      });

      const response = await newURL.json();

      console.log(response);
    },
    async login() {
      const loginUrl = '/divergen/api/auth/login';
      const newURL = await fetch(loginUrl, {
        method: 'GET',
        mode: 'cors',
      });

      const response = await newURL.json();

      if ('url' in response) {
        console.log(response['url']);
        window.location = response['url'];
      } else if ('username' in response) {
        console.log(response['username']);
        this.username = response['username'];
      }
    },
    async logout() {
      const logoutUrl = '/divergen/api/auth/logout';
      const newURL = await fetch(logoutUrl, {
        method: 'GET',
        mode: 'cors',
      });

      const response = await newURL.json();
      console.log(response['url']);

      window.location = response['url'];
    },
  },
};
</script>

<style>
.center {
  margin: auto;
  text-align: center;
  width: 50%;
  border: 3px solid green;
  padding: 10px;
}
</style>