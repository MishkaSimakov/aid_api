const {defineConfig} = require('@vue/cli-service')
const path = require("path");

module.exports = defineConfig({
    transpileDependencies: true,
    chainWebpack: (config) => {
        config.plugin('define').tap((definitions) => {
            Object.assign(definitions[0], {
                __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: 'false'
            })
            return definitions
        })
    }
})
