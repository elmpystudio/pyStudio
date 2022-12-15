<template>
    <div>
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
                    <CCard :id="marketplace.id" :type="marketplace.type" :name="marketplace.name"
                        :description="marketplace.description" :tags="marketplace.tags" :date="'02.06.2020'" :rate="3.5"
                        :is_public="marketplace.is_public"
                        :to="`/marketplace/${marketplace.type === 'Dataset' ? 'dataset' : 'va'}/${marketplace.item}`"
                        @download="doanload_dataset">

                        <template #footer>
                            <button>dd</button>
                        </template>
                    </CCard>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
import Filters from '@/components/Marketplace/Filters';
import CCard from '@/components/Marketplace/CCard.vue';

import { mdiStar, mdiChevronDown, mdiChevronUp } from '@mdi/js'
import { API_URL, getMarketplaces, downloadMarketplace } from '@/api_client.js';

export default {
    name: "MarketplaceView",
    components: {
        Filters,
        CCard
    },

    data() {
        return {
            data: [],
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
        downloadURI(uri) {
            let link = document.createElement("a");
            link.href = uri;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        },

        update(data) {
            this.data = data;
        },

        doanload_dataset(id) {
            downloadMarketplace(id)
                .then(({ data }) => {
                    this.downloadURI(API_URL + data.file)
                })
                .catch((error) => console.error(error))
        }
    }
}
</script>

<style scoped>
.loading {
    position: absolute;
    top: 50%;
    left: 45%;
}
</style>
