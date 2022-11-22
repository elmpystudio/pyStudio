<template>
  <v-timeline dense clipped>
    <v-timeline-item
      v-for="(version, i) in versions"
      :key="i"
      :color="version.color"
      left
    >
      <div class="py-4">
        <v-card class="elevation-2">
          <v-card-title class="headline">{{ version.title }}</v-card-title>
          <v-card-text>
            {{ version.description }}
          </v-card-text>
        </v-card>
      </div>
    </v-timeline-item>
  </v-timeline>
</template>

<script>
  export default {
    name: "Versions",
    data() {
      return {
        versions: [
          {
            color: '#2f6bff',
            year: '12.09.2019',
            title: 'Version 3.0',
            description: 'Fitch Solutions rates the overall operational risk of Argentina with 47.8 in 2019, meaning the risk decreased compared to the previous year. Find out more about Argentina in our report focusing on the general economy, trade and investment, society, consumers, retail and eCommerce markets, infrastructure, and politics.',
          },
          {
            color: '#2f6bff',
            year: '30.07.2019',
            title: 'Version 2.0',
            description: 'Fitch Solutions rates the overall operational risk of Argentina with 47.8 in 2019, meaning the risk decreased compared to the previous year. Find out more about Argentina in our report focusing on the general economy, trade and investment, society, consumers, retail and eCommerce markets, infrastructure, and politics.',
          },
          {
            color: '#2f6bff',
            year: '01.07.2019',
            title: 'Version 1.0',
            description: 'Fitch Solutions rates the overall operational risk of Argentina with 47.8 in 2019, meaning the risk decreased compared to the previous year. Find out more about Argentina in our report focusing on the general economy, trade and investment, society, consumers, retail and eCommerce markets, infrastructure, and politics.',
          },
        ],
      }
    },
  }
</script>

<style scoped lang="scss">
</style>
