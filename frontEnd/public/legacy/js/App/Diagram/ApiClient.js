import { API_URL } from "../env.js";
import { roundNumberToTwoDigits } from "./Util.js";

const GET_NODE_OUTPUT = '/api/ml/node/output/';
const WORKFLOW_EXECUTION_URL = '/api/ml/workflow/execute/';
const GET_WORKFLOW = "/api/ml/experiment/retrieve/";
const GET_WORKFLOW_STATUS = '/api/ml/workflow/progress/';
const SAVE_WORKFLOW = '/api/ml/experiment/save/';
const CREATE_WORKFLOW = '/api/ml/experiment/create/';
// const SAVE_DEPLOYED_WORKFLOW = "workflow/deploy/";
const GET_PORT_OUTPUT_HIST = "/api/ml/node/get_node_output_hist/";
const GET_PORT_OUTPUT_PAIRWISE = "/api/ml/node/get_node_output_pairwise/";
const GET_PORT_OUTPUT_CORR_MATRIX = "/api/ml/node/get_node_output_corr_matrix/";
const GET_NODE_OUTPUT_METADATA = "/api/ml/node/get_workflow_ports_md/";
const GET_MODEL_OUTPUT = '/api/ml/node/get_model_info/';
const GET_EVAL_METRICS = '/api/ml/node/get_eval_metrics/';
const GET_ROC_CHART = '/api/ml/node/get_roc_chart/';
const SAVE_DEPLOY = '/api/ml_models/';
const SEND_REACCSV = '/api/ml_models/uploadcsv';
const PROGRESS_NODE_UNDER_PROCESS = "START";
const PROGRESS_NODE_FINISHED_SUCCESSFULY = "SUCCESS";
const PROGRESS_NODE_FINISHED_WITH_FAILURE = "FAILURE";
const UNDER_PROCESS_GIF = "gif/Spinner.gif";
const FINISHED_SUCCESSFULY_PNG = "images/green-tick.png";
const FINISHED_WITH_FAILURE_PNG = "images/x-mark.png";
const TIMEOUT_IN_SECONDS = 1000;
var CONTEXT_PATH = "/ml/";
let NODES_WITH_METADATA = {};
let ORIGINAL_NODES_WITH_METADATA = {}; //jsplumb

//static
/*
- loading all nodes for sidebar from local file and now loading dataset from server.
*/

function getWorkflowStatus(experimentId, isWorkflowRanSuccessfuly, executionType) {
    $.ajax({
        // url: CONTEXT_PATH + GET_WORKFLOW_STATUS + experimentId,
        url: API_URL + GET_WORKFLOW_STATUS + experimentId + "/",
        method: "GET",
        // dataType: "json",
        cache: false,
        // headers: {
        //     'Cache-Control': 'no-cache, no-store, must-revalidate',
        //     'Pragma': 'no-cache',
        //     'Expires': '0'
        // },
        success: function (response) {
            // $.each(response.nodes_status, function(i, e){
            //     if(e.node.includes("task")){
            //         // e.node = e.node.replace("task", "flowchartNode");
            //         nodeId = parseInt(e.node.split("flowchartNode")[1]);
            //         nodeId = nodeId + 1;
            //         e.node = "flowchartNode"+nodeId;
            //     }
            // });
            updateNodesStatus(experimentId, response, isWorkflowRanSuccessfuly, executionType);
        },
        error: function (response) {
            //showPopupError(response.message);
        }
    });
}

//static
function showIconStatusByNodeId(nodeId, iconPath) {
    if ($("#" + nodeId + " :first-child :first-child").prop('nodeName') === "IMG") { //Image alreedy present

        $("#" + nodeId + "_statusIcon").attr('src', iconPath);

        // In case it's available
        $("#" + nodeId + "_statusIcon").removeAttr("data-toggle");
        $("#" + nodeId + "_statusIcon").removeAttr("data-placement");
        $("#" + nodeId + "_statusIcon").removeAttr("title");

    } else { // create the image

        $("#" + nodeId).css('background-color', 'rgb(235 255 227)');
        //$("#" + nodeId).css('line-height', '35px');
        $("#" + nodeId).prepend(
            '<div class="statusIconDiv" id="' + nodeId + '_statusIconDiv">' +
            '<img id="' + nodeId + '_statusIcon" src="' + iconPath + '">' +
            '</div>')

    }
}

