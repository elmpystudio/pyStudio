<template>
    <div class="marketplace-view">
        <div class="loading" v-if="!datasets.isLoaded && !ml_models.isLoaded">
            <v-progress-circular :size="90" color="primary" indeterminate></v-progress-circular>
        </div>

        <v-container class="content pt-6" v-else>
            <!-- <Filters :data="data" @onUpdate="update" /> -->

            <!--error message-->
            <div class="red--text text--lighten-3" v-if="datasets.data.length === 0 && ml_models.data.length === 0">
                <h1>No Data Found</h1>
            </div>

            <v-row no-gutters>
                <v-col v-for="data in filtered_datasets" :key="`dataset_${data.id}`">
                    <CCard :id="data.id" :name="data.name" :description="data.description" :date="data.date"
                        :rate="data.rate" :access="data.access" :type="data.type" :to="'/marketplace/dataset'"
                        @action="handle_action">
                    </CCard>
                </v-col>

                <v-col v-for="data in filtered_ml_models" :key="`ml_model_${data.id}`">
                    <CCard :id="data.id" :name="data.name" :description="data.description" :date="data.date"
                        :rate="data.rate" :access="data.access" :type="data.type" :to="'/marketplace/dataset'"
                        @action="handle_action">
                    </CCard>
                </v-col>
            </v-row>
        </v-container>

        <CModal title="Request" :active="modalToggle" @close="handle_close()">
            <template #default>
                <div class="modal-contaienr">
                    <div class="message-container">
                        <textarea class="message" placeholder="Your Message" v-model="request.message" />

                        <v-btn class="request_btn" @click="send_request()" color="primary"
                            style="width: 100px; height: 30px; font-size:12px" elevation="1">Send</v-btn>
                    </div>

                    <div v-if="request.status === true" class="status good">
                        <i class="fa fa-check-circle" aria-hidden="true"></i>
                        <div class="message">Request Sent Successfully</div>
                    </div>
                    <div v-else-if="request.status === false" class="status bad">
                        <i class="fa fa-times-circle" aria-hidden="true"></i>
                        <div class="message">Request Error</div>

                    </div>
                </div>
            </template>
        </CModal>
    </div>
</template>

<script>
// import Filters from '@/components/Marketplace/Filters';
import CCard from '@/components/Marketplace/CCard.vue';
import CModal from '@/components/CModal.vue';
import {
    API_URL,
    getMarketplaceDatasets,
    getMarketplaceMlModels,
    downloadDataset,
    createNotification
} from '@/api_client.js';

export default {
    name: "MarketplaceView",
    components: {
        // Filters,
        CCard,
        CModal,
    },

    data() {
        return {
            datasets: {
                data: [],
                selected: 0,
                isLoaded: false
            },
            ml_models: {
                data: [],
                isLoaded: false
            },
            request: {
                message: null,
                status: null
            },
            modalToggle: false,
        }
    },

    computed: {
        filtered_datasets() {
            return this.datasets.data.map((dataset) => ({
                id: dataset.id,
                name: dataset.name,
                description: dataset.description,
                access: dataset.access,
                type: 'dataset',

                //fake
                rate: 3.5,
                date: '02.06.2020'
            }));
        },
        filtered_ml_models() {
            return this.ml_models.data.map((ml_model) => ({
                id: ml_model.id,
                name: ml_model.name,
                description: ml_model.description,
                access: ml_model.access,
                type: 'ml_model',

                //fake
                rate: 3.5,
                date: '02.06.2020'
            }));
        }
    },

    created() {
        getMarketplaceDatasets()
            .then(({ data }) => {
                this.datasets.data = data;
                this.datasets.isLoaded = true;
            })
            .catch((error) => console.error(error))

        getMarketplaceMlModels()
            .then(({ data }) => {
                this.ml_models.data = data;
                this.ml_models.isLoaded = true;
            })
            .catch((error) => console.error(error))
    },

    methods: {
        // staic function
        download(url) {
            let link = document.createElement("a");
            link.href = url;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        },

        handle_close() {
            // close toggle window
            this.modalToggle = false;

            // reset
            this.request.message = null;
            this.request.status = null;
        },

        handle_action(data) {
            this.datasets.selected = data.id;
            if (data.type === 'download')
                this.download_dataset();

            else if (data.type === 'request')
                this.modalToggle = true;
        },

        download_dataset() {
            downloadDataset(this.datasets.selected)
                .then(({ data }) => {
                    this.download(API_URL + data.file)
                })
                .catch((error) => console.error(error))
        },

        send_request() {
            createNotification({ dataset: this.datasets.selected, message: this.request.message })
                .then((response) => {
                    if (response.status === 201)
                        this.request.status = true;
                    else
                        this.request.status = false;
                })
                .catch((erroe) => console.error(erroe))
        }
    }
}
</script>

<style scoped lang="scss">
.marketplace-view {
    width: 100%;
    height: 100%;
    position: relative;
    background-color: #F5F5F5;

    .loading {
        position: absolute;
        top: 50%;
        left: 45%;
    }

    .modal-contaienr {
        width: 100%;
        height: 100%;
        padding: 10px 0;

        display: flex;
        flex-flow: column nowrap;
        align-items: center;

        .message-container {
            flex: 1 1 100%;
            width: 100%;
            display: flex;
            flex-flow: column nowrap;
            align-items: center;
            row-gap: 10px;

            .message {
                width: 80%;
                min-height: 120px;
                max-height: 200px;
                padding: 10px;
                background-color: rgb(233 233 233);

                border: 2px solid #1976d2;
                border-radius: 5px;
                transition: all 300ms;

                &:focus {
                    outline: none !important;
                    box-shadow: 0 0 10px #719ECE;
                }
            }

            .request_btn {}
        }

        .status {
            flex: 1 1 50%;

            >i {

                font-size: 40px;
            }

            .message {
                font-size: 20px;
            }

            &.good {
                >i {
                    color: #2B81D6;
                }

                .message {
                    color: #2B81D6;
                }
            }

            &.bad {
                >i {
                    color: red;
                }

                .message {
                    color: red;
                }
            }

        }
    }
}
</style>
