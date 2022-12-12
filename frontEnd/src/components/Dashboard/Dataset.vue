<template>
  <div>
    <div class="header">
      <div class="d-flex align-center">
        <div class="icon-container">
          <DatasetIcon />
        </div>
        <div>
          <h4>{{ dataset.name }}</h4>
          <span class="item-type">Dataset</span>
        </div>
      </div>

      <div class="d-flex justify-end">
        <div class="actions-container" @click="showActions = true" v-click-outside="onClickOutside">
          <span>Actions</span>
          <v-icon class="actions-icon">{{ icons.arrow }}</v-icon>
          <div v-show="showActions" class="actions-content">
            <div @click="analyticsDialog = true" class="actions-content--row">
              <ChartIcon class="mr-2" />
              <span>Open in Visual Analytics</span>
            </div>
            <v-divider></v-divider>
            <router-link :to="{ name: 'dataset-edit', params: { id: this.$route.params.id } }" tag="div"
              class="actions-content--row">
              <EditIcon class="mr-2" />
              <span>Edit</span>
            </router-link>
            <v-divider></v-divider>
            <div @click="dialog = true" class="actions-content--row">
              <PublishIcon class="mr-2" />
              <span>Publish</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="content">
      <Report />

      <v-dialog v-model="dialog" max-width="600">
        <v-card>
          <v-card-title class="headline">
            Publish dataset
            <v-icon @click="handleClose" class="close-icon">{{ icons.close }}</v-icon>
          </v-card-title>

          <v-divider></v-divider>

          <v-card-text>
            <div class="publish-container">
              <p class="description">This dataset was published before. Choose what you want to do:</p>
              <div class="offering">
                <img src="@/assets/publish_icon.png" alt="icon" />
                <p class="offering--description">Publish as new offering</p>
              </div>
            </div>
          </v-card-text>

          <v-divider></v-divider>
          <div class="upload-controls">
            <button class="button cancel" @click="handleClose">Cancel</button>
            <button class="button submit" @click="handleNext">
              <span>Next</span>
            </button>
          </div>
        </v-card>
      </v-dialog>

      <v-dialog v-model="analyticsDialog" max-width="600">
        <v-card>
          <v-card-title class="headline">
            Open in Visual Analytics
            <v-icon @click="analyticsDialog = false" class="close-icon">{{ icons.close }}</v-icon>
          </v-card-title>

          <v-divider></v-divider>

          <v-card-text>
            <div class="form-group">
              <label for="analytics-name">Name</label>
              <input type="text" class="field" placeholder="Visual Analytics name" id="analytics-name"
                v-model="analyticsName">
            </div>
          </v-card-text>

          <v-divider></v-divider>
          <div class="upload-controls">
            <button class="button submit" :disabled="!analyticsName || isCreatingVA">
              <span v-if="isCreatingVA">Loading...</span>
              <span v-else>Submit</span>
            </button>
          </div>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script>
import vClickOutside from 'v-click-outside';
import { getDataset, getDatasetSample } from '@/api_client.js';
import { mdiClose, mdiChevronDown } from "@mdi/js";
import DatasetIcon from '@/assets/icons/dataset.svg';
import ChartIcon from '@/assets/icons/chart.svg';
import EditIcon from '@/assets/icons/edit.svg';
import PublishIcon from '@/assets/icons/publish.svg';
import Report from './Report';

