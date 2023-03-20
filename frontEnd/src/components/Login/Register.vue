<template>
    <div class="my-container">
        <div class="name">Register</div>
        <CInput :id="username.id" :type="username.type" :placeholder="username.placeholder" :iconName="username.iconName"
            :value="username.value" :rules="username.rules" @onChange="handleInput" />
        <CInput :id="email.id" :type="email.type" :placeholder="email.placeholder" :iconName="email.iconName"
            :value="email.value" :rules="email.rules" @onChange="handleInput" />
        <CInput :id="about.id" :type="about.type" :placeholder="about.placeholder" :iconName="about.iconName"
            :value="about.value" :rules="about.rules" @onChange="handleInput" />
        <div class="password-form">
            <CInput :id="password.id" :type="password.type" :placeholder="password.placeholder"
                :iconName="password.iconName" :value="password.value" :rules="password.rules" @onChange="handleInput" />
            <CInput :id="password_confirm.id" :type="password_confirm.type" :placeholder="password_confirm.placeholder"
                :iconName="password_confirm.iconName" :value="password_confirm.value" :rules="password_confirm.rules"
                @onChange="handleInput" />
        </div>
        <CInputFile :id="image.id" :rules="image.rules" @onChange="handleInputFile" />

        <CButton name="Register" @onClick="handleSubmit" :disabled="!isValid" />

        <div class="error_message">{{ `${password_error} ${error}` }}</div>
    </div>
</template>

<script>
import CInput from "@/components/CInput.vue";
import CInputFile from "@/components/CInputFile.vue";
import CButton from "@/components/CButton.vue";
import { register } from "@/api_client.js";

export default {
    name: "Register",
    components: {
        CInput,
        CInputFile,
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
            email: {
                id: "email", //pass
                type: "email", //pass
                placeholder: "Email", //pass
                iconName: "fa-envelope", //pass
                value: "", //pass
                rules: { required: true, min: 10 }, //pass
                isValid: false,
            },
            about: {
                id: "about", //pass
                type: "text", //pass
                placeholder: "About", //pass
                iconName: "fa-info", //pass
                value: "", //pass
                rules: { required: false, min: 0 }, //pass
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
            password_confirm: {
                id: "password_confirm", //pass
                type: "password", //pass
                placeholder: "Password Confirm", //pass
                iconName: "fa-key", //pass
                value: "", //pass
                rules: { required: true, min: 8 }, //pass
                isValid: false,
            },

            image: {
                id: "image", //pass
                rules: { required: false }, //pass
                file: null,
            },

            error: ""
        };
    },

    computed: {
        password_error() {
            if (
                this.password.value !== "" &&
                this.password_confirm.value !== ""
            )
                if (this.password.value !== this.password_confirm.value)
                    return "Password not match";
            return "";
        },

        isValid() {
            //username
            if (this.username.rules.required && !this.username.isValid)
                return false;
            //email
            else if (this.email.rules.required && !this.email.isValid)
                return false;
            //password
            else if (this.password.rules.required && !this.password.isValid)
                return false;
            //password_confirm
            else if (
                (this.password_confirm.rules.required &&
                    !this.password_confirm.isValid) ||
                this.password_error !== ""
            )
                return false;

            return true;
        },
    },

    methods: {
        //handles
        handleInput(data) {
            this[data.id].value = data.value;
            this[data.id].isValid = data.isValid;
        },

        handleSubmit() {
            register({
                username: this.username.value,
                email: this.email.value,
                password: this.password.value,
                about: this.about.value,
                image: this.image.file
            })
                .then(() => {
                    this.$emit("go");
                })
                .catch((error) => {
                    this.error = error;
                });
        },

        handleInputFile(data) {
            this[data.id].file = data.file;
        },
    },
};
</script>

<style lang="scss" scoped>
.my-container {
    width: 100%;
    height: 100%;
    padding: 20px 10%;

    display: flex;
    flex-flow: column nowrap;
    justify-content: center;
    row-gap: 22px;
    animation: play 500ms linear forwards;

    .name {
        width: 100%;
        height: auto;
        margin: -15px 0;

        font-size: 23px;
        text-align: center;
        letter-spacing: 2px;
        color: #364150;
    }

    .password-form {
        display: flex;
        flex-flow: row nowrap;
        column-gap: 5px;
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