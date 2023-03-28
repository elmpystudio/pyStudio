<template>
    <div class="mycontainer">
        <div class="content">
            <div class="info-container">
                <div class="welcome">Welcome to PyStudio</div>
                <div class="description">
                    <p>PyStudio is an open-source machine learning platform to train and deploy ML models in a workflow environment.</p>
                    <p>It allows you to go from preparing data to deploying a model within seconds.</p>
                    <p>PyStudio is designed to avoid coding in ML experiments just drag and drop</p>
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
.mycontainer {
    width: 100%;
    height: 100%;

    background-color: white;

    position: relative;

    .content {
        height: 100%;
        width: 100%;

        display: flex;
        flex-flow: row nowrap;
        justify-content: center;

        animation: play 800ms linear forwards;

        .info-container {
            background-color: #384352;
            width: 420px;
            height: 505px;

            /*flex*/
            display: flex;
            flex-flow: column nowrap;
            justify-content: center;

            .welcome {
                text-align: center;
                font-weight: bold;
                font-size: 24px;
                letter-spacing: 1.2px;
                color: #f1f1f1;
            }

            .description {
                text-align: center;
                font-size: 20px;
                color: #f1f1f1;
                padding: 5px 30px;

            }
        }

        ///////////////////////////////

        .form-container {
            position: relative;
            background-color: #e3e3e3;
            margin-top: 55px;
            /* because ".tab" top */

            width: 550px;
            height: 450px;
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
                    background-color: #364150;
                    color: #f1f1f1;

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
                    background-color: #e3e3e3;
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