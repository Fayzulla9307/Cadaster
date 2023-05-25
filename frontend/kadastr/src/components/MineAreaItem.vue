<template>
  <div class="item">
    <ConfirmModal
      v-if="showConfirmModal"
      v-bind:message="confirmMessage"
      v-bind:header="confirmHeader"
      v-on:confirm="onConfirm"
      v-on:cancel="onCancel"
    />
    <EditMineAreaModal
      v-bind:deposit_id="depositId"
      v-bind:mine_area_id="mineAreaId"
      v-on:save-edit-mine-area="saveMineAreaEdit"
      v-on:close-edit-mine-area="closeMineAreaEdit"
      v-if="showEditMineAreaModal"
    />
    <OkModal
      v-if="showAuthError"
      v-bind:message="authMessage"
      v-bind:header="authHeader"
      v-on:confirm="hideAuthMessage"
    />
    <ProtocolEditModal
      v-bind:deposit_id="deposit_id"
      v-bind:mine_area_id="mine_area_id"
      v-bind:component_id="component_id"
      v-if="showProtocolEditModal"
      v-on:reselect="closeProtocolEditModal"
    />
    <ComponentSelectionModal
      v-if="showComponentSelectionModal"
      v-bind:deposit_id="deposit_id"
      v-bind:mine_area_id="mine_area_id"
      v-on:confirm="selectComponent"
      v-on:cancel="closeAllWindows"
    />
    <table style="border-style: none !important; width: 100%">
      <tr style="border-style: none !important; width: 100%">
        <td style="width: 50px; border-style: none !important">
          <button
            @click="removeItem"
            class="btn btn-dark btn-lg btn-block"
            style="float: left; width: 200px"
          >
            <BootstrapIcon icon="trash" />
            Удалить
          </button>
        </td>
        <td style="width: 50px">
          <button
            @click="editItem"
            class="btn btn-dark btn-lg btn-block"
            style="float: left; width: 200px"
          >
            <BootstrapIcon icon="pencil" />
            Редактировать
          </button>
        </td>
        <td style="width: 50px">
          <button
            @click="openProtocolModal"
            class="btn btn-dark btn-lg btn-block"
            style="float: left; width: 200px"
          >
            <BootstrapIcon icon="file-word" />
            Протокол
          </button>
        </td>
        <td style="width: 100%">
          <input
            type="text"
            class="form-control form-control-lg"
            style="display: inline; width: calc(100%)"
            v-model="mineAreaName"
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
import EditMineAreaModal from "../components/EditMineAreaModal.vue";
import ConfirmModal from "../components/ConfirmModal.vue";
import OkModal from "./OkModal.vue";
import ProtocolEditModal from "../components/ProtocolEditModal.vue";
import ComponentSelectionModal from "../components/ComponentSelectionModal.vue";

export default {
  name: "MineAreaItem",
  props: ["deposit_id", "mine_area_id", "mine_area_name"],
  data() {
    return {
      depositId: this.deposit_id,
      mineAreaId: this.mine_area_id,
      mineAreaName: this.mine_area_name,
      showEditMineAreaModal: false,
      showEditReserves: false,
      confirmMessage: "",
      confirmHeader: "",
      showConfirmModal: false,
      showAuthError: false,
      authMessage: "Доступ запрещен",
      authHeader: "Ошибка безопасности",
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
      const url = this.$BASE_URL + "/api/delete_mine_area/";
      axios
        .post(
          url,
          { deposit_id: this.depositId, mine_area_id: this.mine_area_id },
          { headers }
        )
        .then((response) => {
          if (!response.data[0].auth_fail) {
            this.$emit("mine-area-deleted", {});
          } else {
            this.showAuthError = true;
          }
        });
    },
    onCancel() {
      this.showConfirmModal = false;
    },
    removeItem(e) {
      this.confirmMessage =
        "Удалить участок? Это приведет к потере данных (лицензий, запасов, а также всех движений и исторических данных!)";
      this.confirmHeader = "Удаление данных!";
      this.showConfirmModal = true;
      e.preventDefault();
    },
    editItem(e) {
      this.showEditMineAreaModal = true;
      /*this.$emit('mine-area-edited', {
          "deposit_id": this.depositId,
          "mine_area_id": this.mineAreaId
        });
      */
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
    closeMineAreaEdit() {
      this.showEditMineAreaModal = false;
    },
    saveMineAreaEdit(mineArea) {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/update_mine_area/";
      axios.post(url, mineArea, { headers }).then(() => {
        this.$emit("mine-area-edited");
      });
      this.showEditMineAreaModal = false;
    },
  },
  components: {
    EditMineAreaModal,
    BootstrapIcon,
    ConfirmModal,
    OkModal,
    ProtocolEditModal,
    ComponentSelectionModal,
  },
  mounted() {},
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
