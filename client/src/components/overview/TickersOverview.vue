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
    this.scene = animate('tickers-overview', this.tickers, this.indices, this.$router);
    this.scene?.transitionTo(this.focus ?? 'MOEXIT', 0);
  },
  watch: {
    focus(newFocus) {
      console.log(newFocus)
      this.scene?.transitionTo(newFocus, 1000);
    }
  }
}
</script>
