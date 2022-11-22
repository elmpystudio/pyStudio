<template>
    <div>
        <input id="trigger-menu" type="checkbox" hidden />
        <div class="page-bar">
            <label for="trigger-menu" class="trigger-menu">
                <i class="icon fa fa-angle-up" aria-hidden="true"></i>
            </label>
            <div class="page-actions">
                <div class="buttons">
                    <button id="executeButton" type="button" class="btn-run">
                        <span class="icon fa fa-play"></span>
                    </button>

                    <button id="deployWorkflow" type="button" class="link deploy">
                        <span class="icon fa fa-rocket"></span>
                        <span class="btn-text">Deploy</span>
                    </button>

                    <button id="exportExperiment" type="button" class="link">
                        <span class="icon fa fa-save"></span>
                        <span class="btn-text">Save</span>
                    </button>

                    <label for="selectFiles" class="btn custom-file-upload">
                        <i class="fa fa-cloud-upload"></i>Choose a file...
                    </label>
                    <input
                        type="file"
                        id="selectFiles"
                        class="import-input"
                        value="Import"
                        accept="application/json"
                        data-toggle="tooltip"
                        @change="play"
                    />
                    <button id="importWorkFlow" type="button" hidden></button>
                </div>

                <button id="full-screen" class="full-screen">
                    <span class="icon fa fa-arrows-alt"></span>
                </button>
            </div>
        </div>

        <CModal :id="'deploy_modal'">
            <template v-slot:title>Deploy</template>

            <template v-slot:body>
                <div class="deploy_body">
                    <div class="other">
                        <div class="myrow">
                            <input type="text" name="name" placeholder="Name" />
                            <input
                                type="text"
                                name="version"
                                placeholder="Version"
                            />
                        </div>
                        <div class="myrow">
                            <textarea
                                name="description"
                                placeholder="Description"
                            />
                        </div>
                    </div>
                </div>
            </template>

            <template v-slot:footer>
                <button type="button" class="savebtn" id="deploy_click">
                    Save
                </button>
            </template>
        </CModal>

        <CMessage 
            :id="'deploy_status'"
            :type="'success'"
            :title="'Deploy Status'"
        />
    </div>
</template>

<script>
import $ from "jquery";
import CModal from "@/components/MachineLearning/CModal.vue";
import CMessage from "@/components/MachineLearning/CMessage.vue";

export default {
    name: "CMenuBar",
    components: {
        CModal,
        CMessage,
    },
    mounted() {
        $("#trigger-menu").click(() => {
            $(".trigger-menu").children("i").toggleClass("fa-angle-down");
        });
    },

    methods: {
        play() {
            document.getElementById("importWorkFlow").click();
        },
    },
};
</script>

<style>
.columnBox {
    width: 200px;
    padding: 10px;
    margin: 4px 0;
    box-sizing: border-box;
    background: #364150;
    color: #fff;
    border: 1px solid #fff;
    border-radius: 5px;
}

.deploy.active {
    opacity: 1 !important;
    pointer-events: auto !important;
}
</style>
<style scoped lang="scss">
.deploy_body {
    width: 100%;
    height: 100%;
    padding: 20px;

    display: flex;
    flex-flow: column nowrap;
    align-items: center;

    row-gap: 10px;

    .other {
        .myrow {
            width: 100%;
            height: auto;
            display: flex;
            flex-flow: row nowrap;
            justify-content: center;
            align-content: flex-start;
            column-gap: 5px;
        }
    }

    input {
        width: 100%;
        padding: 10px;
        margin: 4px 0;
        box-sizing: border-box;

        border: 1px solid #364150;
        border-radius: 5px;
    }

    textarea{
        width: 100%;
        height: 200px;
        padding: 10px;
        margin: 4px 0;
        box-sizing: border-box;

        border: 1px solid #364150;
        border-radius: 5px;
    }
}

.page-bar {
    position: relative;
    padding: 0 !important;
    background: #364150;
    justify-content: center !important;
    border-radius: 0 0 30px 30px;
    margin-bottom: 5px;
    transition: margin-top 300ms;
}

.import-input {
    display: inline;
    width: 200px;
}

.fa {
    padding-right: 8px;
}

.fa-rocket {
    margin-top: -5px !important;
}

.fa-cloud-upload {
    margin-top: 5px;
}

input[type="file"] {
    display: none;
}

.custom-file-upload {
    margin: 0;
    font-size: 13px;
    background: rgba(255, 255, 255, 0.863);
    border-radius: 5px;
    cursor: pointer;
    text-align: start;
    height: 30px;
    width: 130px;
    padding: 3px 2px 2px 10px;
}

.page-actions {
    position: relative;
    padding: 0 !important;
    padding-top: 5px !important;
    margin: 4px 0;
    height: 45px !important;
    max-height: 45px !important;
    width: 100%;

    .buttons {
        display: flex;
        flex-wrap: nowrap;
        justify-content: center;
        align-items: center;
        gap: 20px;

        .link {
            &.deploy {
                pointer-events: none;
                opacity: 0.5;
            }

            .icon {
                color: white;
                font-size: 12px;
            }

            .btn-text {
                text-transform: uppercase;
                font-size: 12px;
            }
        }

        .link:hover {
            opacity: 0.8;
        }

        .btn-run {
            position: relative;
            width: 35px;
            height: 35px;
            border-radius: 50%;
            border: 2.5px solid rgba(255, 255, 255, 0.863);
            background: rgba(255, 255, 255, 0.863);

            .icon {
                padding: 0;
                padding-left: 3px;
            }
        }

        .btn-run-success {
            border: 2.5px solid green;
        }

        .btn-run-error {
            border: 2.5px solid red;
        }

        .play {
            -webkit-animation: flash 1s linear infinite;
            animation: flash 1s linear infinite;
        }

        @keyframes flash {
            50% {
                opacity: 0.1;
            }
        }

        .btn-run:hover {
            opacity: 0.8;
        }
    }

    .full-screen {
        position: absolute;
        top: 8px;
        right: 35px;
        font-size: 20px;
        color: rgba(255, 255, 255, 0.863);

        span {
            padding: 0;
        }
    }

    .full-screen:hover {
        opacity: 0.8;
    }
}

.btn:hover {
    opacity: 0.7;
}

#trigger-menu:checked + div {
    margin-top: -45px !important;
}

.trigger-menu {
    position: absolute;
    z-index: 1;
    bottom: -23px;
    left: calc(50% - 50px);
    width: 100px;
    height: 15px;
    border-radius: 0 0 30px 30px;
    background: #364150;

    .icon {
        display: inherit;
        padding: 0;
        margin-top: -6px;
        color: rgba(255, 255, 255, 0.863);
        font-size: 25px;
    }
}

.trigger-menu:hover {
    cursor: pointer;
    opacity: 0.98;
}
</style>