<template>
  <div class="modal-mask">
    <div class="modal-window">
      <div class="header">{{ header }}</div>
      <div class="message">{{ message }}</div>
      <button @click="confirm" class="btn btn-dark btn-lg btn-block confirm">
        Подтвердить
      </button>
      <button @click="cancel" class="btn btn-dark btn-lg btn-block cancel">
        Отменить
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "ConfirmModal",
  props: ["header", "message"],
  data() {
    return {};
  },
  methods: {
    confirm() {
      this.$emit("confirm", {});
    },
    cancel() {
      this.$emit("cancel", {});
    },
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
  width: 400px;
  height: 200px;
  top: 50%;
  left: 50%;
  margin-top: -100px;
  margin-left: -200px;
  z-index: 1000093;
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

.confirm {
  position: absolute;
  bottom: 10px;
  left: 10px;
}

.cancel {
  position: absolute;
  bottom: 10px;
  right: 10px;
}
</style>
