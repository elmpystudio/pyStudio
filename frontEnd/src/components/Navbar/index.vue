<template>
    <nav>
        <v-toolbar class="content" elevation="2" outlined>
            <div class="icon-box" v-if="title.toLowerCase() === 'dashboard'">
                <DashboardIcon class="icon" />
            </div>
            <div class="icon-box" v-else-if="title.toLowerCase() === 'marketplace'">
                <MarketplaceIcon class="icon" />
            </div>
            <div class="icon-box" v-else-if="title.toLowerCase() === 'notebook'">
                <v-icon class="icon">mdi-book-open</v-icon>
            </div>

            <div class="icon-box" v-else-if="title.toLowerCase() === 'machine learning studio'">
                <v-icon class="icon">mdi-laptop</v-icon>
            </div>

            <div class="icon-box" v-else-if="title.toLowerCase() === 'test'">
                <v-icon class="icon">mdi-test-tube</v-icon>
            </div>

            <div class="icon-box" v-else-if="title.toLowerCase() === 'administration'">
                <v-icon class="icon">mdi-book-open</v-icon>
            </div>


            <div class="title">{{ title }}</div>

            <v-spacer></v-spacer>

            <div class="control-container">
                <Bell />
                <Profile />
            </div>
        </v-toolbar>
    </nav>
</template>

<script>
//components
import Bell from './Bell.vue';
import Profile from './Profile.vue';
//icons
import DashboardIcon from '@/assets/icons/dashboard.svg';
import MarketplaceIcon from '@/assets/icons/marketplace.svg';

export default {
    name: "Navbar",
    props: {
        title: { type: String, required: true },
        icon: { type: String, required: true }
    },

    components: {
        Bell,
        Profile,
        DashboardIcon,
        MarketplaceIcon
    }
}
</script>

<style scoped lang="scss">
.content {
    padding: 0 10px;
    z-index: 100 !important;
    height: 64px !important;
    background: white !important;
    filter: brightness(95%);

    .title {
        display: inline;
        font-size: 24px !important;
        letter-spacing: 2px !important;
        text-align: start;
        padding-left: 10px;
    }

    .icon-box {
        display: flex;
        border-radius: 4px;
        background-color: #e7eeff;
        justify-content: center;
        align-items: center;
        height: 35px;
        width: 35px;

        .icon {
            color: #002279cb;

            g {
                stroke: #002279cb;

                path {
                    stroke: #002279cb !important;
                }
            }
        }
    }

    .control-container {
        display: flex;
        flex-flow: row nowrap;
        align-items: center;
        column-gap: 15px;
    }
}
</style>