<template>
    <div class="input-component">
        <div class="input-container">
            <i aria-hidden="true" :class="`fa ${iconName} icon`"></i>

            <input
                class="input"
                :type="type"
                :placeholder="placeholder"
                :value="value"
                @input="onChange"
                :readonly="readonly"
            />
        </div>
        <span class="error-message">{{ error }}</span>
    </div>
</template>

<script>
export default {
    name: "CInput",
    props: {
        id: { type: String, required: true },
        type: { type: String, required: true },
        iconName: { type: String, required: true },
        value: { type: String, required: true },
        rules: { type: Object, required: true },
        placeholder: { type: String, required: false },
        readonly: { type: Boolean, default: false }
    },
    data() {
        return {};
    },
    computed: {
        error() {
            return this.validate(this.value);
        },
    },

    methods: {
        onChange(event) {
            this.$emit("onChange", {
                id: this.id,
                value: event.target.value,
                isValid: this.validate(event.target.value) ? false : true,
            });
        },

        validate(value) {
            if (this.rules.required && !value) return "reqiured";
            if (value !== "" && this.rules.min && value.length < this.rules.min)
                return `must be > ${this.rules.min}`;
            //return `${this.id} must be > ${this.rules.min}`;

            //email validate
            /*if(this.type === "email"){
				var mailformat = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
				if(!this.value.match(mailformat))
					return "not email";
			}*/
        },
    },
};
</script>

<style lang="scss" scoped>
.input-component {
    position: relative;

    .input-container {
        width: 100%;
        height: 37px;

        display: flex;
        flex-flow: row nowrap;

        .icon {
            width: 100%;
            height: 100%;
            max-width: 50px;

            background-color: #364150;
            color: #d6d6d6;

            border-radius: 2px;

            display: flex !important;
            flex-flow: column nowrap;
            justify-content: center;
            align-items: center;
        }

        .input {
            flex-grow: 1;
            width: 100%;
            height: 100%;
            outline: none;
            border: none;
            background: #d6d6d6;
            border-bottom: 2px solid #364150;
            color: #364150;

            padding: 10px 12px;

            font-size: 14px;

            &:focus {
                border: 2px solid;
            }
        }

        .inputError {
            border-bottom: 2px solid red;
        }
    }

    .error-message {
        position: absolute;
        content: "";
        bottom: -19px;
        left: 50px;
        color: darkred;
        font-size: 13px;
    }
}
</style>