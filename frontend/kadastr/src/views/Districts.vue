<template>
  <div>
    <div class="nav-menu-container">
      <AreaMenu v-on:area-clicked="menuItemClicked" />
    </div>
    <div class="props">
      <div style="font-weight: bold; text-align: center">
        Спаравочник районов: {{ area_name }}
      </div>
      <DistrictTable v-if="loaded" v-bind:id_area="id_area" />
    </div>
  </div>
</template>

<script>
import DistrictTable from "../components/DistrictTable.vue";
import AreaMenu from "../components/AreaMenu.vue";

export default {
  name: "Districts",
  data() {
    return {
      loaded: false,
      id_republic: 1,
      id_area: 1,
      area_name: "",
    };
  },
  methods: {
    menuItemClicked(item) {
      this.loaded = true;
      this.id_republic = item.id_republic;
      this.id_area = item.id_area;
      this.area_name = item.area_name;
    },
  },
  components: {
    DistrictTable,
    AreaMenu,
  },
  mounted() {},
};
</script>

<style scoped>
.nav-menu-container {
  width: 25%;
  height: 100%;
  float: left;
  display: inline;
  margin-left: 10px;
}
.props {
  width: calc(70% - 20px);
  height: 100%;
  float: left;
  display: inline;
  margin-right: 10px;
}
</style>