//static
function showExceptionStatusByNodeId(nodeId, iconPath, errorMessage) {
    if ($("#" + nodeId + " :first-child :first-child").prop('nodeName') === "IMG") { //Image alreedy present

        $("#" + nodeId + "_statusIcon").attr('src', iconPath);
        $("#" + nodeId + "_statusIcon").attr("data-toggle", "tooltip");
        $("#" + nodeId + "_statusIcon").attr("data-placement", "top");
        $("#" + nodeId + "_statusIcon").attr("title", errorMessage);

    } else { // create the image

        $("#" + nodeId).css('background-color', 'rgb(255, 213, 213)');

        $("#" + nodeId).prepend(
            '<div class="statusIconDiv" id="' + nodeId + '_statusIconDiv">' +
            '<img id="' + nodeId + '_statusIcon" src="' + iconPath + '">' +
            '</div>'
        )

        $("#ml_error").modal({
            backdrop: 'static',
            keyboard: false
        })
        $("#ml_error .message").text(errorMessage);

    }

    $('[data-toggle="tooltip"]').tooltip();

}

//static
function handleFinishedWorkflow(executionType, isWorkflowRanSuccessfuly) {
    if (executionType === "deployment" && isWorkflowRanSuccessfuly) {
        $("#deplymentNameModal").modal("show");
    }
    executionType = "execution"
}

//static
function updateNodesStatus(experimentId, workflowProgressJson, isWorkflowRanSuccessfuly, executionType) {

    // let numberOfNotFinishedNodes = 0;
    let isWorkFlowFinished = false;
    $.each(workflowProgressJson.nodes_status, function (index, el) {
        if (el.node !== 'WORKFLOW_PROCESS' && el.node !== 'WORKFLOW') {

            // nodeId = parseInt(el.node.split("task")[1]);
            // nodeId = nodeId + 1;
            // el.node = "flowchartNode"+nodeId;

            if (el.status === PROGRESS_NODE_UNDER_PROCESS) {

                // numberOfNotFinishedNodes ++;
                showIconStatusByNodeId(el.node, UNDER_PROCESS_GIF);

            } else if (el.status === PROGRESS_NODE_FINISHED_SUCCESSFULY) {
                isWorkflowRanSuccessfuly = true;
                showIconStatusByNodeId(el.node, FINISHED_SUCCESSFULY_PNG);

            } else if (el.status === PROGRESS_NODE_FINISHED_WITH_FAILURE) {

                isWorkflowRanSuccessfuly = false;
                showExceptionStatusByNodeId(el.node, FINISHED_WITH_FAILURE_PNG, el.note);
                isWorkFlowFinished = true; // Stop Checking in case of any failure

            }
            /*else{
                                    numberOfNotFinishedNodes++;
                            }*/
        }
        if (workflowProgressJson.wf_status === PROGRESS_NODE_FINISHED_SUCCESSFULY || workflowProgressJson.wf_status === PROGRESS_NODE_FINISHED_WITH_FAILURE) {
            isWorkFlowFinished = true;
        }
    });
    if (!isWorkFlowFinished) {
        setTimeout(function () {
            getWorkflowStatus(experimentId, isWorkflowRanSuccessfuly, executionType);
        }, TIMEOUT_IN_SECONDS);
    } else {
        handleFinishedWorkflow(executionType, isWorkflowRanSuccessfuly);
    }
}

//static
function handleRegressionTasksOutput(response, wfId, nodeId) {
    $('a[href="#model-desc"]').hide();
    $("#topLabelsContainer").show();
    $("#labelsContainer").hide();

    let tbody = '<tr><th>Mean Absolute Error</th><th>Mean Squared </th><th>R2 Score</th></tr>';
    tbody += '<tr><td>' + roundNumberToTwoDigits(response.mean_absolute_error) + '</td><td>' + roundNumberToTwoDigits(response.mean_squared_error) + '</td><td>' + roundNumberToTwoDigits(response.r2_score) + '</td></tr>';


    $("#topLabelsTable").html(tbody);

    $("#model-eval-container").addClass("regressionEvalContainer");
    $("#rocChart").removeClass("rocChartClassification").addClass("rocChartRegression");
    $("#topModelEvalLabels").addClass("regressionEvalLabelsTabDiv");
    $('a[href="#model-eval"]').tab('show');

    getRocChart(wfId, nodeId);
}

