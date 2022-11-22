<template>
    <div class="dashboard">
        <div class="header">
            <v-tabs
                class="tabs"
                v-model="tab"
                slider-color="#2f6bff"
                slider-size="3"
                color="#0a1448"
            >
                <v-tab key="projects" @click="handle_click('projects')">Projects</v-tab>
                <v-tab key="datasets" @click="handle_click('datasets')">Datasets</v-tab>
                <v-tab key="services" @click="handle_click('services')">Services</v-tab>
            </v-tabs>
        </div>

        <div class="content">
            <v-tabs-items v-model="tab" class="tabs-items" style="height: 100%">
                <v-tab-item key="projects">
                    <Projects v-if="isActive === 'projects'"/>
                </v-tab-item>
                <v-tab-item key="datasets">
                    <Items v-if="isActive === 'datasets'"/>
                </v-tab-item>
                <v-tab-item key="services">
                    <Services v-if="isActive === 'services'"/>
                </v-tab-item>
            </v-tabs-items>
        </div>
    </div>
</template>

<script>
import Items from "./Items";
import Projects from "./Projects";
import Services from "./Services.vue";
import { getMyIP, getTableauToken } from "@/api_client.js";

export default {
    name: "Dashboard",
    components: {
        Items,
        Projects,
        Services,
    },
    data() {
        return {
            tab: null,
            isActive: "projects"
        };
    },
    mounted() {
        getMyIP()
            .then((response) => {
                getTableauToken(response.data).then(({ status, data }) => {
                    if (status === 200) {
                        data.key && localStorage.setItem("key", data.key);
                    }
                });
            })
            .catch((error) => console.error(error));
    },
    methods: {
        handle_click(name) {
            this.isActive = name;
        }
    }
};
</script>

<style scoped lang="scss">
.dashboard {
    height: 100%;
    .header {
        padding: 30px 30px 0 30px;
        position: relative;
        background-color: #ffffff;

        .tabs {
            .v-tab {
                text-transform: capitalize;
                color: #858ba0;
                font-weight: 500;
                font-size: 16px;

                &--active {
                    color: #0a1448;
                }
            }
        }
    }

    .content {
        width: 100%;
        height: 100%;
        padding: 20px;
        background-color: #fff;
    }
}
</style>
