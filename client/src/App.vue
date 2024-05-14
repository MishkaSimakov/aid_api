<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <RouterLink to="/" class="navbar-brand">💰 Финансы</RouterLink>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
              aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown"
               aria-expanded="false">
              Индексы
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <template v-if="isLoadingIndices">
                <li class="text-center w-100 dropdown-item disabled">
                  <div class="spinner-border text-secondary"></div>
                </li>
              </template>
              <template v-else-if="loadingState === LoadingState.ERROR">
                <li class="text-center w-100 dropdown-item disabled text-danger">
                  Не удалось загрузить индексы
                </li>
              </template>
              <template v-else>
                <li v-for="index in indices" v-bind:key="index.id">
                  <RouterLink class="dropdown-item" :to="getIndexURL(index)">{{ index.id }}</RouterLink>
                </li>
              </template>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <RouterView></RouterView>
</template>

<script>
import {createNamespacedHelpers} from "vuex";
import {LoadingState} from "@/store/companies";

const {mapState} = createNamespacedHelpers('companies');

export default {
  name: 'App',
  computed: {
    LoadingState() {
      return LoadingState;
    },
    isLoadingIndices() {
      return this.loadingState === LoadingState.LOADING || this.loadingState === LoadingState.READY_TO_LOAD;
    },

    ...mapState(['loadingState', 'indices']),
  },
  methods: {
    getIndexURL(index) {
      return `/?index=${index.id}`;
    }
  },
  mounted() {
    this.$store.dispatch('companies/fetchData');
  }
}
</script>

