import { createRouter, createWebHistory } from "vue-router";
import Dicts from "../views/Dicts.vue";
import Districts from "../views/Districts.vue";
import SecuritySettings from "../views/SecuritySettings.vue";
import About from "../views/About.vue";
import Protocols from "../views/Protocols.vue";
import Reports from "../views/Reports.vue";
import Transfer from "../views/Transfer.vue";
import Deposits from "../views/Deposits.vue";

const routes = [
  {
    path: "/",
    name: "Протоколы",
    component: Protocols,
  },
  {
    path: "/protocols",
    name: "Протоколы",
    component: Protocols,
  },
  {
    path: "/transfer",
    name: "Мастер переноса",
    component: Transfer,
  },
  {
    path: "/deposits",
    name: "Месторождения",
    component: Deposits,
  },
  {
    path: "/dicts",
    name: "Справочники",
    component: Dicts,
  },
  {
    path: "/reports",
    name: "Отчеты",
    component: Reports,
  },
  {
    path: "/districts",
    name: "Районы",
    component: Districts,
  },
  {
    path: "/about",
    name: "О программе",
    component: About,
  },
  {
    path: "/security",
    name: "Безопасность",
    component: SecuritySettings,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.replace({ path: "*", redirect: "/" });

export default router;
