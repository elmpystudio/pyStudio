<template>
    <div class="mycontent">
        <router-link class="profile" :to="{ name: 'profile' }">
            {{ username }}
        </router-link>
        <div class="logout" @click="handleLogout">Logout</div>

        <iframe
            v-if="clicked"
            :src="`http://localhost:9000/user/${username}/logout`"
            @load="load_handler"
            hidden
        ></iframe>
    </div>
</template>

<script>
import { clearToken } from "@/helpers";

export default {
    name: "Profile",
    data() {
        return {
            clicked: false,
            username: localStorage.getItem("username"),
        };
    },

    methods: {
        load_handler() {
            this.$router.push({ name: "login" });
            clearToken();
            this.clicked = false;
        },
        handleLogout() {
            this.clicked = true;
        },
    },
};
</script>

<style scoped lang="scss">
.mycontent {
    width: 100%;
    height: 100%;
    display: flex;
    flex-flow: row nowrap;
    column-gap: 15px;

    .profile {
        color: grey;
        text-decoration: none;
        transition: all 500ms;

        &:hover {
            color: black;
        }
    }

    .logout {
        color: red;
        transition: all 500ms;

        &:hover {
            cursor: pointer;
            opacity: 0.5;
        }
    }
}
</style>