<template>
    <nav>
        <v-navigation-drawer
        app 
        fixed
        v-model="drawer"
        :mini-variant="mini"
        width="210"
        mini-variant-width="70"
        mobile-breakpoint="0"
        class="content elevation-4">
         
            <div class="logo" @click="mini = !mini">
                <img src="@/assets/logo.png" alt="logo" >
            </div>

            <v-divider></v-divider>

            <v-list dense>
                <v-list-item-group mandatory v-model="selectedRoute" color="primary">
                    <router-link v-for="(route, index) in routes" :key="index" :to="route.path" :class="{ disabled: route.disabled }">
                        <v-list-item :disabled="route.disabled">
                            <!--icons-->
                            <v-list-item-icon class="icon-container" v-if="route.name.toLowerCase() === 'dashboard'">
                                <DashboardIcon  :class="{icon: !route.disabled}" />
                            </v-list-item-icon>
                            <v-list-item-icon class="icon-container" v-else-if="route.name.toLowerCase() === 'marketplace'">
                                <MarketplaceIcon :class="{icon: !route.disabled}" />
                            </v-list-item-icon>
                            <v-list-item-icon class="icon-container" v-else-if="route.name.toLowerCase() === 'notebooks'">
                                <v-icon :class="{externalIcon: !route.disabled}">mdi-book-open</v-icon>
                            </v-list-item-icon>
                            <!--names-->
                            <v-list-item-content>
                                <v-list-item-title class="name" v-text="route.title"></v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </router-link>

                    <a :href="$router.resolve({name: 'machine-learning'}).href">
                        <v-list-item :disabled="false">
                            <!--icons-->    
                            <v-list-item-icon class="icon-container">
                                <v-icon :class="{externalIcon: true}">mdi-laptop</v-icon>
                            </v-list-item-icon>

                            <!--names-->
                            <v-list-item-content>
                                <v-list-item-title class="name" v-text="'Machine Learning'"></v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </a>    

                    <router-link to='/administration' v-if="isAdmin()">
                        <v-list-item :disabled="false">
                            <!--icons-->    
                            <v-list-item-icon class="icon-container">
                                <v-icon :class="{externalIcon: true}">mdi-book-open</v-icon>
                            </v-list-item-icon>

                            <!--names-->
                            <v-list-item-content>
                                <v-list-item-title class="name" v-text="'Administration'"></v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </router-link>
                </v-list-item-group>

            </v-list>
        </v-navigation-drawer>
    </nav>
    
</template>

<script>
import DashboardIcon from '@/assets/icons/dashboard.svg';
import MarketplaceIcon from '@/assets/icons/marketplace.svg';

export default {
    components: {
        DashboardIcon,
        MarketplaceIcon
    },

    data: () => ({
        drawer: true,
        mini: false,

        route: 0,
        routes: [
            {
                name: 'Dashboard', 
                title: 'Workspace', 
                path: '/',
                disabled: false
            },
            {
                name: 'Marketplace',
                title: 'Marketplace',
                path: '/marketplace',
                disabled: false
            },
            { 
                name: 'Notebooks',
                title: 'Notebooks',
                path: '/notebook',
                disabled: false
            },
        ],
    }),

    created(){
        if(this.$route.name === "machine-learning")
            this.mini = true;
        else
            this.mini = false;
    },

    computed: {
        selectedRoute: {
            get() {
                switch(this.$route.name){
                    case "dashboard":
                        return 0;
                    case "marketplace":
                        return 1;
                    case "notebook":
                        return 2;
                    case "machine-learning":
                        return 3;
                    case "administration":
                        return 4;
                }
                return 0;
            },

            set(value){
                this.route = value;
            }
        }
    },
    methods: {
        isAdmin() {
            if (localStorage.getItem("username") === 'root')
                return true;
            return false;
        }
    }
}
</script>

<style scoped lang="scss">
.content {
    background: white;
    filter: brightness(95%);
}

.logo {
    text-align: start;
    padding-top: 10px;
    padding-left: 8px;

    img {
        cursor: pointer;
        width: 50px;
        height: 50px;
    }
}

a:hover{
    text-decoration: none;
}

.name {
    text-align: start;
    font-size: 14px !important;
}

.icon-container {
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    background-color: #e7eeff;
    padding: 5px;
    width: 30px;
 
    .icon {
        g {
            stroke: #002279cb !important;

            path {
                stroke: #002279cb !important;
            }
        }

    }

    .externalIcon{
        color: #002279cb !important;
    }
}

.disabled {
    opacity: 0.5;
    pointer-events: none;
}
</style>
