<template>
    <CModal :id="'outputModal'">
        <template v-slot:title>Data Output</template>

        <template v-slot:body>
            <div role="tabpanel">
                <v-tabs v-model="tab" background-color="transparent" color="basil" grow>
                    <v-tab v-for="item in items" :key="item">
                        {{ item }}
                    </v-tab>
                </v-tabs>

                <v-tabs-items v-model="tab">
                    <v-tab-item v-for="item in items" :key="item">
                        <div v-if="item === 'data-summary'">
                            <div id="data-summary">
                                <CDataSummary />
                            </div>
                        </div>

                        <div v-else-if="item === 'data-sample'">
                            <div id="data-sample">
                                <CDataSample />
                            </div>
                        </div>

                        <div v-else-if="item === 'histogram'">
                            <div id="histogram-div">
                                <CHistogram />
                            </div>
                        </div>

                        <div v-else-if="item === 'pairwise'">
                            <div id="pairwise-div">
                                <CPairwise />
                            </div>
                        </div>

                        <div v-else-if="item === 'correlation'">
                            <div id="correlation-div">
                                <CCorrelation />
                            </div>
                        </div>
                    </v-tab-item>
                </v-tabs-items>
            </div>
        </template>

        <template v-slot:footer>
            <button type="button" class="savebtn" id="save_as_pdf">Save</button>
        </template>
    </CModal>
</template>

<script>
import CModal from "@/components/MachineLearning/CModal.vue";
import CDataSummary from "@/components/MachineLearning/COutput/CDataSummary.vue";
import CDataSample from "@/components/MachineLearning/COutput/CDataSample.vue";
import CHistogram from "@/components/MachineLearning/COutput/CHistogram.vue";
import CPairwise from "@/components/MachineLearning/COutput/CPairwise.vue";
import CCorrelation from "@/components/MachineLearning/COutput/CCorrelation.vue";

export default {
    name: "index",
    components: {
        CModal,
        CDataSummary,
        CDataSample,
        CHistogram,
        CPairwise,
        CCorrelation,
    },

    data() {
        return {
            tab: null,
            items: [
                'data-summary', 'data-sample', 'histogram', 'pairwise', 'correlation',
            ],

        };
    },
};
</script>

<style lang="scss" scoped>
.navbar {
    background: #616975;
    padding: 0;
    justify-content: space-between;

    a {
        text-decoration: none;
        color: #bbbbbb;
    }

    .active {
        color: inherit;
    }

    li {
        color: white;
        border: 0;
    }
}

.savebtn {
    color: #f2f2f2;
    background: #364150;
    text-transform: uppercase;
    width: 100%;
    height: 100%;
    font-size: 15px;
}

.savebtn:hover {
    opacity: 0.8;
}
</style>

<style lang="scss">
.nav-tabs .nav-link.active,
.nav-tabs .nav-item.show .nav-link {
    background: #e3e3e3;
    color: #2869b2;
}
</style>