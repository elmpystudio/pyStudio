<template>
    <div class="input-component">
        <input class="input" type="file" accept="image/*" @change="onChange" />

        <span class="error_message">{{ error }}</span>
    </div>
</template>

<script>
export default {
    name: "CInputFile",
    props: {
        id: { type: String, required: true },
        rules: { type: Object, required: true },
    },
    data() {
        return {};
    },
    computed: {
        error() {
            if (this.rules.required) return "reqiured";

            return null;
        },
    },

    methods: {
        onChange(event) {
            this.$emit("onChange", {
                id: this.id,
                file: event.target.files[0]
            });
        },

        validate(value) {
            if (this.rules.required && !value) return "reqiured";
            if (value !== "" && this.rules.min && value.length < this.rules.min)
                return `must be > ${this.rules.min}`;
        },
    },
};
</script>

<style lang="scss" scoped>
.input-component {
    position: relative;

    .input {
        visibility: hidden;
        padding: 0;
        padding-top: 2px;
        transition: all 300ms;

        &:hover {
            &:hover {
                opacity: 0.8;
            }
        }

        &::before {
            visibility: visible;
            content: "Select Image...";
            display: inline-block;
            background: #d6d6d6;
            border: 2px solid #364150;
            padding: 2px 8px;

            outline: none;
            white-space: nowrap;

            cursor: pointer;
            color: #364150;

            font-size: 12px;
        }
    }

    .error_message {
        position: absolute;
        content: "";
        bottom: -19px;
        left: 10px;
        color: darkred;
        font-size: 13px;
    }
}
</style>