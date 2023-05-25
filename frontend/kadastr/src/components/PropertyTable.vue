<template>
  <div class="table">
    <Spinner v-if="showSpinner" />
    <Filter v-on:filter="filterTable" v-bind:filterVal="filter" />
    <PropertyItem
      v-for="item in items"
      v-bind:key="item.id"
      v-bind:displayButtons="true"
      v-bind:id="item.id"
      v-bind:category="item.category"
      v-bind:description="item.description"
      v-on:updated="updated"
      v-on:loaded="onItemLoaded"
    />
    <ProperyNewItem v-bind:category="categoryLocal" v-on:updated="updated" />
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
import PropertyItem from "../components/PropertyItem.vue";
import ProperyNewItem from "../components/PropertyNewItem.vue";
import Paginator from "../components/Paginator.vue";
import Filter from "../components/Filter.vue";
import Spinner from "../components/Spinner.vue";

export default {
  name: "PropertyTable",
  props: ["category"],
  watch: {
    category: {
      deep: true,
      handler(n) {
        this.categoryLocal = n;
        this.page = 1;
        this.countItems();
        this.loadItems();
      },
    },
  },
  data() {
    return {
      items: [],
      categoryLocal: this.category,
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
      var url = this.$BASE_URL + "/api/get_dictionary_count/";
      axios
        .post(
          url,
          { category: this.categoryLocal, item: this.filter },
          { headers }
        )
        .then((response) => {
          if (!response.data.auth_fail) {
            this.totalItems = response.data.result;
          }
        });
    },
    loadItems() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      var url = this.$BASE_URL + "/api/get_dictionary_contents/";
      const offset = (this.page - 1) * this.ipp;
      axios
        .post(
          url,
          {
            category: this.categoryLocal,
            item: this.filter,
            offset: offset,
            limit: this.ipp,
          },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            console.log(JSON.stringify(response.data[0].result));
            this.items = response.data[0].result;
          }
        });
    },
    onItemLoaded() {
      this.loadedItems++;
      //alert(this.totalItems + " " + this.loadedItems)
      if (this.loadedItems == this.ipp) {
        this.loadedItems = 0;
        this.showSpinner = false;
      }
      if (
        this.loadedItems == 0 &&
        this.totalItems - this.ipp * Math.floor(this.totalItems / this.ipp)
      ) {
        this.loadedItems = 0;
        this.showSpinner = false;
      }
      if (this.loadedItems == this.totalItems) {
        this.loadedItems = 0;
        this.showSpinner = false;
      }
    },
    changePage(o) {
      this.page = o.page;
      this.loadItems();
    },
    updated() {
      this.page = 1;
      this.filter = "";
      this.countItems();
      this.loadItems();
    },
    filterTable(filter) {
      this.page = 1;
      this.filter = filter;
      this.countItems();
      this.loadItems();
    },
  },
  components: {
    PropertyItem,
    ProperyNewItem,
    Paginator,
    Filter,
    Spinner,
  },
  mounted() {
    this.countItems();
    this.loadItems();
  },
};
</script>

<style scoped>
.table {
  width: 100%;
  height: 100%;
}
</style>
