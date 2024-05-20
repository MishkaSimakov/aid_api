<template>
  <div v-if="state === LoadingState.READY_TO_LOAD || state === LoadingState.LOADING" class="w-100 text-center">
    <slot name="loader">
      <div class="mx-auto my-5 spinner-border text-secondary"></div>
    </slot>
  </div>

  <div v-else-if="state === LoadingState.ERROR" class="text-center">
    <slot name="error">
      <p class="mx-auto my-5 text-danger fw-bold">Ошибка при загрузке данных.</p>
    </slot>
  </div>

  <template v-else>
    <slot name="content"></slot>
  </template>
</template>

<script>
import {LoadingState} from "@/components/loading/LoadingState";

export default {
  computed: {
    LoadingState() {
      return LoadingState
    }
  },
  props: ['state']
}
</script>
