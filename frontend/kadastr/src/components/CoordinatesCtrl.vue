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
      <div class="item">
        <button
          @click="removeItem"
          class="btn btn-dark btn-lg btn-block"
          style="float: left; width: 70px"
        >
          <BootstrapIcon icon="trash" />
        </button>
        <label
          style="
            margin-left: 10px;
            margin-right: 10px;
            width: 150px;
            text-align: right;
            font-weight: bolder;
          "
          >Широта</label
        >
        <input
          type="text"
          class="form-control form-control-lg"
          v-model="item.lat"
          style="width: 200px"
          placeholder="Широта"
        />
        <label
          style="
            margin-left: 10px;
            margin-right: 10px;
            width: 150px;
            text-align: right;
            font-weight: bolder;
          "
          >Долгота</label
        >
        <input
          type="text"
          class="form-control form-control-lg"
          v-model="item.long"
          style="width: 200px"
          placeholder="Долгота"
        />
      </div>
    </div>
    <div style="width: calc(100%)">
      <div class="item">
        <button
          @click="removeItem"
          class="btn btn-dark btn-lg btn-block"
          style="height: 50px"
        >
          <!-- BootstrapIcon icon="check" / -->
          Добавить запись
        </button>
        <label
          style="
            margin-left: 10px;
            margin-right: 10px;
            width: 150px;
            text-align: right;
            font-weight: bolder;
          "
          >Широта</label
        >
        <input
          type="text"
          class="form-control form-control-lg"
          style="width: 200px"
          placeholder="Широта"
          v-model="longitude"
        />
        <label
          style="
            margin-left: 10px;
            margin-right: 10px;
            width: 150px;
            text-align: right;
            font-weight: bolder;
          "
          >Долгота</label
        >
        <input
          type="text"
          class="form-control form-control-lg"
          style="width: 200px"
          placeholder="Долгота"
          v-model="latitude"
        />
      </div>
    </div>
  </div>
</template>

<script>
//import axios from "axios";
import BootstrapIcon from "@dvuckovic/vue3-bootstrap-icons";
//import ConfirmModal from "../components/ConfirmModal.vue";
import OkModal from "./OkModal.vue";

export default {
  name: "CoordinatesCtrl",
  props: ["deposit_id", "mine_area_id", "component_id"],
  data() {
    return {
      items: [],
      year: null,
      stages: [],
      showSpinner: false,
      showError: false,
      latitude: 0,
      longitude: 0,
    };
  },
  methods: {},
  mounted() {},
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
