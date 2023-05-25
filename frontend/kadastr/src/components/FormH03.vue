<template>
  <div>
    Hello
  </div>
</template>
<script>
import axios from "axios";
    export default {
  name: "FormH03",
  props: ["deposit_id", "mine_area_id", "component_id"],
  data() {
    return {
      description: "",
      selected_H01: false,
      selected_H02: false,
      selected_H03: true,
      depositInfo: {},
      mineAreaInfo: {},
      dev: "",
      depositDesc: this.description,
      district: "",
      area: "",
    };
  },
  methods: {
    selectTab(tab) {
        if (tab == "H03") {
        this.selected_title = false;
        this.selected_H01 = false;
        this.selected_H02 = false;
        this.selected_H03 = true;
        this.selected_H04 = false;
        this.selected_H05 = false;
        this.selected_H06 = false;
        this.selected_H07 = false;
        this.selected_H08 = false;
        this.selected_H0910 = false;
        this.selected_H11 = false;
        this.selected_H12 = false;
        this.selected_H13 = false;
      }
    },
    selectDeposit() {
      this.$emit("reselect", {});
    },
    getArea(id) {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/get_area/";
      axios.post(url, { id_area: id }, { headers }).then((response) => {
        if (!response.data[0].auth_fail) {
          this.area = response.data[0].result.area_name;
        }
      });
    },
    getDistrict(id_area, id_district) {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/get_district/";
      axios
        .post(url, { id_area: id_area, id_district: id_district }, { headers })
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.district = response.data[0].result.district_name;
          }
        });
    },
    getComponent() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/get_dictionary_item_description/";
      axios
        .post(url, { id: this.component_id }, { headers })
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.component = response.data[0].result.description;
          }
        });
    },
    getLandTypes() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/get_dictionary_contents/";
      axios
        .post(
          url,
          { category: "SPR_TIP_ZEMEL", limit: 10000, offset: 0 },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.land_type = response.data[0].result;
          }
        });
    },
    getReliefType() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/get_dictionary_contents/";
      axios
        .post(
          url,
          { category: "SPR_TIP_RELEFA", limit: 10000, offset: 0 },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.relief = response.data[0].result;
          }
        });
    },
    getAvalanchType() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/get_dictionary_contents/";
      axios
        .post(
          url,
          { category: "SPR_OPOLZNEOPASNOST", limit: 10000, offset: 0 },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.avalanch_score = response.data[0].result;
          }
        });
    },
    getMudflowType() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/get_dictionary_contents/";
      axios
        .post(
          url,
          { category: "SPR_SELEOPASNOST", limit: 10000, offset: 0 },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.drought_score = response.data[0].result;
          }
        });
    },
    getOrganizations() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/get_dictionary_contents/";
      axios
        .post(
          url,
          { category: "SPR_VED", limit: 10000, offset: 0 },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.organizations = response.data[0].result;
          }
        });
    },
    getDevStatus(id) {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/get_dictionary_item_description/";
      axios.post(url, { id: id }, { headers }).then((response) => {
        if (!response.data[0].auth_fail) {
          this.dev = response.data[0].result.description;
        }
      });
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
            //alert(JSON.stringify(response.data[0]))
            if (this.deposit_id == this.mine_area_id) {
              this.description = response.data[0].result.deposit_name;
              this.deposit = response.data[0].result.deposit_name;
              this.mineArea = "-";
              this.depositInfo = response.data[0].result;
              this.getDevStatus(this.depositInfo.dev_id);
              this.getArea(this.depositInfo.area_id);
              this.getDistrict(
                this.depositInfo.area_id,
                this.depositInfo.district_id
              );
              this.saveOrUpdateProtocol();
            } else {
              this.description = response.data[0].result.deposit_name;
              this.deposit = response.data[0].result.deposit_name;
              this.depositInfo = response.data[0].result;
              this.getMineAreaInfo();
            }
          }
        });
    },
    getMineAreaInfo() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/get_mine_area/";
      axios
        .post(
          url,
          { deposit_id: this.deposit_id, mine_area_id: this.mine_area_id },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            //alert(JSON.stringify(response.data[0].result))
            this.description += ", " + response.data[0].result.mine_area_name;
            this.mineArea = response.data[0].result.mine_area_name;
            this.mineAreaInfo = response.data[0].result;
            this.getDevStatus(this.mineAreaInfo.dev_id);
            this.getDistrict(
              this.mineAreaInfo.area_id,
              this.mineAreaInfo.district_id
            );
            this.saveOrUpdateProtocol();
          }
        });
    },
    saveOrUpdateProtocol() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/create_or_ignore_general_info/";
      axios
        .post(
          url,
          {
            deposit_id: this.deposit_id,
            mine_area_id: this.mine_area_id,
            component_id: this.component_id,
          },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            console.log(response.data[0].auth_fail);
          }
        });
    },
    hideErrorMessage() {
      this.showError = false;
    }  
}
}
</script>
