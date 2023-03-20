<template>
    <div class="my-container">
        <div class="name">Verify Your Account</div>
        <CInput :id="email.id" :type="email.type" :placeholder="email.placeholder" :iconName="email.iconName"
            :value="email.value" :rules="email.rules" @onChange="handleInput" />

        <CInput :id="otp.id" :type="otp.type" :placeholder="otp.placeholder" :iconName="otp.iconName" :value="otp.value"
            :rules="otp.rules" @onChange="handleInput" />

        <CButton name="Verify" @onClick="handleSubmit" :disabled="!isValid" />

        <div class="error_message">{{ error }}</div>
    </div>
</template>

<script>
import CInput from "@/components/CInput.vue";
import CButton from "@/components/CButton.vue";
import { verify } from "@/api_client.js";

export default {
    name: "Verify",
    components: {
        CInput,
        CButton,
    },
    data() {
        return {
            email: {
                id: "email", //pass
                type: "email", //pass
                placeholder: "Email", //pass
                iconName: "fa-envelope", //pass
                value: "", //pass
                rules: { required: true, min: 4 }, //pass
                isValid: false,
            },
            otp: {
                id: "otp", //pass
                type: "text", //pass
                placeholder: "OTP", //pass
                iconName: "fa-barcode", //pass
                value: "", //pass
                rules: { required: true, min: 4 }, //pass
                isValid: false,
            },

            error: null,
        };
    },

    computed: {
        isValid() {
            if (this.email.isValid && this.otp.isValid) return true;
            return false;
        },
    },

    methods: {
        //handles
        handleInput(data) {
            this[data.id].value = data.value;
            this[data.id].isValid = data.isValid;
        },

        handleSubmit() {
            verify({ email: this.email.value, otp: this.otp.value })
                .then(({ status }) => {
                    if (status === 200)
                        this.$emit("go");
                })
                .catch(() => {
                    this.error = "Invalid credentials";
                });
        },
    },
};
</script>

<style lang="scss" scoped>
.my-container {
    width: 100%;
    height: 90%;
    padding: 20px 10%;

    display: flex;
    flex-flow: column nowrap;
    justify-content: center;
    row-gap: 30px;
    animation: play 500ms linear forwards;

    .name {
        width: 100%;
        height: auto;
        margin: -20px 0;

        font-size: 23px;
        text-align: center;
        letter-spacing: 2px;
        color: #364150;
    }

    .error_message {
        color: darkred;
        font-size: 14px;
    }
}

@keyframes play {
    from {
        visibility: hidden;
        opacity: 0;
    }

    to {
        visibility: visible;
        opacity: 1;
    }
}
</style>