<template>
    <div class="my-container">
        <div class="name">Login</div>
        <CInput
            :id="username.id"
            :type="username.type"
            :placeholder="username.placeholder"
            :iconName="username.iconName"
            :value="username.value"
            :rules="username.rules"
            @onChange="handleInput"
        />

        <CInput
            :id="password.id"
            :type="password.type"
            :placeholder="password.placeholder"
            :iconName="password.iconName"
            :value="password.value"
            :rules="password.rules"
            @onChange="handleInput"
        />

        <CButton name="Login" @onClick="handleSubmit" :disabled="!isValid" />

        <div class="error_message">{{ error }}</div>
    </div>
</template>

<script>
import CInput from "@/components/CInput.vue";
import CButton from "@/components/CButton.vue";
import { login } from "@/api_client.js";

export default {
    name: "CLogin",
    components: {
        CInput,
        CButton,
    },
    data() {
        return {
            username: {
                id: "username", //pass
                type: "text", //pass
                placeholder: "Username", //pass
                iconName: "fa-user", //pass
                value: "", //pass
                rules: { required: true, min: 4 }, //pass
                isValid: false,
            },
            password: {
                id: "password", //pass
                type: "password", //pass
                placeholder: "Password", //pass
                iconName: "fa-key", //pass
                value: "", //pass
                rules: { required: true, min: 8 }, //pass
                isValid: false,
            },

            error: null,
        };
    },

    computed: {
        isValid() {
            if (this.username.isValid && this.password.isValid) return true;
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
            login({ username: this.username.value, password: this.password.value })
                .then(({ status, data }) => {
                    if (status === 200) {
                            localStorage.setItem("token", data.token);
                            localStorage.setItem("username", this.username.value);
                        this.$router.push("/");
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