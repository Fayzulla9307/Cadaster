<template>
  <div class="modal-mask">
    <div class="modal-window">
      <div class="header">Участки месторождения {{ deposit.deposit_name }}</div>
      <div class="body">
        <MineAreaTable
          v-bind:deposit_id="deposit_id"
          v-bind:deposit_name="deposit.deposit_name"
        />
        <div class="form-group" style="margin-top: 10px">
          <button @click="close" class="btn btn-dark btn-lg btn-block close">
            Закрыть
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import MineAreaTable from "../components/MineAreaTable.vue";

export default {
  name: "MineAreaModal",
  props: ["deposit_id"],
  data() {
    return {
      deposit: {
        deposit_name: "",
      },
    };
  },
  methods: {
    getDepositInfo() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      var url = this.$BASE_URL + "/api/get_deposit/";
      axios
        .post(url, { deposit_id: this.deposit_id }, { headers })
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.deposit = response.data[0].result;
          }
        });
    },
    close(e) {
      this.$emit("mine-areas-close", {});
      e.preventDefault();
    },
  },
  mounted() {
    this.getDepositInfo();
  },
  components: {
    MineAreaTable,
  },
};
</script>

<style scoped>
.modal-mask {
  position: fixed;
  z-index: 9998;
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
  width: calc(100%);
  height: calc(100%);
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

.close {
  position: absolute;
  bottom: 10px;
  right: 10px;
}

.save {
  position: absolute;
  bottom: 10px;
  left: 10px;
}
</style>
