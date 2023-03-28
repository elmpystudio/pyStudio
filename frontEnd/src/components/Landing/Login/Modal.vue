<template>
    <div class="c-modal" :class="{ active: active }">
        <div class="content">
            <div class="container">
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
        left: 50%;
        top: 50%;
        width: 600px;
        height: 300px;
        margin: -150px 0 0 -300px;


        .container {
            padding: 0;
            width: auto;
            height: auto;
            display: flex;
            flex-flow: column nowrap;
            justify-content: space-between;
            background-color: #f1f1f1;

            .body {
                flex-grow: 100%;
                padding: 20px 30px;
            }

            .footer {
                flex: 1 1 35px;

                button {
                    width: 100%;
                    height: 100%;
                    background: #364150;
                    ;
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