export default {
  name: "Dataset",
  props: ['id'],
  directives: {
    clickOutside: vClickOutside.directive,
  },
  components: {
    DatasetIcon,
    PublishIcon,
    ChartIcon,
    Report,
    EditIcon,
  },
  data() {
    return {
      tab: null,
      dataset: {},
      dialog: false,
      analyticsDialog: false,
      analyticsName: '',
      icons: {
        close: mdiClose,
        arrow: mdiChevronDown,
      },
      showActions: false,
      raport: {
        data: {
          memory_size: {},
          types: {}
        },
        isLoading: true
      },
      isCreatingVA: false,
    }
  },
  methods: {
    // handleCreate() {
    //   this.isCreatingVA = true;

    //   getMyIP()
    //     .then(response => {
    //       getTableauToken(response.data)
    //         .then(() => {
    //           createVA({ dataset: this.$route.params.id, name: this.analyticsName })
    //             .then(() => {
    //               this.isCreatingVA = false;
    //               this.$router.push({
    //                 name: 'analytics-edit',
    //                 params: { name: this.analyticsName },
    //               });
    //             })
    //             .catch(error => {
    //               this.isCreatingVA = false;
    //               console.error(error);
    //             });
    //         });
    //     });
    // },
    handleClose() {
      this.dialog = false;
    },
    handleNext() {
      this.$router.push({ name: 'dataset-publish', params: { id: this.$route.params.id } })
    },
    onClickOutside() {
      this.showActions = false;
    }
  },
  created() {
    this.raport.isLoadind = true;

    getDataset(this.$route.params.id)
      .then(({ data }) => this.dataset = data[0])
      .catch(error => console.error(error))

    getDatasetSample(this.$route.params.id)
      .then(({ data }) => data)
      .catch(error => console.error(error))
  }
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

  .actions-container {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #333333;
    color: #ffffff;
    cursor: pointer;
    max-width: 120px;
    position: relative;
    border-radius: 4px;
    box-shadow: 0 5px 7px 0 rgba(94, 130, 245, 0.24);
    background-image: linear-gradient(to right, #2f6bff, #5e82f5);
    padding: 8px 16px;
    font-weight: bold;
    font-size: 14px;

    .actions-icon {
      color: #ffffff;
    }

    .actions-content {
      background-color: #ffffff;
      position: absolute;
      min-width: 240px;
      padding: 10px;
      box-shadow: 0px 0px 10px rgba(138, 138, 138, 0.349019607843137);
      top: 100%;
      z-index: 1;
      margin-top: 10px;
      right: 0;
      border-radius: 5px;

      &--row {
        color: #5f5f5f;
        display: flex;
        align-items: center;
        padding: 8px 0;

        img {
          margin-right: 10px;
        }
      }
    }
  }
}

.content {
  width: 100%;
  height: 100%;
  padding: 30px;

  .subtitle {
    color: #0a1448;
    ;
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
  }


  h1 {
    color: #5f5f5f;
    margin-left: 10px;
  }


  .overview {
    background-color: #f4f6fa;
    display: flex;
    flex-direction: column;
  }

  .details {
    display: flex;
    flex-direction: column;
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
}

.publish-container {
  display: flex;
  flex-direction: column;
  padding-top: 20px;

  .offering {
    align-self: center;
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;
    width: 200px;
    height: 200px;
    border-radius: 5px;
    box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.125490196078431);
    cursor: pointer;

    &--description {
      font-weight: bold;
    }
  }
}

.close-icon {
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
}

.upload-controls {
  display: flex;
  justify-content: flex-end;
  padding: 10px 20px;

  .button {
    border-radius: 5px;
    padding: 4px 10px;
    outline: none;
    font-weight: bold;
    font-size: 14px;

    &.submit {
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #333333;
      color: #ffffff;
      cursor: pointer;
      max-width: 120px;
      position: relative;
      border-radius: 4px;
      box-shadow: 0 5px 7px 0 rgba(94, 130, 245, 0.24);
      background-image: linear-gradient(to right, #2f6bff, #5e82f5);
      padding: 8px 16px;

      &:disabled {
        opacity: 0.6;
        cursor: not-allowed;
      }
    }

    &.cancel {
      background: #f5f5f5;
      color: #000000;
      margin: 0 10px;
    }
  }
}

.form-group {
  margin: 20px 0 0 0;
  display: flex;
  flex-direction: column;

  label {
    color: #5F5F5F;
    font-weight: bold;
    margin: 0 0 6px 0;
  }

  .field {
    border: 1px solid #d7d7d7;
    border-radius: 4px;
    padding: 14px;
    outline: none;
  }

  .error-input {
    border: 1px solid #ff5252;
  }

  .error-label {
    color: #ff5252;
    margin: 4px 0 0 0;
  }
}
</style>
