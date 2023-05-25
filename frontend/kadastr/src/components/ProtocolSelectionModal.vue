<template>
  <div class="modal-mask">
    <div class="modal-window">
      <Spinner v-if="showSpinner" />
      <div class="header">Выбор месторождения</div>
      <div class="body">
        <DepositTable v-on:confirm="confirm" v-on:loaded="onLoaded" />
      </div>
      <button @click="cancel" class="btn btn-dark btn-lg btn-block cancel">
        Отменить
      </button>
    </div>
  </div>
</template>

<script>
import DepositTable from "../components/DepositTable.vue";
import Spinner from "../components/Spinner.vue";

export default {
  name: "ProtocolSelectionModal",
  props: [],
  data() {
    return {
      showSpinner: true,
    };
  },
  methods: {
    onLoaded() {
      this.showSpinner = false;
    },
    confirm(data) {
      this.$emit("confirm", {
        deposit_id: data.deposit_id,
        mine_area_id: data.mine_area_id,
      });
    },
    cancel() {
      this.$emit("cancel", {});
    },
  },
  components: {
    Spinner,
    DepositTable,
  },
  mounted() {},
};
</script>

<style scoped>
.modal-mask {
  position: fixed;
  z-index: 1000092;
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
  width: calc(80%);
  height: calc(90%);
  left: 10%;
  z-index: 1000093;
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

.confirm {
  position: absolute;
  bottom: 10px;
  left: 10px;
}

.add {
  position: absolute;
  bottom: 10px;
  left: calc(50% - 50px);
}

.cancel {
  position: absolute;
  bottom: 10px;
  right: 10px;
}
</style>
