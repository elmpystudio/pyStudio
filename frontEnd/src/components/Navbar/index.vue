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
                <Notifications class="notification" />
                <Profile class="profile" />
            </div>
        </v-toolbar>
    </nav>
</template>

<script>
//components
import Notifications from '@/components/Navbar/Notifications.vue';
import Profile from '@/components/Navbar/Profile.vue';
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
        Notifications,
        Profile,
        DashboardIcon,
        MarketplaceIcon
    }
}
</script>

<style scoped lang="scss">
.content {
    z-index: 100 !important;
    height: 64px !important;
    background: white !important;
    filter: brightness(95%);
}

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
    width: 200px;
    padding-top: 5px;


    display: flex;
    flex-flow: row nowrap;
    justify-content: space-around;
    .notification {
        flex-basis: 100%;
    }
    .profile {
        flex-basis: 100%;
    }
}
</style>