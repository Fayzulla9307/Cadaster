<template>
  <div class="table">
    <Spinner v-if="showSpinner" />
    <Filter v-on:filter="filterTable" v-bind:filterVal="filter" />
    <DistrictItem
      v-for="item in items"
      v-bind:key="item.id_district + '_' + item.id_area"
      v-bind:id="item.id_district + '_' + item.id_area"
      v-bind:displayButtons="true"
      v-bind:id_republic="1"
      v-bind:id_area="item.id_area"
      v-bind:id_district="item.id_district"
      v-bind:district_name="item.district_name"
      v-on:district-updated="updated"
    />
    <DistrictNewItem
      v-bind:id_area="areaIdLocal"
      v-on:district-updated="added"
    />
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
import DistrictItem from "../components/DistrictItem.vue";
import DistrictNewItem from "../components/DistrictNewItem.vue";
import Paginator from "../components/Paginator.vue";
import Filter from "../components/Filter.vue";
import Spinner from "../components/Spinner.vue";

export default {
  name: "DistrictTable",
  props: ["id_area"],
  watch: {
    id_area: {
      deep: true,
      handler(n) {
        this.page = 1;
        this.showSpinner = true;
        this.areaIdLocal = n;
        console.log(this.areaIdLocal);
        this.countItems();
        //this.loadItems();
      },
    },
  },
  data() {
    return {
      items: [],
      areaIdLocal: this.id_area,
      totalItems: 0,
      page: 1,
      ipp: 10,
      filter: "",
      loadedItems: 0,
      showSpinner: true,
    };
  },
  methods: {
    countItems() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      var url = this.$BASE_URL + "/api/get_district_count/";
      axios
        .post(
          url,
          { area_id: this.areaIdLocal, district_name: this.filter },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.totalItems = response.data[0].result;
            console.log(this.totalItems);
            this.loadItems();
          }
        });
    },
    loadItems() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      var url = this.$BASE_URL + "/api/get_districts/";
      const offset = (this.page - 1) * this.ipp;
      console.log({
        id_area: this.areaIdLocal,
        district_name: this.filter,
        offset: offset,
        limit: this.ipp,
      });
      axios
        .post(
          url,
          {
            id_area: this.areaIdLocal,
            district_name: this.filter,
            offset: offset,
            limit: this.ipp,
          },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.items = response.data[0].result;
            this.loadedItems = 0;
            this.showSpinner = false;
          }
        });
    },
    changePage(o) {
      this.page = o.page;
      this.countItems();
      //this.loadItems();
    },
    added() {
      this.page = 1;
      this.filter = "";
      this.countItems();
    },
    updated() {
      this.filter = "";
      this.countItems();
      //this.loadItems();
    },
    filterTable(filter) {
      this.page = 1;
      this.filter = filter;
      this.countItems();
      //this.loadItems();
    },
  },
  components: {
    DistrictItem,
    DistrictNewItem,
    Paginator,
    Filter,
    Spinner,
  },
  mounted() {
    this.page = 1;
    this.countItems();
    //this.loadItems();
  },
};
</script>

<style scoped>
.table {
  width: 100%;
  height: 100%;
}
</style>
