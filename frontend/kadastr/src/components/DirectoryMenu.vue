<template>
  <div class="menu">
    <div
      v-for="(item, index) in items"
      class="menu-item"
      @click="loadDictionary(item.category)"
      v-bind:key="index"
      v-bind:class="item.selected ? 'selected-menu-item' : ''"
    >
      {{ item.description }}
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "DirectoryMenu",
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
      const url = this.$BASE_URL + "/api/get_all_dictionaries/";
      axios.get(url, { headers }).then((response) => {
        if (!response.data.auth_fail) {
          this.items = JSON.parse(JSON.stringify(response.data.result));
          var count = 0;
          for (var item of this.items) {
            if (count == 0) {
              item.selected = true;
              this.loadDictionary(item.category, item.description);
            } else {
              item.selected = false;
            }
            count++;
          }
        }
      });
    },
    loadDictionary(category) {
      for (var item of this.items) {
        if (item.category == category) {
          item.selected = true;
          this.$emit("item-clicked", item);
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
.menu {
  min-width: 100%;
  font-weight: bolder;
  height: 100%;
}

.menu-item {
  display: flex;
  justify-content: left;
  align-items: center;
  border-radius: 5px;
  min-width: calc(100% - 20px);
  height: 55px;
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
