import {
    diagramContainer_MouseMove,
    diagramContainer_Click,
    diagramContainer_MouseUp,
    diagramContainer_MouseDown
} from "./WorkFlowManager.js";

import {
    loadNodes,
    buildWorkflow
} from "./NodeManager.js";

import {
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
    getNodeOutputMetadata,
    GET_NODES_DATA,
    sendReadcsvFile,
    getKaggleDatasetsList
} from "./ApiClient.js";

import {
    removeNumbersFromStr,
    showPanel,
    hidePanel,
    getUrlParameterByName,
    prepareSelect,
    appendToSelect,
    removeNumberFromString,
    roundNumberToTwoDigits
} from "./Util.js";

const propertiesWindowDeafultHintMessage = "Task Properties and Description";
const connectAnode = "Please connect a node to select one";
const canvasDeafultHintMessage = "Please drag and drop Tasks Here";
let workflow = null

function showPropertiesWindowDefaultMessage() {
    $("#propertiesBody").html('<h4 id="propertiesWindowHint">' + propertiesWindowDeafultHintMessage + '</h4>');
}

function showConnectNodetMessage() {
    $("#propertiesBody").html('<h4 id="propertiesWindowHint">' + connectAnode + '</h4>');
}

function showCanvasDefaultMessage() {
    if (nodesList.length < 1) { //No Nodes in canvas
        $("#canvas > h4").after('<h2 id="canvasHint">' + canvasDeafultHintMessage + '</h2>');
    }
}

function removeUnneededOptionFromPlotlyChart() {
    $(".plotlyjsicon").remove();
    $("[data-title='Save and edit plot in cloud']").remove();
}

function preparePairwiseTab(jsonData) {
    $("#pairwise-graph-div").html(jsonData);
    $("#pairwise-graph-div>img").css("max-height", "510px");
    removeUnneededOptionFromPlotlyChart();
}

