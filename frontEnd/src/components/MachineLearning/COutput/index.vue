<template>
    <CModal :id="'outputModal'">
        <template v-slot:title>Data Output</template>

        <template v-slot:body>
            <!--tabs-->
            <nav class="navbar navbar-expand-lg navbar-light bg-light custom-navbar">
                <ul class="nav nav-tabs">
                    <li class="nav-item">
                        <a class="nav-link active" data-toggle="tab" href="#data-summary">Data Summary</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-toggle="tab" href="#data-sample">Data Sample</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-toggle="tab" href="#histogram-div">Histogram</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-toggle="tab" href="#pairwise-div">Pairwise</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-toggle="tab" href="#correlation-div">Correlation Matrix</a>
                    </li>
                </ul>
            </nav>

            <!--content-->
            <div class="tab-content">
                <div id="data-summary" class="tab-pane fade show active">
                    <CDataSummary />
                </div>
                <div id="data-sample" class="tab-pane fade">
                    <CDataSample />
                </div>
                <div id="histogram-div" class="tab-pane fade">
                    <CHistogram />
                </div>
                <div id="pairwise-div" class="tab-pane fade">
                    <CPairwise />
                </div>
                <div id="correlation-div" class="tab-pane fade">
                    <CCorrelation />
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
    }
};
</script>

<style lang="scss" scoped>
.custom-navbar {
    padding: 0;

    ul {
        display: flex;
        width: 100%;
        flex-flow: row nowrap;
        justify-content: center;

        li {
            a {
                color: #364150;

                &.active {
                    background-color: #364150;
                    color: white;
                }
            }
        }
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