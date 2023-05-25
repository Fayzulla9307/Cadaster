<template>
  <div v-if="loaded">
    <div v-if="isAuthenticated">
      <header>
        <div class="title">
          <img src="@/assets/micromine.png" alt="Micromine" width="150" id="logo_top" />
          <span id="caption-text">Система ведения кадастровой инфомации</span>
        </div>
        <div class="menu_container">
          <div class="menu">
            <div id="nav">
              <!-- MainWindow / -->
              <router-link to="/dicts" class="nav-btn" @click="setActive('dicts')" v-bind:class="
                menuItemsActive['dicts'] ? 'selected-menu-item' : ''
              ">Общие справочники</router-link>
              <router-link to="/districts" class="nav-btn" @click="setActive('districts')" v-bind:class="
                menuItemsActive['districts'] ? 'selected-menu-item' : ''
              ">Справочники районов</router-link>
              <router-link to="/deposits" class="nav-btn" @click="setActive('deposits')" v-bind:class="
                menuItemsActive['deposits'] ? 'selected-menu-item' : ''
              ">Месторождения</router-link>
              <router-link to="/reports" class="nav-btn" @click="setActive('reports')" v-bind:class="
                menuItemsActive['reports'] ? 'selected-menu-item' : ''
              ">Отчеты</router-link>
              <router-link to="/security" class="nav-btn" @click="setActive('security')" v-bind:class="
                menuItemsActive['security'] ? 'selected-menu-item' : ''
              ">Безопасность</router-link>
              <router-link to="/about" class="nav-btn" @click="setActive('about')" v-bind:class="
                menuItemsActive['about'] ? 'selected-menu-item' : ''
              ">О программе</router-link>
              <!-- router-link to="/configuration">Настройки</router-link> | -->
              <button id="exit-btn">
                <a href="#" @click="logout()">Выход</a>
              </button>
            </div>
          </div>
        </div>
      </header>
      <div class="main_content_container">
        <div class="main_content"></div>
      </div>
      <footer></footer>

      <router-view></router-view>
    </div>
    <div v-if="!isAuthenticated">
      <Login />
      <img src="@/assets/micromine.png" alt="Micromine" width="150" id="logo" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Login from "@/views/Login.vue";

export default {
  name: "App",
  data() {
    return {
      isAuthenticated: false,
      loaded: false,
      menuItemsActive: {},
    };
  },
  methods: {
    checkAuth() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/auth/validate_token/";
      console.log(url);
      axios.post(url, {}, { headers }).then((response) => {
        this.loaded = true;
        if (response.data[0].valid) {
          this.isAuthenticated = true;
          //this.$router.push("/main/");
        } else {
          this.isAuthenticated = false;
        }
      });
    },
    logout() {
      sessionStorage.setItem("token", null);
      this.isAuthenticated = false;
      this.$router.push("/");
      this.initializeSelectedMenu();
    },
    pollAuthData() {
      this.polling = setInterval(() => {
        this.checkAuth();
      }, 60000);
    },
    setActive(item) {
      this.menuItemsActive["dicts"] = false;
      this.menuItemsActive["districts"] = false;
      this.menuItemsActive["deposits"] = false;
      this.menuItemsActive["reports"] = false;
      this.menuItemsActive["security"] = false;
      this.menuItemsActive["about"] = false;
      this.menuItemsActive[item] = true;
    },
    initializeSelectedMenu() {
      this.menuItemsActive["dicts"] = false;
      this.menuItemsActive["districts"] = false;
      this.menuItemsActive["deposits"] = true;
      this.menuItemsActive["reports"] = false;
      this.menuItemsActive["security"] = false;
      this.menuItemsActive["about"] = false;
    },
  },
  mounted() {
    this.checkAuth();
    this.pollAuthData();
    this.$router.push("/deposits");
    this.initializeSelectedMenu();
  },
  components: {
    Login,
  },
};
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  width: 100%;
}

#nav {
  padding: 25px 30px;
  margin: 0 auto;
}

#nav a {
  font-weight: bold;
  color: #ffffff;
  font-family: "Dazzed", sans-serif;
  text-decoration: none;
  margin: 0 2px;
}


#caption-text {
  font-size: 18px;
}

#logo {
  position: absolute;
  bottom: 20px;
  margin-left: 20px;
}

#logo_top {
  position: absolute;
  display: block;
  margin-left: 3.4%;
}

.nav-btn {
  display: inline-block;
  height: 35px;
  max-width: 100%;
  align-items: center;
  line-height: 2.28571em;
  vertical-align: middle;
  padding: 0 6px;
}

.nav-btn:hover {
  color: rgb(255, 255, 255);
  box-shadow: transparent 0px 0px 0px 2px;
  background-color: rgba(120, 119, 125, 0.6);
  transition: background 0.1s ease-out 0s,
    box-shadow 0.15s cubic-bezier(0.47, 0.03, 0.49, 1.38) 0s;
  border-radius: 3px;
}

.nav-btn:focus {
  background-color: rgba(106, 103, 121, 0.6);
  border-radius: 3px;
}

.title {
  width: 100%;
  display: block;
  position: fixed;
  top: 0%;
  z-index: 1;
  background: #ffffff;
  text-align: center;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  font-weight: bold;
}

.selected-menu-item {
  color: rgb(255, 255, 255);
  box-shadow: transparent 0px 0px 0px 2px;
  background-color: rgba(120, 119, 125, 0.6);
  transition: background 0.1s ease-out 0s,
    box-shadow 0.15s cubic-bezier(0.47, 0.03, 0.49, 1.38) 0s;
  border-radius: 3px;
}

#exit-btn {
  background-color: rgb(79, 67, 140);
  border-style: none;
  border-radius: 3px;
  display: inline-flex;
  height: 35px;
  max-width: 100%;
  align-items: center;
  line-height: 2.28571em;
  vertical-align: middle;
  padding: 0 6px;
}

#exit-btn:hover {
  background-color: rgba(79, 67, 140, 0.8);
  box-shadow: transparent 0px 0px 0px 2px;
  transition: background 0.1s ease-out 0s,
    box-shadow 0.15s cubic-bezier(0.47, 0.03, 0.49, 1.38) 0s;
  border-radius: 3px;
}

#exit-btn:focus {
  background-color: inherit;
}
</style>
