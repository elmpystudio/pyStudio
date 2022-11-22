<template>
    <div class="jtk-container">
        <div class="jtk-diagram-main">
            <div
                id="canvas"
                class="
                    jtk-diagram-canvas
                    canvas-wide
                    flowchart-demo
                    jtk-surface jtk-surface-nopan
                "
            >
                <div id="rubberband"></div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "CWorkSpace",
};
</script>

<style lang="scss">
@import "src/assets/styles/jsplumbtoolkit-default";
@import "src/assets/styles/jsplumbtoolkit-demo";

#canvas {
    border: 0;
    margin: 0;
}

.ml-studio .jtk-diagram-canvas {
    background: none;
    height: 1000vh !important;
    max-height: 1000vh !important;
}

@media (max-width: 600px) {
    .ml-studio .jtk-diagram-canvas {
        height: 1000vh;
    }
}

#rubberband {
    border: 2px dotted darkred;
    border-radius: 5px;
    display: none;
    position: fixed;
}

.jtk-diagram-main {
    margin-top: 0 !important;
}

.jtk-bootstrap-wide .jtk-container {
    margin: 0 !important;
}

.iconStyle {
    margin-top: 8px;
    margin-left: 8px;
    font-size: 15px;
    color: rgb(144, 38, 143);
}

.flowchart-demo .window strong {
    font-size: 13px;
    overflow: hidden;
    word-break: break-all;
}

.flowchart-demo .window {
    display: flex;
    justify-content: space-around;
    border: 2px solid grey !important;
    border-radius: 10px;

    opacity: 0.8;
    width: auto;
    min-width: 160px;
    height: 50px;
    line-height: 32px !important;
    cursor: pointer;
    position: absolute;
    background-color: #ffffff;
    color: #313131;
    font-family: helvetica, sans-serif;
    padding: 0.5em;
    font-size: 0.9em;
    box-shadow: 2px 2px 19px #aaa;
    -o-box-shadow: 2px 2px 19px #aaa;
    -webkit-box-shadow: 2px 2px 19px #aaa;
    -moz-box-shadow: 2px 2px 19px #aaa;
    -moz-border-radius: 0.5em;
    -webkit-transition: -webkit-box-shadow 0.15s ease-in;
    -moz-transition: -moz-box-shadow 0.15s ease-in;
    -o-transition: -o-box-shadow 0.15s ease-in;
    transition: box-shadow 0.15s ease-in;

    span {
        margin-right: 5px;
    }

    strong {
        flex-grow: 1;
    }
}

.flowchart-demo .window:hover {
    box-shadow: 2px 2px 15px #444;
    -o-box-shadow: 2px 2px 15px #444;
    -webkit-box-shadow: 2px 2px 15px #444;
    -moz-box-shadow: 2px 2px 15px #444;
    opacity: 0.8;

    border: 2px solid rgb(144, 38, 143) !important;
}

.flowchart-demo .selected {
    border: 2px solid rgb(144, 38, 143) !important;
}

.flowchart-demo .active {
    border: 1px dotted green;
}

.flowchart-demo .hover {
    border: 1px dotted red;
}

.flowchart-demo .jtk-connector {
    z-index: 4;
}

.flowchart-demo .jtk-endpoint,
.endpointTargetLabel,
.endpointSourceLabel {
    z-index: 21;
    cursor: pointer;
}

.flowchart-demo .aLabel {
    background-color: white;
    padding: 0.4em;
    font: 12px sans-serif;
    color: #444;
    z-index: 21;
    border: 1px dotted gray;
    opacity: 0.8;
    cursor: pointer;
}

.flowchart-demo .aLabel.jtk-hover {
    background-color: #5c96bc;
    color: white;
    border: 1px solid white;
}

.window.jtk-connected {
    border: 1px solid #a5a5a5;
}

.jtk-drag {
    outline: 4px dotted rgb(144, 38, 143);
}

path {
    stroke: rgb(144, 38, 143);
}

path:hover {
    stroke: #2c3e50;
}
</style>