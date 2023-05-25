<template>
  <div class="item">
    <OkModal
      v-if="showAuthError"
      v-bind:message="authMessage"
      v-bind:header="authHeader"
      v-on:confirm="hideAuthMessage"
    />
    <table style="border-style: none !important; width: 100%">
      <tr style="border-style: none !important; width: 100%">
        <td style="width: 50px; border-style: none !important">
          <button
            @click="addItem"
            class="btn btn-dark btn-md btn-block btn-add"
            style="float: left; width: 250px"
          >
            <BootstrapIcon icon="plus-square-fill" />
            Добавить новую запись
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
import OkModal from "./OkModal.vue";

export default {
  name: "DistrictNewItem",
  props: ["id_republic", "id_area"],
  data() {
    return {
      areaId: this.id_area,
      republicId: this.id_republic,
      districtName: "",
      showAuthError: false,
      authMessage: "Доступ запрещен",
      authHeader: "Ошибка безопасности",
    };
  },
  watch: {
    id_area: {
      deep: true,
      handler(n) {
        this.areaId = n;
      },
    },
    id_republic: {
      deep: true,
      handler(n) {
        this.republicId = n;
      },
    },
  },
  methods: {
    hideAuthMessage() {
      this.$emit("district-updated", {});
      this.showAuthError = false;
    },
    addItem(e) {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/add_district/";
      axios
        .post(
          url,
          { area_id: this.areaId, district_name: this.districtName },
          { headers }
        )
        .then((response) => {
          if (response.data[0].auth_fail) {
            this.showAuthError = true;
            return;
          }

          this.districtName = "";
        });
      e.preventDefault();
    },
  },
  components: {
    BootstrapIcon,
    OkModal,
  },
  mounted() {},
};
</script>

<style scoped>
.item {
  width: calc(100%);
  margin-top: 20px;
  height: 50px;
  font-weight: bolder;
  font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS", sans-serif;
  border-style: none !important;
}
</style>
