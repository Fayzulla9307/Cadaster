<template>
  <div class="security">
    <ConfirmModal
      v-if="showConfirmModal"
      v-bind:message="confirmMessage"
      v-bind:header="confirmHeader"
      v-on:confirm="onConfirm"
      v-on:cancel="onCancel"
    />
    <OkModal
      v-if="showError"
      v-bind:message="errorMessage"
      v-bind:header="header"
      v-on:confirm="hideErrorMessage"
    />
    <Spinner v-if="showSpinner" />
    <UsersTable v-if="hasPermissions" />
    <div class="disclaimer" v-if="!hasPermissions">
      Добро пожаловать в конфигурацию системы безопасности. Здесь вы сможете
      добавить пользователей, удалить пользователей, назначить пользователей в
      группы, задать пароль для пользователя. Данный функционал доступен только
      для администраторов системы!
    </div>
  </div>
</template>

<script>
import axios from "axios";
import OkModal from "../components/OkModal.vue";
import ConfirmModal from "../components/ConfirmModal.vue";
import Spinner from "../components/Spinner.vue";
import UsersTable from "../components/UsersTable.vue";

export default {
  name: "SecuritySettings",
  props: [],
  data() {
    return {
      showError: false,
      header: "Сохранение данных",
      errorMessage: "",
      failed: false,
      showSpinner: false,
      showConfirmModal: false,
      hasPermissions: false,
      roles: [],
    };
  },
  methods: {
    has_permissions() {
      const data = {};
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      axios
        .post(
          this.$BASE_URL + "/api/has_permissions_to_security_settings/",
          data,
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.hasPermissions = true;
          }
        });
    },
  },
  components: {
    Spinner,
    OkModal,
    ConfirmModal,
    UsersTable,
  },
  mounted() {
    this.has_permissions();
  },
};
</script>

<style scoped>
.modal-mask {
  position: fixed;
  z-index: 100009;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  transition: opacity 0.3s ease;
}

.modal-window {
  border: rgb(169, 255, 202);
  background-color: white;
  position: fixed;
  width: 400px;
  height: 400px;
  top: 50%;
  left: 50%;
  margin-top: -100px;
  margin-left: -200px;
  z-index: 1000092;
}

.header {
  height: 30px;
  width: 100%;
  background-color: rgb(143, 150, 150);
  text-align: center;
  font-weight: bold;
}

.message {
  font-weight: bolder;
  color: black;
  text-align: center;
}

.close {
  position: absolute;
  bottom: 10px;
  right: 10px;
}

.excel {
  position: absolute;
  bottom: 10px;
  left: 10px;
}

.html {
  position: absolute;
  bottom: 10px;
  left: 30px;
}

td {
  margin-left: 100px !important;
}

table {
  border-spacing: 20px !important;
}

.disclaimer {
  position: absolute;
  top: 50%;
  left: calc(50% - 300px);
  width: 600px;
  margin: auto;
}
</style>
