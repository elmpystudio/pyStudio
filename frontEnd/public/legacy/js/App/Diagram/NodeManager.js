import { API_URL } from "../env.js";
import { getNodeOutputMetadata } from "./ApiClient.js";

const GET_ALL_NODES_URL = `${API_URL}/api/ml/nodes/list`;
const GET_ALL_NODES_URL_LOCAL = "json/get_nodes_list.json";
const GET_DATASET_NAMES = "/api/datasets/";
let nodesFromServer = [];

//local
// this is the paint style for the connecting lines..
// the definition of source endpoints (the small green ones)
// the definition of target endpoints (will appear when the user drags a connection)
let connectorPaintStyle = {
    strokeWidth: 2,
    stroke: "#61B7CF",
    joinstyle: "round",
    // outlineStroke: "white",
    outlineWidth: 2
},
    // .. and this is the hover style.
    connectorHoverStyle = {
        strokeWidth: 3,
        stroke: "#90268f",
        outlineWidth: 5,
        // outlineStroke: "white"
    },
    endpointHoverStyle = {
        fill: "#90268f",
        stroke: "#90268f"
    },
    //For models
    modelConnectorHoverStyle = {
        strokeWidth: 3,
        stroke: "#191970",
        outlineWidth: 5,
        // outlineStroke: "white"
    },
    modelEndpointHoverStyle = {
        fill: "#191970",
        stroke: "#191970"
    };

let sourceEndpoint = {
    endpoint: "Dot",
    maxConnections: 2,
    paintStyle: {
        fill: "#90268f",
        radius: 7
    },
    isSource: true,
    connector: ["Flowchart", {
        stub: 15,
        gap: 5,
        cornerRadius: 5,
        alwaysRespectStubs: true
    }],
    connectorStyle: connectorPaintStyle,
    hoverPaintStyle: endpointHoverStyle,
    connectorHoverStyle: connectorHoverStyle,
    dragOptions: {},
    overlays: [
        ["Label", {
            location: [0.5, 1.5],
            label: "Drag",
            cssClass: "endpointSourceLabel",
            visible: false
        }]
    ]
};

let modelSourceEndpoint = {
    endpoint: "Dot",
    maxConnections: 2,
    paintStyle: {
        fill: "#0970b9",
        radius: 7
    },
    isSource: true,
    connector: ["Flowchart", {
        stub: [40, 60],
        gap: 10,
        cornerRadius: 5,
        alwaysRespectStubs: true
    }],
    connectorStyle: connectorPaintStyle,
    hoverPaintStyle: modelEndpointHoverStyle,
    connectorHoverStyle: modelConnectorHoverStyle,
    dragOptions: {},
    overlays: [
        ["Label", {
            location: [0.5, 1.5],
            label: "Drag",
            cssClass: "endpointSourceLabel",
            visible: false
        }]
    ]
};

let targetEndpoint = {
    endpoint: "Dot",
    paintStyle: {
        stroke: "#90268f",
        fill: "transparent",
        radius: 7,
        strokeWidth: 1
    },
    hoverPaintStyle: endpointHoverStyle,
    maxConnections: -1,
    dropOptions: {
        hoverClass: "hover",
        activeClass: "active"
    },
    isTarget: true,
    overlays: [
        ["Label", {
            location: [0.5, -0.5],
            label: "Drop",
            cssClass: "endpointTargetLabel",
            visible: false
        }]
    ]
};

let modelTargetEndpoint = {
    endpoint: "Dot",
    paintStyle: {
        stroke: "#0970b9",
        fill: "transparent",
        radius: 7,
        strokeWidth: 1
    },
    hoverPaintStyle: modelEndpointHoverStyle,
    maxConnections: -1,
    dropOptions: {
        hoverClass: "hover",
        activeClass: "active"
    },
    isTarget: true,
    overlays: [
        ["Label", {
            location: [0.5, -0.5],
            label: "Drop",
            cssClass: "endpointTargetLabel",
            visible: false
        }]
    ]
};

//static
function showPopupError(message) {
    swal(message, "", "error");
}

//static
function prepareHasForBoxes(nodes) {
    // TODO preparer a has for fast next function indexing...
}

