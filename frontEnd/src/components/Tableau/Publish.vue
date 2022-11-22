<template>
  <div class="content">
    <div class="header">
      <router-link :to="{ name: 'analytics'}" class="link">
        <v-icon>{{ icons.chevron }}</v-icon>
        <span>Back to visual analytics</span>
      </router-link>
      <v-row>
        <v-col class="d-flex justify-space-between align-center">
          <h1>Publish Visual Analytics</h1>
          <button @click="handleSubmit" class="button submit" :disabled="!isValidStepOne">Next</button>
        </v-col>
      </v-row>
    </div>
    <div class="publish-content">
      <v-row>
        <v-col cols="12">
          <v-row>
            <v-col cols="6">
              <div class="form-container">
                <div class="form-group">
                  <h4 class="form-title">Title</h4>
                  <input type="text" class="input-field" v-model="title" />
                </div>
                <div class="form-group">
                  <h4 class="form-title">Brief Description</h4>
                  <textarea class="area-field" v-model="briefDescription"></textarea>
                </div>
                <div class="form-group">
                  <h4 class="form-title">Description</h4>
                  <textarea class="area-field" v-model="description" rows="4"></textarea>
                </div>
                <div class="form-group">
                  <h4 class="form-title">Tags</h4>
                  <v-combobox
                    v-model="select"
                    :items="items"
                    multiple
                    chips
                    deletable-chips
                    class="tags"
                  ></v-combobox>
                </div>
                <div class="form-group">
                  <h4 class="form-title">Version notes</h4>
                  <textarea class="area-field" v-model="versionNotes" rows="4"></textarea>
                </div>
              </div>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
      <v-overlay :value="isLoading">
        <v-progress-circular indeterminate size="64"></v-progress-circular>
      </v-overlay>
    </div>
  </div>
</template>

<script>
  import { mdiChevronLeft } from '@mdi/js'
  import { publishOffering } from '@/api_client.js';

  export default {
    name: "PublishTableau",
    data() {
      return {
        title: '',
        description: '',
        briefDescription: '',
        version: '1.0',
        versionNotes: '',
        icons: {
          chevron: mdiChevronLeft,
        },
        isPublic: false,
        agencies: false,
        sector: false,
        select: [],
        items: [
          'Datasets',
          'Regressions',
        ],
        radios: 'subscription',
        isLoading: false,
      }
    },
    computed: {
      isValidStepOne() {
        return this.title && this.description && this.briefDescription;
      },
    },
    methods: {
      handleSubmit() {
        this.isLoading = true;
        const payload = {
          title: this.title,
          briefDescription: this.briefDescription,
          description: this.description,
          tags: [{ name: 'Datasource' }],
          price: "0",
          item: null,
          va: this.$route.params.id
        };

        publishOffering(payload)
          .then(({ data }) => {
            this.isLoading = false;
            this.$router.push({ name: 'va-offering', params: { id: data.id} });
          })
          .catch(error => {
            this.isLoading = false;
            console.error(error);
          })
      },
    },
  }
</script>

<style scoped lang="scss">
  .content {
    width: 100%;
    height: 100%;
    background-color: #f3f3f3;

    h1 {
      color: #5f5f5f;
    }

    .tabs {

    }

    .link {
      color: #5f5f5f;
      text-decoration: none;
    }
  }

  .step-title {
    color: #5f5f5f;
  }

  .form-container {
    box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.125490196078431);
    border-radius: 5px;
    padding: 20px;
    background-color: #ffffff;

    .form-group {
      margin-bottom: 20px;

      .form-title {
        color: #5f5f5f;
      }

      .input-field {
        border: 1px solid #d7d7d7;
        border-radius: 4px;
        width: 100%;
        padding: 4px 10px;
        outline: none;
        margin-top: 6px;
      }

      .area-field {
        border: 1px solid #d7d7d7;
        border-radius: 4px;
        width: 100%;
        padding: 4px 10px;
        outline: none;
        margin-top: 6px;
        resize: none;
      }
    }
  }

  .header {
    box-shadow: rgba(0, 0, 0, 0.047) 0px 5px 5px;
    padding: 30px;
  }

  .button {
    border-radius: 5px;
    padding: 4px 18px;
    outline: none;
    height: 32px;
    font-weight: bold;

    &.next {
      background: #000000;
      color: #ffffff;
    }

    &.cancel {
      background: #dddddd;
      color: #000000;
      margin: 0 10px;
    }

    &.submit {
      background-color: #0029e6;
      color: #ffffff;
    }

    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
  }

  .publish-content {
    padding: 30px;
  }
</style>
