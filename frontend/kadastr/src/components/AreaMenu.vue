<template>
  <div class="nav-menu">
    <div
      v-for="(item, index) in items"
      class="menu-item"
      @click="loadArea(item.id_republic, item.id_area)"
      v-bind:key="index"
      v-bind:class="item.selected ? 'selected-menu-item' : ''"
    >
      {{ item.area_name }}
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AreaMenu",
  props: [],
  watch: {},
  data() {
    return {
      items: [],
    };
  },
  methods: {
    loadMenu() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/get_areas/";
      axios
        .post(url, { offset: 0, limit: 100 }, { headers })
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.items = JSON.parse(JSON.stringify(response.data[0].result));
            var count = 0;
            for (var item of this.items) {
              if (count == 0) {
                item.selected = true;
                this.loadArea(item.id_republic, item.id_area);
              } else {
                item.selected = false;
              }
              count++;
            }
          }
        });
    },
    loadArea(id_republic, id_area) {
      for (var item of this.items) {
        if (item.id_area == id_area && item.id_republic == id_republic) {
          item.selected = true;
          this.$emit("area-clicked", item);
        } else {
          item.selected = false;
        }
      }
    },
  },
  components: {},
  mounted() {
    this.loadMenu();
  },
};
</script>

<style scoped>


.nav-menu {
  width: 85%;
  height: 100%;
  float: left;
  display: inline;
  margin-left: 10px;
}

.menu-item {
  display: flex;
  justify-content: left;
  align-items: center;
  border-radius: 5px;
  min-width: calc(100% - 250px);
  height: 48px;
  color: #fff;
  background-color: #372d69;
  font-weight: bold;
  margin-right: 20px;
  margin-bottom: 8px;
  padding-left: 20px;
}

.menu-item:hover {
  background-color: #23185b;
  cursor: pointer;
}

.selected-menu-item {
  background-color: #23185b;
  color: #fff9a4;
}
</style>