//static
function connectTwoNodes(sourceNodeId, sourcePortId, destinationNodeId, destinationPortId, instance) {
    instance.connect({
        uuids: ["Node" + sourceNodeId + "position:" + sourcePortId, "Node" + destinationNodeId + "position:" + destinationPortId],
        editable: true
    });
}

//static
// All the sidebar are getting loaded
function loadSidebarMenu(nodesList, is_nested = false) {
    let menuStr = "";
    if (nodesList.groups !== undefined && nodesList.groups.length > 0) {
        $.each(nodesList.groups, function (i, el) {
            //groups
            menuStr += '<li class="nav-item">';
            menuStr += '<a href="javascript:;" class="nav-link">'
            menuStr += '<i class="icon ' + el.iconName + '"></i>';
            menuStr += '<div class="name-container">'
            menuStr += '<span title="click to expand" class="name">' + el.name + '</span>';
            menuStr += '</div>'
            menuStr += '<i class="arrow-icon fa fa-angle-double-down"></i>';
            menuStr += '</a>';
            menuStr += '<ul class="sub-menu">';

            //nested groups
            if (el.groups !== undefined && el.groups.length > 0)
                menuStr += loadSidebarMenu(el, true);

            //nodes
            $.each(el.nodes, function (i, node) {
                node.iconName = el.iconName;
                node.backgroundColor = el.backgroundColor;
                node.iconColor = el.iconColor;
                nodesFromServer.push(node);
                menuStr += '<li class="nav-item draggable-node">';
                menuStr += '<a class="sub-nav-link sub-nav-link ui-draggable" type="' + node.type + '"kind="' + node.kind + '">' +
                    '<span title="drag and drop" class="sub-name">' + node.name + '</span>';
                menuStr += '</a>';
                menuStr += '</li>';
            });

            menuStr += '</ul>';
            menuStr += '</li>';
        });
    }

    if(is_nested)
        return menuStr;
    $("#sidebar-menu").append(menuStr);
}

//static
function applyDraggin(nodesList, instance) {
    let element;
    $(".draggable-node").draggable({
        revert: "invalid",
        scope: "items",
        helper: "clone",
        // eslint-disable-next-line no-unused-vars
        drag: function (event, ui) {
            $("div").data("elementTypeName", $(this).children("a").attr('type'));
            element = $(this);
        }
    });

    $("#canvas").droppable({
        scope: "items",
        drop: function (event, ui) {
            let data = $("div").data("elementTypeName");
            let x = event.clientX - $("#canvas").offset().left;
            let y = event.clientY - $("#canvas").offset().top;
            addNodeToCanvas(nodesList, data, x, y, instance);
            $(element).css("left", "");
            $(element).css("top", "");
        }
    });

}

//static
// There is two way to chnage the size of text, either set font-size as 12 px or min-width as 200 ox for proper text visualisation
// droping the box, when you drorp a node
function addNodeToCanvas(nodesList, nodeTypeParam, x, y, instance) {
    $("#canvasHint").remove();

    let i = (parseInt(getLastNodeId()) + 1);

    let node = getNodeDetailsByType(nodesFromServer, nodeTypeParam);
    $("#canvas").append("<div class='window jtk-node' id='flowchartNode" + i + "' type='" + node.type + "'  kind='" + node.kind + "'  style='left:" + x + "px; top:" + y + "px;color: " + node.iconColor + ";background-color: " + node.backgroundColor + ";min-width: 200px" + ";'>" + `<span class='` + node.iconName + ` iconStyle'></span>` + "<strong>" + node.name + "</strong></div>");
    let portsList = separatePortsList(node.ports);
    let listOfSources = portsList.listOfSources;
    let listOfTargets = portsList.listOfTargets;
    _addEndpoints("Node" + i, listOfSources, listOfTargets, instance);
    let properties = node.proprties;
    addNodeToNodesList(nodesList, "flowchartNode" + i, properties, node.desc, listOfSources);
    //Make the node draggable
    instance.draggable(jsPlumb.getSelector(".flowchart-demo .window"), {
        grid: [20, 20]
    });
    // $("#canv").mCustomScrollbar("update");
}

//static
function getLastNodeId() {
    if ($(".jtk-node").length > 0) {
        let lastNodeId = $(".jtk-node")[($(".jtk-node").length - 1)].id;
        return lastNodeId.split("flowchartNode")[1];
    }
    return 0;
}

