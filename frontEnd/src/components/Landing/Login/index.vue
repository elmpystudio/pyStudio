<template>
    <div class="login-container">
        <div class="login-content">
            <div class="info-container">
                <div class="description">
                    <ul>
                        <li>PyStudio is an open-source machine learning platform to train and deploy ML models in a workflow environment.</li>
                        <li>It allows you to go from preparing data to deploying a model within seconds.</li>
                        <li>PyStudio is designed to avoid coding in ML experiments just drag and drop.</li>
                    </ul>
                </div>
            </div>

            <div class="form-container">
                <div class="tab">
                    <button class="tab-link" @click="openTab('login')">
                        Login
                    </button>

                    <button class="tab-link" @click="openTab('register')">
                        Register
                    </button>
                </div>

                <div id="login" class="tab-content">
                    <Login @done="handle_login"/>
                </div>

                <div id="register" class="tab-content">
                    <Register @done="handle_register" @onClick="loader_toggle = true"/>
                </div>                
            </div>
        </div>

        <Modal :active="modal_toggle" @close="modal_toggle = false">
            <template #default>
                <Verify :email_value="email" @done="handle_verify"/>
            </template>
        </Modal>

        <CLoader v-if="loader_toggle"/>
    </div>
</template>

<script>
import Login from "./Login.vue";
import Register from "./Register.vue";
import Verify from "./Verify.vue";
import Modal from "./Modal.vue";
import CLoader from "@/components/CLoader.vue";

export default {
    name: "Login-view",
    components: {
        Login,
        Register,
        Verify,
        Modal,
        CLoader
    },

    data() {
        return {
            tabLinks: null,
            tabContents: null,
            modal_toggle: false,
            loader_toggle: false,
            email: null
        };
    },

    mounted() {
        this.tabLinks = document.getElementsByClassName("tab-link");
        this.tabContents = document.getElementsByClassName("tab-content");

        for (let i = 1; i < this.tabContents.length; i++)
            this.tabContents[i].style.display = "none";

        this.tabLinks[0].classList.add("active");
    },

    methods: {
        // handles
        handle_login() {
            this.modal_toggle = true
        },

        handle_register(response) {
            if (response.good){
                this.email = response.email;
                this.modal_toggle = true;
                this.openTab('login');
            }
            this.loader_toggle = false;
        },

        handle_verify() {
            this.modal_toggle = false;
        },

        openTab(tabID) {
            //hide all
            for (let i = 0; i < this.tabContents.length; i++) {
                this.tabLinks[i].className = this.tabLinks[i].className.replace(
                    " active",
                    ""
                );
                this.tabContents[i].style.display = "none";
            }

            //acrive this
            document.getElementById(tabID).style.display = "block";

            if (tabID === "login")
                this.tabLinks[0].classList.add("active");

            else if (tabID === "register")
                this.tabLinks[1].classList.add("active");
        }
    },
};
</script>

<style lang="scss" scoped>
.login-container {
    width: 100%;
    height: 100%;
    position: relative;

    display: flex;
    flex-flow: row nowrap;
    justify-content: center;

   
    .login-content {
        width: 1200px;
        height: 600px;
        display: flex;
        flex-flow: row nowrap;
        justify-content: center;

        animation: play 800ms linear forwards;

        .info-container {
            background-color: rgba(0, 0, 0, 0.2);
            width: 50%;
            padding: 35px;

            display: flex;
            flex-flow: column nowrap;
            justify-content: center;

            .description {
                text-align: start;
                font-size: 20px;
                color: white;

                ul>li {
                    margin: 0;
                    margin-bottom: 10px;
                }

            }
        }

        ///////////////////////////////

        .form-container {
            position: relative;
            background-color: white;
            margin-top: 55px;

            width: 50%;
            min-width: 300px;

            .tab {
                position: absolute;
                content: "";
                top: -55px;
                left: 0;
                width: 100%;

                display: flex;
                flex-flow: row nowrap;
                justify-content: space-around;
                align-items: center;

                .tab-link {
                    background-color: rgba(0, 0, 0, 0.2);
                    color: white;

                    width: 100%;
                    border: none;
                    outline: none;
                    cursor: pointer;
                    padding: 14px 16px;
                    font-size: 20px;
                    letter-spacing: 2px;

                    transition: all 300ms;

                    &:hover {
                        opacity: 0.9;
                    }
                }

                .active {
                    opacity: 1 !important;
                    background-color: white;
                    color: #364150;

                }
            }

            .tab-content {
                width: 100%;
                height: 100%;
            }
        }
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

@media only screen and (max-width: 450px) {
    .info-container {
        display: none !important;
    }
}
</style>