<template>
  <div class="login-div">
    <OkModal
      v-bind:header="dsOffer"
      v-bind:message="dsNotImplMsg"
      v-if="showDsModal"
      v-on:confirm="closeDsModal"
    />
    <h3>
      Система ведения государственного геологического кадастра Республики
      Узбекистан
    </h3>
    <form class="login-form">
      <div class="form-group">
        <label>Учетная запись</label>
        <div class="input-group input-group-lg">
          <div class="input-group-addon">
            <span class="input-group-text">
              <BootstrapIcon icon="person" size="2x" />
            </span>
          </div>
          <input
            type="username"
            class="form-control form-control-lg"
            v-model="username"
          />
        </div>
      </div>
      <div class="form-group">
        <label>Пароль</label>
        <div class="input-group input-group-lg">
          <div class="input-group-append">
            <span class="input-group-text">
              <BootstrapIcon icon="lock" size="2x" />
            </span>
          </div>
          <input
            type="password"
            class="form-control form-control-lg"
            v-model="password"
          />
        </div>
      </div>
      <div class="form-group" style="margin-top: 10px">
        <button @click="login" class="btn btn-dark btn-lg btn-block">
          <BootstrapIcon icon="arrow-right-square" size="1x" />
          Войти
        </button>
        <button
          @click="dslogin"
          class="btn btn-dark btn-lg btn-block"
          style="float: right"
        >
          <BootstrapIcon icon="key" size="1x" />
          Войти с цифровым ключом
        </button>
      </div>
      <div class="form-group" v-if="failed" style="margin-top: 10px">
        <div class="alert alert-danger" role="alert">
          Неверный логин или пароль
        </div>
      </div>
    </form>
    Мы поддерживаем RSA ключи Tokey®JCOP3 от CrypToken
  </div>
</template>

<script>
import axios from "axios";
import OkModal from "../components/OkModal.vue";
import BootstrapIcon from "@dvuckovic/vue3-bootstrap-icons";

export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      failed: false,
      dsOffer: "Использование лицензионного ключа для входа",
      dsNotImplMsg: "Обратитесь к производителю ПО для консультации",
      showDsModal: false,
    };
  },
  methods: {
    login(e) {
      const data = { username: this.username, password: this.password };
      const headers = {
        "Content-Type": "application/json",
      };
      axios
        .post(this.$BASE_URL + "/auth/signin/", data, { headers })
        .then((response) => {
          if (response.data[0].success) {
            sessionStorage.setItem("token", response.data[0].token);
            this.$parent.isAuthenticated = true;
            this.$router.push("/deposits/");
          }
          this.failed = !response.data[0].success;
        });
      e.preventDefault();
    },
    dslogin(e) {
      this.showDsModal = true;
      e.preventDefault();
    },
    closeDsModal() {
      this.showDsModal = false;
    },
  },
  components: {
    OkModal,
    BootstrapIcon,
  },
};
</script>

<style scoped>
h3 {
  color: black;
  text-align: center;
}

.login-div {
  position: absolute;

  width: 450px;
  height: 300px;

  /* Center form on page horizontally & vertically */
  top: 50%;
  left: 50%;
  margin-top: -150px;
  margin-left: -225px;
}

.login-form {
  width: 450px;
  height: 300px;

  background: white;
  border-radius: 10px;

  margin: 0;
  padding: 0;
}
</style>
