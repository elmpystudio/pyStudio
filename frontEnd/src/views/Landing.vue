<template>
    <div class="mycontainer">
        <div class="header">
            <Header />
        </div>

        <div class="contents">
            <section class="welcome-container" id="welcome-section">
                <Welcome />
            </section>

            <section class="login-container" id="login-section">
                <Login />
            </section>
        </div>
    </div>
</template>

<script>
import Header from "@/components/Landing/Header.vue";
import Welcome from "@/components/Landing/Welcome.vue";
import Login from "@/components/Landing/Login/index.vue";


export default {
    name: "Landing",
    components: {
        Header,
        Welcome,
        Login
    }

};
</script>

<style lang="scss" scoped>
.mycontainer {
    width: 100%;
    height: 100%;
    

    .header {
        width: 100%;
        height: 70px;
    }

    .contents {
        width: 100%;
        height: 100%;

        .welcome-container {
            height: 70%;
            margin-bottom: 20px;
        }

        .login-container {
            height: auto;
            padding-bottom: 20px;
        }
    }

}
</style>