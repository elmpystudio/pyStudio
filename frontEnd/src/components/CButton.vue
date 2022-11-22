<template>
    <div>
        <button
            @click="onClick"
            class="button"
            :class="{ button_disable: disabled }"
        >
            {{ name }}
        </button>
    </div>
</template>

<script>
export default {
    name: "CButton",
    props: {
        name: { type: String, required: true },
        disabled: { type: Boolean, required: true },
    },

    methods: {
        onClick() {
            this.$emit("onClick");
        },
    },
};
</script>

<style lang="scss" scoped>
.button {
    width: 100%;
    height: 40px;
    outline: none;

    border: none;
    font-size: 15px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    border-radius: 2px;
    color: white;

    background-color: #364150;

    &:hover {
        opacity: 0.9;
    }

    &:active {
        transform: translateY(1px);
    }
}

.button_disable {
    pointer-events: none;
    opacity: 0.5;
}
</style>