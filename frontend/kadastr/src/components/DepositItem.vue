<template>
  <div class="item">
    <ConfirmModal
      v-if="showConfirmModal"
      v-bind:message="confirmMessage"
      v-bind:header="confirmHeader"
      v-on:confirm="onConfirm"
      v-on:cancel="onCancel"
    />
    <OkModal
      v-if="showAuthError"
      v-bind:message="authMessage"
      v-bind:header="authHeader"
      v-on:confirm="hideAuthMessage"
    />
    <MineAreaModal
      v-bind:deposit_id="depositId"
      v-on:mine-areas-close="closeMineAreas"
      v-if="showMineAreaModal"
    />
    <ProtocolEditModal
      v-bind:deposit_id="id_deposit"
      v-bind:mine_area_id="id_deposit"
      v-bind:component_id="component_id"
      v-if="showProtocolEditModal"
      v-on:reselect="closeProtocolEditModal"
    />
    <ComponentSelectionModal
      v-if="showComponentSelectionModal"
      v-bind:deposit_id="id_deposit"
      v-bind:mine_area_id="id_deposit"
      v-on:confirm="selectComponent"
      v-on:cancel="closeAllWindows"
    />
    <table style="border-style: none !important; width: 100%">
      <tr style="border-style: none !important; width: 100%">
        <td style="width: 50px; border-style: none !important">
          <button
            @click="removeItem"
            class="btn btn-dark btn-md btn-block btn-delete"
            style="float: left; width: 42px" title="Удалить запись"
          >
            <BootstrapIcon icon="trash" />
          </button>
        </td>
        <td style="width: 50px">
          <button
            @click="editItem"
            class="btn btn-dark btn-md btn-block btn-edit"
            style="float: left; width: 42px" title="Редактировать запись"
          >
            <BootstrapIcon icon="pencil" />
          </button>
        </td>
        <td style="width: 50px">
          <button
            @click="openProtocolModal"
            class="btn btn-md btn-block btn-edit"
            v-bind:class="hasMineAreas == 0 ? 'btn-dark' : 'btn-danger'"
            style="float: left; width: 42px" title="Протокол"
            :disabled="hasMineAreas == 1"
          >
            <BootstrapIcon icon="file-earmark-word" />
          </button>
        </td>
        <td style="width: 50px">
          <button
            @click="editMineAreas"
            class="btn btn-dark btn-md btn-block btn-location"
            style="float: left; width: 42px" title="Участки месторождения"
          >
            <BootstrapIcon icon="pin-map" />
          </button>
        </td>
        <td style="width: 100%">
          <input
            type="text"
            class="form-control form-control-md"
            style="display: inline; width: calc(100%)"
            v-model="depositDecription"
            disabled
          />
        </td>
      </tr>
    </table>
  </div>
</template>

<script>
import axios from "axios";
import BootstrapIcon from "@dvuckovic/vue3-bootstrap-icons";
import MineAreaModal from "../components/MineAreaModal.vue";
import ConfirmModal from "../components/ConfirmModal.vue";
import OkModal from "../components/OkModal.vue";
import ProtocolEditModal from "../components/ProtocolEditModal.vue";
import ComponentSelectionModal from "../components/ComponentSelectionModal.vue";

export default {
  name: "DepositItem",
  props: ["id_deposit", "deposit_name", "type_id", "type"],
  data() {
    return {
      depositId: this.id_deposit,
      depositName: this.deposit_name,
      depositDecription: this.deposit_name + ", " + this.type,
      showEditReserves: false,
      showMineAreaModal: false,
      showDepositPropertiesModal: false,
      confirmMessage: "",
      confirmHeader: "",
      showConfirmModal: false,
      showAuthError: false,
      authMessage: "Доступ запрещен",
      authHeader: "Ошибка безопасности",
      hasMineAreas: false,
      showComponentSelectionModal: false,
      showProtocolEditModal: false,
    };
  },
  methods: {
    closeProtocolEditModal() {
      this.showProtocolEditModal = false;
    },
    selectComponent(data) {
      this.showComponentSelectionModal = false;
      this.component_id = data.component_id;
      this.showProtocolEditModal = true;
    },
    closeAllWindows() {
      this.showComponentSelectionModal = false;
    },
    openProtocolModal() {
      this.showComponentSelectionModal = true;
    },
    hideAuthMessage() {
      this.showAuthError = false;
    },
    onConfirm() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/delete_deposit/";
      axios
        .post(url, { deposit_id: this.depositId }, { headers })
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.$emit("deposit-deleted", {});
          } else {
            this.showAuthError = true;
          }
        });
    },
    getHasMineAreas() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/has_mine_areas/";
      axios
        .post(url, { deposit_id: this.depositId }, { headers })
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.hasMineAreas = response.data[0].result;
          }
        });
    },
    onCancel() {
      this.showConfirmModal = false;
    },
    removeItem(e) {
      this.confirmMessage =
        "Удалить месторождение? Это приведет к потере данных (лицензий, запасов, а также всех движений и исторических данных!)";
      this.confirmHeader = "Удаление данных!";
      this.showConfirmModal = true;
      e.preventDefault();
    },
    editItem(e) {
      this.$emit("deposit-edited", { deposit_id: this.depositId });
      e.preventDefault();
    },
    editReserves(e) {
      //this.$emit('reserves-edited-for-deposit', {"deposit_id": this.depositId});
      this.showEditReserves = true;
      e.preventDefault();
    },
    closeEditReserves() {
      this.showEditReserves = false;
      //e.preventDefault();
    },
    editMineAreas(e) {
      this.showMineAreaModal = true;
      e.preventDefault();
    },
    editItemProperties(e) {
      this.showDepositPropertiesModal = true;
      e.preventDefault();
    },
    closeMineAreas() {
      this.showMineAreaModal = false;
    },
    closeDepositPropsModal() {
      this.showDepositPropertiesModal = false;
    },
  },
  components: {
    BootstrapIcon,
    MineAreaModal,
    ConfirmModal,
    OkModal,
    ProtocolEditModal,
    ComponentSelectionModal,
  },
  mounted() {
    this.getHasMineAreas();
  },
};
</script>

<style scoped>
img {
  height: 30px;
  width: 30px;
}

.item {
  width: calc(100%);
  height: 50px;
  font-weight: bolder;
  font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS", sans-serif;
  border-style: none !important;
}
.delete-btn {
  height: 30px;
  display: inline;
  /*margin-right: 5px;*/
}
.save-btn {
  height: 30px;
  display: inline-block;
  /*margin-right: 5px;*/
}
.inputfield {
  display: inline;
  height: 30px;
  width: 330px;
}
</style>
