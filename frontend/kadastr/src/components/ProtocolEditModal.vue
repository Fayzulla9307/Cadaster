<template>
  <div class="modal-mask">
    <div class="modal-window">
      <Spinner v-if="showSpinner" />
      <OkModal v-if="showError" v-bind:message="errorMessage" v-bind:header="header" v-on:confirm="hideErrorMessage" />
      <OkModal v-if="showAuthError" v-bind:message="authMessage" v-bind:header="authHeader"
        v-on:confirm="hideAuthMessage" />
      <div class="header">
        <div class="form-group close">
          <button @click="selectDeposit" class="btn btn-dark btn-xxs btn-block">
            <!-- BootstrapIcon icon="journal-x" size="1x" / -->
            <span class="align-middle">X</span>
          </button>
        </div>
        Протокол для месторождения: {{ description }}
      </div>

      <div class="body">
        <ul class="nav nav-tabs">
          <li class="nav-item">
            <a class="nav-link" v-bind:class="selected_title ? 'active' : ''" @click="selectTab('title')"
              href="#">Титул</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" v-bind:class="selected_H01 ? 'active' : ''" @click="selectTab('H01')" href="#">Форма
              H01</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" v-bind:class="selected_H02 ? 'active' : ''" @click="selectTab('H02')" href="#">Форма
              H02</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" v-bind:class="selected_H03 ? 'active' : ''" @click="selectTab('H03')" href="#">Форма
              H03</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" v-bind:class="selected_H04 ? 'active' : ''" @click="selectTab('H04')" href="#">Форма
              H04</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" v-bind:class="selected_H05 ? 'active' : ''" @click="selectTab('H05')" href="#">Форма
              H05</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" v-bind:class="selected_H06 ? 'active' : ''" @click="selectTab('H06')" href="#">Форма
              H06</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" v-bind:class="selected_H07 ? 'active' : ''" @click="selectTab('H07')" href="#">Форма
              H07</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" v-bind:class="selected_H08 ? 'active' : ''" @click="selectTab('H08')" href="#">Форма
              H08</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" v-bind:class="selected_H0910 ? 'active' : ''" @click="selectTab('H0910')" href="#">Форма
              H09 и H10</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" v-bind:class="selected_H11 ? 'active' : ''" @click="selectTab('H11')" href="#">Форма
              H11</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" v-bind:class="selected_H12 ? 'active' : ''" @click="selectTab('H12')" href="#">Форма
              H12</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" v-bind:class="selected_H13 ? 'active' : ''" @click="selectTab('H13')" href="#">Форма
              H13</a>
          </li>
        </ul>
        <!-- TITLE -->
        <div class="tab-title" v-if="selected_title" style="height: 400px; width: calc(80%); margin: auto">
          <!-- title -->
          <div class="body">
            <div class="title">ТИТУЛЬНЫЙ ЛИСТ</div>
            <form class="form-inline">
              <table style="border: none !important">
                <tr>
                  <td>
                    <div class="form-group col-xs-3">
                      <label>Месторождение</label>
                      <input type="text" class="form-control form-control-md" v-model="deposit" disabled />
                    </div>
                  </td>
                  <td>
                    <div class="form-group col-xs-3">
                      <label>Участок</label>
                      <input type="text" class="form-control form-control-md" v-model="mineArea" disabled />
                    </div>
                  </td>
                  <td>
                    <div class="form-group col-xs-3">
                      <label>Степень освоения</label>
                      <input type="text" class="form-control form-control-md" v-model="dev" disabled />
                    </div>
                  </td>
                  <td>
                    <div class="form-group col-xs-3">
                      <label>Полезное ископаемое</label>
                      <input type="text" class="form-control form-control-md" v-model="component" disabled />
                    </div>
                  </td>
                </tr>
                <tr>
                  <td>
                    <div class="form-group col-xs-3">
                      <label>Наименование раздела</label>
                      <input type="text" class="form-control form-control-md" v-model="chapter" />
                    </div>
                  </td>
                  <td>
                    <div class="form-group col-xs-3">
                      <label>Госбаланс</label>
                      <input type="text" class="form-control form-control-md" v-model="balance" />
                    </div>
                  </td>
                </tr>
                <tr>
                  <td>
                    <div class="form-group col-xs-3">
                      <label>Составил</label>
                      <input type="text" class="form-control form-control-md" v-model="prepared" />
                    </div>
                  </td>
                  <td>
                    <div class="form-group col-xs-3">
                      <label>Дата составления</label>
                      <input type="date" class="form-control form-control-md" v-model="datePrepared" />
                    </div>
                  </td>
                </tr>
                <tr>
                  <td>
                    <div class="form-group col-xs-3">
                      <label>Утвердил</label>
                      <input type="text" class="form-control form-control-md" v-model="prepared" />
                    </div>
                  </td>
                  <td>
                    <div class="form-group col-xs-3">
                      <label>Дата утверждения</label>
                      <input type="date" class="form-control form-control-md" v-model="dateConfirmed" />
                    </div>
                  </td>
                </tr>
              </table>
            </form>
          </div>
        </div>
        <!-- H01 -->
        <div class="tab-H01" v-if="selected_H01" style="height: 400px; width: calc(80%); margin: auto">
          <div class="body">
            <!-- inner menu for H01 -->
            <nav class="inner-nav">
              <ul class="inner-nav-tab">
                <li class="inner-nav-item">
                  <a class="inner-nav-link" v-bind:class="selected_H01_inner1 ? 'active' : ''"
                    @click="selectTab('inner-H01-1')" href="#">Общие сведения</a>
                </li>
                <li class="inner-nav-item">
                  <a class="inner-nav-link" v-bind:class="selected_H01_inner2 ? 'active' : ''"
                    @click="selectTab('inner-H01-2')" href="#">Координаты</a>
                </li>
                <li class="inner-nav-item">
                  <a class="inner-nav-link" v-bind:class="selected_H01_inner3 ? 'active' : ''"
                    @click="selectTab('inner-H01-3')" href="#">Населенные пункты</a>
                </li>
                <li class="inner-nav-item">
                  <a class="inner-nav-link" v-bind:class="selected_H01_inner4 ? 'active' : ''"
                    @click="selectTab('inner-H01-4')" href="#">Источники</a>
                </li>
                <li class="inner-nav-item">
                  <a class="inner-nav-link" v-bind:class="selected_H01_inner5 ? 'active' : ''"
                    @click="selectTab('inner-H01-5')" href="#">Доп. сведения</a>
                </li>
                <li class="inner-nav-item">
                  <a class="inner-nav-link" v-bind:class="selected_H01_inner6 ? 'active' : ''"
                    @click="selectTab('inner-H01-6')" href="#">Изученность</a>
                </li>
              </ul>
              <!-- inner tabs to show -->
              <div class="tab-H01-inner1 inner" v-if="selected_H01_inner1">
                <div class="inner-body">
                  <div class="title">1. ОБЩИЕ СВЕДЕНИЯ О МЕСТОРОЖДЕНИИ</div>
                  <form class="form-inline" style="width: calc(100%)">
                    <table style="border: none !important; width: calc(100%)">
                      <tr>
                        <td style="margin: 10px">
                          <div class="form-group col-xs-3">
                            <label style="float: left">01. Название объекта</label>
                            <input type="text" class="form-control form-control-md" v-model="description"
                              placeholder="Месторождение" disabled />
                          </div>
                        </td>
                        <td style="margin: 10px">
                          <div class="form-group col-xs-3">
                            <label style="float: left">06. Полезное ископаемое</label>
                            <input type="text" class="form-control form-control-md" v-model="component"
                              placeholder="Полезное ископаемое" disabled />
                          </div>
                        </td>
                      </tr>
                      <tr>
                        <td style="margin: 10px">
                          <div class="form-group col-xs-3">
                            <label style="float: left">02. Участок</label>
                            <input type="text" class="form-control form-control-md" v-model="mineArea"
                              placeholder="Участок" disabled />
                          </div>
                        </td>
                        <td style="margin: 10px">
                          <div class="form-group col-xs-3">
                            <label style="float: left">07. Применение</label>
                            <select class="form-select form-control-md" v-model="selectedDiffId" aria-label="Применение"
                              placeholder="Выберите применение">
                              <option v-for="o in diffs" v-bind:value="o.id" v-bind:key="o.id">
                                {{ o.description }}
                              </option>
                            </select>
                            <select class="form-select form-control-md" v-model="selectedDiffId" aria-label="Применение"
                              placeholder="Выберите применение">
                              <option v-for="o in diffs" v-bind:value="o.id" v-bind:key="o.id">
                                {{ o.description }}
                              </option>
                            </select>
                            <select class="form-select form-control-md" v-model="selectedDiffId" aria-label="Применение"
                              placeholder="Выберите применение">
                              <option v-for="o in diffs" v-bind:value="o.id" v-bind:key="o.id">
                                {{ o.description }}
                              </option>
                            </select>
                          </div>
                        </td>
                      </tr>
                      <tr>
                        <td style="margin: 10px">
                          <div class="form-group col-xs-3">
                            <label style="float: left">03. Область</label>
                            <input type="text" class="form-control form-control-md" v-model="area" placeholder="Область"
                              disabled />
                          </div>
                        </td>
                        <td></td>
                      </tr>
                      <tr>
                        <td style="margin: 10px">
                          <div class="form-group col-xs-3">
                            <label style="float: left">04. Район</label>
                            <input type="text" class="form-control form-control-md" v-model="district" placeholder="Район"
                              disabled />
                          </div>
                        </td>
                        <td style="margin: 10px">
                          <div class="form-group col-xs-3">
                            <label style="float: left">08. Ведомственная принадлежность</label>
                            <select class="form-select form-control-md" v-model="selectedOrganizationId"
                              aria-label="Ведомственная принадлежность">
                              <option v-for="o in organizations" v-bind:value="o.id" v-bind:key="o.id">
                                {{ o.description }}
                              </option>
                            </select>
                          </div>
                        </td>
                      </tr>
                      <tr style="margin: 10px">
                        <td>
                          <div class="form-group col-xs-3">
                            <label style="float: left">05. Номенклатура листа м-ба 1:200000</label>
                            <input type="text" class="form-control form-control-md" v-model="area01"
                              placeholder="Номенклатура" />
                          </div>
                        </td>
                      </tr>
                    </table>
                  </form>
                </div>
              </div>
              <div class="tab-H01-inner2 inner" v-if="selected_H01_inner2">
                <div class="inner-body">
                  <form class="form-inline" style="width: calc(100%)">
                    <table style="border: none !important; width: calc(100%)">
                      <tr style="margin: 10px">
                        <td style="margin: 10px">
                          <div class="form-group col-xs-3">
                            <table>
                              <caption>
                                09. Географические координаты центра объекта
                              </caption>
                              <thead>
                                <tr class="tab-data">
                                  <th colspan="3">Долгота</th>
                                  <th colspan="3">Широта</th>
                                </tr>
                              </thead>
                              <tbody>
                                <tr class="tab-data">
                                  <th>град.</th>
                                  <th>мин.</th>
                                  <th>сек.</th>
                                  <th>град.</th>
                                  <th>мин.</th>
                                  <th>сек.</th>
                                </tr>
                                <tr class="tab-data">

                                  <td>
                                    <input type="number" class="form-control form-control-md" v-model="lat_ang"
                                      placeholder="град." />
                                  </td>
                                  <td>
                                    <input type="number" class="form-control form-control-md" v-model="lat_ang"
                                      placeholder="мин." />
                                  </td>
                                  <td>
                                    <input type="number" class="form-control form-control-md" v-model="lat_ang"
                                      placeholder="сек." />
                                  </td>
                                  <td>
                                    <input type="number" class="form-control form-control-md" v-model="lat_ang"
                                      placeholder="град." />
                                  </td>
                                  <td>
                                    <input type="number" class="form-control form-control-md" v-model="lat_ang"
                                      placeholder="мин." />
                                  </td>
                                  <td>
                                    <input type="number" class="form-control form-control-md" v-model="lat_ang"
                                      placeholder="сек." />
                                  </td>
                                </tr>
                              </tbody>
                            </table>
                            <button class="btn btn-dark btn-save">
                              Сохранить
                            </button>
                          </div>
                        </td>
                      </tr>
                    </table>
                  </form>
                </div>
              </div>
              <div class="tab-H01-inner3 inner" v-if="selected_H01_inner3">
                <div class="inner-body">
                  <form class="form-inline" style="width: calc(100%)">
                    <div style="width: calc(100%) !important">
                      <div>
                        <label style="display: flex; justify-content: center">10. Ближайшие пункты</label>
                      </div>
                      <table>
                        <tr>
                          <td>Название</td>
                          <td>Расст. км.</td>
                          <td>Направление, румб</td>
                          <td>Путь сообщения</td>
                        </tr>
                        <tr>
                          <td>Населенный пункт</td>
                        </tr>
                        <tr>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="inh_area_name"
                              placeholder="Название" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="inh_area_dist"
                              placeholder="Расстояние, км" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="inh_area_dir"
                              placeholder="Направление" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="inh_area_path"
                              placeholder="Путь сообщения" />
                          </td>
                        </tr>
                        <tr>
                          <td>ЖД станция</td>
                        </tr>
                        <tr>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="inh_area_name"
                              placeholder="Название" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="inh_area_dist"
                              placeholder="Расстояние, км" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="inh_area_dir"
                              placeholder="Направление" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="inh_area_path"
                              placeholder="Путь сообщения" />
                          </td>
                        </tr>
                      </table>
                    </div>
                  </form>
                </div>
              </div>
              <div class="tab-H01-inner4 inner" v-if="selected_H01_inner4">
                <div class="inner-body">
                  <form class="form-inline" style="width: calc(100%)">
                    <div style="width: calc(100%) !important; float: left">
                      <table>
                        <tr>
                          <td>Источники</td>
                          <td>Название</td>
                          <td>Расстояние, км.</td>
                        </tr>
                        <tr>
                          <td>Питьевой воды</td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="water_pure_name"
                              placeholder="Название" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="water_pure_dist"
                              placeholder="Расстояние, км." />
                          </td>
                        </tr>
                        <!-- tr>
                    <td>Источники</td>
                    <td>Название</td>
                    <td>Расстояние, км.</td>
                  </tr -->
                        <tr>
                          <td>Технической воды</td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="water_tech_name"
                              placeholder="Название" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="water_tech_dist"
                              placeholder="Расстояние, км." />
                          </td>
                        </tr>
                        <tr>
                          <td>Электроэнергии</td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="electricity_name"
                              placeholder="Название" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="electricity_dist"
                              placeholder="Расстояние, км." />
                          </td>
                        </tr>
                      </table>
                    </div>
                  </form>
                </div>
              </div>
              <div class="tab-H01-inner5 inner" v-if="selected_H01_inner5">
                <div class="inner-body">
                  <form class="form-inline" style="width: calc(100%)">
                    <div style="
                                                                          width: calc(100%) !important;
                                                                          margin: 0px;
                                                                          float: left;
                                                                        ">
                      <table style="width: calc(100%) !important">
                        <tr>
                          <td>11. Абсолют. отметки рельефа м-я, м.</td>
                          <td>Мин.</td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="landscape_mark_min"
                              placeholder="Мин." />
                          </td>
                          <td>Макс.</td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="landscape_mark_max"
                              placeholder="Макс." />
                          </td>
                        </tr>
                      </table>
                    </div>

                    <div style="
                                                                          width: calc(100%) !important;
                                                                          float: left !important;
                                                                          align: left;
                                                                        ">
                      <table style="width: calc(100%) !important">
                        <tr>
                          <td style="width: calc(40%)">12. Тип рельефа:</td>
                          <td style="width: calc(60%)">
                            <select class="form-select form-control-md" v-model="selectedLandascapeId"
                              aria-label="Тип рельефа">
                              <option v-for="l in relief" v-bind:value="l.id" v-bind:key="l.id">
                                {{ l.description }}
                              </option>
                            </select>
                          </td>
                        </tr>
                      </table>
                    </div>

                    <div style="width: calc(100%) !important; float: left">
                      <table style="width: calc(100%) !important">
                        <tr>
                          <td style="width: calc(40%)">13. Сейсмичность:</td>
                          <td style="width: calc(60%)">
                            <input type="text" class="form-control form-control-md" v-model="seismic_score"
                              placeholder="Сейсмичность" />
                          </td>
                        </tr>
                      </table>
                    </div>

                    <div style="width: calc(100%) !important; float: left">
                      <table style="width: calc(100%) !important">
                        <tr>
                          <td style="width: calc(40%)">14. Селеопасность:</td>
                          <td style="width: calc(60%)">
                            <select class="form-select form-control-md" v-model="selectedDroughtScoreId"
                              aria-label="Селеопасность">
                              <option v-for="s in drought_score" v-bind:value="s.id" v-bind:key="s.id">
                                {{ s.description }}
                              </option>
                            </select>
                          </td>
                        </tr>
                      </table>
                    </div>

                    <div style="width: calc(100%) !important; float: left">
                      <table style="width: calc(100%) !important">
                        <tr>
                          <td style="width: calc(40%)">
                            15. Оползнеопасность:
                          </td>
                          <td style="width: calc(60%)">
                            <select class="form-select form-control-md" v-model="selectedAvalanchScoreId"
                              aria-label="Оползнеопасность">
                              <option v-for="s in avalanch_score" v-bind:value="s.id" v-bind:key="s.id">
                                {{ s.description }}
                              </option>
                            </select>
                          </td>
                        </tr>
                      </table>
                    </div>

                    <div style="width: calc(100%) !important; float: left">
                      <table style="width: calc(100%) !important">
                        <tr>
                          <td style="width: calc(40%)">
                            16. Принадлежность площади объекта к занятым жилой и
                            промышленной застройкой, горным отводам, охранным
                            зонам и гидротехническим сооружениям, заповедникам,
                            национальным паркам:
                          </td>
                          <td style="width: calc(60%)">
                            <input type="text" class="form-control form-control-md" style="width: calc(100%)"
                              v-model="attachment" placeholder="Принадлежность" />
                          </td>
                        </tr>
                      </table>
                    </div>

                    <div style="width: calc(100%) !important; float: left">
                      <table style="width: calc(100%) !important">
                        <tr>
                          <td style="width: calc(40%)">17. Тип земель:</td>
                          <td style="width: calc(60%)">
                            <select class="form-select form-control-md" v-model="selectedLandTypeId"
                              aria-label="Тип земель">
                              <option v-for="s in land_type" v-bind:value="s.id" v-bind:key="s.id">
                                {{ s.description }}
                              </option>
                            </select>
                          </td>
                        </tr>
                      </table>
                    </div>
                  </form>
                </div>
              </div>
              <div class="tab-H01-inner6 inner" v-if="selected_H01_inner6">
                <div class="inner-body">
                  <form class="form-inline" style="width: calc(100%)">
                    <div style="width: calc(100%) !important; float: left">
                      <div>
                        <label style="display: flex; justify-content: center">19. Изученность объекта</label>
                      </div>
                      <ExplorationCtrl />
                    </div>

                    <div style="width: calc(100%) !important; float: left">
                      <div>
                        <label style="display: flex; justify-content: center">Угловые координаты, определенные в системе
                          Google</label>
                      </div>
                      <CoordinatesCtrl />
                    </div>
                  </form>
                </div>
              </div>
            </nav>
          </div>
        </div>
        <!-- H02 -->
        <div class="tab-H02" v-if="selected_H02" style="height: 400px; width: calc(80%); margin: auto">
          <div class="body">
            <div class="title">
              2. ГЕОЛОГИЧЕСКАЯ ХАРАКТЕРИСТИКА МЕСТОРОЖДЕНИЯ
            </div>
            <form class="form-inline" style="width: calc(100%)">
              <table style="border: none !important; width: calc(30%)">
                <tr>
                  <td style="margin: 10px; width: calc(30%)">
                    <div class="form-group col-xs-3">
                      <label style="float: left">Объект (название):</label>
                      <input type="text" class="form-control form-control-md" v-model="description"
                        placeholder="Месторождение" disabled />
                    </div>
                  </td>
                </tr>
                <tr>
                  <td style="margin: 10px; width: calc(30%)">
                    <div class="form-group col-xs-3">
                      <label style="float: left">Полезное ископаемое:</label>
                      <input type="text" class="form-control form-control-md" v-model="component"
                        placeholder="Полезное ископаемое" disabled />
                    </div>
                  </td>
                </tr>
              </table>

              <table style="border: none !important; width: calc(100%)">
                <tr>
                  <td style="margin: 10px; width: calc(30%)">
                    <div class="form-group col-xs-3">
                      <label style="float: left">01. Группа сложности геологического строения
                        м-ния</label>
                      <select class="form-select form-control-md" v-model="selectedDiffId"
                        aria-label="Группа сложности геологического строения м-ния">
                        <option v-for="o in diffs" v-bind:value="o.id" v-bind:key="o.id">
                          {{ o.description }}
                        </option>
                      </select>
                    </div>
                  </td>
                  <td style="margin: 10px; width: calc(30%)" rowspan="2">
                    <div class="form-group col-xs-3">
                      <label style="float: left">10. Группа сложности геологического строения
                        м-ния</label><br />
                      <textarea class="form-control-md" rows="4" v-model="geoAge" style="width: calc(100%)" />
                    </div>
                  </td>
                </tr>
                <tr>
                  <td style="margin: 10px; width: calc(30%)">
                    <div class="form-group col-xs-3">
                      <label style="float: left">Тип</label>
                      <select class="form-select form-control-md" v-model="selectedDiffTypeId" aria-label="Тип">
                        <option v-for="o in diffTypes" v-bind:value="o.id" v-bind:key="o.id">
                          {{ o.description }}
                        </option>
                      </select>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td style="margin: 10px; width: calc(30%)" colspan="2">
                    <div class="form-group col-xs-3">
                      <label style="float: left">02. Породы, слагающие полезное ископаемое</label>
                      <select class="form-select form-control-md" v-model="selecteOreTypeId"
                        aria-label="Породы, слагающие полезное ископаемое">
                        <option v-for="o in oreTypes" v-bind:value="o.id" v-bind:key="o.id">
                          {{ o.description }}
                        </option>
                      </select>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td style="margin: 10px; width: calc(30%)" colspan="2">
                    <div class="form-group col-xs-3">
                      <label style="float: left">03. Форма тел</label>
                      <select class="form-select form-control-md" v-model="selecteBodyTypeId" aria-label="Форма тел">
                        <option v-for="o in bodyTypes" v-bind:value="o.id" v-bind:key="o.id">
                          {{ o.description }}
                        </option>
                      </select>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td style="margin: 10px; width: calc(30%)" colspan="2">
                    <div class="form-group col-xs-3">
                      <label style="float: left">04. Количество тел</label>
                      <input type="text" class="form-control form-control-md" v-model="numberOfOreBodies"
                        placeholder="Количество тел" />
                    </div>
                  </td>
                </tr>
                <tr>
                  <td style="margin: 10px; width: calc(100%)" colspan="2">
                    <div class="form-group col-xs-3" style="width: calc(100%)">
                      <table style="width: calc(100%)">
                        <tr>
                          <td colspan="2">05. Размер тел:</td>
                          <td style="text-align: center">от</td>
                          <td style="text-align: center">до</td>
                          <td style="text-align: center">среднее</td>
                        </tr>
                        <tr>
                          <td colspan="2">- длина по простиранию, м</td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyLengthHorizFrom"
                              placeholder="От" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyLengthHorizTo"
                              placeholder="До" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyLengthHorizMean"
                              placeholder="Среднее" />
                          </td>
                        </tr>
                        <tr>
                          <td colspan="2">- длина по падению, м</td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyLengthVerticalFrom"
                              placeholder="От" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyLengthVerticalTo"
                              placeholder="До" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyLengthVerticalMean"
                              placeholder="Среднее" />
                          </td>
                        </tr>
                        <tr>
                          <td colspan="2">Мощьность, м</td>
                          <td></td>
                          <td></td>
                          <td></td>
                        </tr>
                        <tr>
                          <td colspan="2">- Общая</td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyWidthFrom"
                              placeholder="От" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyWidthVerticalTo"
                              placeholder="До" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyWidthVerticalMean"
                              placeholder="Среднее" />
                          </td>
                        </tr>
                        <tr>
                          <td colspan="2">- Вскрытая</td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyExcavatedFrom"
                              placeholder="От" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyWidthExcavatedTo"
                              placeholder="До" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyWidthExcavatedMean"
                              placeholder="Среднее" />
                          </td>
                        </tr>
                        <tr>
                          <td colspan="2">- Вошедшая в подсчет запасов</td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyCalculatedFrom"
                              placeholder="От" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyWidthCalculatedTo"
                              placeholder="До" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyWidthCalculatedMean"
                              placeholder="Среднее" />
                          </td>
                        </tr>
                        <tr>
                          <td colspan="2">- Отдельных слоев</td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodySeparatedLayersFrom"
                              placeholder="От" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md"
                              v-model="oreBodyWidthSeparatedLayersTo" placeholder="До" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md"
                              v-model="oreBodyWidthSeparatedLayersMean" placeholder="Среднее" />
                          </td>
                        </tr>
                        <tr>
                          <td colspan="2">06. Условия залегания</td>
                          <td></td>
                          <td></td>
                          <td></td>
                        </tr>
                        <tr>
                          <td colspan="2">- Направление простирания, румб</td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyDirection"
                              placeholder="От" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyDirectionTo"
                              placeholder="До" />
                          </td>
                        </tr>
                        <tr>
                          <td colspan="2">- Азимут падения, град.</td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyAzimuthFrom"
                              placeholder="От" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyAzimuthTo"
                              placeholder="До" />
                          </td>
                        </tr>
                        <tr>
                          <td colspan="2">- Угол падения, град.</td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyDropAngleFrom"
                              placeholder="От" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyWidthDropAngleTo"
                              placeholder="До" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyWidthDropAngleMean"
                              placeholder="Среднее" />
                          </td>
                        </tr>
                        <tr>
                          <td colspan="2">- Глубина залегания, м</td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyDepthFrom"
                              placeholder="От" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyDepthTo"
                              placeholder="До" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyDepthMean"
                              placeholder="Среднее" />
                          </td>
                        </tr>

                        <tr>
                          <td colspan="2">07. Мощьность</td>
                          <td></td>
                          <td></td>
                          <td></td>
                        </tr>
                        <tr>
                          <td colspan="2">- Зоны выветривания, м</td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyErosionZoneFrom"
                              placeholder="От" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyErosionZoneTo"
                              placeholder="До" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyErosionZoneMean"
                              placeholder="Среднее" />
                          </td>
                        </tr>
                        <tr>
                          <td colspan="2">
                            - зоны частичного выветьривания, м
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md"
                              v-model="oreBodyErosionPartialZoneFrom" placeholder="От" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyErosionPartialZoneTo"
                              placeholder="До" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md"
                              v-model="oreBodyErosionPartialZoneMean" placeholder="Среднее" />
                          </td>
                        </tr>
                        <tr>
                          <td colspan="2">- вскрыши, м</td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyWidthExcavatedFrom"
                              placeholder="От" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyWidthExcavatedTo"
                              placeholder="До" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyWidthExcavatedMean"
                              placeholder="Среднее" />
                          </td>
                        </tr>
                        <tr>
                          <td colspan="2">
                            &nbsp;&nbsp;&nbsp;в т.ч. четвертичных отложений
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyQuaterDepositFrom"
                              placeholder="От" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyQuaterDepositTo"
                              placeholder="До" />
                          </td>
                          <td>
                            <input type="text" class="form-control form-control-md" v-model="oreBodyQuaterDepositMean"
                              placeholder="Среднее" />
                          </td>
                        </tr>
                      </table>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td style="margin: 10px; width: calc(100%)" colspan="2">
                    <div class="form-group col-xs-3">
                      <label style="float: left">08. Линейная плотность трещин, к-во тр/п.м.</label>
                      <input type="text" class="form-control form-control-md" v-model="crackDensity"
                        placeholder="Линейная плотность трещин" />
                    </div>
                  </td>
                </tr>
                <tr>
                  <td style="margin: 10px; width: calc(100%)" colspan="2">
                    <div class="form-group col-xs-3">
                      <label style="float: left">09. Закарстованность, %</label>
                      <input type="text" class="form-control form-control-md" v-model="karstness"
                        placeholder="Закарстованность" />
                    </div>
                  </td>
                </tr>
                <tr>
                  <td style="margin: 10px; width: calc(100%)" colspan="2">
                    <div class="form-group col-xs-3">
                      <label style="float: left">&nbsp;&nbsp;&nbsp;&nbsp;- заполнитель карста</label>
                      <input type="text" class="form-control form-control-md" v-model="karstFiller"
                        placeholder="Заполнитель карста" />
                    </div>
                  </td>
                </tr>
              </table>
            </form>
          </div>
        </div>
        <!-- H03 -->
        <div class="tab-H03" v-if="selected_H03" style="height: 400px; width: calc(80%); margin: auto">
          <div class="body">
            <!-- inner menu for H03 -->
            <nav class="inner-nav">
              <ul class="inner-nav-tab">
                <li class="inner-nav-item">
                  <a class="inner-nav-link" v-bind:class="selected_H03_inner1 ? 'active' : ''"
                    @click="selectTab('inner-H03-1')" href="#" style="display: none;">#</a>
                </li>
              </ul>
              <!-- inner tabs to show -->
              <div class="tab-H03-inner1 inner" v-if="selected_H03_inner1">
                <div class="inner-body">
                  <div class="caption-table">
                    <table>
                      <tr class="tab-data">
                        <th>Объект (название):</th>
                        <td>
                          <input type="text" class="form-control form-control-md" v-model="description"
                            placeholder="Месторождение" disabled />
                        </td>
                      </tr>
                      <tr class="tab-data">
                        <th>Полезное ископаемое:</th>
                        <td>
                          <input type="text" class="form-control form-control-md" v-model="component"
                            placeholder="Полезное ископаемое" disabled />
                        </td>
                      </tr>
                    </table>
                  </div>
                  <div class="title">3. КАЧЕСТВЕННАЯ ХАРАКТЕРИСТИКА ПОЛЕЗНОГО ИСКОПАЕМОГО</div>
                  <form class="form-inline" style="width: calc(100%)">
                    <table>
                      <thead>
                        <tr class="tab-data">
                          <th rowspan="2" style="width: 350px;">Показатели (компоненты химического, мине- рального и
                            петрографического состава,
                            раз- мер фракций грансостава, размер отверстий сит, остатки на ситах, просев через сита,
                            наименование продуктов рассева)</th>
                          <th rowspan="2">Единица измерения</th>
                          <th colspan="3">Значения показателей</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr class="tab-data">
                          <th></th>
                          <th></th>
                          <th>от</th>
                          <th>до</th>
                          <th>среднее</th>
                        </tr>
                        <tr class="tab-data">
                          <td>01</td>
                          <td>02</td>
                          <td>03</td>
                          <td>04</td>
                          <td>05</td>
                        </tr>
                        <tr class="tab-data">
                          <td>
                            <select class="form-select form-control-md" v-model="selecteOreTypeId"
                              aria-label="Породы, слагающие полезное ископаемое">
                              <option v-for="o in oreTypes" v-bind:value="o.id" v-bind:key="o.id">
                                {{ o.description }}
                              </option>
                            </select>
                          </td>
                          <td>
                            <select class="form-select form-control-md" v-model="selecteOreTypeId"
                              aria-label="Породы, слагающие полезное ископаемое">
                              <option v-for="o in oreTypes" v-bind:value="o.id" v-bind:key="o.id">
                                {{ o.description }}
                              </option>
                            </select>
                          </td>
                          <td>
                            <input type="number" class="form-control form-control-md" v-model="lat_ang" />
                          </td>
                          <td>
                            <input type="number" class="form-control form-control-md" v-model="lat_ang" />
                          </td>
                          <td>
                            <input type="number" class="form-control form-control-md" v-model="lat_ang" />
                          </td>
                          <td class="for-btn"><button @click="editItem" class="btn btn-dark btn-md btn-block btn-edit"
                              title="Редактировать запись">
                              <BootstrapIcon icon="pencil" />
                            </button>
                          </td>
                          <td class="for-btn">
                            <button @click="removeItem" class="btn btn-dark btn-md btn-block btn-delete"
                              style="float: left; width: 42px" title="Удалить запись">
                              <BootstrapIcon icon="trash" />
                            </button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                    <button @click="addItem" class="btn btn-dark btn-md btn-block btn-add">
                      <BootstrapIcon icon="plus-square-fill" />
                      Добавить
                    </button>
                    <button data-v-4d803cea="" class="btn btn-dark btn-save"> Сохранить </button>
                  </form>
                </div>
              </div>
            </nav>
          </div>
        </div>
        <!-- H04 -->
        <div class="tab-H04" v-if="selected_H04" style="height: 400px; width: calc(80%); margin: auto">
          <div class="body">
            <!-- inner menu for H04 -->
            <nav class="inner-nav">
              <ul class="inner-nav-tab">
                <li class="inner-nav-item">
                  <a class="inner-nav-link" v-bind:class="selected_H04_inner1 ? 'active' : ''"
                    @click="selectTab('inner-H04-1')" href="#">Лист 1</a>
                </li>
                <li class="inner-nav-item">
                  <a class="inner-nav-link" v-bind:class="selected_H04_inner2 ? 'active' : ''"
                    @click="selectTab('inner-H04-2')" href="#">Лист 2</a>
                </li>
                <li class="inner-nav-item">
                  <a class="inner-nav-link" v-bind:class="selected_H04_inner3 ? 'active' : ''"
                    @click="selectTab('inner-H04-3')" href="#">Лист 3</a>
                </li>
              </ul>
              <!-- inner tabs to show -->
              <div class="tab-H04-inner1 inner" v-if="selected_H04_inner1">
                <div class="inner-body">
                  <div class="caption-table">
                    <table>
                      <tr class="tab-data">
                        <th>Объект (название):</th>
                        <td>
                          <input type="text" class="form-control form-control-md" v-model="description"
                            placeholder="Месторождение" disabled />
                        </td>
                      </tr>
                      <tr class="tab-data">
                        <th>Полезное ископаемое:</th>
                        <td>
                          <input type="text" class="form-control form-control-md" v-model="component"
                            placeholder="Полезное ископаемое" disabled />
                        </td>
                      </tr>
                    </table>
                  </div>
                  <div class="title">4. ФИЗИКО-МЕХАНИЧЕСКИЕ И ТЕХНОЛОГИЧЕСКИЕ СВОЙСТВА ПОЛЕЗНОГО ИСКОПАЕМОГО</div>
                  <form class="form-inline" style="width: calc(100%)">
                    <table style="display: table">
                      <thead>
                        <tr class="tab-data">
                          <th rowspan="2" style="width: 250px">Свойства</th>
                          <th rowspan="2" style="width: 150px;">Единица измерения</th>
                          <th colspan="3">Величина</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr class="tab-data">
                          <th></th>
                          <th></th>
                          <th>от</th>
                          <th>до</th>
                          <th>средняя</th>
                        </tr>
                        <tr class="tab-data">
                          <td>01</td>
                          <td>02</td>
                          <td>03</td>
                          <td>04</td>
                          <td>05</td>
                        </tr>
                        <tr class="tab-data">
                          <td>
                            <div class="drpdwn-container">
                              <select class="form-select form-control-md" v-model="selecteOreTypeId"
                                aria-label="Породы, слагающие полезное ископаемое">
                                <option v-for="o in oreTypes" v-bind:value="o.id" v-bind:key="o.id">
                                  {{ o.description }}
                                </option>
                              </select>
                            </div>
                          </td>
                          <td>
                            <div class="drpdwn-container">
                              <select class="form-select form-control-md" v-model="selecteOreTypeId"
                                aria-label="Породы, слагающие полезное ископаемое">
                                <option v-for="o in oreTypes" v-bind:value="o.id" v-bind:key="o.id">
                                  {{ o.description }}
                                </option>
                              </select>
                            </div>

                          </td>
                          <td>
                            <input type="number" class="form-control form-control-md" v-model="lat_ang" />
                          </td>
                          <td>
                            <input type="number" class="form-control form-control-md" v-model="lat_ang" />
                          </td>
                          <td>
                            <input type="number" class="form-control form-control-md" v-model="lat_ang" />
                          </td>
                          <td class="for-btn"><button @click="editItem" class="btn btn-dark btn-md btn-block btn-edit"
                              title="Редактировать запись">
                              <BootstrapIcon icon="pencil" />
                            </button>
                          </td>
                          <td class="for-btn">
                            <button @click="removeItem" class="btn btn-dark btn-md btn-block btn-delete"
                              style="float: left; width: 42px" title="Удалить запись">
                              <BootstrapIcon icon="trash" />
                            </button>
                          </td>
                        </tr>
                        <tr class="tab-data">
                          <td>
                            <div class="drpdwn-container">
                              <select class="form-select form-control-md" v-model="selecteOreTypeId"
                                aria-label="Породы, слагающие полезное ископаемое">
                                <option v-for="o in oreTypes" v-bind:value="o.id" v-bind:key="o.id">
                                  {{ o.description }}
                                </option>
                              </select>
                            </div>
                          </td>
                          <td>
                            <div class="drpdwn-container">
                              <select class="form-select form-control-md" v-model="selecteOreTypeId"
                                aria-label="Породы, слагающие полезное ископаемое">
                                <option v-for="o in oreTypes" v-bind:value="o.id" v-bind:key="o.id">
                                  {{ o.description }}
                                </option>
                              </select>
                            </div>


                          </td>
                          <td>
                            <input type="number" class="form-control form-control-md" v-model="lat_ang" />
                          </td>
                          <td>
                            <input type="number" class="form-control form-control-md" v-model="lat_ang" />
                          </td>
                          <td>
                            <input type="number" class="form-control form-control-md" v-model="lat_ang" />
                          </td>
                          <td class="for-btn"><button @click="editItem" class="btn btn-dark btn-md btn-block btn-edit"
                              title="Редактировать запись">
                              <BootstrapIcon icon="pencil" />
                            </button>
                          </td>
                          <td class="for-btn">
                            <button @click="removeItem" class="btn btn-dark btn-md btn-block btn-delete"
                              style="float: left; width: 42px" title="Удалить запись">
                              <BootstrapIcon icon="trash" />
                            </button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                    <button @click="addItem" class="btn btn-dark btn-md btn-block btn-add">
                      <BootstrapIcon icon="plus-square-fill" />
                      Добавить
                    </button>
                    <button data-v-4d803cea="" class="btn btn-dark btn-save"> Сохранить </button>
                  </form>
                </div>
              </div>
              <div class="tab-H04-inner2 inner" v-if="selected_H04_inner2">
                <div class="inner-body">
                  <div class="caption-table">
                    <table>
                      <tr class="tab-data">
                        <th>Объект (название):</th>
                        <td>
                          <input type="text" class="form-control form-control-md" v-model="description"
                            placeholder="Месторождение" disabled />
                        </td>
                      </tr>
                      <tr class="tab-data">
                        <th>Полезное ископаемое:</th>
                        <td>
                          <input type="text" class="form-control form-control-md" v-model="component"
                            placeholder="Полезное ископаемое" disabled />
                        </td>
                      </tr>
                    </table>
                  </div>
                  <form class="form-inline" style="width: calc(100%)">
                    <div class="q-ed-container">
                      <label for="q-editor">4.1. Прочие сведения</label>
                      <QuillEditor theme="snow" toolbar="full" style="height: 300px;" id="q-editor" />
                    </div>
                    <div class="q-ed-container">
                      <label for="q-editor">4.2. Результаты технологических и полузаводских испытаний</label>
                      <QuillEditor theme="snow" toolbar="full" style="height: 600px;" id="q-editor" />
                    </div>
                    <button data-v-4d803cea="" class="btn btn-dark btn-save"> Сохранить </button>
                  </form>
                </div>
              </div>
              <div class="tab-H04-inner3 inner" v-if="selected_H04_inner3">
                <div class="inner-body">
                  <div class="caption-table">
                    <table>
                      <tr class="tab-data">
                        <th>Объект (название):</th>
                        <td>
                          <input type="text" class="form-control form-control-md" v-model="description"
                            placeholder="Месторождение" disabled />
                        </td>
                      </tr>
                      <tr class="tab-data">
                        <th>Полезное ископаемое:</th>
                        <td>
                          <input type="text" class="form-control form-control-md" v-model="component"
                            placeholder="Полезное ископаемое" disabled />
                        </td>
                      </tr>
                    </table>
                  </div>
                  <form class="form-inline" style="width: calc(100%)">
                    <div class="table-container">
                      <table style="width: 100%;">
                        <caption>4.3. Продукция, получаемая из сырья:</caption>
                        <thead>
                          <tr class="tab-data">
                            <th style="width: 50%">Вид</th>
                            <th style="width: 50%;">Сорт или марка</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr class="tab-data">
                            <td>
                              <div class="drpdwn-container">
                                <select class="form-select form-control-md" v-model="selecteOreTypeId"
                                  aria-label="Породы, слагающие полезное ископаемое">
                                  <option v-for="o in oreTypes" v-bind:value="o.id" v-bind:key="o.id">
                                    {{ o.description }}
                                  </option>
                                </select>
                              </div>
                            </td>
                            <td>
                              <input type="text" class="form-control form-control-md" v-model="lat_ang" />
                            </td>
                            <td class="for-btn"><button @click="editItem" class="btn btn-dark btn-md btn-block btn-edit"
                                title="Редактировать запись">
                                <BootstrapIcon icon="pencil" />
                              </button>
                            </td>
                            <td class="for-btn">
                              <button @click="removeItem" class="btn btn-dark btn-md btn-block btn-delete"
                                style="float: left; width: 42px" title="Удалить запись">
                                <BootstrapIcon icon="trash" />
                              </button>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                    <div class="q-ed-container">
                      <label for="q-editor">4.4. Соответствие получаемой продукции требованиям:
                        ГОСТ, ОСТ, ТУ, СНиП и др.
                      </label>
                      <QuillEditor theme="snow" toolbar="full" style="height: 400px;" id="q-editor" />
                    </div>
                    <button data-v-4d803cea="" class="btn btn-dark btn-save"> Сохранить </button>
                  </form>
                </div>
              </div>
            </nav>
          </div>
        </div>
        <!-- H05 -->
        <div class="tab-H05" v-if="selected_H05" style="height: 400px; width: calc(80%); margin: auto"></div>
        <!-- H06 -->
        <div class="tab-H06" v-if="selected_H06" style="height: 400px; width: calc(80%); margin: auto"></div>
        <!-- H07 -->
        <div class="tab-H07" v-if="selected_H07" style="height: 400px; width: calc(80%); margin: auto"></div>
        <!-- H08 -->
        <div class="tab-H08" v-if="selected_H08" style="height: 400px; width: calc(80%); margin: auto"></div>
        <!-- H09-H10 -->
        <div class="tab-H0910" v-if="selected_H0910" style="height: 400px; width: calc(80%); margin: auto"></div>
        <!-- H11 -->
        <div class="tab-H11" v-if="selected_H11" style="height: 400px; width: calc(80%); margin: auto"></div>
        <!-- H12 -->
        <div class="tab-H12" v-if="selected_H12" style="height: 400px; width: calc(80%); margin: auto"></div>
        <!-- H13 -->
        <div class="tab-H13" v-if="selected_H13" style="height: 400px; width: calc(80%); margin: auto"></div>

        <!-- div class="form-group">
          <button @click="saveForm" class="btn btn-dark btn-md btn-block save">
            Сохранить
          </button>
        </div>
        <div class="form-group">
          <button
            @click="selectDeposit"
            class="btn btn-dark btn-md btn-block select"
          >
            Выбраить месторождение
          </button>
        </div -->
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

