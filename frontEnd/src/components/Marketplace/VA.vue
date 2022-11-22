<template>
  <div>
    <div class="header">
      <div class="d-flex align-center">
        <div class="icon-container">
          <MarketplaceIcon />
        </div>
        <div>
          <h4>{{ item.data.title }}</h4>
          <span class="item-type">{{ item.data.type }}</span>
        </div>
      </div>

      <v-tabs class="tabs" slider-color="#2f6bff" slider-size="3" color="#0a1448" v-model="tab">
        <v-tab key="overview">Overview</v-tab>
        <v-tab key="versions">Versions</v-tab>
        <v-tab key="reviews">Reviews</v-tab>
      </v-tabs>
    </div>

    <div class="content">
      <v-row>
        <v-col cols="8">
          <v-tabs-items v-model="tab">
            <v-tab-item key="overview">
              <v-row>
                <v-col cols="8">
                  <div>
                    <DescriptionIcon />
                    <span class="subtitle">Description</span>
                    <div class="description">{{ item.data.description }}</div>
                  </div>
                </v-col>
              </v-row>

              <div class="divider"></div>

              <div>
                <img class="va-screen" src="@/assets/va-screen.png" alt="Screen">
              </div>

              <div class="divider"></div>
            </v-tab-item>
            <v-tab-item key="versions">
              <Versions />
            </v-tab-item>
            <v-tab-item key="reviews">
              <Reviews />
            </v-tab-item>
          </v-tabs-items>

          <div>
            <ShareIcon />
            <span class="subtitle">You may also like</span>
            <div class="mt-6">
              <Recommended />
            </div>
          </div>
        </v-col>
        <v-col cols="4">
          <div class="details-card">
            <div class="details-card--row d-flex justify-space-between align-center">
              <div class="stars-container">
                <span class="stars-number">5.0</span>
                <v-icon class="star active">{{ icons.star }}</v-icon>
                <v-icon class="star active">{{ icons.star }}</v-icon>
                <v-icon class="star active">{{ icons.star }}</v-icon>
                <v-icon class="star active">{{ icons.star }}</v-icon>
                <v-icon class="star active">{{ icons.star }}</v-icon>
              </div>
              <span class="reviews">36 reviews</span>
            </div>

            <v-divider></v-divider>

            <div class="details-card--row d-flex justify-space-between align-center">
              <div class="details-key">Released</div>
              <div class="details-value">12.02.2019</div>
            </div>
            <div class="details-card--row d-flex justify-space-between align-center">
              <div class="details-key">Size:</div>
              <div class="details-value">6 Mb</div>
            </div>

            <v-divider></v-divider>

            <div class="details-card--row d-flex justify-space-between align-center">
              <div class="details-key">Language</div>
              <div class="details-value">English</div>
            </div>
            <div class="details-card--row d-flex justify-space-between align-center">
              <div class="details-key">Tags</div>
              <div class="details-value">
                <div :key="tag.name" class="tag" v-for="tag in item.data.tags">{{ tag.name }}</div>
              </div>
            </div>
            <div class="details-card--row d-flex justify-space-between align-start">
              <img class="logo" src="@/assets/ministry.png" alt="icon">
              <div class="ml-3">
                <div class="details-title">Ministry of Interior</div>
                <div class="details-description">Argentina is a high income country with was slower and real GDP per capita at US$5,418 was higher than average in 2018. Fitch Solutions rates the overall operational risk of Argentina.</div>
              </div>
            </div>
          </div>
          <div class="mt-4">
            <Subscription :id="this.$route.params.id"/>
          </div>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
  import { mdiStar } from '@mdi/js'
  import MarketplaceIcon from '@/assets/icons/marketplace_details.svg';
  import DescriptionIcon from '@/assets/icons/description.svg';
  import ShareIcon from '@/assets/icons/share.svg';
  import Recommended from '@/components/Recommended';
  import Subscription from '@/components/Subscription';
  import { getMarketplaceOfferingById } from '@/api_client.js';
  import Reviews from '@/components/Reviews';
  import Versions from './Versions';

  export default {
    name: "VAOffering",
    components: {
      Recommended,
      Subscription,
      MarketplaceIcon,
      DescriptionIcon,
      ShareIcon,
      Reviews,
      Versions,
    },
    data() {
      return {
        tab: null,
        icons: {
          star: mdiStar,
        },
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
  .header {
    position: relative;
    padding: 30px 30px 0 30px;
    background-color: #ffffff;

    .icon-container {
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 4px;
      background-color: #e7eeff;
      padding: 10px;
      margin-right: 18px;
      height: 48px;
      width: 48px;
    }

    h4 {
      color: #0a1448;
      font-size: 28px;
    }

    .item-type {
      color: #858ba0;
      font-weight: bold;
    }

    .tabs {
      margin-top: 30px;

      .v-tab {
        text-transform: capitalize;
        color: #858ba0;
        font-weight: 500;
        font-size: 16px;

        &--active {
          color: #0a1448;
        }
      }
    }
  }

  .content {
    width: 100%;
    height: 100%;
    padding: 30px;

    .va-screen {
      width: 100%;
      margin: 30px 0;
    }

    .subtitle {
      color: #0a1448;;
      font-size: 20px;
      font-weight: 500;
      margin-left: 10px;
    }

    .description {
      background: #ffffff;
      border-radius: 4px;
      padding: 26px;
      margin-top: 20px;
      display: flex;
      color: #38406a;
      font-size: 13px;
      line-height: 1.77;
      box-shadow: 0 13px 9px 0 rgba(234, 237, 244, 0.67);
      min-height: 150px;
      word-break: break-all;
    }

    .variables-types {
      display: flex;
      width: 100%;
      flex-direction: column;

      .variables-row {
        display: flex;
        justify-content: space-between;

        .variables-key,
        .variables-value {
          display: flex;
          flex: 1;
        }

        .variables-value {
          color: #0a1448;
          font-weight: bold;
          padding-left: 10px;
        }
      }
    }

    .details-card {
      border-radius: 5px;
      background-color: #ffffff;
      box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.125490196078431);

      &--row {
        padding: 20px;

        .tag {
          color: #858ba0;
          font-size: 13px;
          border-radius: 3px;
          background-color: #f4f6fa;
          padding: 2px 8px;
          margin: 6px 6px 0 0;
        }

        .logo {
          width: 60px;
        }

        .details-title {
          color: #0a1448;
          font-weight: bold;
        }

        .details-key {
          display: flex;
          flex: 2;
        }

        .details-value {
          display: flex;
          flex-wrap: wrap;
          color: #0a1448;
          font-weight: bold;
          padding-left: 10px;
          flex: 3;
        }
      }

      .stars-container {
        display: flex;
        align-items: center;

        .stars-number {
          font-size: 24px;
          font-weight: bold;
          margin-right: 10px;
        }

        .star {
          width: 16px;
          color: #c5c5c5;

          &.active {
            color: #000000;
          }
        }
      }

      .reviews {
        color: #2D2D2D;
        font-size: 13px;
      }
    }
  }

  .theme--light.v-tabs-items {
    background-color: transparent;
  }
</style>
