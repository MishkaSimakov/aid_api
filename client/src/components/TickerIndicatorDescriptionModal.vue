<template>
  <div class="modal fade" id="indicatorModal" aria-hidden="true" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <p class="h6 my-auto">{{ presentedIndicator?.name }}</p>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="text-center w-100 mb-3">
            <p class="text-secondary">Наши эксперты считают, что данный тикер, исходя из данного индикатора,</p>
            <p
                class="fw-bold text-uppercase h3"
                :class="indicatorParameters?.className"
            >
              {{ indicatorParameters?.action }}
            </p>
          </div>

          <hr>

          <p class="mt-3" v-html="indicatorParsedDescription"></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {marked} from "marked";
import {Modal} from "bootstrap";

export default {
  name: "TickerIndicatorDescriptionModal",
  props: ['presentedIndicator'],
  computed: {
    indicatorParsedDescription() {
      return marked(this.presentedIndicator?.description ?? "");
    },
    indicatorParameters() {
      if (this.presentedIndicator === undefined) {
        return undefined;
      }

      let verdict = this.presentedIndicator.verdict;
      if (verdict === 0) {
        return this.indicatorVerdictsParameters.neutral;
      }

      if (verdict < 0) {
        return this.indicatorVerdictsParameters.sell;
      }

      return this.indicatorVerdictsParameters.buy;
    }
  },
  data() {
    return {
      modal: undefined,
      indicatorVerdictsParameters: {
        buy: {
          action: 'стоит покупать',
          className: 'text-success',
        },
        neutral: {
          action: 'лучше не трогать',
          className: 'text-secondary',
        },
        sell: {
          action: 'стоит продавать',
          className: 'text-danger',
        },
      }
    }
  },
  emits: ['closed'],
  mounted() {
    this.modal = new Modal(document.getElementById('indicatorModal'), {
      keyboard: true
    });

    document.getElementById('indicatorModal')
        .addEventListener('hidden.bs.modal', (e) => {
          this.$emit('closed');
        });
  },
  watch: {
    presentedIndicator(newValue) {
      console.log(newValue);

      if (this.modal === undefined || newValue === undefined) {
        return;
      }

      this.modal.show();
    },
  }
}
</script>

<style scoped>

</style>