export default function run() {
    const experimentId = localStorage.getItem("username");
    let isSummaryTableRan = false;
    let isSampleDataTableRan = false;
    let isWorkflowRanSuccessfuly = false;
    let executionType = "execution";
    let nodesList = [];
    localStorage.removeItem("kaggle_dataset_node");

    jsPlumb.ready(function () {
        let instance = window.jsp = jsPlumb.getInstance({
            // default drag options
            DragOptions: {
                cursor: 'pointer',
                zIndex: 2000
            },
            // the overlays to decorate each connection with.  note that the label overlay uses a function to generate the label text; in this
            // case it returns the 'labelText' member that we set on each connection in the 'init' method below.
            ConnectionOverlays: [
                ["Arrow", {
                    location: 1,
                    visible: true,
                    width: 11,
                    length: 11,
                    id: "ARROW",
                    events: {
                        click: function () {
                            //alert("you clicked on the arrow overlay")
                        }
                    }
                }],
                ["Label", {
                    location: 0.1,
                    id: "label",
                    cssClass: "aLabel",
                    events: {
                        tap: function () {
                            //alert("hey");
                        }
                    }
                }]
            ],
            Container: "canvas"
        });

        //showPropertiesWindowDefaultMessage();
        //showCanvasDefaultMessage();

        loadNodes(instance, nodesList);

        //to select some nodes (sub-selecttion) from the whole diagram
        // we need node-selector.js for this
        $("#canvas").mousedown(diagramContainer_MouseDown);
        $("#canvas").mousemove(diagramContainer_MouseMove);
        $("#canvas").mouseup(diagramContainer_MouseUp);
        $("#canvas").click(diagramContainer_Click);

        let basicType = {
            connector: "StateMachine",
            paintStyle: {
                stroke: "red",
                strokeWidth: 4
            },
            hoverPaintStyle: {
                stroke: "blue"
            },
            overlays: [
                "Arrow"
            ]
        };
        instance.registerConnectionType("basic", basicType);

        let init = function (connection) {
            connection.getOverlay("label").setLabel(connection.sourceId.substring(15) + "-" + connection.targetId.substring(15));
        };

        // suspend drawing and initialise.
        instance.batch(function () {

            // listen for new connections; initialise them the same way we initialise the connections at startup.
            instance.bind("connection", function (connInfo, originalEvent) {
                init(connInfo.connection);
            });

            // make all the window divs draggable
            instance.draggable(jsPlumb.getSelector(".flowchart-demo .window"), {
                grid: [20, 20]
            });

            //
            // listen for clicks on connections, and offer to delete connections on click.
            //
            instance.bind("click", function (conn, originalEvent) {
                conn.toggleType("basic");
            });

            instance.bind("connectionDrag", function (connection) {
                console.log("connection " + connection.id + " is being dragged. suspendedElement is ", connection.suspendedElement, " of type ", connection.suspendedElementType);
            });

            instance.bind("connectionDragStop", function (connection) {
                console.log("connection " + connection.id + " was dragged");
            });

            instance.bind("connectionMoved", function (params) {
                console.log("connection " + params.connection.id + " was moved");
            });
        });

        jsPlumb.fire("jsPlumbDemoLoaded", instance);

        $("#executeButton").click(function () {
            isWorkflowRanSuccessfuly = false;
            let nodeName = isWorkflowSAVED();
            if (nodeName === "")
                executeWorkflow();
        });

        $("#deployWorkflow").click(function () {
            $("#deploy_modal").modal("show");
        });

        $("#deploy_click").click(function () {
            const request_data = {
                name: "", //input
                description: "", //input
                version: "", //input
                model_name: "", //input
                username: "", // input
                columns: "", //json as string
                eval_metrics: "", //json as string
            };

            // extra inputs
            if ($('#deploy_modal input[name="name"]')[0].value !== "")
                request_data.name = $('#deploy_modal input[name="name"]')[0].value;
            if ($('#deploy_modal input[name="version"]')[0].value !== "")
                request_data.version = $('#deploy_modal input[name="version"]')[0].value;
            if ($('#deploy_modal textarea')[0].value !== "")
                request_data.description = $('#deploy_modal textarea')[0].value;

            // eval_matrics and username
            const USERNAME = localStorage.getItem("username");
            const NODE_ID = $("#canvas div[type*=metrics]").attr("id")
            request_data.eval_metrics = JSON.stringify(newGetEvalMetrics(USERNAME, NODE_ID));
            request_data.username = USERNAME;

            // get Run Model seleced value
            let run_model_value = null;
            for (let i = 0; i < workflow.length; i++) {
                const DESCRIPTION = workflow[i].desc;
                const MODEL_NAME = DESCRIPTION.slice("Task Name: ".length, DESCRIPTION.indexOf("<br>"));
                if (MODEL_NAME === "Run Model") {
                    run_model_value = workflow[i].proprties[0].value;
                    break;
                }
            }
            // columns
            const COLUMNS = [];
            const NODES_DATA = GET_NODES_DATA(USERNAME);
            let isCategoryExist = false;
            for (let node_index = 0; node_index < NODES_DATA.length; node_index++) {
                const TYPES = NODES_DATA[node_index].outputs[0].dtypes;
                const KEYS = Object.keys(TYPES);

                if (NODES_DATA[node_index].task_name === "CategoryEncoding") {
                    isCategoryExist = true;
                    for (let key_index = 0; key_index < KEYS.length; key_index++) {

                        if (KEYS[key_index] === "mappings")
                            continue;

                        const COLUMN = {
                            name: KEYS[key_index]
                        };

                        // if column is classifcation or run_dev_value
                        if (KEYS[key_index] === run_model_value)
                            COLUMN.run_model = true;

                        // if column has categories
                        if (TYPES.mappings.hasOwnProperty(KEYS[key_index])) {
                            const VALUES = {};
                            Object.keys(TYPES.mappings[KEYS[key_index]]).forEach(node => {
                                VALUES[node] = TYPES.mappings[KEYS[key_index]][node]
                            });
                            COLUMN.values = VALUES;
                        }
                        COLUMNS.push(COLUMN)
                    }
                    break;
                }
            }

            if (!isCategoryExist) {
                for (let node_index = 0; node_index < NODES_DATA.length; node_index++) {
                    const TYPES = NODES_DATA[node_index].outputs[0].dtypes;
                    const KEYS = Object.keys(TYPES);

                    if (NODES_DATA[node_index].task_name === "SelectColumns") {
                        for (let key_index = 0; key_index < KEYS.length; key_index++) {
                            if (KEYS[key_index] === run_model_value)
                                continue;

                            COLUMNS.push({
                                name: KEYS[key_index]
                            })
                        }
                        break;
                    }
                }
            }
            request_data.columns = JSON.stringify(COLUMNS);

            // model_name
            const models = [
                // *Incremental Learning [GROUP]
                // >Classification [SUB-GROUP]
                "SGDC_Calissifier",
                "MultinomialNB_Classifier",
                "BernoulliNB_Classifier",
                "Perceptron_Classifier",
                "PassiveAggressive_Classifier",
                // >Regression [SUB-GROUP]
                "PassiveAggressive_Regressor",
                // >Clustering [SUB-GROUP]
                "MiniBatchKMeans",

                // *Machine Learning [GROUP]
                // >TOP [SUB-GROUP]
                "XGBRegressor",
                "XGBClassifier",
                "LGBMClassifier",
                "BaggingClassifier",
                "LGBMRegressor",
                "Adaboost",
                "CatBoost",
                "LSTM_Model",
                // >Classic [SUB-GROUP]
                "RandomForestClassifier",
                "LinearRegression",
                "RandomForestRegression",
                "DecisionTreeClassifier",
                "KNeighborsClassifier",
                "LogisticRegressionClassifier",
                "MultilayerPerceptronClassifier",
                "Kmeans"
            ];
            const nodes = $("#canvas div[id*='flowchartNode']");
            nodes.each((index) => {
                const type = nodes[index].getAttribute('type');
                if (models.includes(type))
                    request_data.model_name = type;
            })

            saveDeployedWorkflow(request_data);
        });

        $("#importWorkFlow").click(function () {
            let files = document.getElementById('selectFiles').files;
            console.log(files);
            if (files.length <= 0) {
                window.alert('have you choose the file?');
                return false;

            }
            console.log(files[0]);
            if (files[0].type != 'application/json') {
                window.alert('Invalid file type, expecting json file only');
                return false;
            }

            console.log(files[0].name);

            let fr = new FileReader();

            fr.onload = function (e) {
                console.log(e);
                let result = JSON.parse(e.target.result);
                let formatted = JSON.stringify(result, null, 2);
                formatted = JSON.parse(result);
                let aux = buildWorkflow(JSON.stringify(formatted), instance);
                nodesList.push(...aux);
                workflow = aux;
            }

            fr.readAsText(files.item(0));
        });

        // $("#clearWorkflow").click(function () { //Save file locally
        //     swal({
        //         title: "Are You Sure You Want to Clear?",
        //         text: "Click On OK for YES!",
        //         type: "warning",
        //         showCancelButton: true,
        //         closeOnConfirm: true,
        //         showLoaderOnConfirm: false
        //     }, function () {
        //         setTimeout(function () {
        //             location.reload();
        //         }, 500);
        //     })
        // });

        //Deleting selected nodes
        $("#remove_node").click(function () {
            removeAllSelectedNodes();
            removeAllSelectedConnections();
        });

        $("#clear").click(function () {
            removeAllNodes();
            removeAllSelectedConnections();
        });

        // $("#saveDeployedWorkflowButton").click(function () {


        //     workflowName = $("#workflowNameFeild").val();
        //     if (workflowName !== "") {
        //         let flowDiagramJson = formatFlowDiagramAsJson(instance.getAllConnections());
        //         flowDiagramJson = JSON.parse(flowDiagramJson);
        //         flowDiagramJson.experimentName = workflowName;
        //         flowDiagramJson.userId = user.userId;
        //         flowDiagramJson = JSON.stringify(flowDiagramJson);

        //         saveDeployedWorkflow(flowDiagramJson);
        //     }

        // });


        //To catch any click on node list frm side bar
        // $("#sidebar-menu").on("click", "a.sub-nav-link", function (event) {

        // });

        // To highlight any node on click for showing properties or for deletion
        $("#canvas").on("mouseenter", "div.jtk-node", function (event) {

            //determine whether it's been draged or just clicked
            let isDragging = false;
            $(this)
                .mousedown(function () {
                    isDragging = false;
                })
                .mousemove(function () {
                    // isDragging = true;
                })
                .mouseup(function () {
                    let wasDragging = isDragging;
                    isDragging = false;
                    if (!wasDragging) {
                        //it's clicked only

                        //Multi node selection
                        // $(document).keydown(function(event){
                        if (event.ctrlKey) {
                            // 17 means Control button is pressed
                            handleMultiNodeSelection(this);
                        }
                        // });
                        else {
                            //Single node Selection
                            handleSingleNodeSelection(this);
                        }
                    }
                    $("div.jtk-node").unbind('mouseup');
                });

            // For Right click (context menu)
            $(this).contextMenu({
                menuSelector: "#contextMenu",
                menuSelected: function (invokedOn, selectedMenu) {

                    let nodeId = invokedOn.attr("id");
                    //Probably hitted on <strong>
                    if (nodeId == undefined) {

                        nodeId = invokedOn.parent().attr("id");

                    } else if (nodeId.includes("_")) {
                        nodeId = nodeId.split("_")[0];
                    }
                    //TODO for demo puprpose only (workaround)
                    let nodeType = $("#" + nodeId).attr("type");


                    $("#histogram-div").attr("nodeId", nodeId);
                    $("#pairwise-div").attr("nodeId", nodeId);
                    $("#correlation-div").attr("nodeId", nodeId);

                    let pressedOptionValue = $(this).attr("value").split("_")[0];
                    if (pressedOptionValue === 'execute') {

                        isWorkflowRanSuccessfuly = false;
                        executeWorkflow(nodeId);

                    } else if (pressedOptionValue === 'showOutput') {

                        let outputNumber = selectedMenu.attr("value").split("_")[1];
                        $("#histogram-div").attr("outputId", outputNumber);
                        $("#pairwise-div").attr("outputId", outputNumber);
                        $("#correlation-div").attr("outputId", outputNumber);
                        getOutputData(experimentId, nodeId, outputNumber, nodeType, handleDataOutput);

                    } else if (pressedOptionValue === 'showModelOutput') {

                        let outputNumber = selectedMenu.attr("value").split("_")[1];
                        getModelOutput(experimentId, nodeId, outputNumber, nodeType, handleModelOutput);

                    } else if (pressedOptionValue === 'showModelEval') {
                        getEvalMetrics(experimentId, nodeId);

                    }

                }
            });
        });

        function isWorkflowSAVED() {
            let i = 1;
            let result = "";
            $.each(nodesList, function (key, val) {
                for (const property of val.proprties) {
                    //TODO rerturn the node name with needs to be saved
                    if (property['value'] === "") {
                        result = val.id;
                    }
                }
                i++;
            });
            return result;
        }


        //click box, onclick box, box
        function handleSingleNodeSelection(node) {
            //remove highlight from any highlighted nodes
            unHighlightAllNodes();
            //Highlight selected node onle
            highlightSelectedNode(node);

            // Kaggle Dataset ONLY
            if ($(node).attr("type") === "KaggleDataset") {
                // init
                let page = 1;
                let search = "";
                let html = "";

                if (localStorage.getItem("kaggle_dataset_node")) {
                    const kaggle_dataset_node = JSON.parse(localStorage.getItem("kaggle_dataset_node"));
                    $("#propertiesBody").html(kaggle_dataset_node.html);
                    $("#kaggle_dataset_pagenumber").html(kaggle_dataset_node.page);
                    $("#kaggle_dataset_search_input").val(kaggle_dataset_node.search)
                    if (page < 1)
                        $("#kaggle_dataset_back").addClass("disabled");
                }
                else {
                    getKaggleDatasetsList(1, "")
                        .success((data) => {
                            html = updateKaggleDatasets(data)
                            $("#propertiesBody").html(html);
                            $("#kaggle_dataset_pagenumber").html(page);
                            $("#kaggle_dataset_search_input").val(search)
                            $("#kaggle_dataset_back").addClass("disabled");
                            localStorage.setItem("kaggle_dataset_node", JSON.stringify({
                                html,
                                page,
                                search
                            }))
                        })
                }

                // When You clik into dataset
                $("#propertiesBody").on("click", ".option", function () {
                    // switch active
                    $(".option.active").removeClass("active")
                    $(this).addClass("active")
                    // remove disabled from the submit button
                    $("#kaggle_dataset_submit").removeClass("disabled");
                    // set value
                    $("#kaggle_dataset").attr("value", $(this).attr('value'));
                });

                // SEARCH Button
                $("#propertiesBody").on("click", "#kaggle_dataset_search_submit", function (e) {
                    page = 1;
                    search = $("#kaggle_dataset_search_input").val();
                    getKaggleDatasetsList(page, search)
                        .success((data) => {
                            html = updateKaggleDatasets(data)
                            $("#propertiesBody").html(html);
                            $("#kaggle_dataset_pagenumber").html(page);
                            $("#kaggle_dataset_search_input").val(search)
                            $("#kaggle_dataset_back").addClass("disabled");
                            localStorage.setItem("kaggle_dataset_node", JSON.stringify({
                                html,
                                page,
                                search
                            }))
                        })
                    e.preventDefault();
                });

                // BACK Button
                $("#propertiesBody").on("click", "#kaggle_dataset_back", function (e) {
                    const kaggle_dataset_node = JSON.parse(localStorage.getItem("kaggle_dataset_node"));
                    page = kaggle_dataset_node.page;
                    search = kaggle_dataset_node.search;
                    if (page > 1) {
                        getKaggleDatasetsList(--page, search)
                            .success((data) => {
                                html = updateKaggleDatasets(data)
                                $("#propertiesBody").html(html);
                                $("#kaggle_dataset_pagenumber").html(page);
                                $("#kaggle_dataset_search_input").val(search);
                                localStorage.setItem("kaggle_dataset_node", JSON.stringify({
                                    html,
                                    page,
                                    search
                                }));

                                if (page === 1)
                                    $("#kaggle_dataset_back").addClass("disabled");
                            });
                    }
                    e.preventDefault();
                });

                // NEXT Button
                $("#propertiesBody").on("click", "#kaggle_dataset_next", function (e) {
                    const kaggle_dataset_node = JSON.parse(localStorage.getItem("kaggle_dataset_node"));
                    page = kaggle_dataset_node.page;
                    search = kaggle_dataset_node.search;
                    getKaggleDatasetsList(++page, search)
                        .success((data) => {
                            html = updateKaggleDatasets(data)
                            $("#propertiesBody").html(html);
                            $("#kaggle_dataset_pagenumber").html(page);
                            $("#kaggle_dataset_search_input").val(search);
                            localStorage.setItem("kaggle_dataset_node", JSON.stringify({
                                html,
                                page,
                                search
                            }));
                        });
                    e.preventDefault();
                });

                // SUBMIT Button
                $("#propertiesBody").on("click", "#kaggle_dataset_submit", function (e) {
                    let value = $("#kaggle_dataset").attr('value');

                    // save value in nodesList
                    nodesList.forEach(function (object, index) {
                        object.proprties.forEach(function (property, index) {
                            if (property.display_name === "Dataset Name")
                                property.value = value;
                        })
                    })

                    updateNodeProperties(value);
                    let workflowJson = formatFlowDiagramAsJson(instance.getAllConnections());
                    let asjson = JSON.parse(workflowJson);
                    asjson.wf_body.nodes[0].parameters[0].value = value;
                    workflowJson = JSON.stringify(asjson)
                    let flowDiagramJson = workflowJson.replace('SelectDataset', 'SelectDatasetSample').replace('ReadCSV', 'ReadCSVSample')
                    workFlowExecution(flowDiagramJson);
                    e.preventDefault();
                });
            }

            // OTHER
            else {
                sampleExecuteWorkflow(node['id']);
                //get node attributes        
                let windowBody = getPropertiesAsHtml($(node).attr("id"), $(node).attr("kind"));
                //replace properties window
                $("#propertiesBody").html(windowBody);
                // incase we have Multi select element needs to be prepared
                $("#propertiesBody").find('.multiselect-ui').multiselect({
                    includeSelectAllOption: true
                });
            }
        }

        function updateKaggleDatasets(datasets) {
            const startHTML =
                `
            <form> 
            <div id="kaggle_dataset">
            <div class="kaggle_dataset_title">Kaggle Datasets</div>
            <div class="search_input_container">
                <input id="kaggle_dataset_search_input" type="text" placeholder="Ex: Car Dataset">
                <button id="kaggle_dataset_search_submit">Search</button>
            </div>
            <div class="select-container">
                <div class="layout">
            `
            const endHTML =
                `
                </div>
                </div>
                <div class="pagination-container">
                    <button id="kaggle_dataset_back">
                        <div class="icon-container left">
                            <i class="icon left fa fa-angle-left" aria-hidden="true"></i>
                        </div>
                    </button>
                    <div id="kaggle_dataset_pagenumber"></div>
                    <button id="kaggle_dataset_next">
                        <div class="icon-container right">
                            <i class="icon right fa fa-angle-right" aria-hidden="true"></i>
                        </div>
                    </button>
                </div>
                <div class="button-container">
                    <button id="kaggle_dataset_submit" class="disabled">Set Value</button>
                </div>
            </div>
            `
            let middleHTML = ''
            $.each(datasets, function (i, dataset) {
                middleHTML += `<div class="option" value="${dataset.ref}"> ${dataset.name}</div>`
            });
            return startHTML + middleHTML + endHTML;
        }

        function handleMultiNodeSelection(node) {
            // alert("Multi Selection");
            $(node).addClass("selected");
        }

        function formatFlowDiagramAsJson(connectionsList, executeToNode) {
            let nodesWithNoRelation = [];
            nodesWithNoRelation = getAllNodesInFlowDiagram();
            //JSON Elements Init.
            let jsonObj = new Object();
            let nodes = [];
            let node;
            let outputs;

            let allConnectionsArrCopy = connectionsList.slice();
            for (let i = 0; i < nodesWithNoRelation.length; i++) {
                // $.each(allConnectionsArrCopy, function(index, el){
                if (nodesWithNoRelation[i] !== undefined) {
                    // nodesWithNoRelation.splice(index, 1);

                    //create new Node
                    node = {};
                    node.task_name = $("#" + nodesWithNoRelation[i]).attr("type");
                    node.task_id = nodesWithNoRelation[i];
                    node.position = $("#" + nodesWithNoRelation[i]).attr("style");

                    //Create its Output List
                    outputs = [];
                    //Search for other relations for the same node
                    outputs = fetchNodeOutputs(nodesWithNoRelation[i], allConnectionsArrCopy);
                    // i--;
                    node.outputs = outputs;
                    node.parameters = retreiveNodeProperties(node.task_id, node.task_name);
                    nodes.push(node);

                    // if(searchForNodeInList(allConnectionsArrCopy, el.sourceId) != null){
                    //     output = new Object();
                    //     output.id = removeNumbersFromStr(el.endpoints[0].id);
                    // }
                }
                // });
            }
            jsonObj.nodes = nodes;
            let tmpObj = new Object();
            tmpObj.wf_unique_id = experimentId;
            tmpObj.wf_body = jsonObj;
            tmpObj.run_to_task_id = "";
            if (executeToNode != undefined) {
                tmpObj.run_to_task_id = executeToNode;
            }
            return JSON.stringify(tmpObj);

        }

        function getAllNodesInFlowDiagram() {
            let allNodes = [];
            $.each($("div.jtk-node"), function (index, el) {
                allNodes.push(el.id);
            });

            return allNodes;
        }

        function searchForNodeInList(nodes, nodeId) {
            $.each(nodes, function (index, el) {
                if (el.id === nodeId) {
                    return el;
                }
            });
            return null;
        }

        function fetchNodeOutputs(nodeId, connecionsList) {
            let output;
            let target;
            let outputs = [];

            $.each(connecionsList, function (index, el) {
                if (el != undefined && el.sourceId === nodeId) {
                    output = new Object();
                    output.id = /*convertToLuigiPortNames(el.endpoints[0].id.substring(0,2))*/ removeNumbersFromStr(el.endpoints[0].id);
                    output.targets = [];

                    target = new Object();
                    target.nodeId = el.targetId;
                    target.id = /*convertToLuigiPortNames(el.endpoints[1].id.substring(0,2))*/ removeNumbersFromStr(el.endpoints[1].id);

                    output.targets.push(target);
                    outputs.push(output);
                    // connecionsList.splice(index, 1);
                }
            });

            return outputs;

        }

        $(document).keydown(function (event) {

            if (event.which == "46") {
                //Del button is pressed
                removeAllSelectedNodes();
                removeAllSelectedConnections();
            }

        });

        function isConnectionHighlited(connection) {
            let types = connection._jsPlumb.types;
            let found = false;
            $.each(types, function (i, el) {
                if (el === "basic") {
                    found = true;
                }
            });
            return found;
        }

        function removeAllNodes() {
            if ($(this).attr("type") === "KaggleDataset")
                localStorage.removeItem("kaggle_dataset_node");

            $("div.jtk-node").each(function () {
                let nodeId = $(this).attr("id");
                //remove all Endpoints and attached connections
                instance.removeAllEndpoints(nodeId);
                //renove the node itself
                instance.remove(nodeId);
                //close properties if opened
                hidePanel("propertiesWindow");
                //Remove from nodeList
                removeNodeFromNodeList(nodeId);
                //showPropertiesWindowDefaultMessage();
                //showCanvasDefaultMessage();
            });
        }

        function removeAllSelectedNodes() {
            $("div.jtk-node.selected").each(function () {
                let nodeId = $(this).attr("id");
                //remove all Endpoints and attached connections
                instance.removeAllEndpoints(nodeId);
                //renove the node itself
                instance.remove(nodeId);
                //close properties if opened
                hidePanel("propertiesWindow");
                //Remove from nodeList
                removeNodeFromNodeList(nodeId);
                //showPropertiesWindowDefaultMessage();
                //showCanvasDefaultMessage();
            });
        }

        function removeAllSelectedConnections() {
            let allConnections = instance.getAllConnections();
            $.each(allConnections, function (i, conn) {
                if (isConnectionHighlited(conn)) {
                    instance.deleteConnection(conn);
                }
            });
        }


        function retreiveNodeProperties(nodeId, nodeType) {
            let properties = [];
            $.each(nodesList, function (key, val) {
                if (val.id === nodeId) {
                    // properties = val.proprties;
                    // if(nodeType === 'ChangeDtypes'){
                    $.each(val.proprties, function (key, property) {
                        let prop = new Object();
                        prop.name = property.name;
                        prop.type = property.type;
                        prop.display_name = property.display_name;
                        if (property.lookup) {
                            prop.lookup = property.lookup;
                        }
                        if (property.type === 'columns_with_names' || property.type === 'columns_with_types') {
                            prop.value = new Object();
                            if (property.value !== "") {
                                if (typeof property.value === "object") { //if value is retrived from old workflow
                                    prop.value = property.value
                                } else { //if it's a new workflow
                                    prop.value = JSON.parse(property.value.replace(/\'/g, '"'));
                                }
                            }
                        } else {
                            if (prop.name === "csv_path") {
                                if ($("#csv_path_value") !== null)
                                    prop.value = $("#csv_path_value").attr('value')
                            }
                            else
                                prop.value = property.value;
                        }
                        properties.push(prop);
                    });
                    // }
                    return false; // to break out
                }
            });
            return properties;
        }

        function updateNodeProperties(nodeId) {

            $.each(nodesList, function (key, val) {
                if (val.id === nodeId) {
                    $.each(val.proprties, function (i, el) {
                        if (el.lookup != undefined) {

                            el.value = $("#" + el.name + "_value").find(":selected").val();

                        } else if (el.type === "text_area") {

                            el.value = $("#" + el.name + "_value").val();

                        } else if (el.type === "single_column") {

                            el.value = $("#" + el.name + "_value").find(":selected").val();

                        } else if (el.type === "multiple_columns") {
                            let theValue = $("#" + el.name + "_value");
                            if (theValue.val() !== null) {
                                el.value = theValue.val().toString();
                            }

                        } else if (el.type === "columns_with_types") {
                            //alert("lookups here 44444??")
                            let value = "";

                            if ($("#propertiesBody > form > div").length > 0) {
                                value = "{";
                                $("#propertiesBody > form > div").each(function () {
                                    value += "'" + $(this).find("#" + el.name + "_value").val() + "'";
                                    value += ":";
                                    value += "'" + $(this).find("#dataTypeSelect").val() + "',";
                                });
                                value = value.substring(0, value.length - 1) // to remove last unneeded comma
                                value += "}";
                            }

                            el.value = value;

                        } else if (el.type === "columns_with_names") {
                            let value = "";

                            if ($("#propertiesBody > form > div").length > 0) {
                                value = "{";
                                $("#propertiesBody > form > div").each(function () {
                                    value += "'" + $(this).find("#" + el.name + "_value").val() + "'";
                                    value += ":";
                                    value += "'" + $(this).find("#columnNewName").val() + "',";
                                });
                                value = value.substring(0, value.length - 1) // to remove last unneeded comma
                                value += "}";
                            }

                            el.value = value;

                        } else {
                            el.value = $("#" + el.name + "_value").val();
                        }

                    });
                }
            });
        }

        function removeNodeFromNodeList(nodeId) {
            $.each(nodesList, function (key, val) {
                if (val.id === nodeId) {
                    nodesList.splice(key, 1);
                    return false; //To breake out
                }
            });
        }

        function getInputs(nodeId) {
            let inputsOutputs = giveMeMyDATA();
            if (inputsOutputs.length > 0) {
                for (const meta of inputsOutputs) {
                    if (meta.task_id === nodeId) {
                        let e = meta.outputs[0];
                        if (e === undefined) {
                            e = meta.outputs;
                        }
                        let columnItems = Object.keys(e.dtypes);
                        return columnItems;
                    }

                }
            }
            return null;
        }


        function getMyInputs(inputs, name, n) {
            if (n < 2) return inputs;

            let predicted = inputs.map(function (o) {
                if (o.includes("predic")) return o;
            }).filter(Boolean);

            if (name === "predict_column") {
                return predicted
            } else {
                return inputs.filter(x => !predicted.includes(x));
            }

        }

        function getNodeInputs(nodeId) {
            let parentNodeDetails = getDataPortParentSourceNode(nodeId);
            let inputs = getInputs(parentNodeDetails.sourceNodeId);
            // debugger
            return [inputs, parentNodeDetails];
        }

        function updateInputWithOutputs(nodesList, nodeId, nodeType) {
            //the metadata is tricked by a suspicious code, then actual nodeName has the output
            // of the previous one and first node is out of business.

            if (nodeType !== "noInput") {
                let inputsAndParents = getNodeInputs(nodeId);
                let inputs = inputsAndParents[0];
                if (inputs === null) {
                    showConnectNodetMessage();
                    return nodesList;
                }
                let parentNodeDetails = inputsAndParents[1];
                if (Object.keys(parentNodeDetails).length > 0) {
                    let includedTypes = ["single_column"];
                    let i = 1;
                    $.each(nodesList, function (key, val) {

                        //fitmodel runmodel and others
                        if (val.id === nodeId) {
                            let n = val.proprties.length;
                            for (const property of val.proprties) {
                                //TODO generic for all columns types, sigle and multiple...
                                if (includedTypes.includes(property['type']) || nodeType === 'dataTransformation') {
                                    //lookUp = JSON.parse('{"lookup":["y","not select me"]}');
                                    property['lookup'] = getMyInputs(inputs, property['name'], n); //lookUp['lookup'];
                                }
                            }
                            return nodesList
                        }
                        i++;
                    });
                } else {
                    showConnectNodetMessage();
                    //alert("Please connect the node");
                }
            }
            return nodesList;
        }

        /*
        Rendering of right menu after click of elements
        right menu
        */

        function getPropertiesAsHtml(nodeId, nodeType) {
            let html = "";
            nodesList = updateInputWithOutputs(nodesList, nodeId, nodeType);
            $.each(nodesList, function (key, val) {
                if (val.id === nodeId) {
                    if (val.proprties.length > 0) {
                        html += '<form>';
                        $.each(val.proprties, function (i, el) {

                            // Replace display_name
                            if (el.display_name === "CSV Path")
                                el.display_name = "CSV"

                            html += '<div class="form-group">';
                            html += '<label for="' + el.name + '">' + el.display_name + '</label>';

                            if (el.lookup != undefined) { // for props with lookups
                                html += '<select id="' + el.name + '_value" class="form-control" style="background-color: #8080805c  ; margin-left: 8px;">';
                                if (el.name == "dataset_name") {
                                    $.each(el.lookup, function (i, element) {
                                        html += '<option value="' + element['uuid'] + '"';
                                        if (el.value === element['uuid']) {
                                            html += ' selected="selected"';
                                        }
                                        html += '>' + element['name'] + '</option>'; //showing drop down
                                    });
                                } else {
                                    $.each(el.lookup, function (i, element) {
                                        html += '<option value="' + element + '"';
                                        if (el.value === element) {
                                            html += ' selected="selected"';
                                        }
                                        html += '>' + element + '</option>';
                                    });
                                }
                                html += '</select>';
                            } else if (el.type === "text_area") {

                                html += '<textarea id="' + el.name + '_value" type="text" class="form-control" value="' + el.value + '">' + el.value + '</textarea>';

                            } else if (el.type === "single_column") {
                                html += '<select id="' + el.name + '_value" class="form-control">';
                                html += getColumnNamesMetaDataAsOptions(nodeId, el.value);
                                html += '</select>';

                            } else if (el.type === "multiple_columns") {
                                html += '<select id="' + el.name + '_value" class="multiselect-ui form-control" multiple="multiple" style="background-color: #8080805c  color: #ffffff;padding: 8px 16px; border: 1px solid transparent; border-color: transparent transparent rgba(0, 0, 0, 0.1) transparent; cursor: pointer; user-select: none;">';
                                html += getColumnNamesMetaDataAsOptions(nodeId, el.value, nodeType);
                                html += '</select>';

                            } else if (el.type === "columns_with_types") { //changeDType
                                html = ''; //to start the string over in order to drow add Column div
                                html += '<div id="addColumnWithType" class="addColumn">';
                                html += '<i class="fa fa-plus"></i>';
                                html += '<label>Add column</label>';
                                html += '<hr>';
                                html += '</div>';

                                html += '<form>';
                                if (el.value === "") { // not set before (New)
                                    html += '<div>';
                                    html += '<div class="form-group">';
                                    html += '<label for="' + el.name + '">' + el.display_name + '</label>';
                                    html += '<div class="removeColumn">';
                                    html += '<i class="fa fa-minus"></i> Remove</div>';
                                    html += '<select id="' + el.name + '_value" class="form-control">';
                                    html += getColumnNamesMetaDataAsOptions(nodeId, undefined, nodeType);
                                    html += '</select>';
                                    html += '</div>';
                                    html += '<div class="form-group">';
                                    html += '<label for="dataTypeSelect">Data Type</label>';
                                    html += '<select id="dataTypeSelect" class="form-control">';
                                    html += getDataTypesAsOptions();
                                    html += '</select>';
                                    html += '</div>';
                                    html += '<hr>';
                                    html += '</div>';
                                } else {
                                    if (typeof el.value !== "object") {
                                        el.value = JSON.parse(el.value.replace(/\'/g, '"'));
                                    }
                                    $.each(el.value, function (columnName, dataType) {
                                        html += '<div>';
                                        html += '<div class="form-group">';
                                        html += '<label for="' + el.name + '">' + el.display_name + '</label>';
                                        html += '<div class="removeColumn">';
                                        html += '<i class="fa fa-minus"></i> Remove</div>';
                                        html += '<select id="' + el.name + '_value" class="form-control">';
                                        html += getColumnNamesMetaDataAsOptions(nodeId, columnName);
                                        html += '</select>';
                                        html += '</div>';
                                        html += '<div class="form-group">';
                                        html += '<label for="dataTypeSelect">Data Type</label>';
                                        html += '<select id="dataTypeSelect" class="form-control">';
                                        html += getDataTypesAsOptions(dataType);
                                        html += '</select>';
                                        html += '</div>';
                                        html += '<hr>';
                                        html += '</div>';
                                    })
                                }

                            } else if (el.type === "columns_with_names") { //changeColumnNames

                                html = ''; //to start the string over in order to drow add Column div
                                html += '<div id="addColumnWithName" class="addColumn">';
                                html += '<i class="fa fa-plus"></i>';
                                html += '<label>Add column</label>';
                                html += '<hr>';
                                html += '</div>';

                                html += '<form>';
                                if (el.value === "") { // not set before (New)
                                    html += '<div>';
                                    html += '<div class="form-group">';
                                    html += '<label for="' + el.name + '">' + el.display_name + '</label>';
                                    html += '<div class="removeColumn">';
                                    html += '<i class="fa fa-minus"></i> Remove</div>';
                                    html += '<select id="' + el.name + '_value" class="form-control">';
                                    html += getColumnNamesMetaDataAsOptions(nodeId);
                                    html += '</select>';
                                    html += '</div>';
                                    html += '<div class="form-group">';
                                    html += '<label for="columnNewName">New Name</label>';
                                    html += '<input id="columnNewName" type="text" class="form-control" value="">';
                                    html += '</div>';
                                    html += '<hr>';
                                    html += '</div>';
                                } else {
                                    if (typeof el.value !== "object") {
                                        el.value = JSON.parse(el.value.replace(/\'/g, '"'));
                                    }
                                    $.each(el.value, function (columnName, newName) {
                                        html += '<div>';
                                        html += '<div class="form-group">';
                                        html += '<label for="' + el.name + '">' + el.display_name + '</label>';
                                        html += '<div class="removeColumn">';
                                        html += '<i class="fa fa-minus"></i> Remove</div>';
                                        html += '<select id="' + el.name + '_value" class="form-control">';
                                        html += getColumnNamesMetaDataAsOptions(nodeId, columnName);
                                        html += '</select>';
                                        html += '</div>';
                                        html += '<div class="form-group">';
                                        html += '<label for="columnNewName">New Name</label>';
                                        html += '<input id="columnNewName" type="text" class="form-control" value="' + newName + '">';
                                        html += '</div>';
                                        html += '<hr>';
                                        html += '</div>';
                                    });
                                }

                            } else {
                                if (el.name === "csv_path") {
                                    html += `
                                        <div class=uploadcsv-container>
                                            <label for="${el.name}_value" class="btn">
                                                <i class="fa fa-cloud-upload"></i>Choose a file... 
                                            </label>
                                            <input
                                                type="file"
                                                id="${el.name}_value"
                                                accept=".csv" 
                                                data-toggle="tooltip"
                                                value=""
                                            />
                                        </div>
                                    `
                                }
                                else
                                    html += '<input id="' + el.name + '_value" type="text" class="form-control" value="' + el.value + '">';
                            }
                            html += '</div>'; // to close form group div
                        });
                        html += '</form>';
                        html += '<a id="saveProperties" href="#" class="btn btn-primary">Set value</a>'; //Save button
                        html += '<hr>';
                    }
                    // html += '<img src="'+DJANGO_STATIC_URL+'images/info-icon.png">';
                    // html += '<div>';
                    // html += val.desc;
                    // html += '</div>';
                    html += '<h5>DESCRIPTION</h5>'
                    html += '<p class="card-text">';
                    html += val.desc;
                    html += '</p>';
                    return false;
                }
            });
            return html;
        }

        //onclick save, save on the side, save
        $("#propertiesBody").on("click", "#saveProperties", function () {
            // only for ReadCSV
            if ($("div.jtk-node.selected")[0].attributes[2].nodeValue === "ReadCSV") {
                let readcsv_input = $("#csv_path_value");
                let files = readcsv_input.prop('files');
                readcsv_input.attr("value", sendReadcsvFile(files[0]));
            }

            let nodeId = $("div.jtk-node.selected")[0].id;
            updateNodeProperties(nodeId);
            let workflowJson = formatFlowDiagramAsJson(instance.getAllConnections());
            let flowDiagramJson = workflowJson.replace('SelectDataset', 'SelectDatasetSample').replace('ReadCSV', 'ReadCSVSample')

            workFlowExecution(flowDiagramJson);
        });

        $("#propertiesBody").on("change", "#csv_path_value", function () {
            const FILES = $(this).prop('files');
            if (FILES.length !== 0) {
                $('.uploadcsv-container label').text(FILES[0].name)
            }
        })

        $("#propertiesBody").on("click", "#addColumnWithType", function () {
            let nodeId = $("div.jtk-node.selected")[0].id;
            $.each(nodesList, function (key, val) {
                if (val.id === nodeId) {
                    if (val.proprties.length > 0) {
                        $.each(val.proprties, function (i, el) {
                            if (el.type === "columns_with_types") { //changeDType
                                let html = '';
                                html += '<div>';
                                html += '<div class="form-group">';
                                html += '<label for="' + el.name + '">' + el.display_name + '</label>';
                                html += '<div class="removeColumn">';
                                html += '<i class="fa fa-minus"></i> Remove</div>';
                                html += '<select id="' + el.name + '_value" class="form-control">';
                                html += getColumnNamesMetaDataAsOptions(nodeId);
                                html += '</select>';
                                html += '</div>';
                                html += '<div class="form-group">';
                                html += '<label for="dataTypeSelect">Data Type</label>';
                                html += '<select id="dataTypeSelect" class="form-control">';
                                html += getDataTypesAsOptions();
                                html += '</select>';
                                html += '</div>';
                                html += '<hr>';
                                html += '</div>';
                                $("#propertiesBody > form").append(html);
                                return false;
                            }
                        });
                    }
                }
            });
        });

        $("#propertiesBody").on("click", "#addColumnWithName", function () {
            //alert("lookups here 2222??")
            let nodeId = $("div.jtk-node.selected")[0].id;
            $.each(nodesList, function (key, val) {
                if (val.id === nodeId) {
                    if (val.proprties.length > 0) {
                        $.each(val.proprties, function (i, el) {
                            if (el.type === "columns_with_names") { //changeColumnNames
                                let html = '';
                                html += '<div>';
                                html += '<div class="form-group">';
                                html += '<label for="' + el.name + '">' + el.display_name + '</label>';
                                html += '<div class="removeColumn">';
                                html += '<i class="fa fa-minus"></i> Remove</div>';
                                html += '<select id="' + el.name + '_value" class="form-control">';
                                html += getColumnNamesMetaDataAsOptions(nodeId);
                                html += '</select>';
                                html += '</div>';
                                html += '<div class="form-group">';
                                html += '<label for="columnNewName">New Name</label>';
                                html += '<input id="columnNewName" type="text" class="form-control" value="">';
                                html += '</div>';
                                html += '<hr>';
                                html += '</div>';
                                $("#propertiesBody > form").append(html);
                                return false;
                            }
                        });
                    }
                }
            });
        });

        $("#propertiesBody").on("click", ".removeColumn", function () {
            $(this).parent().parent().remove();
        });

        $("#view-histogram-button").click(function () {
            if ($('#histogram_first_column').val() !== '-1' && $("#numberOfBins").val() >= 0) {
                let histogram_request = new Object();
                histogram_request.wf_unique_id = experimentId;
                histogram_request.node_name = $("#histogram-div").attr("nodeId");
                histogram_request.output_port_id = $("#histogram-div").attr("outputId");
                histogram_request.col_1 = $('#histogram_first_column').val();
                histogram_request.norm = $("#normRadio").val();
                histogram_request.num_bins = $("#numberOfBins").val();
                getHistogram(JSON.stringify(histogram_request));
            }
        });


        $("#view-pairwise-button").click(function () {
            if ($('#pairwise_first_column').val() !== '-1' && $('#pairwise_second_column').val() !== '-1') {
                let pairWise_request = new Object();
                pairWise_request.wf_unique_id = experimentId;
                pairWise_request.node_name = $("#pairwise-div").attr("nodeId");
                pairWise_request.output_port_id = $("#pairwise-div").attr("outputId");
                pairWise_request.col_1 = $('#pairwise_first_column').val();
                pairWise_request.col_2 = $('#pairwise_second_column').val();
                getPairwise(JSON.stringify(pairWise_request));
            }
        });

        $("#view-correlation-button").click(function () {
            if ($('#correlation_first_column').val() !== '-1') {
                let correlation_request = new Object();
                correlation_request.wf_unique_id = experimentId;
                correlation_request.node_name = $("#correlation-div").attr("nodeId");
                correlation_request.output_port_id = $("#correlation-div").attr("outputId");
                correlation_request.plot_type = $('#plotTypeRadio').val()
                let selectedValues = $('#correlation_select_columns').val();
                let selectedValuesAsStr = "";
                $.each(selectedValues, function (i, el) {
                    if (el !== "-1") {
                        selectedValuesAsStr = selectedValuesAsStr + el + ",";
                    }
                });
                if (selectedValuesAsStr !== "") {
                    selectedValuesAsStr = selectedValuesAsStr.substring(0, selectedValuesAsStr.length - 1) // to remove last comma
                    correlation_request.col_names = selectedValuesAsStr;
                    getCorrelationMatrix(JSON.stringify(correlation_request));
                }
            }
        });

        function unHighlightAllNodes() {
            $("div.jtk-node.selected").each(function () {
                $(this).removeClass("selected").trigger("classChange");
                $(this).children(".iconCircle").children("svg").children("circle").css("stroke", "#a5a5a5");
                $(this).children(".iconCircle").children("svg").children("circle").css("stroke-width", "1");
            });
            hidePanel("propertiesWindow");
        }

        function highlightSelectedNode(node) {
            $(node).addClass("selected").trigger("classChange");
            $(node).children(".iconCircle").children("svg").children("circle").css("stroke", "#90268f");
            $(node).children(".iconCircle").children("svg").children("circle").css("stroke-width", "2");

        }

        function removeIconStatusForAllNodes() {
            if ($($("div.jtk-node :first-child :first-child")[0]).prop('nodeName') === "IMG") { //Image alreedy present

                $(".statusIconDiv").remove();
                $("div.jtk-node").css('line-height', '80px');

            }
        }

        function prepareDataSummaryTable(jsonData) {

            if (isSummaryTableRan) {
                try {
                    $('#outputDataSummaryTable').DataTable().destroy();
                } catch (error) {
                    console.log("you are trying something silly")
                }
                $('#outputDataSummaryTable').empty();
            }
            // For horizontal columns
            let tmpThead = '<thead>';
            let horizontalHeaders = [];
            let verticalHeaders = [];
            tmpThead = tmpThead + '<tr>';
            tmpThead = tmpThead + '<th></th>';
            for (let el in jsonData.df_description) {
                horizontalHeaders.push(el);
                for (let innerFactors in jsonData.df_description[el]) {
                    if (!verticalHeaders.includes(innerFactors)) {
                        verticalHeaders.push(innerFactors);
                    }
                }
                tmpThead = tmpThead + '<th>' + el + '</th>';
            }
            tmpThead = tmpThead + '</tr>';
            tmpThead = tmpThead + '</thead>';
            $('#outputDataSummaryTable').append(tmpThead);

            //Fill Data Types Row
            let tmpRow = '<tr>';
            tmpRow = tmpRow + '<td>Data Types</td>';
            $.each(horizontalHeaders, function (i, el) {
                if (jsonData.dtypes[el] != undefined) {
                    tmpRow = tmpRow + '<td>' + jsonData.dtypes[el] + '</td>';
                } else {
                    tmpRow = tmpRow + '<td></td>';
                }
            });
            tmpRow = tmpRow + '</tr>';

            //Fill Flixable vertical header (Factors)
            let tr;
            $.each(verticalHeaders, function (index, verticalHeader) {
                tr = tr + '<tr>';
                tr = tr + '<td>' + verticalHeader + '</td>';
                $.each(horizontalHeaders, function (i, horizontalHeader) {
                    if (jsonData.df_description[horizontalHeader][verticalHeader] != undefined) {
                        let value = jsonData.df_description[horizontalHeader][verticalHeader];
                        if (typeof value === "number") {
                            tr = tr + '<td>' + roundNumberToTwoDigits(value) + '</td>';
                        } else {
                            tr = tr + '<td>' + value + '</td>';
                        }
                    } else {
                        tr = tr + '<td></td>';
                    }
                })
                tr = tr + '</tr>';
            });
            let tmpTableBody = '<tbody>' + tmpRow + tr + '</tbody>';
            $('#outputDataSummaryTable').append(tmpTableBody);

            $('#outputDataSummaryTable').DataTable({
                //            "scrollX": true
            });

            //Number of Records
            let numberOfRecords = $("#outputModal-numberOfRecords > b").html();
            numberOfRecords = numberOfRecords.replace(numberOfRecords.split(":")[1].trim(), jsonData.number_of_records);
            $("#outputModal-numberOfRecords > b").html(numberOfRecords);

            isSummaryTableRan = true;
        }

        function prepareDataSampleTable(jsonData, nodeType) {
            prepareSelect('histogram_first_column');
            prepareSelect('pairwise_first_column');
            prepareSelect('pairwise_second_column');
            prepareSelect('correlation_first_column');

            if (isSampleDataTableRan) {
                $('#outputDataSampleData').DataTable().destroy();
                $('#outputDataSampleData').empty();
            }
            // For columns
            let tmpThead = '<thead>';
            let columns = [];
            tmpThead = tmpThead + '<tr>';
            if (jsonData.sample_data.length > 0) {
                for (let el in jsonData.sample_data[0]) {
                    columns.push(el);
                    tmpThead = tmpThead + '<th>' + el + '</th>';

                    // Fill up dropdowns for Histogram tab
                    appendToSelect('histogram_first_column', el);

                    // Fill up dropdowns for pairwise tab
                    appendToSelect('pairwise_first_column', el);
                    appendToSelect('pairwise_second_column', el);

                    //Fill up dropdown for correaltion matrix tab
                    if (jsonData.dtypes[el] === "int64" || jsonData.dtypes[el] === "float64") {
                        appendToSelect('correlation_select_columns', el);
                    }

                }
            }
            tmpThead = tmpThead + '</tr>';
            tmpThead = tmpThead + '</thead>';
            $('#outputDataSampleData').append(tmpThead);

            // For Body
            let body = '<tbody>';
            $.each(jsonData.sample_data, function (i, element) {
                body = body + '<tr>';
                $.each(columns, function (i, innerElement) {
                    if (element[innerElement] != undefined) {
                        let value = element[innerElement];
                        if (typeof value === "number") {
                            body = body + '<td>' + roundNumberToTwoDigits(value) + '</td>';
                        } else {
                            body = body + '<td>' + value + '</td>';
                        }
                    }
                });
                body = body + '</tr>';
            });
            body = body + '</tbody>';
            $('#outputDataSampleData').append(body);
            $('#outputDataSampleData').DataTable({
                // "scrollX": true
            });


            isSampleDataTableRan = true;
            $('#outputModal').modal('show');

            $('.multiselect-ui').multiselect({
                includeSelectAllOption: true
            });

            $('#radioBtn a').on('click', function () {
                let sel = $(this).data('title');
                let tog = $(this).data('toggle');
                $('#' + tog).prop('value', sel);

                $('a[data-toggle="' + tog + '"]').not('[data-title="' + sel + '"]').removeClass('active').addClass('notActive');
                $('a[data-toggle="' + tog + '"][data-title="' + sel + '"]').removeClass('notActive').addClass('active');
            });

            $('#normRadioBtn a').on('click', function () {
                let sel = $(this).data('title');
                let tog = $(this).data('toggle');
                $('#' + tog).prop('value', sel);

                $('a[data-toggle="' + tog + '"]').not('[data-title="' + sel + '"]').removeClass('active').addClass('notActive');
                $('a[data-toggle="' + tog + '"][data-title="' + sel + '"]').removeClass('notActive').addClass('active');
            });

            $("ul.dropdown-menu input[type=checkbox]").each(function () {
                $(this).change(function () {
                    let line = "";
                    $("ul.dropdown-menu input[type=checkbox]").each(function () {
                        if ($(this).is(":checked")) {
                            line += $(this).next().text() + ",";
                        }
                    });
                    $("span.span-values").text(line);
                });
            });

            //TODO TO be removed
            $('a[href="#data-summary"]').show();
            $('a[href="#histogram-div"]').show();
            $('a[href="#pairwise-div"]').show();
            $('a[href="#correlation-div"]').show();
            $('a[href="#data-sample"]').show();
            if (nodeType == 'ClassificationMetrics' || nodeType == 'RegressionMetrics') {
                $('a[href="#data-sample"]').tab('show');
                $('a[href="#data-sample"]').hide();
                $('a[href="#data-summary"]').hide();
                $('a[href="#histogram-div"]').hide();
                $('a[href="#pairwise-div"]').hide();
                $('a[href="#correlation-div"]').hide();
            }


        }

        function prepareHistogramTab(jsonData) {
            $("#histogram-graph-div").html(jsonData);
            $("#histogram-graph-div>img").css("max-height", "510px");
            removeUnneededOptionFromPlotlyChart();
        }


        function executeWorkflow(executeToNode) {
            // console.log('execute to node: ' + executeToNode);
            // console.log('get all connections: ' + instance.getAllConnections());
            let flowDiagramJson = formatFlowDiagramAsJson(instance.getAllConnections(), executeToNode);
            if (flowDiagramJson !== "[]") {
                removeIconStatusForAllNodes();
                sendWorkflowToExecute(flowDiagramJson, experimentId, isWorkflowRanSuccessfuly, executionType);
            } else {
                //alert("Nothing to execute !!");
            }
        }

        function getFlowDiagram(executeToNode) {
            let flowDiagramJson = formatFlowDiagramAsJson(instance.getAllConnections(), executeToNode);
            flowDiagramJson = flowDiagramJson.replace('SelectDataset', 'SelectDatasetSample').replace('ReadCSV', 'ReadCSVSample')
            return flowDiagramJson;
        }



        function sampleExecuteWorkflow(executeToNode) {
            let flowDiagramJson = getFlowDiagram(executeToNode);
            if (flowDiagramJson !== "[]") {
                getNodeOutputMetadata(flowDiagramJson);
                //workFlowExecution(flowDiagramJson);
            }
        }

        (function ($, window) {

            $.fn.contextMenu = function (settings) {
                return this.each(function () {

                    // Open context menu
                    $(this).on("contextmenu", function (e) {
                        formatContextMenuBasedOnNodeOutputs(this.id); //To fillup the menu list
                        // return native menu if pressing control
                        if (e.ctrlKey) return;

                        //open menu
                        let $menu = $(settings.menuSelector)
                            .data("invokedOn", $(e.target))
                            .show()
                            .css({
                                position: "fixed",
                                left: getMenuPosition(e.clientX, 'width', 'scrollLeft'),
                                top: getMenuPosition(e.clientY, 'height', 'scrollTop')
                            })
                            .off('click')
                            .on('click', 'a', function (e) {
                                $menu.hide();

                                let $invokedOn = $menu.data("invokedOn");
                                let $selectedMenu = $(e.target);

                                settings.menuSelected.call(this, $invokedOn, $selectedMenu);
                            });

                        return false;
                    });

                    //make sure menu closes on any click
                    $('body').click(function () {
                        $(settings.menuSelector).hide();
                    });
                });

                function getMenuPosition(mouse, direction, scrollDir) {
                    let win = $(window)[direction](),
                        scroll = $(window)[scrollDir](),
                        menu = $(settings.menuSelector)[direction](),
                        position = mouse + scroll;

                    // opening menu would pass the side of the page
                    if (mouse + menu > win && menu < mouse)
                        position -= menu;

                    return position;
                }

            };
        })(jQuery, window);

        $("#saveExperiment").on("click", function () { //Saving workflow to server
            saveWorkflow();
        })

        $("#exportExperiment").on("click", function () { //Exporting Workflow locally
            exportExperiment();
        })

        function saveWorkflow() {
            // swal({
            //     title: "Are You Sure You Want to Save?",
            //     text: "Click On OK for YES!",
            //     type: "info",
            //     showCancelButton: true,
            //     closeOnConfirm: false,
            //     showLoaderOnConfirm: true
            //   },function () {

            /* old changes */
            let experiment = new Object();
            experiment.experimentId = getUrlParameterByName("experimentId", window.location.href);
            experiment.workflowJson = JSON.parse(formatFlowDiagramAsJson(instance.getAllConnections()));
            console.log(JSON.stringify(experiment))

            if (experiment.experimentId == null) {
                createWorkflow(JSON.stringify(experiment));
            } else {
                sendWorkflowForSaving(JSON.stringify(experiment));
            }
        }

        function exportExperiment() { //Prepare data to save
            let obj = new Object();
            let experiment = new Object();
            experiment.experimentId = getUrlParameterByName("experimentId", window.location.href);
            experiment.experimentId = Date.now() + "exp_id";
            experiment.last_save = Date.now();
            experiment.experiment_name = "Marketing campaign 2019";
            obj = JSON.parse(formatFlowDiagramAsJson(instance.getAllConnections())); //retrieving unique_id and wf_body from object
            experiment.wf_unique_id = obj.wf_unique_id;
            experiment.wf_body = obj.wf_body;
            experiment.run_to_task_id = obj.run_to_task_id;
            save_locally(JSON.stringify(experiment));

        }

        function save_locally(json_request) {
            // localStorage.setItem('save_experiment', JSON.stringify(json_request)); // No local storage required

            //Exporting the work flow to local drive
            let name = window.prompt("Enter JSON file name to be saved: ");
            if (name.split(".").pop() == 'json') {
                //alert('no file extension is allowed with file name')
                return
            }
            if (!name) {
                //alert('no file name found')
                return
            }
            let text = JSON.stringify(json_request);
            name = name + '.json'
            const a = document.createElement('a');
            const type = name.split(".").pop();
            a.href = URL.createObjectURL(new Blob([text], { type: `text/${type === "txt" ? "plain" : type}` }));
            a.download = name;
            a.click();
            swal(name + " file Saved Successfully", "", "success");
        }

        // page loading
        let exp_json = {}
        exp_json.experimentId = getUrlParameterByName("experimentId", window.location.href);
        getWorkflowByExperimentId(JSON.stringify(exp_json), instance);


        function getDataTypesAsOptions(dataType) {
            let options = '<option value="category"';
            if (dataType != undefined && dataType === "category") {
                options += ' selected="selected"';
            }
            options += '>category</option>';

            options += '<option value="int64"';
            if (dataType != undefined && dataType === "int64") {
                options += ' selected="selected"';
            }
            options += '>int64</option>';

            options += '<option value="float64"';
            if (dataType != undefined && dataType === "float64") {
                options += ' selected="selected"';
            }
            options += '>float64</option>';

            options += '<option value="object"';
            if (dataType != undefined && dataType === "object") {
                options += ' selected="selected"';
            }
            options += '>object</option>';

            return options
        }
        let sourceDetails = null;
        function getDataPortParentSourceNode(nodeId) {
            let connections = instance.getAllConnections();
            let oldSourceDetails = (sourceDetails ? Object.assign({}, sourceDetails) : {});
            sourceDetails = {};
            $.each(connections, function (i, e) {
                if (e.targetId === nodeId && e.endpoints[0].portType === "data") {
                    sourceDetails.sourceNodeId = e.sourceId;
                    sourceDetails.sourcePortId = removeNumberFromString(e.endpoints[0].id);
                    if (oldSourceDetails.sourceNodeId !== sourceDetails.sourceNodeId) {
                        return false;
                    }

                }
            });
            return sourceDetails;
        }

        //function to display columns change afte selection and save
        function getColumnNamesMetaDataAsOptions(nodeId, selectedOptions, nodeType) {
            let html = "";
            let valueSelected = "";
            let selectedOptionsList = [];
            if (selectedOptions) {
                selectedOptionsList = selectedOptions.split(",");
                valueSelected = "selected";
            } else {
                selectedOptionsList = getNodeInputs(nodeId)[0];
                if (selectedOptionsList === null) {
                    showConnectNodetMessage();
                    return html;
                }
            }
            // remove metadatlist with selectedOptionsList.
            $.each(selectedOptionsList, function (i, e) {
                html += '<option value="' + e + '"';
                if (selectedOptionsList.indexOf(e) >= 0) {
                    html += ' selected=' + valueSelected;
                }
                html += '>' + e + '</option>';
            });

            return html;
        }

        function formatContextMenuBasedOnNodeOutputs(nodeId) {
            let html = '<li><a tabindex="-1" value="execute" href="#">Execute This Node</a></li>';
            let numberOfDataOutputs = getNumberOfDataOutputsByNodeId(nodeId);
            let numberOfModelOutputs = getNumberOfModelOutputsByNodeId(nodeId);
            let numberOfOutputs = numberOfDataOutputs + numberOfModelOutputs;
            let nodeType = getNodeTypeByNodeId(nodeId);
            if (numberOfOutputs == 1 && numberOfDataOutputs == 1) {

                html += '<li><a tabindex="-1" value="showOutput_' + numberOfOutputs + '" href="#">Show Data Output</a></li>';

            } else if (numberOfOutputs == 1 && numberOfModelOutputs == 1) {

                html += '<li><a tabindex="-1" value="showModelOutput_' + numberOfOutputs + '" href="#">Show Model Output</a></li>';

            } else if (nodeType === "SplitData") {

                html += '<li><a tabindex="-1" value="showOutput_' + 1 + '" href="#">Show Training Data</a></li>';
                html += '<li><a tabindex="-1" value="showOutput_' + 2 + '" href="#">Show Testing Data</a></li>';

                // }else if(nodeType === "SplitTrainTest"){
            } else if (numberOfOutputs > 1) {

                html += '<li><a tabindex="-1" value="showModelOutput_' + 1 + '" href="#">Show Model Output</a></li>';
                html += '<li><a tabindex="-1" value="showOutput_' + 2 + '" href="#">Show Data Output</a></li>';

            } else if (numberOfOutputs == 0) {

                html += '<li><a tabindex="-1" value="showModelEval" href="#">Show Model Evaluation</a></li>';

            }
            // for(let i=0; i< numberOfOutputs; i++){

            //     html += '<li><a tabindex="-1" value="showOutput_'+(i+1)+'" href="#">Show Output: '+(i+1)+'</a></li>';
            // }
            $("#contextMenu").html(html);
        }

        function setContextMenuPostion(event, contextMenu) {

            let mousePosition = {};
            let menuPostion = {};
            let menuDimension = {};

            menuDimension.x = contextMenu.outerWidth();
            menuDimension.y = contextMenu.outerHeight();
            mousePosition.x = event.pageX;
            mousePosition.y = event.pageY;

            if (mousePosition.x + menuDimension.x > $(window).width() + $(window).scrollLeft()) {
                menuPostion.x = mousePosition.x - menuDimension.x;
            } else {
                menuPostion.x = mousePosition.x;
            }

            if (mousePosition.y + menuDimension.y > $(window).height() + $(window).scrollTop()) {
                menuPostion.y = mousePosition.y - menuDimension.y;
            } else {
                menuPostion.y = mousePosition.y;
            }

            return menuPostion;
        }
        function getNumberOfDataOutputsByNodeId(nodeId) {
            let numberOfDataSources = 0;
            $.each(nodesList, function (i, e) {
                if (e.id === nodeId) {
                    numberOfDataSources = e.numberOfDataSources;
                    return false;
                }
            });
            return numberOfDataSources;
        }

        function getNumberOfModelOutputsByNodeId(nodeId) {
            let numberOfModelSources = 0;
            $.each(nodesList, function (i, e) {
                if (e.id === nodeId) {
                    numberOfModelSources = e.numberOfModelSources;
                    return false;
                }
            });
            return numberOfModelSources;
        }

        function getNodeTypeByNodeId(nodeId) {
            let nodeType = $("#" + nodeId).attr("type");
            return nodeType;
        }

        function handleModelOutput(nodeId, response) {

            let nodeType = getNodeTypeByNodeId(nodeId);

            if (nodeType === "ClassificationMetrics" ||
                nodeType === "ClusteringMetrics" ||
                nodeType === "RegressionMetrics") {

                handleMetricsTasksOutput(response);

            } else if (nodeType === "SplitTrainTest") {

                handleSTTEOutput(response);

            } else {
                handleClassificationTasksOutput(response, false, nodeId);
            }

        }

        function handleDataOutput(nodeId, response) {

            let nodeType = getNodeTypeByNodeId(nodeId);
            prepareDataSummaryTable(response);
            prepareDataSampleTable(response, nodeType);
            prepareHistogramTab(response);
            preparePairwiseTab(response);
        }

        // function showRocChart(response) {
        //   $("#evaluationOutput").modal("toggle");
        //   $("#rocChart").html(response);
        //   $("rect.scrollbar").removeClass("scrollbar");
        //   removeUnneededOptionFromPlotlyChart();
        // }

        function handleSTTEOutput(response) {
            $('a[href="#model-desc"]').show();

        }
    });
}
