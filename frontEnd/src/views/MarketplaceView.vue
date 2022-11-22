<template>
    <div>
        <div class="loading" v-if="!isLoaded">
            <v-progress-circular
            :size="90"
            color="primary"
            indeterminate
            ></v-progress-circular>
        </div>

        <v-container class="content pt-6" v-else>
            <Filters
            :data="data"
            @onUpdate="update"
            />
            
            <!--error message-->
            <div class="red--text text--lighten-3" v-if="data.length === 0">
                <h1>No Data Found</h1>
            </div>

            <v-row no-gutters >
                <v-col v-for="(offering, index) in data" :key="index">
                    <CCard
                    :type="offering.type"
                    :title="offering.title"
                    :description="offering.briefDescription"
                    :tags="offering.tags"
                    :date="'02.06.2020'"
                    :rate="3.5"
                    :to="`/marketplace/${offering.type === 'Dataset' ? 'dataset' : 'va'}/${offering.item}`"
                    />
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
import Filters from '@/components/Marketplace/Filters';
import CCard from '@/components/Marketplace/CCard.vue';

import { mdiStar, mdiChevronDown, mdiChevronUp } from '@mdi/js'
import { getMarketplaceOfferings } from '@/api_client.js';

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
        getMarketplaceOfferings()
        .then(({ data }) => {
                this.data = data; 
                this.isLoaded = true;
            })
        .catch((error) => console.error(error))
    },

    methods: {
        update(data){
            this.data = data;
        }
    }
}
</script>

<style scoped> 
.loading{
    position: absolute;
    top: 50%;
    left: 45%;
}
</style>
