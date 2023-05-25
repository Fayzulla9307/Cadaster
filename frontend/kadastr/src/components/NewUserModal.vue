<template>
  <div class="modal-mask">
    <div class="modal-window">
      <div class="header">Добавление нового пользователя</div>
      <div class="body">
        <form class="login-form">
          <div class="form-group">
            <label>Имя пользователя</label>
            <input
              type="text"
              class="form-control form-control-lg"
              v-model="username"
            />
          </div>
          <div class="form-group">
            <label>Роль</label>
            <select
              class="form-select"
              v-model="selectedRoleId"
              aria-label="Роль"
            >
              <option
                v-for="role in roles"
                v-bind:value="role.role_id"
                v-bind:key="role.role_id"
              >
                {{ role.role }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Пароль</label>
            <input
              type="password"
              class="form-control form-control-lg"
              v-model="password"
            />
          </div>
          <div class="form-group">
            <label>Описание пользователя</label>
            <input
              type="text"
              class="form-control form-control-lg"
              v-model="description"
            />
          </div>
          <div class="form-group" style="margin-top: 10px">
            <button @click="save" class="btn btn-dark btn-lg btn-block save">
              Сохранить
            </button>
            <button @click="cancel" class="btn btn-dark btn-lg btn-block close">
              Отменить
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "NewUserModal",
  props: [],
  data() {
    return {
      roles: [],
      failed: false,
      username: null,
      password: null,
      description: null,
      selectedRoleId: null,
    };
  },
  methods: {
    save(e) {
      this.$emit("save", {
        username: this.username,
        description: this.description,
        role_id: this.selectedRoleId,
        password: this.password,
      });
      e.preventDefault();
    },
    cancel(e) {
      this.$emit("cancel", {});
      e.preventDefault();
    },
    getRoles() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      var url = this.$BASE_URL + "/api/get_roles/";
      axios
        .post(url, { user_id: this.user_id }, { headers })
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.roles = response.data[0].result;
            this.getUser();
          }
        });
    },
  },
  mounted() {
    this.getRoles();
  },
};
</script>

<style scoped>
.modal-mask {
  position: fixed;
  z-index: 9998;
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
  width: 500px;
  height: 500px;
  top: 50%;
  left: 50%;
  margin-top: -250px;
  margin-left: -250px;
  z-index: 100;
}

.header {
  height: 30px;
  width: 100%;
  background-color: rgb(143, 150, 150);
  text-align: center;
  font-weight: bold;
}

.body {
  font-weight: bolder;
  color: black;
  text-align: center;
}

.close {
  position: absolute;
  bottom: 10px;
  right: 10px;
}

.save {
  position: absolute;
  bottom: 10px;
  left: 10px;
}
</style>
