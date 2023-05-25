<template>
  <div>
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
    <!-- ConfirmModal
      v-if="showConfirmModal"
      v-bind:message="confirmMessage"
      v-bind:header="confirmHeader"
      v-on:confirm="onConfirm"
      v-on:cancel="onCancel"
    / -->
    <div
      v-for="item in items"
      v-bind:key="
        item.deposit_id +
        '_' +
        item.mine_area_id +
        '_' +
        item.component_id +
        '_' +
        item.year
      "
    >
      <div class="item" >
        <button
          @click="removeItem"
          class="btn btn-dark btn-lg btn-block"
          style="float: left; width: 70px"
        >
          <BootstrapIcon icon="trash" />
        </button>
        <input
          type="text"
          class="form-control form-control-lg"
          v-model="item.year"
          placeholder="Введите год"
        />
        <input
          type="text"
          class="form-control form-control-lg"
          v-model="item.exploration_stage"
          placeholder="Введите степень освоения"
        />
      </div>
    </div>
    <div style="width: calc(100%)">
      <div class="item">
        <button
          @click="addItem"
          class="btn btn-dark btn-lg btn-block"
          style="height: 50px"
        >
          <!-- BootstrapIcon icon="check" / -->
          Добавить запись
        </button>
        <label style="margin-left: 10px; margin-right: 10px; width: 150px; text-align: right; font-weight: bolder;">Год</label>
        <input
          type="text"
          class="form-control form-control-lg"
          style="width: 100px"
          v-model="newItemYear"
          placeholder="Год"
        />
        <label style="margin-left: 10px; margin-right: 10px; width: 150px; text-align: right; font-weight: bolder;">Стадии изученности</label>
        <select
          class="form-select form-control-lg"
          v-model="selectedStageId"
          aria-label="Стадии изученности"
          style="width: calc(100% - 640px);"
          placeholder="Введите степень освоения"
        >
          <option v-for="o in stages" v-bind:value="o.id" v-bind:key="o.id">
            {{ o.description }}
          </option>
        </select>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import BootstrapIcon from "@dvuckovic/vue3-bootstrap-icons";
//import ConfirmModal from "../components/ConfirmModal.vue";
import OkModal from "./OkModal.vue";

export default {
  name: "EmptyBodyCtrl",
  props: ["id_geo_characteristics"],
  data() {
    return {
      items: [],
      showSpinner: false,
      showError: false,
    };
  },
  methods: {
    loadEmptyBodies() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/get_empty_bodies/";
      axios
        .post(url, {  }, { headers })
        .then((response) => {
          if (!response.data[0].auth_fail) {            
            this.stages = response.data[0].result;
          }
        });
    },
  },
  mounted() {
    this.loadEmptyBodies();
  },
  components: {
    OkModal,
    BootstrapIcon,
  },
};
</script>

<style scoped>
input,
select {
  display: inline-block;
  vertical-align: middle;
  margin-left: 10px;
  height: 30px;
}
</style>