function sendReadcsvFile(file) {
    let formData = new FormData();

    formData.append("file", file);
    formData.append("upload_file", true);
    
    let path = null;
    $.ajax({
        url: API_URL + SEND_REACCSV,
        method: 'post',
        processData: false,
        contentType: false,
        cache: false,
        enctype: 'multipart/form-data',
        data: formData,
        async: false,
        success: function (response) {
            path = response;
        },
        error: function (response) {
        }
    });

    return path;
}

//static
function getRocChart(wfId, nodeId) {
    $.ajax({
        url: API_URL + GET_ROC_CHART,
        method: "POST",
        cache: false,
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            "wf_unique_id": wfId,
            "node_name": nodeId
        }),
        success: function (response) {
            $('#evaluationOutput').modal('show');

            console.log("ROC MEETRIC Err", response);

            $('#evaluation-graph-div').empty();
            $('#evaluation-graph-div').append(response);

            // showRocChart(response);
        },
        error: function (response) {
            console.log("ROC MEETRIC Err", response);
            //alert("not be here... " + response);
        }
    });
}

//static
function prepareCorrelationMatrixTab(jsonData) {
    $("#correlation-graph-div").html(jsonData);
    removeUnneededOptionFromPlotlyChart();
    // $("#correlation-graph-div>img").css("max-height", "510px");
}
////////////////////////////////////////////////////////////////////////////
//jsplumbClient
function getCorrelationMatrix(json_request) {
    $("#correlation-graph-div").html("");
    $("#correlation-graph-div").addClass("loader");

    $.ajax({
        url: API_URL + GET_PORT_OUTPUT_CORR_MATRIX,
        method: "POST",
        cache: false,
        contentType: "application/json; charset=utf-8",
        datatype: "json",
        data: json_request,
        success: function (response) {
            $("#correlation-graph-div").removeClass("loader");
            prepareCorrelationMatrixTab(response);
        },
        error: function (response) {
            $("#correlation-graph-div").removeClass("loader");
            $("#correlation-graph-div").append(response.responseText)
        }
    });
}

//jsplumbClient
function saveDeployedWorkflow(request) {
    let message = "";
    $.ajax({
        url: API_URL + SAVE_DEPLOY,
        method: "POST",
        data: request,
        cache: false,
        dataType: "json",
        beforeSend: function () {
            // $("#deploy_modal_loader").css("display", "block");
        },
        complete: function () {
            // $("#loader").css("display", "none");
            $("#deploy_status").modal({
                backdrop: 'static',
                keyboard: false
            })
            $("#deploy_status .message").text(message);
        },
        success: function (response) {
            $("#deploy_modal").modal("hide");
            message = "Saved Successfully";
        },
        error: function (response) {
            console.log(response.message);
            message = "Error";
        }
    });
}

//jsplumbClient
function workFlowExecution(flowDiagramJson) {
    $.ajax({
        url: API_URL + WORKFLOW_EXECUTION_URL,
        method: "POST",
        data: flowDiagramJson,
        cache: false,
        dataType: "json",
        beforeSend: function () {
            $("#loader").css("display", "block");
        },
        complete: function () {
            $("#loader").css("display", "none");
        },

        success: function (response) {
            // getNodeOutputMetadata(flowDiagramJson);
            // console.log('formatted response ' + response);
            setTimeout(function () {
                getNodeOutputMetadata(flowDiagramJson);
            }, 1100);
        },
        error: function (response) {
            console.log(response.message);
        }
    });
}

