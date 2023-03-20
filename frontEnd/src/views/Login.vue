<template>
    <div class="mycontainer">
        <div class="content">
            <div class="info-container">
                <div class="welcome">Welcome to Analytics Platform</div>
                <div class="description">
                    We provide most of the tools that data scientists need to
                    carry out their tasks
                </div>
            </div>

            <div class="form-container">
                <div class="tab">

                    <button class="tab-link" @click="openTab('register')">
                        1-Register
                    </button>

                    <button class="tab-link" @click="openTab('verify')">
                        2-Verify
                    </button>

                    <button class="tab-link" @click="openTab('login')">
                        3-Login
                    </button>
                </div>

                <div id="register" class="tab-content">
                    <Register @go="openTab('verify')" />
                </div>

                <div id="verify" class="tab-content">
                    <Verify @go="openTab('login')" />
                </div>

                <div id="login" class="tab-content">
                    <Login @go="openTab('verify')" />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Login from "@/components/Login/Login.vue";
import Register from "@/components/Login/Register.vue";
import Verify from "@/components/Login/Verify.vue";

export default {
    name: "UserView",
    components: {
        Login,
        Register,
        Verify
    },

    data() {
        return {
            tabLinks: null,
            tabContents: null,
            step: 1
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

            if (tabID === "register")
                this.tabLinks[0].classList.add("active");

            else if (tabID === "verify")
                this.tabLinks[1].classList.add("active");

            else if (tabID === "login")
                this.tabLinks[2].classList.add("active");
        },

        //handles
        handleRegister() {
            this.openTab("login");
        },
    },
};
</script>

<style lang="scss" scoped>
.mycontainer {
    width: 100%;
    height: 100%;
    background-color: #f1f1f1;

    .content {
        height: 100%;
        width: 100%;
        padding: 10px;

        display: flex;
        flex-flow: row nowrap;
        justify-content: center;
        align-items: center;

        animation: play 800ms linear forwards;

        .info-container {
            background-color: #384352;
            width: 420px;
            height: 505px;
            /*.form-container + .top*/

            padding: 0 20px;

            /*flex*/
            display: flex;
            flex-flow: column nowrap;
            justify-content: center;

            .welcome {
                text-align: center;
                font-weight: bold;
                font-size: 22px;
                letter-spacing: 1.2px;
                color: #f1f1f1;
            }

            .description {
                text-align: center;
                font-size: 18px;
                color: #f1f1f1;
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