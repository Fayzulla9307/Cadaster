<template>
  <div>
    <div class="menu">
      <DirectoryMenu v-on:item-clicked="menuItemClicked" />
    </div>
    <div class="props">
      <div style="font-weight: bold; text-align: center">
        Справочные данные: {{ description }}
      </div>
      <PropertyTable v-if="loaded" v-bind:category="category" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import PropertyTable from "../components/PropertyTable.vue";
import DirectoryMenu from "../components/DirectoryMenu.vue";

export default {
  name: "Dicts",
  data() {
    return {
      loaded: false,
      category: null,
      description: "",
    };
  },
  methods: {
    getAllCategories() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      axios
        .get(this.$BASE_URL + "/api/get_all_dictionaries/", { headers })
        .then((response) => {
          console.log(!response.data.auth_fail);
          if (!response.data.auth_fail) {
            this.loaded = true;
            this.category = "SPR_ED_IZM";
            console.log("Dictionaries loaded");
          }
        });
    },
    menuItemClicked(item) {
      this.category = item.category;
      this.description = item.description;
    },
  },
  components: {
    PropertyTable,
    DirectoryMenu,
  },
  mounted() {
    this.getAllCategories();
  },
};
</script>

<style scoped>
.menu {
  width: 30%;
  height: 100%;
  float: left;
  display: inline;
  margin-left: 10px;
}
.props {
  width: calc(70% - 20px);
  height: 100%;
  float: right;
  display: inline;
  margin-right: 10px;
}
</style>