//jsplumbClient
function sendWorkflowToExecute(workflowJson, experimentId, isWorkflowRanSuccessfuly, executionType) {
    $.ajax({
        url: API_URL + WORKFLOW_EXECUTION_URL,
        method: "POST",
        data: workflowJson,
        cache: false,
        dataType: "json",
        beforeSend: function () {
            //reset
            if ($("#executeButton").hasClass("btn-run-success"))
                $("#executeButton").removeClass("btn-run-success");
            if ($("#executeButton").hasClass("btn-run-error"))
                $("#executeButton").removeClass("btn-run-error");

            $("#executeButton").toggleClass("play");

            $("#loader").css("display", "block");
        },
        success: function (response) {
            console.log('formatted response ' + response);
            setTimeout(function () {
                getWorkflowStatus(experimentId, isWorkflowRanSuccessfuly, executionType);
            }, 500);

            $("#executeButton").addClass("btn-run-success");
            $("#deployWorkflow").addClass("active");
        },
        error: function (response) {
            $("#executeButton").addClass("btn-run-error");
            $("#ml_error").modal({
                backdrop: 'static',
                keyboard: false
            })
            $("#ml_error .message").text("Error in Execute");
        },
        complete: function (response) {
            $("#executeButton").toggleClass("play");

            $("#loader").css("display", "none");
        }
    });

}

//jsplumbClient
function getOutputData(expId, nodeId, outputId, nodeType, callback) {
    $.ajax({
        url: API_URL + GET_NODE_OUTPUT,
        method: "POST",
        dataType: "json",
        cache: false,
        data: JSON.stringify({
            "wf_unique_id": expId,
            "node_name": nodeId,
            "output_port_id": outputId
        }),
        success: function (response) {
            callback(nodeId, response);
        },
        error: function (response) {
            //showPopupError(response.message);
        }
    });
}

//jsplumbClient
function getModelOutput(expId, nodeId, outputId, nodeType, callback) {
    $.ajax({
        url: API_URL + GET_MODEL_OUTPUT,
        method: "POST",
        dataType: "json",
        cache: false,
        data: JSON.stringify({
            "wf_unique_id": expId,
            "node_name": nodeId,
            "output_port_id": outputId
        }),
        success: function (response) {
            callback(nodeId, response);
        },
        error: function (response) {
            //showPopupError(response.message);
        }
    });
}

//jsplumbClient
function handleClassificationTasksOutput(response, wfId, nodeId) {
    $('a[href="#model-desc"]').hide();
    $("#topLabelsContainer").hide();
    $("#labelsContainer").show();
    $("#modelEvalTable").show();


    $("#tpValue").html(response.tp);
    $("#fpValue").html(response.fp);
    $("#fnValue").html(response.fn);
    $("#tnValue").html(response.tn);

    let tbody = '<tr><th>Accuracy Score</th><td>' + roundNumberToTwoDigits(response.accuracy_score) + '</td></tr>';
    tbody += '<tr><th>Precision Score</th><td>' + roundNumberToTwoDigits(response.precision_score) + '</td></tr>';
    tbody += '<tr><th>Recall Score</th><td>' + roundNumberToTwoDigits(response.recall_score[0]) + '</td></tr>';
    tbody += '<tr><th>F1 Score</th><td>' + roundNumberToTwoDigits(response.f1_score[0]) + '</td></tr>';

    $("#labelsTable").html(tbody);

    $("#model-eval-container").removeClass("regressionEvalContainer");
    $("#rocChart").removeClass("rocChartRegression").addClass("rocChartClassification");
    $("#labelsContainer").removeClass("regressionEvalLabelsContainer").addClass("classificationEvalLabelsContainer");
    $("#modelEvalLabels").removeClass("regressionEvalLabelsTabDiv");
    $('a[href="#model-eval"]').tab('show');
    if (wfId) {
        getRocChart(wfId, nodeId);
    }
}

//jsplumbClient
function getEvalMetrics(wfId, nodeId) {
    $.ajax({
        url: API_URL + GET_EVAL_METRICS,
        method: "POST",
        dataType: "json",
        cache: false,
        data: JSON.stringify({
            "wf_unique_id": wfId,
            "node_name": nodeId
        }),
        success: function (response) {
            $('#evaluationOutput').modal('show');

            console.log("Evaluation Modal Err", response)
            $('#evaluation-graph-div').append(response.responseText)
            if (response.model_type === "classification") {

                console.log(response);

                handleClassificationTasksOutput(response, wfId, nodeId);

            } else if (response.model_type === "regression") {

                handleRegressionTasksOutput(response, wfId, nodeId);

            }
            console.log("Evaluation Modal Suc", response)
        },
        error: function (response) {
            console.log("getEvalMetrics Err", response);
            //alert("Please run for details");
        }
    });
}

