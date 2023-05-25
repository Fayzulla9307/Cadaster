<template>
  <div class="modal-mask">
    <div class="modal-window">
      <div class="header">Добавление нового участка</div>
      <div class="body">
        <form>
          <div class="form-group">
            <label>Область</label>
            <select
              class="form-select"
              v-model="selectedAreaId"
              aria-label="Область"
              @change="changeArea"
              disabled="true"
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
              disabled="true"
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
            <label>Наименование участка</label>
            <input
              type="text"
              class="form-control form-control-lg"
              v-model="mineAreaName"
            />
          </div>
          <div class="form-group">
            <label>Описание участка</label>
            <textarea
              class="form-control form-control-lg"
              v-model="mineAreaDesc"
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

export default {
  name: "NewMineAreaModal",
  props: ["deposit_id"],
  data() {
    return {
      areas: [],
      districts: [],
      devs: [],
      failed: false,
      parentAreaId: null,
      parentDistrictId: null,
      selectedDistrictId: this.deposit_id,
      selectedAreaId: null,
      selectedDevType: null,
      mineAreaName: "",
      mineAreaDesc: "",
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
          if (!response.data.auth_fail) {
            let deposit = response.data.result;
            this.parentAreaId = deposit.area_id;
            this.parentDistrictId = deposit.district_id;
            this.getAreas();
            //this.selectedAreaId = response.data.result.area_id;
            //this.selectedDistrictId = response.data.result;
          }
        });
    },
    save(e) {
      this.$emit("save", {
        deposit_id: this.deposit_id,
        mine_area_name: this.mineAreaName,
        description: this.mineAreaDesc,
        dev_id: this.selectedDevType,
        area_id: this.selectedAreaId,
        district_id: this.selectedDistrictId,
      });
      e.preventDefault();
    },
    cancel(e) {
      this.$emit("cancel", {});
      e.preventDefault();
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
          if (!response.data.auth_fail) {
            this.areas = response.data.result;
            this.selectedAreaId = this.parentAreaId;
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
          if (!response.data.auth_fail) {
            this.districts = response.data.result;
            if (response.data.result.length > 0) {
              this.selectedDistrictId = this.parentDistrictId;
            }
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
          if (!response.data.auth_fail) {
            this.devs = response.data.result;
            if (response.data.result.length > 0) {
              this.selectedDevType = response.data.result[0].id;
            }
          }
        });
    },
    changeArea() {
      this.getDistricts();
    },
  },
  mounted() {
    this.getDepositInfo();
    this.getDevelopmentStatuses();
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
  height: 500px;
  top: 50%;
  left: 50%;
  margin-top: -250px;
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
