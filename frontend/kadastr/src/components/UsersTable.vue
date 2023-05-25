<template>
  <div class="table">
    <Spinner v-if="showSpinner" />
    <EditUserModal
      v-if="showEditUser"
      v-on:cancel="closeUpdate"
      v-on:save="updateExisting"
      v-bind:user_id="currentUserId"
    />
    <OkModal
      v-if="showAuthError"
      v-bind:message="authMessage"
      v-bind:header="authHeader"
      v-on:confirm="hideAuthMessage"
    />
    <NewUserModal
      v-if="showAddNewUser"
      v-on:cancel="closeAddNew"
      v-on:save="saveNew"
    />
    <Filter v-on:filter="filterTable" v-bind:filterVal="filter" />
    <UserItem
      v-for="user in users"
      v-bind:key="user.user_id"
      v-bind:user_id="user.user_id"
      v-bind:username="user.username"
      v-bind:role="user.role"
      v-on:user-edited="onEdit"
      v-on:user-deleted="onDeleted"
    />
    <div class="separator"></div>
    <div class="add">
      <button
        @click="onNew"
        class="btn btn-dark btn-lg btn-block"
        style="width: 300px"
      >
        <BootstrapIcon icon="plus" size="2x" />
        Добавить
      </button>
    </div>
    <div class="separator"></div>
    <Paginator
      v-bind:count="totalItems"
      v-bind:ipp="ipp"
      v-bind:currentPage="page"
      v-on:page-click="changePage"
    />
  </div>
</template>

<script>
import axios from "axios";
import BootstrapIcon from "@dvuckovic/vue3-bootstrap-icons";

import NewUserModal from "../components/NewUserModal.vue";
import EditUserModal from "../components/EditUserModal.vue";
import UserItem from "../components/UserItem.vue";
import Paginator from "../components/Paginator.vue";
import Filter from "../components/Filter.vue";
import Spinner from "../components/Spinner.vue";
import OkModal from "../components/OkModal.vue";

export default {
  name: "UsersTable",
  props: [],
  watch: {},
  data() {
    return {
      users: [],
      totalItems: 0,
      showAddNewUser: false,
      showEditUser: false,
      currentUserId: null,
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
      var url = this.$BASE_URL + "/api/get_users_count/";
      const offset = (this.page - 1) * this.ipp;
      axios
        .post(
          url,
          { username: this.filter, offset: offset, limit: this.ipp },
          { headers }
        )
        .then((response) => {
          if (!response.data.auth_fail) {
            this.totalItems = response.data.result;
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
      var url = this.$BASE_URL + "/api/get_users/";
      const offset = (this.page - 1) * this.ipp;
      axios
        .post(
          url,
          { username: this.filter, offset: offset, limit: this.ipp },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.users = response.data[0].result;
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
      this.currentUserId = o.user_id;
      this.showEditUser = true;
    },
    onNew() {
      this.showAddNewUser = true;
    },
    filterTable(filter) {
      this.filter = filter;
      this.countItems();
      this.loadItems();
    },
    closeAddNew() {
      this.showAddNewUser = false;
    },
    saveNew(user) {
      this.showAddNewUser = false;
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      var url = this.$BASE_URL + "/api/add_user/";
      axios.post(url, user, { headers }).then((response) => {
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
    updateExisting(user) {
      this.showEditUser = false;
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      var url = this.$BASE_URL + "/api/update_user/";
      axios.post(url, user, { headers }).then((response) => {
        if (!response.data[0].auth_fail) {
          this.page = 1;
          this.filter = "";
          this.items = [];
          this.countItems();
          this.loadItems();
        }
      });
    },
    closeUpdate() {
      this.showEditUser = false;
    },
  },
  components: {
    BootstrapIcon,
    NewUserModal,
    EditUserModal,
    UserItem,
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
