<template>
  <div>
    <div class="deposits">
      <div style="font-weight: bold; text-align: center">
        Список месторождений
      </div>
      <DepositsTable v-if="loaded" />
    </div>
  </div>
</template>

<script>
import DepositsTable from "../components/DepositsTable.vue";

export default {
  name: "Deposits",
  data() {
    return {
      loaded: true,
    };
  },
  methods: {},
  components: {
    DepositsTable,
  },
  mounted() {},
};
</script>

<style scoped>
.deposits {
  width: 100%;
  height: 100%;
  float: left;
  display: inline;
  margin-left: 0px;
  margin-right: 0px;
}
</style>
