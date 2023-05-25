<template>
  <div class="table">
    <Spinner v-if="showSpinner" />
    <OkModal
      v-if="showAuthError"
      v-bind:message="authMessage"
      v-bind:header="authHeader"
      v-on:confirm="hideAuthMessage"
    />
    <EditDepositModal
      v-if="showEditDeposit"
      v-on:cancel="closeUpdate"
      v-on:save="updateExisting"
      v-bind:deposit_id="currentDepositId"
    />
    <NewDepositModal
      v-if="showAddNewDeposit"
      v-on:cancel="closeAddNew"
      v-on:save="saveNew"
    />
    <Filter v-on:filter="filterTable" v-bind:filterVal="filter" />
    <DepositItem
      v-for="item in items"
      v-bind:key="item.deposit_id"
      v-bind:id_deposit="item.deposit_id"
      v-bind:deposit_name="item.deposit_name"
      v-bind:type_id="item.type_id"
      v-bind:type="item.type"
      v-on:deposit-edited="onEdit"
      v-on:deposit-deleted="onDeleted"
    />
    <div class="separator"></div>
    <div class="add">
      <button
        @click="onNew"
        class="btn btn-dark btn-md btn-block btn-add"
        style="width: 150px"
      >
        <BootstrapIcon icon="plus-square-fill" />
        Добавить
      </button>
    </div>
    <div class="separator"></div>
    <Paginator
      v-bind:count="totalItems"
      v-bind:ipp="ipp"
      v-bind:currentPage="page"
      v-on:page-click="changePage"
      v-bind:autoMargin="true"
    />
  </div>
</template>

<script>
import axios from "axios";
import BootstrapIcon from "@dvuckovic/vue3-bootstrap-icons";

import NewDepositModal from "../components/NewDepositModal.vue";
import EditDepositModal from "../components/EditDepositModal.vue";
import DepositItem from "../components/DepositItem.vue";
import Paginator from "../components/Paginator.vue";
import Filter from "../components/Filter.vue";
import Spinner from "../components/Spinner.vue";
import OkModal from "./OkModal.vue";

export default {
  name: "DepositsTable",
  props: [],
  watch: {},
  data() {
    return {
      items: [],
      totalItems: 0,
      showAddNewDeposit: false,
      showEditDeposit: false,
      currentDepositId: null,
      page: 1,
      ipp: 10,
      filter: "",
      loadedItems: 0,
      showSpinner: true,
      showAuthError: false,
      authMessage: "Доступ запрещен",
      authHeader: "Ошибка безопасности",
    };
  },
  methods: {
    hideAuthMessage() {
      this.showAuthError = false;
    },
    countItems() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      var url = this.$BASE_URL + "/api/get_deposits_count/";
      axios
        .post(url, { deposit_name: this.filter }, { headers })
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.totalItems = response.data[0].result;
          } else {
            this.showAuthError = true;
          }
        });
    },
    loadItems() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      var url = this.$BASE_URL + "/api/get_deposits/";
      const offset = (this.page - 1) * this.ipp;
      axios
        .post(
          url,
          { deposit_name: this.filter, offset: offset, limit: this.ipp },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.items = response.data[0].result;
            this.loadedItems = 0;
            this.showSpinner = false;
          } else {
            this.showAuthError = true;
          }
        });
    },
    changePage(o) {
      this.page = o.page;
      this.loadItems();
    },
    onDeleted() {
      this.page = 1;
      this.filter = "";
      this.countItems();
      this.loadItems();
    },
    onEdit(o) {
      this.currentDepositId = o.deposit_id;
      this.showEditDeposit = true;
    },
    onNew() {
      this.showAddNewDeposit = true;
    },
    filterTable(filter) {
      this.page = 1;
      this.filter = filter;
      this.countItems();
      this.loadItems();
    },
    closeAddNew() {
      this.showAddNewDeposit = false;
    },
    saveNew(deposit) {
      this.showAddNewDeposit = false;
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      var url = this.$BASE_URL + "/api/add_deposit/";
      axios.post(url, deposit, { headers }).then((response) => {
        if (!response.data[0].auth_fail) {
          this.page = 1;
          this.filter = "";
          this.countItems();
          this.loadItems();
        } else {
          this.showAuthError = true;
        }
      });
    },
    updateExisting(deposit) {
      this.showEditDeposit = false;
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      var url = this.$BASE_URL + "/api/update_deposit/";
      axios.post(url, deposit, { headers }).then((response) => {
        if (!response.data[0].auth_fail) {
          this.page = 1;
          this.filter = "";
          this.items = [];
          this.countItems();
          this.loadItems();
        } else {
          this.showAuthError = true;
        }
      });
    },
    closeUpdate() {
      this.showEditDeposit = false;
    },
    onEditReservesForDeposit(o) {
      this.currentDepositId = o.deposit_id;
    },
  },
  components: {
    BootstrapIcon,
    EditDepositModal,
    NewDepositModal,
    DepositItem,
    Paginator,
    Filter,
    Spinner,
    OkModal,
  },
  mounted() {
    this.showSpinner = true;
    this.countItems();
    this.loadItems();
  },
};
</script>

<style scoped>
.table {
  margin: auto;
  width: calc(100% - 20px);
  height: calc(100% - 20px);
  border-top: none !important;
  border-bottom: none !important;
}
.separator {
  padding: 10px;
  margin-left: 10px;
  border-top: none !important;
  border-bottom: none !important;
}

.add {
  border-top: none !important;
  border-bottom: none !important;
}
</style>
