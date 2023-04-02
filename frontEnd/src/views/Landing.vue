<template>
    <div class="landing-container">
        <div class="header">
            <Header />
        </div>

        <div class="body">
            <section class="welcome" id="welcome-section">
                <Welcome />
            </section>

            <section class="login" id="login-section">
                <Login />
            </section>
        </div>

        <div class="footer">
            <Footer />
        </div>
    </div>
</template>

<script>
import Header from "@/components/Landing/Header.vue";
import Footer from "@/components/Landing/Footer.vue";
import Welcome from "@/components/Landing/Welcome.vue";
import Login from "@/components/Landing/Login/index.vue";



export default {
    name: "Landing",
    components: {
        Header,
        Footer,
        Welcome,
        Login
    }

};
</script>

<style lang="scss" scoped>
.landing-container {
    width: 100%;
    height: 100%;
    display: flex;
    flex-flow: column nowrap;
    justify-content: space-between;
    background: linear-gradient(306deg, rgba(56, 67, 82, 1) 0%, rgba(106, 44, 145, 1) 50%, rgba(15, 108, 182, 1) 100%);


    .header {
        //
    }

    .body {
        width: 100%;
        height: 100%;
        display: flex;
        flex-flow: column nowrap;
        justify-content: center;
        row-gap: 20px;
        padding: 10px 0;

        .welcome {
            // 
        }

        .login {
            // 
        }
    }

    .footer {
        // 
    }
}
</style>