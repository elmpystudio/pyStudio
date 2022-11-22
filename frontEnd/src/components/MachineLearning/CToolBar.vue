<template>
    <div class="content">
        <label for="trigger-tools" class="trigger-tools">
            <i class="icon fa fa-angle-left" aria-hidden="true"></i>
        </label>

        <input type="checkbox" id="trigger-tools" hidden />

        <div class="ml-studio--sidebar">
            <div class="sidebar-title">TOOLS</div>

            <ul id="sidebar-menu" class="sidebar-menu"></ul>

            <ul id="contextMenu" class="dropdown-menu" role="menu" style="display:none"></ul>
        </div>
    </div>
</template>

<script>
import $ from "jquery";

export default {
    name: "CToolBar",
    mounted() {
        $("#trigger-tools").click(() => {
            $(".trigger-tools").children("i").toggleClass("fa-angle-right")
        })
    }
}
</script>

<style scoped lang="scss">
.content {
    position: relative;
}

#trigger-tools:checked + div {
    margin-left: -270px;
}

.trigger-tools {
    position: absolute;
    z-index: 1;
    top: 300px;
    right: -15px;
    width: 15px;
    height: 100px;
    border-radius: 0 30px 30px 0;
    background: #364150;

    .icon {
        display: inherit;
        padding: 0;
        margin-top: 35px;
        margin-left: -4px;
        color: rgba(255, 255, 255, 0.863);
        font-size: 25px;
    }
}

.trigger-tools:hover {
    cursor: pointer;
    opacity: 0.98;
}

//overflow
::-webkit-scrollbar {
    width: 5px;
}

/* Track */
::-webkit-scrollbar-track {
    border-radius: 10px;
}

/* Handle */
::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.212);
    border-radius: 3px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.322);
}
</style>

<style lang="scss">
.ml-studio--sidebar {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 300px;
    min-width: 300px;
    border-radius: 0 30px 30px 0;
    background-color: #364150;
    padding: 0;
    transition: margin-left 300ms;

    .sidebar-title {
        border-radius: 0 30px 0 0;
        text-align: center;
        color: white;
        letter-spacing: 2px;
        font-weight: bold;
        font-size: 22px;
        padding: 2px;
        background: rgba(255, 255, 255, 0.212);
    }

    .sidebar-menu {
        width: 100%;
        padding: 20px 5px 20px 10px;
        height: 820px;
        overflow-y: scroll;

        .nav-item {
            text-align: left;
            margin: 0 8px 5px 8px;

            //PARENT
            .nav-link {
                border-radius: 5px;
                text-decoration: none;
                background: rgba(255, 255, 255, 0.836);
                display: flex;
                justify-content: flex-start;
                padding: 6px 11px;

                .name-container {
                    flex-grow: 1;   
                    padding: 5px;
                    .name {
                        display: block;
                        font-size: 13px;
                        color: black;
                        text-align: center;
                        letter-spacing: 1.3px;
                        text-transform: uppercase;
                    }
                }

                .icon {
                    color: #2c3e50;
                    margin-top: 7px;
                    font-size: 17px;
                }

                .arrow-icon {
                    color: #2c3e50;
                    font-size: 22px;
                    margin-top: 5px;
                }
            }

            //CHILDS
            .sub-menu {
                display: none;
                margin: 0;
                padding: 5px 0;
                animation: growDown 300ms ease-in-out alternate;
                transform-origin: top center;

                .sub-nav-link {
                    border-radius: 5px;
                    text-decoration: none;
                    background: rgb(200 212 223);
                    padding: 5px;
                    display: block;
                    text-align: center;
                    // background: rgb(222,224,226);
                    // background: radial-gradient(circle, rgba(222,224,226,1) 0%, rgba(54,65,80,1) 100%);

                    .sub-name {
                        font-size: 12px;
                        color: black;
                        letter-spacing: 1.2px;
                        text-transform: uppercase;
                        text-align: center;
                    }

                    // .sub-icon {
                    //     color: #2c3e50;
                    //     margin-top: 3px;
                    //     font-size: 15px;
                    // }
                }
            }
        }
    }
}
.dropdown-menu {
    box-shadow: 5px 5px rgba(102, 102, 102, 0.1);
    left: 0;
    min-width: 175px;
    position: absolute;
    z-index: 1000;
    display: none;
    float: left;
    list-style: none;
    text-shadow: none;
    padding: 0 !important;
    background-color: #fff;
    margin: 10px 0 0;
    border: 1px solid #eee;
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    border-radius: 4px;

    li {
        a {
            padding: 8px 16px;
            color: #6f6f6f;
            text-decoration: none;
            display: block;
            clear: both;
            font-weight: 300;
            line-height: 18px;
            white-space: nowrap;
        }
    }
}

.active {
    display: block !important;
}

@keyframes growDown {
    0% {
        transform: scaleY(0);
    }
    80% {
        transform: scaleY(1.05);
    }
    100% {
        transform: scaleY(1);
    }
}

</style>