import OkModal from "../components/OkModal.vue";
import Spinner from "../components/Spinner.vue";
import ExplorationCtrl from "../components/ExplorationCtrl.vue";
import CoordinatesCtrl from "../components/CoordinatesCtrl.vue";
import BootstrapIcon from "@dvuckovic/vue3-bootstrap-icons";

/* Import quill editor */
import { QuillEditor } from "@vueup/vue-quill";
import "@vueup/vue-quill/dist/vue-quill.snow.css";
/* https://vueup.github.io/vue-quill/api/ */

export default {
  name: "ProtocolEditModal",
  props: ["deposit_id", "mine_area_id", "component_id"],
  data() {
    return {
      description: "",
      selected_H01: false,
      selected_H02: false,
      selected_H03: false,
      selected_H04: false,
      selected_H05: false,
      selected_H06: false,
      selected_H07: false,
      selected_H08: false,
      selected_H0910: false,
      selected_H11: false,
      selected_H12: false,
      selected_H13: false,
      selected_title: true,
      showAuthError: false,
      content: "<h1>Initial Content</h1>",
      showSpinner: false,
      showError: false,
      depositInfo: {},
      mineAreaInfo: {},
      dev: "",
      depositDesc: this.description,
      district: "",
      area: "",
      selected_H01_inner1: true,
      selected_H01_inner2: false,
      selected_H01_inner3: false,
      selected_H01_inner4: false,
      selected_H01_inner5: false,
      selected_H01_inner6: false,
      selected_H03_inner1: true,
      selected_H04_inner1: true,
      selected_H04_inner2: false,
      selected_H04_inner3: false,
    };
  },
  methods: {
    saveForm() {
      // Save current form
    },
    hideAuthMessage() {
      this.showAuthError = false;
    },
    selectTab(tab) {
      if (tab == "title") {
        this.selected_title = true;
        this.selected_H01 = false;
        this.selected_H02 = false;
        this.selected_H03 = false;
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

      if (tab == "H01") {
        this.selected_title = false;
        this.selected_H01 = true;
        this.selected_H02 = false;
        this.selected_H03 = false;
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
      if (tab == "H02") {
        this.selected_title = false;
        this.selected_H01 = false;
        this.selected_H02 = true;
        this.selected_H03 = false;
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
      if (tab == "H04") {
        this.selected_title = false;
        this.selected_H01 = false;
        this.selected_H02 = false;
        this.selected_H03 = false;
        this.selected_H04 = true;
        this.selected_H05 = false;
        this.selected_H06 = false;
        this.selected_H07 = false;
        this.selected_H08 = false;
        this.selected_H0910 = false;
        this.selected_H11 = false;
        this.selected_H12 = false;
        this.selected_H13 = false;
      }
      if (tab == "H05") {
        this.selected_title = false;
        this.selected_H01 = false;
        this.selected_H02 = false;
        this.selected_H03 = false;
        this.selected_H04 = false;
        this.selected_H05 = true;
        this.selected_H06 = false;
        this.selected_H07 = false;
        this.selected_H08 = false;
        this.selected_H0910 = false;
        this.selected_H11 = false;
        this.selected_H12 = false;
        this.selected_H13 = false;
      }
      if (tab == "H06") {
        this.selected_title = false;
        this.selected_H01 = false;
        this.selected_H02 = false;
        this.selected_H03 = false;
        this.selected_H04 = false;
        this.selected_H05 = false;
        this.selected_H06 = true;
        this.selected_H07 = false;
        this.selected_H08 = false;
        this.selected_H0910 = false;
        this.selected_H11 = false;
        this.selected_H12 = false;
        this.selected_H13 = false;
      }

      if (tab == "H07") {
        this.selected_title = false;
        this.selected_H01 = false;
        this.selected_H02 = false;
        this.selected_H03 = false;
        this.selected_H04 = false;
        this.selected_H05 = false;
        this.selected_H06 = false;
        this.selected_H07 = true;
        this.selected_H08 = false;
        this.selected_H0910 = false;
        this.selected_H11 = false;
        this.selected_H12 = false;
        this.selected_H13 = false;
      }

      if (tab == "H08") {
        this.selected_title = false;
        this.selected_H01 = false;
        this.selected_H02 = false;
        this.selected_H03 = false;
        this.selected_H04 = false;
        this.selected_H05 = false;
        this.selected_H06 = false;
        this.selected_H07 = false;
        this.selected_H08 = true;
        this.selected_H0910 = false;
        this.selected_H11 = false;
        this.selected_H12 = false;
        this.selected_H13 = false;
      }

      if (tab == "H0910") {
        this.selected_title = false;
        this.selected_H01 = false;
        this.selected_H02 = false;
        this.selected_H03 = false;
        this.selected_H04 = false;
        this.selected_H05 = false;
        this.selected_H06 = false;
        this.selected_H07 = false;
        this.selected_H08 = false;
        this.selected_H0910 = true;
        this.selected_H11 = false;
        this.selected_H12 = false;
        this.selected_H13 = false;
      }

      if (tab == "H11") {
        this.selected_title = false;
        this.selected_H01 = false;
        this.selected_H02 = false;
        this.selected_H03 = false;
        this.selected_H04 = false;
        this.selected_H05 = false;
        this.selected_H06 = false;
        this.selected_H07 = false;
        this.selected_H08 = false;
        this.selected_H0910 = false;
        this.selected_H11 = true;
        this.selected_H12 = false;
        this.selected_H13 = false;
      }

      if (tab == "H12") {
        this.selected_title = false;
        this.selected_H01 = false;
        this.selected_H02 = false;
        this.selected_H03 = false;
        this.selected_H04 = false;
        this.selected_H05 = false;
        this.selected_H06 = false;
        this.selected_H07 = false;
        this.selected_H08 = false;
        this.selected_H0910 = false;
        this.selected_H11 = false;
        this.selected_H12 = true;
        this.selected_H13 = false;
      }

      if (tab == "H13") {
        this.selected_title = false;
        this.selected_H01 = false;
        this.selected_H02 = false;
        this.selected_H03 = false;
        this.selected_H04 = false;
        this.selected_H05 = false;
        this.selected_H06 = false;
        this.selected_H07 = false;
        this.selected_H08 = false;
        this.selected_H0910 = false;
        this.selected_H11 = false;
        this.selected_H12 = false;
        this.selected_H13 = true;
      }

      if (tab == "inner-H01-1") {
        this.selected_H01_inner1 = true;
        this.selected_H01_inner2 = false;
        this.selected_H01_inner3 = false;
        this.selected_H01_inner4 = false;
        this.selected_H01_inner5 = false;
        this.selected_H01_inner6 = false;
      }

      if (tab == "inner-H01-2") {
        this.selected_H01_inner1 = false;
        this.selected_H01_inner2 = true;
        this.selected_H01_inner3 = false;
        this.selected_H01_inner4 = false;
        this.selected_H01_inner5 = false;
        this.selected_H01_inner6 = false;
      }

      if (tab == "inner-H01-3") {
        this.selected_H01_inner1 = false;
        this.selected_H01_inner2 = false;
        this.selected_H01_inner3 = true;
        this.selected_H01_inner4 = false;
        this.selected_H01_inner5 = false;
        this.selected_H01_inner6 = false;
      }

      if (tab == "inner-H01-4") {
        this.selected_H01_inner1 = false;
        this.selected_H01_inner2 = false;
        this.selected_H01_inner3 = false;
        this.selected_H01_inner4 = true;
        this.selected_H01_inner5 = false;
        this.selected_H01_inner6 = false;
      }

      if (tab == "inner-H01-5") {
        this.selected_H01_inner1 = false;
        this.selected_H01_inner2 = false;
        this.selected_H01_inner3 = false;
        this.selected_H01_inner4 = false;
        this.selected_H01_inner5 = true;
        this.selected_H01_inner6 = false;
      }

      if (tab == "inner-H01-6") {
        this.selected_H01_inner1 = false;
        this.selected_H01_inner2 = false;
        this.selected_H01_inner3 = false;
        this.selected_H01_inner4 = false;
        this.selected_H01_inner5 = false;
        this.selected_H01_inner6 = true;
      }

      if (tab == "inner-H04-1") {
        this.selected_H04_inner1 = true;
        this.selected_H04_inner2 = false;
        this.selected_H04_inner3 = false;
      }

      if (tab == "inner-H04-2") {
        this.selected_H04_inner1 = false;
        this.selected_H04_inner2 = true;
        this.selected_H04_inner3 = false;
      }

      if (tab == "inner-H04-3") {
        this.selected_H04_inner1 = false;
        this.selected_H04_inner2 = false;
        this.selected_H04_inner3 = true;
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
    },
  },
  mounted() {
    this.getDepositInfo();
    this.getComponent();
    this.getLandTypes();
    this.getReliefType();
    this.getAvalanchType();
    this.getOrganizations();
    this.getMudflowType();
  },
  components: {
    OkModal,
    Spinner,
    QuillEditor,
    ExplorationCtrl,
    CoordinatesCtrl,
    BootstrapIcon,
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
  overflow: auto;
}

.header {
  height: 30px;
  width: 100%;
  background-color: rgb(150, 143, 146);
  text-align: center;
  font-weight: bold;
}

.body {
  /*font-weight: bolder;*/
  color: black;
  text-align: left;
  padding: 0;
  margin-top: 20px;
  font-family: "Times New Roman", Times, serif;
}

.table> :not(caption)>*>* {
  padding: 0;
}

table {
  padding: 0px !important;
}

.btn-xxs {
  height: 25px;
  width: 25px;
  background-color: rgb(204, 204, 204);
}

.close {
  /*position: relative;*/
  background: none;
  top: 2px;
  display: inline-block;
  height: 25px !important;
  padding-right: 10px;
}

.save {
  /*position: relative;*/
  /*top: 10px;*/
  float: right;
  display: inline-block;
  margin-right: 5px;
  margin-left: 5px;
  height: 25px;
}

.select {
  position: absolute;
  bottom: 10px;
  right: 10px;
}

.nav-link {
  color: #42b883;
}

div {
  padding-bottom: 30px;
  font-weight: bold;
}

label {
  font-weight: bolder;
}

.align-middle {
  display: inline-flex;
  align-items: center;
}

.btn {
  display: inline-flex;
  justify-content: center;
  /* center the content horizontally */
  align-items: center;
  /* center the content vertically */
  --padding-x: 1.2em;
  border-color: transparent;
  /* hide button border */
}
</style>
