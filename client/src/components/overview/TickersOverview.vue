<template>
  <canvas id="tickers-overview" class="m-0 p-0 flex-grow-1"></canvas>
</template>

<script>

import {animate} from "@/components/overview/animation";

export default {
  name: "TickersOverview",
  props: ['tickers', 'indices', 'focus'],
  data() {
    return {
      scene: undefined,
    }
  },
  mounted() {
    // TODO: focus
    this.$watch(
        () => this.$route.query.index,
        newIndex => {
          this.scene?.transitionTo(newIndex, 1000);
        }
    )

    this.scene = animate('tickers-overview', this.tickers, this.indices, this.$router);
    // this.scene?.transitionTo(this.$route.query.index ?? 'MOEX10', 0);
  },
}
</script>

<style scoped>

</style>