//jsplumbClient
function newGetEvalMetrics(wfId, nodeId) {
    let data = {};
    $.ajax({
        url: API_URL + GET_EVAL_METRICS,
        method: "POST",
        dataType: "json",
        async: false,
        cache: false,
        data: JSON.stringify({
            "wf_unique_id": wfId,
            "node_name": nodeId
        }),
        success: function (response) {
            data = response;
        },
        error: function (response) {
            console.error("newGetEvalMetrics", response);
        }
    });
    return data;
}

//jsplumbClient
function getHistogram(json_request) {
    $("#histogram-graph-div").html("");
    $("#histogram-graph-div").addClass("loader");
    $.ajax({
        url: API_URL + GET_PORT_OUTPUT_HIST,
        method: "POST",
        cache: false,
        contentType: "application/json; charset=utf-8",
        datatype: "json",
        data: json_request,
        success: function (response) {
            // console.log("HTNL Response", response)
            // $("#histogram-graph-div").removeClass("loader");
            // prepareHistogramTab(response);
            // $('#histogram-graph-div').html(response)
            $('#histogram-graph-div').append(response.responseText)
            //alert(response.responseText)

        },
        error: function (response) {
            $("#histogram-graph-div").removeClass("loader");
            console.log("Histogram exception", response.responseText)
            console.log("Histogram exception", response)

            $('#histogram-graph-div').append(response.responseText)

            // showPopupError(response.message);
        }
    });
}

//jsplumbClient
function getPairwise(json_request) {
    $("#pairwise-graph-div").html("");
    $("#pairwise-graph-div").addClass("loader");
    $.ajax({
        url: API_URL + GET_PORT_OUTPUT_PAIRWISE,
        method: "POST",
        cache: false,
        contentType: "application/json; charset=utf-8",
        datatype: "json",
        data: json_request,
        success: function (response) {
            $("#pairwise-graph-div").removeClass("loader");
            preparePairwiseTab(response);
        },
        error: function (response) {
            $("#pairwise-graph-div").removeClass("loader");
            // showPopupError(response.message);
            $("#pairwise-graph-div").append(response.responseText)
            console.log("Pair Response", response.responseText)
        }
    });
}

//jsplumbClient
function sendWorkflowForSaving(json_request) {
    //saving the work flow to server
    $.ajax({
        url: API_URL + SAVE_WORKFLOW,
        method: "POST",
        cache: false,
        data: json_request,
        success: function (response) {
            swal("Saved Successfully", "", "success");
            // $("#lastSavedSpan").html(response);
        },
        error: function (response) {
            //showPopupError(response.message);
        }
    });
}

//jsplumbClient
function createWorkflow(json_request) {
    //saving the work flow to server
    $.ajax({
        url: API_URL + CREATE_WORKFLOW,
        method: "POST",
        cache: false,
        data: json_request,
        success: function (response) {
            swal("Saved Successfully", "", "success");
            // $("#lastSavedSpan").html(response);
        },
        error: function (response) {
            //showPopupError(response.message);
        }
    });
}

//jsplumbClient
/*
used on save to local
Propose changed:
1: Workflow is saved and retreived  from local session
2: when js is loaded this function is called and delay has been introduced so that "nodes From Server"
  is loaded before workflow is build.
*/
function getWorkflowByExperimentId(json_request, instance) {
    $.ajax({
        url: API_URL + GET_WORKFLOW,

        method: "GET",
        // cache: false,
        // data: json_request,
        success: function (response) {
            if (response !== "None") {
                console.log(JSON.stringify(response))
                buildWorkflow(JSON.stringify(response, instance));
            }

        },
        error: function (response) {
            //showPopupError(response.message);
        }
    });

    // Fetching the documents from local storage
    // let delayInMilliseconds = 1500; //1.5 second
    // setTimeout(function () {
    //   let response = JSON.parse(localStorage.getItem('save_experiment'));
    //   buildWorkflow(JSON.stringify(response));
    // }, delayInMilliseconds);
}

