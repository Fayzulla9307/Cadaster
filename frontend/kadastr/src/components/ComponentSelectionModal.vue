<template>
  <div class="modal-mask">
    <div class="modal-window">
      <OkModal
        v-if="showError"
        v-bind:message="errorMessage"
        v-bind:header="errorHeader"
        v-on:confirm="hideErrorMessage"
      />
      <div class="header">{{ header }}</div>
      <div class="message">
        <div class="form-group col-xs-3">
          <label style="float: left"
            >Полезные ископаемые доступные для месторождения</label
          >
          <select
            class="form-select form-control-lg"
            v-model="selectedComponentId"
            aria-label="Полезные ископаемые доступные для месторождения"
          >
            <option
              v-for="c in components"
              v-bind:value="c.component_id"
              v-bind:key="c.component_id"
            >
              {{ c.component_name }}
            </option>
          </select>
        </div>
      </div>
      <button @click="confirm" class="btn btn-dark btn-lg btn-block next">
        Далее
      </button>
      <button @click="cancel" class="btn btn-dark btn-lg btn-block close">
        Отменить
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import OkModal from "../components/OkModal.vue";

export default {
  name: "ComponentSelectionModal",
  props: ["deposit_id", "mine_area_id"],
  data() {
    return {
      components: [],
      header: "Выбор полезного ископаемого",
      selectedComponentId: null,
      showError: false,
      errorMessage:
        "Для данного месторождения отсутствуют записи по полезным ископаемым! Вам стоит выбрать полезное ископаемое или отменить действия мастера!",
      errorHeader: "Нет данных по полезным ископаемым",
    };
  },
  methods: {
    hideErrorMessage() {
      this.getAllComponents();
    },
    getAllComponents() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/get_dictionary_contents/";
      axios
        .post(
          url,
          { category: "SPR_POL", offset: 0, limit: 10000 },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            var result = response.data[0].result;
            this.components = [];
            for (var i = 0; i < result.length; i++) {
              this.components.push({
                deposit_id: this.deposit_id,
                mine_area_id: this.mine_area_id,
                component_id: result[i].id,
                component_name: result[i].description,
              });
            }
            this.showError = false;
          }
        });
    },
    getComponentsForDeposit() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/get_available_components_for_deposit/";
      axios
        .post(
          url,
          { deposit_id: this.deposit_id, mine_area_id: this.mine_area_id },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.components = response.data[0].result;
            if (this.components.length == 0) {
              this.showError = true;
            }
          }
        });
    },
    cancel() {
      this.$emit("cancel", {});
    },
    confirm() {
      if (this.selectedComponentId == null) {
        this.errorHeader = "Ошибка при вводе данных";
        this.errorMessage = "Не выбрано полезное ископаемое!";
        this.showError = true;
      } else {
        this.$emit("confirm", {
          deposit_id: this.deposit_id,
          mine_area_id: this.mine_area_id,
          component_id: this.selectedComponentId,
        });
      }
    },
  },
  components: {
    OkModal,
  },
  mounted() {
    this.getAllComponents();
  },
};
</script>

<style scoped>
.modal-mask {
  position: fixed;
  z-index: 1000094;
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
  width: 400px;
  height: 200px;
  top: 50%;
  left: 50%;
  margin-top: -100px;
  margin-left: -200px;
  z-index: 1000095;
}

.header {
  height: 30px;
  width: 100%;
  background-color: rgb(143, 150, 150);
  text-align: center;
  font-weight: bold;
}

.message {
  font-weight: bolder;
  color: black;
  text-align: center;
}

.close {
  position: absolute;
  bottom: 10px;
  left: 10px;
}

.next {
  position: absolute;
  bottom: 10px;
  right: 10px;
}
</style>
