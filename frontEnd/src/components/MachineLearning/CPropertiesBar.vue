<template>
    <div class="content">
        <label for="trigger-properties" class="trigger-properties">
            <i class="icon fa fa-angle-right" aria-hidden="true"></i>
        </label>
        <input id="trigger-properties" type="checkbox" hidden />

        <div class="card">
            <div>
                <h5 class="title">Actions</h5>
                <div class="buttons-container">
                    <button id="remove_node" type="button" class="delete-btn">
                        <span class="mytooltip expand" data-title="Eraser">
                            <span class="icon fa fa-eraser" aria-hidden="true"></span>
                        </span>
                    </button>

                    <button id="clear" type="button" class="clear-btn">
                        <span class="mytooltip expand" data-title="Clear">
                            <span class="icon fa fa-trash-o" aria-hidden="true"></span>
                        </span>
                    </button>
                </div>
            </div>

            <div class="space"></div>

            <h5 class="title">Properties</h5>
            <div id="propertiesBody" class="card-block"></div>
        </div>

        <!--<div id="propertiesWindow" class="portlet box blue-hoki">-->
        <!--<div class="portlet-title elm-color-2">-->
        <!--<div class="caption">-->
        <!--<i class="fa fa-cog"></i>Properties </div>-->
        <!--</div>-->
        <!--<div id="propertiesBody" class="portlet-body">-->
        <!--</div>-->
        <!--</div>-->
    </div>
</template>

<script>
import $ from "jquery";

export default {
    name: "CPropertiesBar",

    mounted() {
        $("#trigger-properties").click(() => {
            let trigger = $(".trigger-properties").children("i");
            if (trigger.hasClass("fa-angle-right"))
                trigger.removeClass("fa-angle-right");
            else trigger.addClass("fa-angle-right");

            $(".trigger-properties").children("i").toggleClass("fa-angle-left");
        });
    },
};
</script>

<style scoped lang="scss">
.content {
    position: relative;
}

.card {
    overflow-y: scroll;
    background: #364150 !important;
    padding: 0 10px;
    width: 300px;
    transition: margin-right 300ms;

    div {
        .buttons-container {
            display: flex;
            justify-content: space-around;
            margin: 10px 10px;
            padding-bottom: 2px;
            padding-top: 4px;
            border-radius: 5px;
            border: 2px solid rgba(255, 255, 255, 0.747);

            .delete-btn {
                .icon {
                    color: rgba(255, 255, 255, 0.747);
                    font-size: 26px;
                }
            }

            .clear-btn {
                .icon {
                    color: rgba(255, 255, 255, 0.747);
                    font-size: 26px;
                }
            }

            .icon:hover {
                opacity: 0.7;
            }

            //tooltip with anmiation
            .mytooltip {
                position: relative;
            }

            //public
            .mytooltip:before,
            .mytooltip:after {
                display: block;
                opacity: 0;
                pointer-events: none;
                position: absolute;
                margin-left: -40px;
            }

            //arrow
            .mytooltip:after {
                border-right: 6px solid transparent;
                border-bottom: 6px solid rgba(255, 255, 255, 0.75);
                border-left: 6px solid transparent;
                content: "";
                height: 0;
                width: 0;
                top: 20px;
                left: 43px;
            }

            //text
            .mytooltip:before {
                background: rgba(255, 255, 255, 0.75);
                border-radius: 6px;
                color: #2c3e50;
                content: attr(data-title);
                font-size: 12px;
                padding: 4px 0;
                top: 26px;
                width: 100px;
                white-space: nowrap;
                text-transform: uppercase;
            }

            .mytooltip.expand:before {
                transform: scale3d(0.2, 0.2, 1);
                transition: all 0.2s ease-in-out;
            }

            .mytooltip.expand:after {
                transform: translate3d(0, 6px, 0);
                transition: all 0.1s ease-in-out;
            }

            .mytooltip.expand:hover:before,
            .mytooltip.expand:hover:after {
                opacity: 1;
                transform: scale3d(1, 1, 1);
            }

            .mytooltip.expand:hover:after {
                transition: all 0.2s 0.1s ease-in-out;
            }
        }
    }

    .space {
        padding: 5px;
    }

    .title {
        margin: 0 -10px;
        padding: 2px;
        text-transform: uppercase;
        font-size: 22px !important;
        letter-spacing: 4px !important;
        color: white;
        background: rgba(255, 255, 255, 0.212);
    }

    #propertiesBody {
        padding: 10px 0;
    }
}

#trigger-properties:checked+div {
    margin-right: -270px;
}

