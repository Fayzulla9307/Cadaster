<template>
  <div class="item">
    <OkModal
      v-if="showError"
      v-bind:message="errorMessage"
      v-bind:header="header"
      v-on:confirm="hideErrorMessage"
    />
    <OkModal
      v-if="showAuthError"
      v-bind:message="authMessage"
      v-bind:header="authHeader"
      v-on:confirm="hideAuthMessage"
    />
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
            @click="removeItem"
            class="btn btn-dark btn-lg btn-block"
            style="float: left; width: 200px"
          >
            <BootstrapIcon icon="trash" />
            Удалить запись
          </button>
        </td>
        <td style="width: 50px">
          <button
            @click="saveItem"
            class="btn btn-dark btn-lg btn-block"
            style="float: left; width: 200px"
          >
            <BootstrapIcon icon="save" />
            Сохранить
          </button>
        </td>
        <td style="width: 100%">
          <input
            type="text"
            class="form-control form-control-lg"
            style="display: inline; width: calc(100%)"
            v-model="itemDescription"
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
import OkModal from "./OkModal.vue";

export default {
  name: "PropertyItem",
  props: ["displayButtons", "id", "category", "description"],
  data() {
    return {
      header: "Сохранение данных формы",
      errorMessage: "",
      showError: false,
      itemCategory: this.category,
      itemId: this.id,
      itemDescription: this.description,
      confirmMessage: "",
      confirmHeader: "",
      showConfirmModal: false,
      showAuthError: false,
      authMessage: "Доступ запрещен",
      authHeader: "Ошибка безопасности",
    };
  },
  methods: {
    hideAuthMessage() {
      this.showAuthError = false;
    },
    hideErrorMessage() {
      this.showError = false;
      this.$emit("updated", {});
    },
    onConfirm() {
      this.showConfirmModal = false;
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/delete_dictionary_contents/";
      axios
        .post(
          url,
          { id: this.itemId, category: this.itemCategory },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            if (response.data[0].result) {
              this.$emit("updated", {});
            } else {
              this.showError = true;
              this.header = "Ошибка при удаление данных";
              this.errorMessage = response.data[0].reason;
            }
          } else {
            this.showAuthError = true;
          }
        });
    },
    onCancel() {
      this.showConfirmModal = false;
    },
    removeItem(e) {
      this.confirmMessage =
        "Удалить справочные данные? Это приведет к потере данных (месторождений, участков, лицензий, запасов, а также всех движений и исторических данных!)";
      this.confirmHeader = "Удаление данных!";
      this.showConfirmModal = true;
      e.preventDefault();
    },
    saveItem(e) {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/update_dictionary_contents/";
      axios
        .post(
          url,
          {
            id: this.itemId,
            category: this.itemCategory,
            description: this.itemDescription,
          },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            if (response.data[0].result) {
              this.showError = true;
              this.errorMessage = "Данные сохранены";
            } else {
              this.showError = true;
              this.header = "Ошибка при сохранение данных";
              this.errorMessage = response.data[0].reason;
            }
          } else {
            this.showAuthError = true;
          }
        });
      e.preventDefault();
    },
  },
  components: {
    BootstrapIcon,
    OkModal,
    ConfirmModal,
  },
  mounted() {
    this.$emit("loaded");
  },
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
