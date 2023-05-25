<template>
  <div class="main">
    <ProtocolSelectionModal
      v-if="showDepositSelectionTable"
      v-on:cancel="closeObjectSelectionWindow"
      v-on:confirm="selectDeposit"
    />
    <ProtocolEditModal
      v-bind:deposit_id="deposit_id"
      v-bind:mine_area_id="mine_area_id"
      v-bind:component_id="component_id"
      v-if="showEditModal"
      v-on:reselect="showDepositSelection"
    />
    <ComponentSelectionModal
      v-if="showComponentSelectionModal"
      v-bind:deposit_id="deposit_id"
      v-bind:mine_area_id="mine_area_id"
      v-on:confirm="selectComponent"
      v-on:cancel="closeAllWindows"
    />
    <div class="instrument">
      Данный инструмент представляет возможность заполнения информации
      обобъекте. Для запуска мастера нажмите на кнопку: <br />
      <button
        @click="selectProtocol"
        class="btn btn-dark btn-lg btn-block close"
      >
        Запустить мастер заполнения протокола?
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ProtocolSelectionModal from "../components/ProtocolSelectionModal.vue";
import ProtocolEditModal from "../components/ProtocolEditModal.vue";
import ComponentSelectionModal from "../components/ComponentSelectionModal.vue";

export default {
  name: "Protocols",
  data() {
    return {
      showDepositSelectionTable: false,
      showComponentSelectionModal: false,
      showEditModal: false,
      depositName: "",
      deposit_id: null,
      mine_area_id: null,
    };
  },
  methods: {
    closeAllWindows() {
      this.showEditModal = false;
      this.showDepositSelectionTable = false;
      this.showComponentSelectionModal = false;
    },
    selectProtocol() {
      this.showDepositSelectionTable = true;
    },
    showDepositSelection() {
      this.showEditModal = false;
      this.showDepositSelectionTable = true;
    },
    closeObjectSelectionWindow() {
      this.showDepositSelectionTable = false;
    },
    selectDeposit(data) {
      this.deposit_id = data.deposit_id;
      this.mine_area_id = data.mine_area_id;
      this.showDepositSelectionTable = false;
      this.showComponentSelectionModal = true;
    },
    selectComponent(data) {
      this.component_id = data.component_id;
      this.showComponentSelectionModal = false;
      this.showEditModal = true;
    },
    getDepositInfo() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/get_deposit/";
      axios
        .post(url, { deposit_id: this.deposit_id }, { headers })
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.depositName = response.data[0].result.deposit_name;
          }
        });
    },
  },
  components: {
    ProtocolSelectionModal,
    ProtocolEditModal,
    ComponentSelectionModal,
  },
  mounted() {},
};
</script>

<style scoped>
h3 {
  color: black;
  text-align: center;
}

.instrument {
  text-align: justify;
  position: absolute;
  width: 300px;
  height: 300px;
  top: calc(50% - 150px);
  left: calc(50% - 150px);
}

.main {
  /*position: absolute;*/

  /* Center form on page horizontally & vertically */
  height: 100%;
  width: calc(90%);
  margin: auto;

  font-weight: bolder;
  font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS", sans-serif;
  border-style: none !important;
  border-top: none !important;
  border-bottom: none !important;
  margin-bottom: 30px !important;
  padding-bottom: 30px !important;
}
</style>
