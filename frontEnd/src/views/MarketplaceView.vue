<template>
    <div class="marketplace-view">
        <div class="loading" v-if="!isLoaded">
            <v-progress-circular :size="90" color="primary" indeterminate></v-progress-circular>
        </div>

        <v-container class="content pt-6" v-else>
            <Filters :data="data" @onUpdate="update" />

            <!--error message-->
            <div class="red--text text--lighten-3" v-if="data.length === 0">
                <h1>No Data Found</h1>
            </div>

            <v-row no-gutters>
                <v-col v-for="(marketplace, index) in data" :key="index">
                    <CCard :id="marketplace.id" :name="marketplace.name" :description="marketplace.description"
                        :date="'02.06.2020'" :rate="3.5" :is_public="marketplace.is_public"
                        :to="`/marketplace/${marketplace.type === 'Dataset' ? 'dataset' : 'va'}/${marketplace.item}`"
                        @action="handle_action">

                        <template #footer>
                            <button>dd</button>
                        </template>
                    </CCard>
                </v-col>
            </v-row>
        </v-container>

        <CModal title="Send Request" :active="modalToggle" @close="modalToggle = false">
            <template #default>
                <div class="modal-contaienr">
                    <div class="message-container">
                        <textarea class="message" placeholder="Your Message" v-model="request_message" />

                        <v-btn class="request_btn" @click="send_request()" color="primary"
                            style="width: 100px; height: 30px; font-size:12px" elevation="1">Send</v-btn>
                    </div>
                    <div class="status">
                        <i v-if="status" class="fa fa-check-circle" aria-hidden="true"></i>
                    </div>
                </div>
            </template>
        </CModal>
    </div>
</template>

<script>
import Filters from '@/components/Marketplace/Filters';
import CCard from '@/components/Marketplace/CCard.vue';
import CModal from '@/components/CModal.vue';

import { mdiStar, mdiChevronDown, mdiChevronUp } from '@mdi/js'
import { API_URL, getMarketplaces, downloadMarketplace, createNotification } from '@/api_client.js';

export default {
    name: "MarketplaceView",
    components: {
        Filters,
        CCard,
        CModal,
    },

    data() {
        return {
            modalToggle: false,
            status: false,
            data: [],
            selected_dataset_id: null,
            request_message: '',
            isLoaded: false,
            icons: {
                star: mdiStar,
                arrowUp: mdiChevronUp,
                arrowDown: mdiChevronDown,
            }
        }
    },

    created() {
        getMarketplaces()
            .then(({ data }) => {
                this.data = data;
                this.isLoaded = true;
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

        update(data) {
            this.data = data;
        },

        handle_action(data) {
            this.selected_dataset_id = data.id;

            if (data.type === 'download') 
                this.download_marketplace();

            else if (data.type === 'request')
                this.modalToggle = true;

        },

        download_marketplace() {
            downloadMarketplace(this.selected_dataset_id)
                .then(({ data }) => {
                    this.download(API_URL + data.file)
                })
                .catch((error) => console.error(error))
        },

        send_request() {
            createNotification({ dataset: this.selected_dataset_id, message: this.request_message })
                .then((response) => {
                    if (response.status === 201)
                        this.status = true;
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
            ;

            .message {
                width: 450px;
                max-height: 120px;
                padding: 10px;
                background-color: rgb(230, 230, 230);

                border: 2px solid #1976d2;
                border-radius: 5px;
            }

            .request_btn {}
        }

        .status {
            flex: 1 1 50%;

            >i {
                font-size: 60px;
                color: green;
            }
        }
    }
}

.loading {
    position: absolute;
    top: 50%;
    left: 45%;
}
</style>
