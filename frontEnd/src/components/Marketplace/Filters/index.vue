<template>
    <v-container class="px-12">
        <v-row class="flex-wrap">
            <v-col v-for="(filter, index) in filters" :key="index">
            <CSelect
            :name="filter.name"
            :items="filter.items"
            :isDisable="filter.isDisable"
            @onUpdate="updateSelect"
            /> 
            </v-col>

            <v-col class="col-5" align-self="center">
                <CSearch @onUpdate="updateSearch"/>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
  import CSelect from '@/components/Marketplace/Filters/CSelect.vue'
  import CSearch from '@/components/Marketplace/Filters/CSearch.vue'

  export default {
    name: "index",
    components: {
      CSelect,
      CSearch
    },

    props: {
        data: { type: Array, required: true }
    },

    data() {
      return {
        offerings: this.data,
        filters: {
                offering_type: {
                    name: "Offering type",
                    items: [
                        "Dataset",
                        "Visual Analytic"
                    ],
                    isDisable: false
                },

                category: {
                    name: "Category",
                    items: [
                        "Regression",
                        "Classification",
                        "Clustering",
                        "Randomforest",
                        "Xgboost",
                        "Cars",
                        "Healthcare",
                        "Sales"
                    ],
                    isDisable: true
                },

                provider: {
                    name: "Provider",
                    items: [
                        "ELM", 
                        "Amanah", 
                        "Haraj",
                        "Ministry of Interior"
                    ],
                    isDisable: true
                },

                rate: {
                    name: "Rate",
                    items: [
                        1,
                        2,
                        3,
                        4,
                        5
                    ],
                    isDisable: true
                }
            }
        }
    },

    methods: {
        //emits
        updateSearch(search){
            this.$emit("onUpdate", this.searching(search));
        },

        updateSelect(filter){
            this.$emit("onUpdate", this.filtering(filter));
        },
        
        //private
        searching(search) {
            return this.offerings.filter(offering => offering.title.toLowerCase().includes(search.toLowerCase()));
        },

        filtering(filter) {
            //if select no items or select all itemes => show all
            if (filter.value.length === 0 || filter.value.length === this.filters[filter.name].items.length)
                return this.offerings;

            //filters
            let filterName = 'type';
            /*switch(filter.name){
                case "offering_type":
                    filterName = "type";
                    break;
                case "category":
                    filterName = "tags";
                    break;
                case "provider":
                    filterName = "";
                    break;
                case "rate":
                    filterName = "";
                    break;
            }*/

            let tmp = [];
            for(let valueIndex = 0; valueIndex < filter.value.length; valueIndex++)
                for(let offeringIndex = 0; offeringIndex < this.offerings.length; offeringIndex++)
                    if(this.offerings[offeringIndex][filterName].toLowerCase() === filter.value[valueIndex].toLowerCase())
                        tmp.push(this.offerings[offeringIndex]);

            return tmp;
        }
    }
  }
</script>

<style scoped lang="scss">

</style>
