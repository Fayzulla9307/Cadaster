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
            class="btn btn-dark btn-lg btn-block"
            style="float: left; width: 300px"
          >
            <BootstrapIcon icon="database-add" />
            Добавить новую запись
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
import OkModal from "./OkModal.vue";

export default {
  name: "PropertyNewItem",
  props: ["category"],
  data() {
    return {
      itemCategory: this.category,
      itemDescription: "",
      showAuthError: false,
      authMessage: "Доступ запрещен",
      authHeader: "Ошибка безопасности",
    };
  },
  watch: {
    category: {
      deep: true,
      handler(n) {
        this.itemCategory = n;
      },
    },
  },
  methods: {
    hideAuthMessage() {
      this.showAuthError = false;
      this.$emit("updated", {});
    },
    addItem(e) {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/add_dictionary_contents/";
      axios
        .post(
          url,
          { category: this.itemCategory, description: this.itemDescription },
          { headers }
        )
        .then((response) => {
          if (response.data[0].auth_fail) {
            this.showAuthError = true;
            return;
          }

          this.itemDescription = "";
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
  height: 50px;
  font-weight: bolder;
  font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS", sans-serif;
  border-style: none !important;
}
</style>
