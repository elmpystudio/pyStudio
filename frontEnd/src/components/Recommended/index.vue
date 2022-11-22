<template>
  <div class="recommended-container">
    <div class="recommended-row" v-for="item in items" :key="item.id">
      <div class="description-container">
        <DatasetIcon />
        <span class="description ml-4">{{ item.description }}</span>
      </div>
      <span class="recommended-link">
        View report <v-icon>{{ icons.arrow }}</v-icon>
      </span>
    </div>
  </div>
</template>

<script>
  import { mdiChevronRight } from '@mdi/js'
  import DatasetIcon from '@/assets/icons/dataset.svg';

  export default {
    name: "Recommended",
    components: {
      DatasetIcon,
    },
    data() {
      return {
        items: [
          { id: 1, description: 'Small car sales in Canada' },
          { id: 2, description: 'Small car sales in the Nordic Countries' },
          { id: 3, description: 'Small car sales in Australia' },
          { id: 4, description: 'Small car sales in the USA' },
        ],
        icons: {
          arrow: mdiChevronRight,
        }
      }
    }
  }
</script>

<style scoped lang="scss">
  .recommended-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    background: #ffffff;
    border-radius: 4px;
    padding: 26px;
    color: #38406a;
    font-size: 16px;
    line-height: 1.77;
    box-shadow: 0 13px 9px 0 rgba(234, 237, 244, 0.67);

    .recommended-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: #5F5F5F;
      padding: 10px 0;
      border-bottom: 1px solid #c7c7c7;

      .description-container {
        display: flex;
        align-items: center;

        .description {
          font-weight: bold;
        }
      }

      .recommended-link {
        font-size: 16px;
        cursor: pointer;
      }
    }
  }
</style>
