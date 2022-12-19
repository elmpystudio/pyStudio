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
                    <slot></slot>
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

    display: none;

    &.active {
        display: block;
    }

    .content {
        position: absolute;
        width: 50%;
        height: 50%;
        left: calc(50% - calc(50%/2));
        top: calc(50% - calc(50%/2));

        border-radius: 10px;
        overflow: hidden;
        border: 2px solid #1976d2;

        .container {
            padding: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-flow: column nowrap;
            justify-content: space-between;
            background-color: #fff;

            .header {
                flex: 0 0 40px;
                padding: 0 10px;

                display: flex;
                flex-flow: row nowrap;
                justify-content: center;
                align-items: center;

                background: #1976d2;

                .mytitle {
                    flex-grow: 1;
                    text-align: center;
                    font-size: 20px;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                    color: #e1e5ee;
                }
            }

            .body {
                flex: 1 1 90%;
            }

            .footer {
                flex: 1 1 40px;
                overflow: hidden;

                button {
                    width: 100%;
                    height: 100%;
                    background: #1976d2;
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