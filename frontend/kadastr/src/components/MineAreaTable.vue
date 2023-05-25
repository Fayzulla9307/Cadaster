<template>
  <div class="table">
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
    <NewMineAreaModal
      v-if="showAddNewMineArea"
      v-bind:deposit_id="deposit_id"
      v-on:cancel="closeAddNew"
      v-on:save="saveNew"
    />
    <MineAreaItem
      v-for="item in items"
      v-bind:key="item.mine_area_name"
      v-bind:deposit_id="item.deposit_id"
      v-bind:mine_area_id="item.mine_area_id"
      v-bind:mine_area_name="item.mine_area_name"
      v-on:mine-area-edited="onEdit"
      v-on:mine-area-deleted="onDeleted"
      v-on:reserves-edited-for-mine-area="onEditReservesForMineArea"
    />
    <div>
      <button
        @click="onNew"
        class="btn btn-dark btn-lg btn-block"
        style="float: left; width: 300px"
      >
        <BootstrapIcon icon="database-add" size="2x" />
        Добавить участок
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import BootstrapIcon from "@dvuckovic/vue3-bootstrap-icons";
import OkModal from "../components/OkModal.vue";
import NewMineAreaModal from "../components/NewMineAreaModal.vue";
import MineAreaItem from "../components/MineAreaItem.vue";

export default {
  name: "MineAreaTable",
  props: ["deposit_id", "deposit_name"],
  watch: {},
  data() {
    return {
      items: [],
      totalItems: 0,
      showAddNewMineArea: false,
      showEditDeposit: false,
      currentDepositId: null,
      showError: false,
      errorMessage: "",
      header: "Невозможно сохранить запись",
      showAuthError: false,
      authMessage: "Доступ запрещен",
      authHeader: "Ошибка безопасности",
    };
  },
  methods: {
    hideAuthMessage() {
      this.showAuthError = false;
    },
    loadItems() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      var url = this.$BASE_URL + "/api/get_mine_areas/";
      axios
        .post(
          url,
          { deposit_id: this.deposit_id, offset: 0, limit: 10000 },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.items = response.data[0].result;
          }
        });
    },
    hideErrorMessage() {
      this.showError = false;
    },
    onDeleted() {
      this.loadItems();
    },
    onEdit() {
      this.loadItems();
    },
    onNew() {
      this.showAddNewMineArea = true;
    },
    closeAddNew() {
      this.showAddNewMineArea = false;
    },
    saveNew(mineArea) {
      this.showAddNewMineArea = false;
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      var url = this.$BASE_URL + "/api/add_mine_area/";
      axios.post(url, mineArea, { headers }).then((response) => {
        console.log(JSON.stringify(response.data));
        if (!response.data[0].auth_fail) {
          if (!response.data[0].result) {
            this.errorMessage = response.data[0].reason;
            this.showError = true;
          } else {
            this.loadItems();
          }
        } else {
          this.showAuthError = true;
        }
      });
    },
  },
  components: {
    NewMineAreaModal,
    MineAreaItem,
    OkModal,
    BootstrapIcon,
  },
  mounted() {
    this.loadItems();
  },
};
</script>

<style scoped>
.table {
  width: 100%;
  height: 100%;
}

.modal-mask {
  position: fixed;
  z-index: 9997;
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
  width: 100%;
  height: 100%;
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
</style>
