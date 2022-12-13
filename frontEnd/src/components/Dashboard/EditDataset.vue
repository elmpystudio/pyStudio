<template>
  <div>
    <div class="header">
      <router-link :to="{ name: 'dataset', params: { id: this.$route.params.id }}" class="link">
        <v-icon>{{ icons.chevron }}</v-icon>
        <span>Back to dataset</span>
      </router-link>
      <v-row>
        <v-col class="d-flex justify-space-between align-center">
          <h1>Edit dataset description</h1>
          <div class="d-flex">
            <button @click="handleSubmit" class="button submit">Save</button>
          </div>
        </v-col>
      </v-row>
    </div>

    <div class="content">
      <div class="publish-content">
        <v-row>
          <v-col cols="6">
            <div class="form-container">
              <div class="form-group">
                <h4 class="form-title">Dataset title</h4>
                <input type="text" class="input-field" v-model="name" />
              </div>
            </div>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="6">
            <div class="form-container">
              <div class="form-group">
                <h4 class="form-title">Description</h4>
                <textarea class="area-field" v-model="description" rows="4"></textarea>
              </div>
            </div>
          </v-col>
        </v-row>
        <v-overlay :value="isLoading">
          <v-progress-circular indeterminate size="64"></v-progress-circular>
        </v-overlay>
      </div>
    </div>
  </div>
</template>

<script>
  import { mdiChevronLeft } from '@mdi/js'
  import { updateDataset, getDataset } from '@/api_client.js';

  export default {
    name: "EditDataset",
    components: {
    },

    data() {
      return {
        name: '',
        description: '',
        icons: {
          chevron: mdiChevronLeft,
        },
        isLoading: false,
      }
    },
    created() {
      getDataset(this.$route.params.id)
        .then(({ data }) => {
          this.name = data[0].name || '';
          this.description = data[0].description || '';
        })
        .catch(error => console.error(error))
    },
    methods: {
      handleSubmit() {
        this.isLoading = true;
        const payload = {
          name: this.name,
          description: this.description,
        };

        updateDataset(this.$route.params.id, payload)
          .then(() => {
            this.isLoading = false;
            this.$router.push({ name: 'dataset', params: { id: this.$route.params.id }});
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
  .header {
    padding: 30px 30px 0 30px;
    position: relative;
    background-color: #ffffff;

    h1 {
      font-size: 28px;
      font-weight: bold;
      color: #0a1448;
    }
  }

  .content {
    width: 100%;
    height: 100%;

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
      .form-title {
        color: #0a1448;
        font-size: 18px;
        font-weight: 500;
      }

      .input-field {
        border-radius: 4px;
        border: solid 1px #dee3ed;
        width: 100%;
        padding: 4px 10px;
        outline: none;
        margin-top: 6px;
      }

      .area-field {
        border: 1px solid #dee3ed;
        border-radius: 4px;
        width: 100%;
        padding: 4px 10px;
        outline: none;
        margin-top: 6px;
        resize: none;
      }
    }
  }

  .button {
    outline: none;
    padding: 4px 14px;
    display: flex;
    justify-content: center;
    font-weight: bold;
    font-size: 14px;
    align-items: center;
    border-radius: 4px;

    &.next {
      color: #ffffff;
      box-shadow: 0 5px 7px 0 rgba(94, 130, 245, 0.24);
      background-image: linear-gradient(to right, #2f6bff, #5e82f5);
    }

    &.cancel {
      background: #dddddd;
      color: #000000;
      margin: 0 10px;
    }

    &.submit {
      color: #ffffff;
      box-shadow: 0 5px 7px 0 rgba(94, 130, 245, 0.24);
      background-image: linear-gradient(to right, #2f6bff, #5e82f5);
    }

    &.add-plan {
      color: #ffffff;
      box-shadow: 0 5px 7px 0 rgba(94, 130, 245, 0.24);
      background-image: linear-gradient(to right, #2f6bff, #5e82f5);
      width: 100px;
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