//jsplumbClient | NodeManager
//metadata tricks
function getNodeOutputMetadata(workflowJson) {
    $.ajax({
        url: API_URL + GET_NODE_OUTPUT_METADATA,
        method: "POST",
        // async: false,
        data: workflowJson,
        contentType: "application/json",
        cache: false,
        datatype: "json",
        //  beforeSend: function(){
        //    let nodeid = JSON.parse(workflowJson)
        //    showIconStatusByNodeId(nodeid.run_to_task_id, UNDER_PROCESS_GIF);
        //
        // },
        //
        //  complete: function(){
        //    console.log("Sent")
        //    removeIconStatusForAllNodes()
        //  },
        success: function (response) {
            let columnItems = []
            let finalMetaDataResponse = []
            ORIGINAL_NODES_WITH_METADATA = response["Result"]
            $.each(response["Result"], function (i, el) {
                let taskIdOutput = el['task_id']
                let taskName = el['task_name']
                // console.log(task_id)
                $.each(el["outputs"], function (j, e) {
                    columnItems = Object.keys(e.dtypes);

                    $.each(JSON.parse(workflowJson)["wf_body"]["nodes"], function (v, wf) {
                        if ((wf["task_id"] == taskIdOutput) & (wf['outputs'].length > 0)) {
                            // console.log(j, wf['outputs'])
                            // console.log("node_path", wf["outputs"][j]["targets"][0]["id"].replace("Top", "").replace("Center", "Left"), e["output_label"].replace("Bottom", "").replace("Center", "Left"), wf["outputs"][j]["targets"][0]["nodeId"], taskIdOutput)
                            let aux = wf["outputs"][j];
                            if (aux === undefined) {
                                aux = wf["outputs"][0];
                            }
                            let nodeID = aux["targets"][0]["nodeId"];

                            if (nodeID === undefined) {
                                nodeID = aux["targets"]["nodeId"];
                            }
                            if (nodeID) {
                                let el_l = JSON.parse(JSON.stringify(el));
                                el_l['task_id'] = nodeID;
                                el_l['outputs'] = e;
                                $.each(JSON.parse(workflowJson)["wf_body"]["nodes"], function (pipe_index, pipe_wf) {
                                    // console.log(el_l['task_id'], pipe_wf['task_id'])
                                    if (el_l['task_id'] === pipe_wf['task_id']) {
                                        el_l['task_name'] = pipe_wf['task_name']
                                    }
                                })
                                // console.log('final stuff-----------',el_l)
                                finalMetaDataResponse.push(el_l)
                            }
                        }
                    })
                })
            });
            NODES_WITH_METADATA = finalMetaDataResponse
            return NODES_WITH_METADATA;
        },
        error: function (response) {
            console.log('error in retreiving resp', response);
            //showPopupError(response.message);
        }
    });
}

function GET_NODES_DATA(username) {
    let data = [];
    $.ajax({
        url: API_URL + GET_NODE_OUTPUT_METADATA,
        method: "POST",
        async: false,
        contentType: "application/json",
        cache: false,
        datatype: "json",
        data: JSON.stringify({
            "wf_unique_id": username
        }),
        success: function(response) {
            data = response;
        },
        error: function(response) {
            console.log("GET_NODE_DATA Errot " + response);
        }
    })
    return data["Result"];
}

function giveMeMyDATA() {
    return ORIGINAL_NODES_WITH_METADATA;
}

export {
    //jsplumbClient
    ORIGINAL_NODES_WITH_METADATA,
    getCorrelationMatrix,
    saveDeployedWorkflow,
    workFlowExecution,
    sendWorkflowToExecute,
    getOutputData,
    getModelOutput,
    handleClassificationTasksOutput,
    getEvalMetrics,
    newGetEvalMetrics,
    getHistogram,
    getPairwise,
    sendWorkflowForSaving,
    createWorkflow,
    getWorkflowByExperimentId,
    giveMeMyDATA,
    //jsplumbClient | NodeManager
    getNodeOutputMetadata,
    GET_NODES_DATA,
    sendReadcsvFile
}