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
                    v-for="(parameters, period) in TickerChartPeriod"
                    v-bind:key="period"
                    type="button"
                    class="btn btn-outline-secondary"
                    :class="{ active: selectedPeriod.alias === parameters.alias }"
                    v-on:click="selectPeriod(parameters)"
                >
                  {{ parameters.name }}
                </button>
              </div>

              <LoadingWrapper :state="chartLoadingState">
                <template v-slot:content>
                  <Line :data="preparedChartData" :options="chartOptions"/>
                </template>
              </LoadingWrapper>
            </div>
          </div>
        </section>

        <section class="mt-5">
          <h2>Индикаторы</h2>
          <p class="small text-secondary">
            Наши лучшие эксперты предсказывают движение денежных масс специально для вас<br>
            <span class="text-light">(но ответственности никакой не несут)</span>
          </p>

          <LoadingWrapper :state="indicatorsLoadingState">
            <template v-slot:content>
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
            </template>
          </LoadingWrapper>
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

import moment from 'moment';
import 'moment/locale/ru'

moment.locale('ru')

import {Line} from 'vue-chartjs'

ChartJS.register(
    LinearScale,
    TimeScale,
    PointElement,
    LineElement,
    Tooltip,
)

import TickerIndicatorDescriptionModal from "@/components/TickerIndicatorDescriptionModal.vue";
import LoadingWrapper from "@/components/loading/LoadingWrapper.vue";
import {TickerChartPeriod} from "@/api/TickerChartPeriod";

export default {
  name: 'TickerView',
  components: {LoadingWrapper, TickerIndicatorDescriptionModal, Line},
  methods: {
    ...mapMutations(['setIdentifier']),
    ...mapActions(['fetchData', 'fetchIndicatorsData', 'selectPeriod']),
  },
  computed: {
    TickerChartPeriod() {
      return TickerChartPeriod
    },
    ...mapGetters(['imageURL', 'preparedChartData', 'preparedIndicatorsData']),
    ...mapState(['chartLoadingState', 'indicatorsLoadingState', 'selectedPeriod']),
    chartOptions() {
      return {
        scales: {
          x: {
            type: 'time',
            time: {
              unit: this.selectedPeriod.unit,
              displayFormats: {
                minute: 'HH:mm DD MMM',
                hour: 'HH:mm DD MMM',
                day: 'LL',
                week: 'LL'
              }
            }
          }
        },
        plugins: {
          tooltip: {
            displayColors: false,
            callbacks: {
              label: (value) => {
                return `Цена при открытии: ${value.parsed.y}₽`;
              },
            }
          }
        }
      };
    },
  },
  data() {
    return {
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
