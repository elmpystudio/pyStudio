<template>
    <div class="c-modal" :class="{ active: active }">
        <div class="content">
            <div class="container">
                <div class="header">
                    <div class="mytitle">
                        {{ title }}
                    </div>
                </div>
                <div class="body">
                    <div class="status">
                        <i class="fa fa-check-circle" aria-hidden="true"></i>
                        <!-- <i class="fa fa-times-circle-o" aria-hidden="true"></i> -->
                    </div>
                    <div class="body_container">
                        <div class="body_container_content">
                            <slot name="body"></slot>
                        </div>
                    </div>
                </div>

                <div class="footer">
                    <button @click="close()">OK</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "CModal",

    props: {
        active: { type: Boolean, required: true },
        title: { type: String, required: true },
    },

    methods: {
        close() {
            this.$emit("close");
        },
    },
};
</script>

<style lang="scss" scoped>
.c-modal {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    min-width: 750px;

    background-color: rgba(0, 0, 0, 0.3);
    z-index: 2;

    opacity: 0;
    transform: scale(0);

    transition: all 300ms;

    &.active {
        opacity: 1;
        transform: scale(1);
    }

    .content {
        position: absolute;
        width: 40%;
        height: 40%;
        left: calc(50% - calc(40%/2));
        top: calc(50% - calc(40%/2));

        border-radius: 10px;
        overflow: hidden;
        border: 2px solid #2b468b;

        .container {
            padding: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-flow: column nowrap;
            justify-content: space-between;
            background-color: #fff;

            .header {
                flex: 0 0 50px;
                padding: 0 10px;

                display: flex;
                flex-flow: row nowrap;
                justify-content: center;
                align-items: center;

                background: #2b468b;

                .mytitle {
                    flex-grow: 1;
                    text-align: center;
                    font-size: 22px;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                    color: #e1e5ee;
                }
            }

            .body {
                flex: 1 1 90%;

                display: flex;
                flex-flow: column nowrap;

                .status {
                    flex: 1 1 10%;

                    > i {
                        font-size: 60px;
                        color: green;
                    }
                }

                &_container {
                    flex: 1 1 90%;
                    position: relative;

                    &_content {
                        position: absolute;
                        top: 0;
                        left: 0;
                        height: 100%;
                        width: 100%;
                        overflow-y: scroll;
                        overflow-x: hidden;

                        // /* width */
                        &::-webkit-scrollbar {
                            width: 8px;
                        }

                        /* Track */
                        &::-webkit-scrollbar-track {
                            // background: #0000000a;
                        }

                        /* Handle */
                        &::-webkit-scrollbar-thumb {
                            background: #2b468b;
                            border-radius: 5px;
                        }

                        /* Handle on hover */
                        &::-webkit-scrollbar-thumb:hover {
                            background: #2b468bb0;
                        }
                    }
                }
            }

            .footer {
                flex: 1 1 50px;
                overflow: hidden;

                button {
                    width: 100%;
                    height: 100%;
                    background: #2b468b;
                    color: white;
                    font-size: 20px;
                    letter-spacing: 1px;
                    transition: all 300ms;

                    &:hover {
                        opacity: 0.9;
                    }
                }
            }
        }
    }
}
</style>