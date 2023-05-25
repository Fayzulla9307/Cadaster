<template>
  <div class="modal-mask">
    <OkModal
      v-if="showAuthError"
      v-bind:message="authMessage"
      v-bind:header="authHeader"
      v-on:confirm="hideAuthMessage"
    />
    <div class="modal-window">
      <div class="header">Редактирование существующего месторождения</div>
      <div class="body">
        <form class="login-form">
          <div class="form-group">
            <label>Область</label>
            <select
              class="form-select"
              v-model="selectedAreaId"
              aria-label="Область"
              @change="changeArea"
            >
              <option
                v-for="area in areas"
                v-bind:value="area.id_area"
                v-bind:key="area.id_area"
              >
                {{ area.area_name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Район</label>
            <select
              class="form-select"
              v-model="selectedDistrictId"
              aria-label="Район"
            >
              <option
                v-for="district in districts"
                v-bind:value="district.id_district"
                v-bind:key="district.id_district"
              >
                {{ district.district_name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Степень освоения</label>
            <select
              class="form-select"
              v-model="selectedDevType"
              aria-label="Степень освоения"
            >
              <option
                v-for="dev in devs"
                v-bind:value="dev.id"
                v-bind:key="dev.id"
              >
                {{ dev.description }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Тип месторождения</label>
            <select
              class="form-select"
              v-model="selectedDepositTypeId"
              aria-label="Тип месторождения"
              disabled
            >
              <option
                v-for="type in types"
                v-bind:value="type.id"
                v-bind:key="type.id"
              >
                {{ type.type }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Наименование месторождения</label>
            <input
              type="text"
              class="form-control form-control-lg"
              v-model="depositName"
            />
          </div>
          <div class="form-group">
            <label>Описание месторождения</label>
            <textarea
              class="form-control form-control-lg"
              v-model="depositDesc"
            ></textarea>
          </div>
          <div class="form-group" style="margin-top: 10px">
            <button @click="save" class="btn btn-dark btn-lg btn-block save">
              Сохранить
            </button>
            <button @click="cancel" class="btn btn-dark btn-lg btn-block close">
              Отменить
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import OkModal from "./OkModal.vue";

export default {
  name: "EditDepositModal",
  props: ["deposit_id"],
  data() {
    return {
      areas: [],
      districts: [],
      devs: [],
      types: [],
      failed: false,
      depositId: this.deposit_id,
      selectedDistrictId: null,
      selectedAreaId: null,
      selectedDevType: null,
      depositName: "",
      depositDesc: "",
      showAuthError: false,
      authMessage: "Доступ запрещен",
      authHeader: "Ошибка безопасности",
      selectedDepositTypeId: null,
    };
  },
  methods: {
    hideAuthMessage() {
      this.showAuthError = false;
    },
    save(e) {
      this.$emit("save", {
        deposit_id: this.depositId,
        deposit_name: this.depositName,
        description: this.depositDesc,
        development_id: this.selectedDevType,
        area_id: this.selectedAreaId,
        district_id: this.selectedDistrictId,
        type_id: this.selectedDepositTypeId,
      });
      e.preventDefault();
    },
    cancel(e) {
      this.$emit("cancel", {});
      e.preventDefault();
    },
    getDeposit() {
      //get_deposit
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      var url = this.$BASE_URL + "/api/get_deposit/";
      axios
        .post(url, { deposit_id: this.depositId }, { headers })
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.selectedAreaId = response.data[0].result.area_id;
            this.selectedDistrictId = response.data[0].result.district_id;
            this.selectedDevType = response.data[0].result.dev_id;
            this.depositName = response.data[0].result.deposit_name;
            this.depositDesc = response.data[0].result.description;
            this.selectedDepositTypeId = response.data[0].result.type_id;
            this.getAreas();
            this.getDevelopmentStatuses();
            this.getDepositTypes();
          }
        });
    },
    getAreas() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      var url = this.$BASE_URL + "/api/get_areas/";
      axios
        .post(url, { offset: 0, limit: 20 }, { headers })
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.areas = response.data[0].result;
            this.getDistricts();
          }
        });
    },
    getDistricts() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      var url = this.$BASE_URL + "/api/get_districts/";
      axios
        .post(
          url,
          { id_area: this.selectedAreaId, offset: 0, limit: 1000 },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.districts = response.data[0].result;
          }
        });
    },
    getDepositTypes() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      var url = this.$BASE_URL + "/api/get_deposit_types/";
      axios.post(url, {}, { headers }).then((response) => {
        if (!response.data[0].auth_fail) {
          this.types = response.data[0].result;
        }
      });
    },
    getDevelopmentStatuses() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      var url = this.$BASE_URL + "/api/get_dictionary_contents/";
      axios
        .post(
          url,
          { category: "SPR_OSV", offset: 0, limit: 10000 },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.devs = response.data[0].result;
          }
        });
    },
    changeArea() {
      this.getDistricts();
    },
  },
  mounted() {
    this.getDeposit();
  },
  components: {
    OkModal,
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
  width: 500px;
  height: 600px;
  top: 50%;
  left: 50%;
  margin-top: -300px;
  margin-left: -250px;
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
