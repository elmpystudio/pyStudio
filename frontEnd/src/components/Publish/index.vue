<template>
  <div>
    <div class="header">
      <router-link :to="{ name: 'dataset', params: { id: this.$route.params.id }}" class="link">
        <v-icon>{{ icons.chevron }}</v-icon>
        <span>Back to dataset</span>
      </router-link>
      <v-row>
        <v-col class="d-flex justify-space-between align-center">
          <h1>Publish Dataset</h1>
          <template v-if="step === 1">
            <button @click="handleNextStep" class="button next" :disabled="!isValidStepOne">Next</button>
          </template>
          <template v-if="step === 2">
            <div class="d-flex">
              <button @click="handlePreviousStep" class="button cancel">Previous</button>
              <button @click="handleSubmit" class="button submit" :disabled="!isValidStepOne">Publish</button>
            </div>
          </template>
        </v-col>
      </v-row>
    </div>

    <div class="content">
      <div class="publish-content">
        <v-row>
          <v-col cols="12">
            <div v-if="step === 1" class="step-title">Step 1 / 2 <b>Overview</b></div>
            <div v-if="step === 2" class="step-title">Step 2 / 2 <b>Details</b></div>
            <v-row>
              <v-col cols="6">
                <div class="form-container" v-show="step === 1">
                  <div class="form-group">
                    <h4 class="form-title">Dataset title</h4>
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

                  <!--buttons on publish-content-->
                  <div class="form-group">
                    <template v-if="step === 1">
                      <div class="d-flex justify-content-end">
                        <button @click="handleNextStep" class="button next" :disabled="!isValidStepOne">Next</button>
                      </div>
                    </template>
                  </div>
                  
                </div>

                <div class="form-container" v-show="step === 2">
                  <div class="form-group">
                    <h4 class="form-title">Payment</h4>
                    <v-radio-group row v-model="radios" :mandatory="false" style="height:20px;">
                      <v-radio label="Subscription" value="subscription"></v-radio>
                      <v-radio label="One-time payment" value="one"></v-radio>
                    </v-radio-group>
                  </div>
                  <div class="form-group d-flex flex-column">
                    <div class="d-flex mt-3" :key="index" v-for="(plan, index) in plans">
                      <div>
                        <h4 class="form-title">Duration in days</h4>
                        <input type="text" class="input-field" v-model="plans[index].period" />
                      </div>
                      <div class="ml-4">
                        <h4 class="form-title">Price</h4>
                        <input type="text" class="input-field" v-model="plans[index].price" />
                      </div>
                    </div>

                    <button class="button add-plan mt-3" :disabled="!isValidAddPlan" @click="addPlan">Add plan</button>
                  </div>
                  <div class="form-group">
                    <h4 class="form-title">Target audience</h4>
                    <v-checkbox
                      v-model="isPublic"
                      label="Public"
                      style="height:20px;"
                    ></v-checkbox>
                    <v-checkbox
                      v-model="agencies"
                      label="Government agencies"
                      style="height:20px;"
                    ></v-checkbox>
                    <v-checkbox
                      v-model="sector"
                      label="Private sector"
                      style="height:20px;"
                    ></v-checkbox>
                  </div>
                  <div class="form-group">
                    <h4 class="form-title">Version</h4>
                    <input type="text" class="input-field" v-model="version" />
                  </div>
                  <div class="form-group">
                    <h4 class="form-title">Version notes</h4>
                    <textarea class="area-field" v-model="versionNotes" rows="4"></textarea>
                  </div>

                  <!--buttons on publish-content-->
                  <div class="form-group">
                    <template v-if="step === 2">
                      <div class="d-flex justify-content-end">
                        <button @click="handlePreviousStep" class="button cancel">Previous</button>
                        <button @click="handleSubmit" class="button submit" :disabled="!isValidStepOne">Publish</button>
                      </div>
                    </template>
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
  </div>
</template>

<script>
  import { mdiChevronLeft } from '@mdi/js'
  import { publishOffering } from '@/api_client.js';

  export default {
    name: "Publish",
    components: {
    },
    
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
        plans: [
          { period: '', price: '' },
        ],
        isPublic: false,
        agencies: false,
        sector: false,
        select: [],
        items: [
          'Datasets',
          'Regressions',
          'Machine Learning'
        ],
        radios: 'subscription',
        step: 1,
        isLoading: false,
      }
    },
    computed: {
      isValidStepOne() {
        return this.title && this.description && this.briefDescription;
      },
      isValidAddPlan() {
        return this.plans.length < 3;
      }
    },
    methods: {
      handleSubmit() {
        this.isLoading = true;
        const payload = {
          title: this.title,
          briefDescription: this.briefDescription,
          description: this.description,
          tags: this.select.map((item) => ({ name: item })),
          subscriptionOptionsData: this.plans,
          price: "0",
          item: this.$route.params.id,
        };

        publishOffering(payload)
          .then(({ data }) => {
            this.isLoading = false;
            this.$router.push({ name: 'dataset-offering', params: { id: data.id} });
          })
          .catch(error => {
            this.isLoading = false;
            console.error(error);
          })
      },
      handleNextStep() {
        this.step = 2;
      },
      handlePreviousStep() {
        this.step = 1;
      },
      addPlan () {
        this.plans.push({
          period: '',
          price: ''
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
      margin-bottom: 24px;

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