//static
function getNodeDetailsByType(nodes, nodeType) {
    //Initialize new Object to avoid pointing
    let nodeDetails = new Object();
    $.each(nodes, function (i, el) {
        if (el.type === nodeType) {
            nodeDetails.name = el.name;
            nodeDetails.type = el.type;
            nodeDetails.desc = el.desc;
            nodeDetails.kind = el.kind;
            nodeDetails.iconName = el.iconName;
            nodeDetails.backgroundColor = el.backgroundColor;
            nodeDetails.iconColor = el.iconColor;
            nodeDetails.ports = [];
            $.each(el.ports, function (i, e) {
                let port = new Object();
                port.is_output = e.is_output;
                port.type = e.type;
                nodeDetails.ports.push(port);
            });
            nodeDetails.proprties = [];
            $.each(el.proprties, function (index, element) {
                //Initialize new Object to avoid pointing
                let prop = new Object();
                prop.name = element.name;
                prop.value = element.value;
                prop.type = element.type;
                prop.kind = element.kind;
                prop.display_name = element.display_name;
                if (element.lookup != undefined) {
                    prop.lookup = element.lookup;
                }
                nodeDetails.proprties.push(prop);
            });
            return false; //To break out

        }
    });

    return nodeDetails;
}

//static
function separatePortsList(ports) {
    let listOfSources = [];
    let listOfTargets = [];
    $.each(ports, function (i, el) {
        if (el.is_output) {
            listOfSources.push(el);
        } else {
            listOfTargets.push(el);
        }
    });

    if (listOfSources.length === 1) {
        listOfSources[0].position = convertToOldNaming(2 + "S");
    } else {
        $.each(listOfSources, function (i, el) {
            el.position = convertToOldNaming(i + "S");
        });
    }

    if (listOfTargets.length === 1) {
        listOfTargets[0].position = convertToOldNaming(2 + "T");
    } else {
        $.each(listOfTargets, function (i, el) {
            el.position = convertToOldNaming(i + "T");
        });
    }

    let listOfPorts = {};
    listOfPorts.listOfSources = listOfSources;
    listOfPorts.listOfTargets = listOfTargets;
    return listOfPorts;
}

//static
function convertToOldNaming(name) {
    if (name === '0T') {
        return "TopLeft";
    } else if (name === '1T') {
        return "TopRight";
    } else if (name === '2T') {
        return "TopCenter";
    } else if (name === '0S') {
        return "BottomLeft";
    } else if (name === '1S') {
        return "BottomRight";
    } else if (name === '2S') {
        return "BottomCenter";
    }
}

//static
//TODO this function needs to refactor.
let _addEndpoints = function (toId, sourceAnchors, targetAnchors, instance) {
    if (sourceAnchors != null && sourceAnchors.length > 0) {
        let sourceEndpointProperties;
        for (let i = 0; i < sourceAnchors.length; i++) {
            sourceEndpointProperties = sourceEndpoint;
            if (sourceAnchors[i].type === 'model') {
                sourceEndpointProperties = modelSourceEndpoint;
            }
            let sourceUUID = toId + "position:" + sourceAnchors[i].position;
            instance.addEndpoint("flowchart" + toId, sourceEndpointProperties, {
                anchor: sourceAnchors[i].position,
                uuid: sourceUUID,
                portType: sourceAnchors[i].type
            });
        }
    }

    if (targetAnchors != null && targetAnchors.length > 0) {
        let targetEndpointProperties;
        for (let j = 0; j < targetAnchors.length; j++) {
            targetEndpointProperties = targetEndpoint;
            if (targetAnchors[j].type === 'model') {
                targetEndpointProperties = modelTargetEndpoint;
            }
            let targetUUID = toId + "position:" + targetAnchors[j].position;
            instance.addEndpoint("flowchart" + toId, targetEndpointProperties, {
                anchor: targetAnchors[j].position,
                uuid: targetUUID,
                portType: targetAnchors[j].type
            });
        }
    }

};

