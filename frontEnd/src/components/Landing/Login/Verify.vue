<template>
    <div class="my-container">
        <div class="name">
            Hey there! Please check your email (including your spam folder) for your OTP. We've sent it your way. Thanks!
        </div>
        <CInput :id="new_email.id" :type="new_email.type" :placeholder="new_email.placeholder" :iconName="new_email.iconName"
            :value="email" :rules="new_email.rules" @onChange="handleInput" />

        <CInput :id="otp.id" :type="otp.type" :placeholder="otp.placeholder" :iconName="otp.iconName" :value="otp.value"
            :rules="otp.rules" @onChange="handleInput" />

        <CButton name="Verify" @onClick="handleSubmit" :disabled="!isValid" />

        <div class="error_message">{{ error }}</div>
    </div>
</template>

<script>
import CInput from "@/components/CInput.vue";
import CButton from "@/components/CButton.vue";
import { verify, login } from "@/api_client.js";

export default {
    name: "Verify",
    components: {
        CInput,
        CButton,
    },

    props: {
        email: { type: String, required: true },
        username: { type: String, required: true },
        password: { type: String, required: true },
    },

    data() {
        return {
            new_email: {
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
            if ((this.email || this.new_email.isValid) && this.otp.isValid) return true;
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
            if (this.new_email.value !== "")
                this.email = this.new_email.value;

            verify({ email: this.email, otp: this.otp.value })
                .then(({ status }) => {
                    if (status === 200) {
                        login({ username: this.username, password: this.password })
                            .then(({ status, data }) => {
                                if (status === 200) {
                                    localStorage.setItem("token", data.token);
                                    localStorage.setItem("username", this.username);
                                    this.$router.push("/");
                                }
                            })
                            .catch((error) => {
                                if (error.response.status === 401)
                                    if (error.response.data.detail === "User account not verified")
                                        this.$emit("done", error.response)

                                this.error = "Invalid credentials";
                            });
                    }
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
    height: 100%;

    display: flex;
    flex-flow: column nowrap;
    justify-content: center;
    row-gap: 20px;
    animation: play 500ms linear forwards;

    .name {
        width: 100%;
        height: auto;

        font-size: 20px;
        text-align: center;
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