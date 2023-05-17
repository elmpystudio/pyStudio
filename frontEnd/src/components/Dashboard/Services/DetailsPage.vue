<template>
    <div class="detailspage-container" :class="{ active: active }">
        <div class="header">
            <div class="icon-container" @click="close()">
                <i class="fa fa-arrow-left" aria-hidden="true"></i>
            </div>
        </div>

        <div class="body">
            <div class="part1">
                <slot name="part1"></slot>
            </div>
            <div class="part2">
                <slot name="part2"></slot>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "DetailsPage",
    props: {
        active: { type: Boolean, required: false },
    },
    methods: {
        close() {
            this.$emit("close");
        },
    },
}
</script>

<style lang="scss" scoped>
.detailspage-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: none;
    flex-flow: column nowrap;
    background-color: white;

    &.active {
        display: flex;
    }

    .header {
        padding: 5px 0;
        display: flex;
        flex-flow: row nowrap;
        justify-content: start;
        align-items: center;

        .icon-container {
            i {
                color: #2b468b;
                font-size: 22px;

                transition: all 300ms;

                &:hover {
                    cursor: pointer;
                    opacity: 0.8;
                }
            }
        }
    }

    .body {
        height: 100%;
        display: flex;
        flex-flow: row nowrap;
        column-gap: 10px;


        .part1 {
            flex-basis: 100%;
        }

        .part2 {
            flex-basis: 100%;
        }
    }
}
</style>