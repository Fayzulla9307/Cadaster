<template>
  <div class="item">
    <ConfirmModal
      v-if="showConfirmModal"
      v-bind:message="confirmMessage"
      v-bind:header="confirmHeader"
      v-on:confirm="onConfirm"
      v-on:cancel="onCancel"
    />
    <table style="border-style: none !important; width: 100%">
      <tr style="border-style: none !important; width: 100%">
        <td style="width: 50px; border-style: none !important">
          <button
            @click="removeUser"
            class="btn btn-dark btn-lg btn-block"
            style="float: left; width: 200px"
          >
            <BootstrapIcon icon="trash" />
            Удалить
          </button>
        </td>
        <td style="width: 50px">
          <button
            @click="editUser"
            class="btn btn-dark btn-lg btn-block"
            style="float: left; width: 200px"
          >
            <BootstrapIcon icon="pencil" />
            Редактировать
          </button>
        </td>
        <td style="width: 100%">
          <input
            type="text"
            class="form-control form-control-lg"
            style="display: inline; width: calc(100%)"
            v-model="userInfo"
            disabled
          />
        </td>
      </tr>
    </table>
  </div>
</template>

<script>
import axios from "axios";
import BootstrapIcon from "@dvuckovic/vue3-bootstrap-icons";
import ConfirmModal from "../components/ConfirmModal.vue";

export default {
  name: "UserItem",
  props: ["user_id", "username", "role"],
  data() {
    return {
      showEditUser: false,
      confirmMessage: "",
      confirmHeader: "",
      showConfirmModal: false,
      userInfo:
        "Имя пользователя: " +
        this.username +
        ", Роль пользователя: " +
        this.role,
    };
  },
  methods: {
    onConfirm() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/delete_user/";
      axios.post(url, { user_id: this.user_id }, { headers }).then(() => {
        this.showConfirmModal = false;
        this.$emit("user-deleted", {});
      });
    },
    onCancel() {
      this.showConfirmModal = false;
    },
    removeUser(e) {
      this.confirmMessage = "Удалить пользователя?";
      this.confirmHeader = "Удаление данных!";
      this.showConfirmModal = true;
      e.preventDefault();
    },
    editUser(e) {
      this.$emit("user-edited", { user_id: this.user_id });
      e.preventDefault();
    },
  },
  components: {
    BootstrapIcon,
    ConfirmModal,
  },
  mounted() {},
};
</script>

<style scoped>
img {
  height: 30px;
  width: 30px;
}

.item {
  width: calc(100%);
  height: 50px;
  font-weight: bolder;
  font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS", sans-serif;
  border-style: none !important;
}
.delete-btn {
  height: 30px;
  display: inline;
  /*margin-right: 5px;*/
}
.save-btn {
  height: 30px;
  display: inline-block;
  /*margin-right: 5px;*/
}
.inputfield {
  display: inline;
  height: 30px;
  width: 330px;
}
</style>
