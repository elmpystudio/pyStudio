<template>
    <CModal :id="'evaluationOutput'">
        <template v-slot:title>Evaluation Metrix</template>

        <template v-slot:body>
            <div id="evaluationOutput-content">
                <div
                    id="evaluation-graph-div"
                    class="modal-results-content graph"
                ></div>
                <div id="labelsContainer" class="row data-container">
                    <div class="col-md-6">
                        <div id="modelEvalTable">
                            <table id="correlationMtrxTab" class="mytable">
                                <tr>
                                    <th>Actual</th>
                                    <td id="tpValue"></td>
                                    <td id="tnValue"></td>
                                </tr>
                                <tr>
                                    <th>Predicted</th>
                                    <td id="fpValue"></td>
                                    <td id="fnValue"></td>
                                </tr>
                            </table>
                        </div>
                    </div>

                    <div id="modelEvalLabels" class="col-md-6">
                        <table id="labelsTable" class="mytable"></table>
                    </div>
                </div>
            </div>
        </template>

        <template v-slot:footer>
            <button
                type="button"
                class="savebtn"
                id="save_as_pdf_evaluationOutput"
            >
                Save
            </button>
        </template>
    </CModal>
</template>

<script>
import CModal from "@/components/MachineLearning/CModal.vue";

export default {
    name: "CEvaluationMetrix",

    components: {
        CModal,
    },
};
</script>

<style lang="scss">
.mytable {
    font-family: Arial, Helvetica, sans-serif;
    border-collapse: collapse;
    width: 100%;
    font-size: 14px;

    th {
        text-align: center;
        background-color: #364150;
        color: white;
        width: 40%;
        padding: 4px;
        border: solid 1px black;
    }

    td {
        padding: 4px;
        border: solid 1px black;
        color: #364150;
    }
}

.graph {
    margin: 10px 20px;
    padding: 5px;
    border: 2px solid #364150;
    border-radius: 5px;

    rect {
        fill: #e3e3e3 !important;
    }
}

.data-container {
    align-items: center !important;
    margin: 20px;
    padding: 20px;

    border: 2px solid #364150;
    border-radius: 5px;

    #modelEvalLabels {
        padding: 0;
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

.plotly-graph-div {
    width: 100% !important;
}

.js-plotly-plot .plotly .main-svg {
    background: rgba(255, 255, 255, 0) !important;
}
.js-plotly-plot .plotly .user-select-none {
    width: 100% !important;
}
.modebar-group {
    background: #e3e3e3 !important;
}

.col-md-6 {
    padding: 0;
    padding-right: 20px;
}
</style>