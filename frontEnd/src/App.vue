<template>
    <v-app>
        <Sidebar v-if="isShow && !fullScreen"/>
        <v-main class="grey lighten-4">
            <Navbar class="main-navbar" v-if="isShow"
            :icon="getIcon"
            :title="getTitle"
            />
            <router-view></router-view>
        </v-main>
    </v-app>
</template>

<script>
import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar";
import $ from "jquery";

export default {
    name: "App",
    components: {
        Sidebar,
        Navbar
    },
    
    mounted(){
        //button in components/machinelearning/CMunuBar.vue
        $("#full-screen").click(() => {
            this.fullScreen = !this.fullScreen;
            $(".main-navbar").toggleClass("main-navbar-hidden")
        })
    },

    data: () => ({
        fullScreen: false,

        sidebarRoutes: [
            "dashboard",
            "analytics",
            "analytics-view",
            "analytics-edit",
            "analytics-create",
            "marketplace",
            "dataset-offering",
            "va-offering",
            "dataset",
            "dataset-publish",
            "dataset-edit",
            "analytics-publish",
            "notifications",
            "profile",
            "test",
            "machine-learning",
            "notebook",
            "administration"
        ]
    }),

    computed: {
        isShow(){
            return this.sidebarRoutes.indexOf(this.$route.name) > -1;
        },

        getTitle(){
            var title = this.$route.name;
            if(title === "machine-learning")
                return "machine learning studio".toUpperCase();

            return title.toUpperCase();
        },

        getIcon() {
            switch(this.getTitle){
                case "home":
                    return "email"
                case "about":
                    return "home";
            } 

            return "home"
        }
    }
}
</script>

<style scoped lang="scss">
.main-navbar{
    transition: margin-top 300ms;
}

.main-navbar-hidden{
    margin-top: -64px;
}
</style>

<style lang="scss">
@import url('https://fonts.googleapis.com/css?family=Poppins&display=swap');
@import'~bootstrap/dist/css/bootstrap.css';

//overflow
::-webkit-scrollbar {
    width: 0;
}

#app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;

    min-height: 100vh;
    display: flex;
    font-family: 'Roboto Condensed', sans-serif;
}

html, body {
    font-family: 'Roboto Condensed', sans-serif;
    scroll-behavior: smooth;
}
</style>