.trigger-properties {
    position: absolute;
    top: 300px;
    left: -15px;
    width: 15px;
    height: 100px;
    border-radius: 30px 0 0 30px;
    background: #2c3e50;

    .icon {
        display: inherit;
        padding: 0;
        margin-top: 35px;
        margin-left: 6px;
        color: rgba(255, 255, 255, 0.795);
        font-size: 25px;
    }
}

.trigger-properties:hover {
    cursor: pointer;
    opacity: 0.98;
}
</style>

<style lang="scss">
#saveProperties {
    color: #2c3e50 !important;
    background: rgba(255, 255, 255, 0.795);
    padding: 4px 20px;
    border-radius: 5px;
    font-size: 15px;
    text-transform: uppercase;
    border: none;
}

#saveProperties:hover {
    opacity: 0.9;
}

.card {
    border-radius: 30px 0 0 30px !important;
    border: none !important;

    .card-block {
        color: rgba(255, 255, 255, 0.836);

        .card-text {
            padding: 10px;
            border: 1px solid rgba(255, 255, 255, 0.836);
            border-radius: 10px;
            color: rgba(255, 255, 255, 0.836);
        }

        form {
            .form-group {
                label {}

                select {
                    margin: 0 !important;
                    background-color: rgba(255, 255, 255, 0.836) !important;
                    color: #2c3e50;
                    border-color: rgb(144, 38, 143) !important;
                }

                div {
                    button {
                        color: rgba(255, 255, 255, 0.836) !important;
                    }
                }
            }
        }

        hr {
            margin: 20px;
            border-color: rgba(255, 255, 255, 0.836);
        }

        #propertiesWindowHint::before {
            content: "! ";
            font-size: 20px;
            color: #d73fda;
        }

        #propertiesWindowHint {
            color: rgba(255, 255, 255, 0.836);
            font-size: 16px;
        }

        #propertiesWindowHint::after {
            content: " !";
            font-size: 20px;
            color: #d73fda;
        }

        #addColumnWithName {
            color: rgba(255, 255, 255, 0.836);
        }
    }
}

.uploadcsv-container {
    display: flex;
    flex-flow: column nowrap;
    justify-content: center;
    align-items: center;
    row-gap: 10px;

    >label {
        margin: 0;
        font-size: 13px;
        background: rgba(255, 255, 255, 0.863);
        border-radius: 5px;
        cursor: pointer;
        text-align: center;
        height: 35px;
        width: 150px;
        padding: 3px 2px 2px 10px;
        line-height: 2.2;

        >.fa-cloud-upload {
            margin-top: 5px;
            margin-right: 13px;
        }
    }

    >input {
        display: none;
    }

    >span {
        color: rgb(202, 0, 0);
        display: none;
    }
}

#kaggle_dataset {
    height: 500px;
    width: 100%;
    display: flex;
    flex-flow: column nowrap;
    row-gap: 5px;

    .select-container {
        flex-grow: 3;
        background: white;
        position: relative;

        .layout {
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            width: 100%;
            padding: 5px;
            overflow-y: scroll;
            overflow-x: none;

            display: flex;
            flex-flow: column nowrap;
            row-gap: 5px;

            &::-webkit-scrollbar {
                width: 5px;
            }

            &::-webkit-scrollbar-track {
                background: transparent;
            }

            &::-webkit-scrollbar-thumb {
                background: #2c3e50;

                &:hover {
                    opacity: 0.9;
                }
            }

            .option {
                background-color: rgb(214, 214, 214);
                border-radius: 5px;
                color: black;
                padding: 5px;
                cursor: pointer;
                transition: all 300ms;

                &.active {
                    background-color: #2c3e50;
                    color: white;
                }

                &:hover {
                    background-color: #2c3e50;
                    color: white;
                }
            }
        }

    }

    .pagination-container {
        display: flex;
        flex-flow: row nowrap;
        width: 100%;
        column-gap: 3px;

        button {
            width: 100%;
            transition: all 300ms;

            &:hover {
                opacity: 0.8;
            }

            .icon-container {
                width: 100%;
                height: 100%;
                background-color: white;

                .icon {
                    color: #2c3e50;
                    font-size: 30px;
                    font-weight: bold;

                    &.right {
                        padding-left: 4px;
                    }

                    &.left {
                        padding-right: 4px;
                    }
                }
            }


        }
    }

    .button-container {
        button {
            border-radius: 5px;
            width: 120px;
            height: 35px;
            background-color: white;
            color: #2c3e50;
            transition: all 300ms;

            &:hover {
                opacity: 0.8;
            }
        }

    }

}
</style>