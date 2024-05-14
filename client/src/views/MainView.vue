<template>
  <LoadingWrapper :state="loadingState">
    <template v-slot:content>
      <TickersOverview
          :tickers="tickers"
          :indices="indices"
      >
      </TickersOverview>
    </template>
  </LoadingWrapper>
</template>

<script>
import {createNamespacedHelpers} from "vuex";
import TickersOverview from "@/components/overview/TickersOverview.vue";
import LoadingWrapper from "@/components/loading/LoadingWrapper.vue";

const {mapState} = createNamespacedHelpers('companies');

export default {
  name: 'MainView',
  components: {LoadingWrapper, TickersOverview},
  computed: {
    ...mapState(['loadingState', 'tickers', 'indices']),
  },
  mounted() {
    this.$store.dispatch('companies/fetchData');
  }
}
</script>
