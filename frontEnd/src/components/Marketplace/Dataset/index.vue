<template>
  <div class="content">
    <v-row>
      <v-col cols="12">
        <div class="header">
          <Icon />
          <h1>{{ item.data.title }}</h1>
          <Label>
            <span v-if="item.data.va">Visual Analytics</span>
            <span v-else>Dataset</span>
          </Label>
        </div>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="8">
        <v-tabs color="#3e3e3e" v-model="tab">
          <v-tab key="overview">Overview</v-tab>
          <v-tab key="variables">Variables</v-tab>
        </v-tabs>

        <v-tabs-items v-model="tab">
          <v-tab-item key="overview">
            <h3 class="subtitle">Description:</h3>
            <p class="description">
              {{ item.data.description }}
            </p>
            <h3 class="subtitle">Variables types</h3>
            <div class="variables-types">
              <div class="variables-row">
                <span>Numeric</span>
                <span>13</span>
              </div>
              <div class="variables-row">
                <span>Categorical</span>
                <span>4</span>
              </div>
              <div class="variables-row">
                <span>Boolean</span>
                <span>5</span>
              </div>
              <div class="variables-row">
                <span>Date</span>
                <span>0</span>
              </div>
              <div class="variables-row">
                <span>Text (Unique)</span>
                <span>0</span>
              </div>
              <div class="variables-row">
                <span>Rejected</span>
                <span>0</span>
              </div>
              <div class="variables-row">
                <span>Unsupported</span>
                <span>0</span>
              </div>
            </div>
            <div class="divider"></div>
            <h3 class="subtitle">Data sample</h3>
            <DataSampleTable />
            <div class="divider"></div>
            <h3 class="subtitle">You may also like:</h3>
            <Recommended />
          </v-tab-item>
        </v-tabs-items>
      </v-col>
      <v-col cols="4">
        <Subscription :id="this.$route.params.id"/>
      </v-col>
    </v-row>
  </div>
</template>

<script>
  import Icon from '@/components/Icon';
  import Label from '@/components/Label';
  import Recommended from '@/components/Recommended';
  import Subscription from '@/components/Subscription';
  import { getMarketplaceOfferingById } from '@/api_client.js';
  import DataSampleTable from "@/components/Dashboard/DataSampleTable";

  export default {
    name: "Dataset",
    components: {
      Icon,
      Label,
      Recommended,
      Subscription,
      DataSampleTable,
    },
    data() {
      return {
        tab: null,
        item: {
          data: {},
          isLoading: false,
        },
      }
    },
    created() {
      this.item.isLoading = true;

      getMarketplaceOfferingById(this.$route.params.id)
        .then(({ data }) => {
          this.item.isLoading = false;
          this.item.data = data[0] || {};
        })
        .catch((error) => {
          this.item.isLoading = false;
          console.error(error);
        })
    },
  }
</script>

<style scoped lang="scss">
  .content {
    width: 100%;
    height: 100%;
    padding: 30px;

    .header {
      display: flex;
      align-items: center;

      h1 {
        color: #5f5f5f;
        margin: 0 20px 0 10px;
      }
    }

    .subtitle {
      color: #5F5F5F;
      margin: 30px 0 20px 0;
    }

    .description {
      background: #ffffff;
      border-radius: 4px;
      padding: 20px;
      display: flex;
      justify-content: center;
      word-wrap: break-word;
    }

    .variables-types {
      display: flex;
      flex-direction: column;
      max-width: 200px;

      .variables-row {
        display: flex;
        justify-content: space-between;
      }
    }

    .divider {
      border-top: 1px solid #c7c7c7;
      margin-top: 30px;
    }
  }
</style>
