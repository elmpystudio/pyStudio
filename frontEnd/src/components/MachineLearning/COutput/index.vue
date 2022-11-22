<template>
    <CModal :id="'outputModal'">
        <template v-slot:title>Data Output</template>

        <template v-slot:body>
            <div role="tabpanel">
                <!--tabs-->
                <ul
                    class="nav nav-tabs navbar"
                    id="outputModalTabs"
                    role="tablist"
                >
                    <li role="presentation" class="nav-link">
                        <a href="#data-summary" data-toggle="tab" role="tab"
                            >Data Summary</a
                        >
                    </li>

                    <li role="presentation" class="nav-link">
                        <a href="#data-sample" data-toggle="tab" role="tab"
                            >Data Sample</a
                        >
                    </li>

                    <li role="presentation" id="histogram_tab" class="nav-link">
                        <a
                            href="#histogram-div"
                            data-toggle="tab"
                            role="tab"
                            aria-controls="histogram-div"
                            >Histogram</a
                        >
                    </li>

                    <li role="presentation" id="pairwise_tab" class="nav-link">
                        <a href="#pairwise-div" data-toggle="tab" role="tab"
                            >Pairwise</a
                        >
                    </li>

                    <li
                        role="presentation"
                        id="correlation_tab"
                        class="nav-link"
                    >
                        <a href="#correlation-div" data-toggle="tab" role="tab"
                            >Correlation Matrix</a
                        >
                    </li>
                </ul>

                <!--content-->
                <div class="tab-content" id="tab-content">
                    <!--content 1-->
                    <div
                        role="tabpanel"
                        class="tab-pane fade in active show"
                        id="data-summary"
                    >
                        <CDataSummary />
                    </div>

                    <!--content 2-->
                    <div role="tabpanel" class="tab-pane fade" id="data-sample">
                        <CDataSample />
                    </div>

                    <!--content 3-->
                    <div
                        nodeId="X"
                        outputId="Y"
                        role="tabpanel"
                        class="tab-pane fade"
                        id="histogram-div"
                    >
                        <CHistogram />
                    </div>

                    <!--content 4-->
                    <div
                        nodeId="X"
                        outputId="Y"
                        role="tabpanel"
                        class="tab-pane fade"
                        id="pairwise-div"
                    >
                        <CPairwise />
                    </div>

                    <!--content 5-->
                    <div
                        nodeId="X"
                        outputId="Y"
                        role="tabpanel"
                        class="tab-pane fade"
                        id="correlation-div"
                    >
                        <CCorrelation />
                    </div>
                </div>
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