//static
function addNodeToNodesList(nodesList, nodeId, properties, node_description, listOfSources) {
    let nodeObj = {};
    nodeObj.id = nodeId;
    nodeObj.proprties = properties;
    nodeObj.desc = node_description;
    let numberOfDataSources = 0;
    let numberOfModelSources = 0;
    $.each(listOfSources, function (i, e) {
        if (e.type === "data") {
            numberOfDataSources++;
        } else if (e.type === "model") {
            numberOfModelSources++;
        }
    });
    nodeObj.numberOfDataSources = numberOfDataSources;
    nodeObj.numberOfModelSources = numberOfModelSources;

    nodesList.push(nodeObj);
}

//static
// fixing the appearnace of icon by assigning line height to 80px in window jtk-node
function addNodeToCanvasFromWorkflow(nodeObj, nodesList, instance) {
    $("#canvasHint").remove();
    let node = getNodeDetailsByType(nodesFromServer, nodeObj.task_name);
    let nodeNumber = nodeObj.task_id.split('Node')[1];

    $("#canvas").append("<div class='window jtk-node' id='" + nodeObj.task_id + "' type='" + node.type + "' style='" + nodeObj.position + "; background-color: #ffffff'>" + ` <span class='` + node.iconName + ` iconStyle'></span>` + "<strong>" + node.name + "</strong></div>");

    let portsList = separatePortsList(node.ports);
    let listOfSources = portsList.listOfSources;
    let listOfTargets = portsList.listOfTargets;
    _addEndpoints("Node" + nodeNumber, listOfSources, listOfTargets, instance);
    let properties = nodeObj.parameters;
    addNodeToNodesList(nodesList, "flowchartNode" + nodeNumber, properties, node.desc, listOfSources);
    //Make the node draggable
    instance.draggable(jsPlumb.getSelector(".flowchart-demo .window"), {
        grid: [20, 20]
    });
}

//jsplumbClient
function loadNodes(instance, nodesList) {
    $.ajax({
        //server
        //url: GET_ALL_NODES_URL,
        //local
        url: GET_ALL_NODES_URL_LOCAL,
        
        method: "GET",
        dataType: "json",
        cache: false,
        success: function (nodes) {
            prepareHasForBoxes(nodes);
            $.ajax({
                url: API_URL + GET_DATASET_NAMES, //fetching data from server
                method: "GET",
                datatype: "json",
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('token')
                },
                cache: false,
                success: function (datasetsList) {
                    nodes['groups'][0]['nodes'][1]['proprties'][0]['lookup'] = datasetsList; //adding this in lookup for dataset

                },
                error: function (error) {
                    showPopupError(error.message);
                }
            });
            loadSidebarMenu(nodes);
            applyDraggin(nodesList, instance);

        },
        error: function (response) {
            showPopupError(response.message);
        }
    });
}

//jsplumbClient | ApiClient
function buildWorkflow(workflowJson, instance) {
    let workflowObj = JSON.parse(workflowJson);
    if (!workflowObj) { // If no workflow is saved, it will return nothing.
        return
    }

    let nodesAsList = [];
    let nodesCopy = JSON.parse(workflowJson).wf_body.nodes;
    if (workflowObj.wf_body != null) {
        // wfBodyAsObj = JSON.parse(workflowObj.wf_body);
        nodesAsList = workflowObj.wf_body.nodes;
        getNodeOutputMetadata(JSON.stringify(workflowObj));
    }
    $.each(nodesAsList, function (i, node) {
        addNodeToCanvasFromWorkflow(node, nodesAsList, instance);
    });

    //Connect them to each other
    $.each(nodesCopy, function (i, node) {

        let sourceNodeId = node.task_id.split("Node")[1];

        $.each(node.outputs, function (i, output) { // has node to connect with

            let sourcePortId = output.id;

            $.each(output.targets, function (i, target) { // in case node is connected to more than one destination
                let destinationNodeId = target.nodeId.split("Node")[1];
                let destinationPortId = target.id;
                connectTwoNodes(sourceNodeId, sourcePortId, destinationNodeId, destinationPortId, instance);
            });
        });
    });

    //let nodesToReturn = nodesAsList.filter(n => !nodesCopy.includes(n));
    let temporary = nodesAsList.slice(nodesAsList.length / 2, nodesAsList.length);
    return temporary;
}

export {
    loadNodes,
    buildWorkflow
}
