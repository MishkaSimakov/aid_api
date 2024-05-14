<template>
  <div class="container-fluid my-3">
    <div class="row">
      <div class="mx-auto col-md-9">
        <h1 class="d-block">{{ $route.params.ticker }}</h1>

        <section>
          <div class="card">
            <div class="card-body">
              <div class="btn-group w-100 mb-3">
                <button
                    v-for="(name, period) in chartPeriodsNames"
                    v-bind:key="period"
                    type="button"
                    class="btn btn-outline-secondary"
                    :class="{ active: selectedPeriod === period }"
                    v-on:click="selectPeriod(period)"
                >
                  {{ name }}
                </button>
              </div>

              <div v-if="isLoading" class="w-100 text-center">
                <div class="mx-auto my-5 spinner-border text-secondary"></div>
              </div>
              <div v-else-if="notEnoughData" class="text-center">
                <p class="mx-auto my-5 text-secondary fw-bold">Недостаточно данных</p>
              </div>

              <Line v-else :data="preparedChartData" :options="options"/>
            </div>
          </div>
        </section>

        <section class="mt-5">
          <h2>Индикаторы</h2>
          <p class="small text-secondary">
            Наши лучшие эксперты предсказывают движение денежных масс специально для вас<br>
            <span class="text-light">(но ответственности никакой не несут)</span>
          </p>

          <div class="row mt-3">
            <div class="col-md-4" v-for="(group, key) in preparedIndicatorsData" v-bind:key="group">
              <div class="text-center w-100">
                <h3 :class="indicatorGroupsParameters[key].className">
                  {{ indicatorGroupsParameters[key].title }}
                </h3>
              </div>

              <ul class="list-group">
                <li
                    v-for="indicator in group"
                    v-bind:key="indicator.id"
                    v-on:click="presentedIndicator = indicator"
                    style="cursor: pointer"
                    class="list-group-item list-group-item-action container">
                  <div class="row">
                    <div class="col-md-8">{{ indicator.name }}</div>
                    <div class="col-md-4 my-auto">{{ indicator.value.toFixed(2) + indicator.postfix }}</div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </section>

        <TickerIndicatorDescriptionModal :presented-indicator="presentedIndicator"
                                         @closed="presentedIndicator = undefined"/>
      </div>
    </div>
  </div>
</template>

<script>
import {createNamespacedHelpers} from "vuex";

const {mapGetters, mapMutations, mapActions, mapState} = createNamespacedHelpers('ticker');

import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  TimeScale,
} from 'chart.js'

import 'chartjs-adapter-moment';
import {Line} from 'vue-chartjs'
import {TickerChartPeriod} from "@/api/api";

ChartJS.register(
    LinearScale,
    TimeScale,
    PointElement,
    LineElement,
    Tooltip,
)

import TickerIndicatorDescriptionModal from "@/components/TickerIndicatorDescriptionModal.vue";

export default {
  name: 'TickerView',
  components: {TickerIndicatorDescriptionModal, Line},
  methods: {
    ...mapMutations(['setIdentifier']),
    ...mapActions(['fetchData', 'fetchIndicatorsData', 'selectPeriod']),
  },
  computed: {
    ...mapGetters(['imageURL', 'preparedChartData', 'preparedIndicatorsData', 'notEnoughData']),
    ...mapState(['isLoading', 'selectedPeriod']),
  },
  data() {
    return {
      options: {
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'month'
            }
          }
        }
      },
      indicatorGroupsParameters: {
        buy: {
          title: 'Покупать',
          className: 'text-success'
        },
        neutral: {
          title: 'Нейтрально',
          className: 'text-secondary'
        },
        sell: {
          title: 'Продавать',
          className: 'text-danger'
        }
      },
      chartPeriodsNames: {
        [TickerChartPeriod.HOUR]: 'час',
        [TickerChartPeriod.DAY]: 'день',
        [TickerChartPeriod.WEEK]: 'неделя',
        [TickerChartPeriod.MONTH]: 'месяц',
        [TickerChartPeriod.YEAR]: 'год',
        [TickerChartPeriod.ALL_TIME]: 'всё',
      },

      indicatorDescriptionModal: undefined,
      presentedIndicator: undefined
    }
  },
  created() {
    this.setIdentifier(this.$route.params.ticker);
    this.fetchData();
    this.fetchIndicatorsData();
  },
}
</script>
