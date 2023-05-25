<template>
  <div>
    <Filter v-on:filter="filterTable" v-bind:filterVal="filter" />
    <table style="border-style: none !important; width: 100%">
      <tr
        style="border-style: none !important; width: 100%"
        v-for="item in items"
        v-bind:key="item.deposit_id + '_' + item.mine_area_id"
      >
        <td style="border-style: none !important">
          <button
            @click="select(item.deposit_id, item.mine_area_id)"
            class="btn btn-dark btn-lg btn-block"
          >
            <BootstrapIcon icon="pencil" />
          </button>
        </td>
        <td style="width: 100%">
          <input
            type="text"
            class="form-control form-control-lg"
            style="display: inline; width: calc(100"
            v-model="item.description"
            disabled
          />
        </td>
      </tr>
    </table>
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

import Filter from "../components/Filter.vue";
import Paginator from "../components/Paginator.vue";

export default {
  name: "DepositTable",
  props: [],
  data() {
    return {
      ipp: 10,
      totalItems: 0,
      page: 1,
      filter: "",
      items: [],
    };
  },
  methods: {
    select(depositId, mineAreaId) {
      this.$emit("confirm", {
        deposit_id: depositId,
        mine_area_id: mineAreaId,
      });
    },
    confirm() {
      this.$emit("confirm", {
        deposit_id: this.depositId,
        mine_area_id: this.mineAreaId,
      });
    },
    cancel() {
      this.$emit("cancel", {});
    },
    countDeposits() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/get_deposits_incl_mine_areas_count/";
      axios
        .post(
          url,
          { deposit_name: this.filter, offset: 0, limit: 10 },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.totalItems = response.data[0].result;
            this.loadDeposits();
          }
        });
    },
    loadDeposits() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/get_deposits_and_mine_areas/";
      const offset = (this.page - 1) * this.ipp;
      axios
        .post(
          url,
          { deposit_name: this.filter, offset: offset, limit: 10 },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.items = JSON.parse(JSON.stringify(response.data[0].result));
            for (var i = 0; i < this.items.length; i++) {
              if (this.items[i].deposit_id == this.items[i].mine_area_id) {
                this.items[i].description = this.items[i].deposit_name;
              } else {
                this.items[i].description =
                  this.items[i].deposit_name +
                  ", " +
                  this.items[i].mine_area_name;
              }
            }
            this.$emit("loaded");
          }
        });
    },
    changePage(o) {
      this.page = o.page;
      this.showSpinner = true;
      this.loadDeposits();
    },
    filterTable(filter) {
      this.page = 1;
      this.filter = filter;
      this.showSpinner = true;
      this.countDeposits();
    },
  },
  components: {
    BootstrapIcon,
    Paginator,
    Filter,
  },
  mounted() {
    this.countDeposits();
  },
};
</script>

<style scoped>
.message {
  font-weight: bolder;
  color: black;
  text-align: center;
}

.confirm {
  position: absolute;
  bottom: 10px;
  left: 10px;
}

.cancel {
  position: absolute;
  bottom: 10px;
  right: 10px;
}

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

.select {
  float: left;
}

.deposit {
  width: calc(100% - 50px);
  float: left;
}
</style>
