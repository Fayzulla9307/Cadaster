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
            class="btn btn-dark btn-md btn-block btn-delete"
            style="float: left; width: 42px"
          >
            <BootstrapIcon icon="trash" />
          </button>
        </td>
        <td style="width: 50px">
          <button
            @click="saveItem"
            class="btn btn-dark btn-md btn-block btn-edit"
            style="float: left; width: 42px"
          >
            <BootstrapIcon icon="check2-square" />
          </button>
        </td>
        <td style="width: 100%">
          <input
            type="text"
            class="form-control form-control-md"
            style="display: inline; width: calc(100%)"
            v-model="districtName"
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
  name: "DistrictItem",
  props: [
    "displayButtons",
    "id_republic",
    "id_area",
    "id_district",
    "district_name",
  ],
  data() {
    return {
      header: "Сохранение данных формы",
      errorMessage: "",
      showError: false,
      areaId: this.id_area,
      republicId: this.id_republic,
      districtId: this.id_district,
      districtName: this.district_name,
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
      this.$emit("district-updated", {});
    },
    onConfirm() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/delete_district/";
      axios
        .post(
          url,
          {
            republic_id: this.republicId,
            area_id: this.areaId,
            district_id: this.districtId,
          },
          { headers }
        )
        .then((response) => {
          if (response.data[0].auth_fail) {
            this.showAuthError = true;
            return;
          }
          this.$emit("district-updated", {});
        });
    },
    onCancel() {
      this.showConfirmModal = false;
    },
    removeItem(e) {
      this.confirmMessage =
        "Удалить район? Это приведет к потере данных (месторождений, участков, лицензий, запасов, а также всех движений и исторических данных!)";
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
      const url = this.$BASE_URL + "/api/update_district/";
      axios
        .post(
          url,
          {
            republic_id: this.republicId,
            area_id: this.areaId,
            district_id: this.districtId,
            distrcit_name: this.districtName,
          },
          { headers }
        )
        .then((response) => {
          if (response.data[0].auth_fail) {
            this.showAuthError = true;
            return;
          }
          this.showError = true;
          this.errorMessage = "Данные сохранены";
        });
      e.preventDefault();
    },
  },
  components: {
    BootstrapIcon,
    OkModal,
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
