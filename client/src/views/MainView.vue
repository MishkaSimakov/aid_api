<template>
  <div v-if="loadingState === LoadingState.LOADING" class="flex-grow-1 d-flex flex-column">
    <div class="mx-auto my-auto spinner-border text-secondary"></div>
  </div>
  <TickersOverview
      v-else-if="loadingState === LoadingState.SUCCESS"
      :tickers="tickers"
      focus="MOEX10"
      :indices="indices"
  >
  </TickersOverview>
  <div v-else class="flex-grow-1 d-flex flex-column">
    <div class="mx-auto my-auto text-danger fw-bold">Ошибка при загрузке данных с сервера</div>
  </div>
</template>

<script>
import {createNamespacedHelpers} from "vuex";
import TickersOverview from "@/components/overview/TickersOverview.vue";
import {LoadingState} from "@/store/companies";

const {mapState} = createNamespacedHelpers('companies');

export default {
  name: 'MainView',
  components: {TickersOverview},
  computed: {
    LoadingState() {
      return LoadingState
    },

    ...mapState(['loadingState', 'tickers', 'indices']),
  },
  mounted() {
    this.$store.dispatch('companies/fetchData');
  }
}
</script>
