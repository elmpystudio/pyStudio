<template>
    <div class="profile">
        <div class="content">
            <img class="avatar" :src="avatar" alt="avatar" />
            <div class="profile-content">
                <!-- <div class="profile-card">
                    <div class="profile-card--header">
                        <h1 class="title">
                            <i class="mr-2 fa fa-code" aria-hidden="true"></i>
                            Jypyter Notebook
                        </h1>
                    </div>

                    <div class="profile-card--row">
                        <div class="name">jhub_token</div>
                        <div class="value">{{jhub_token }}</div>
                    </div>
                </div> -->

                <div class="profile-card">
                    <div class="profile-card--header">
                        <h1 class="title">
                            <v-icon class="mr-2">mdi-account</v-icon>
                            Personal information
                        </h1>
                        <div class="edit">
                            <v-icon size="18" class="mx-1">mdi-pencil</v-icon>
                            <span class="text">Edit</span>
                        </div>
                    </div>

                    <v-divider></v-divider>

                    <div class="profile-card--row">
                        <div class="name">Full Name</div>
                        <div class="value">{{ fullName }}</div>
                    </div>

                    <v-divider></v-divider>

                    <div class="profile-card--row">
                        <div class="name">Job Title</div>
                        <div class="value">{{ jobTitle }}</div>
                    </div>

                    <v-divider></v-divider>

                    <div class="profile-card--row">
                        <div class="name">Email address</div>
                        <div class="value">{{ email }}</div>
                    </div>

                    <v-divider></v-divider>

                    <div class="profile-card--row">
                        <div class="name">About</div>
                        <div class="value">
                            {{ about }}
                        </div>
                    </div>

                    <v-divider></v-divider>

                    <!-- <div class="profile-card--row">
                        <div class="name">Skills</div>
                        <div class="value">
                            <div class="tag" v-for="(val, index) in skills" :key="index">
                                {{val}}
                            </div>
                        </div>
                    </div> -->
                </div>

                <div class="profile-card">
                    <div class="profile-card--header">
                        <h1 class="title">
                            <v-icon class="mr-2">mdi-lock</v-icon>
                            Password
                        </h1>
                        <div class="edit">
                            <v-icon size="18" class="mx-1">mdi-pencil</v-icon>
                            <span class="text">Edit</span>
                        </div>
                    </div>

                    <v-divider></v-divider>

                    <div class="profile-card--row">
                        <div class="name">Password</div>
                        <div class="value justify-space-between">
                            <span>*********</span>
                            <span>Last change: 16.02.2019</span>
                        </div>
                    </div>
                </div>

                <!-- <div class="profile-card">
                    <div class="profile-card--header">
                        <h1 class="title">
                            <v-icon class="mr-2">mdi-bell</v-icon>
                            Notifications
                        </h1>
                        <div class="edit">
                            <v-icon size="18" class="mx-1">mdi-pencil</v-icon>
                            <span class="text">Edit</span>
                        </div>
                    </div>

                    <v-divider></v-divider>

                    <div class="profile-card--row">
                        <div class="name">Subscribed items updates</div>
                        <div class="value justify-end">
                            <v-switch hide-details v-model="itemsUpdate" class="ma-0"
                                :label="itemsUpdate ? 'On' : 'Off'">
                            </v-switch>
                        </div>
                    </div>

                    <v-divider></v-divider>

                    <div class="profile-card--row">
                        <div class="name">Subscription notifications</div>
                        <div class="value justify-end">
                            <v-switch hide-details v-model="subscriptionNotifications" class="ma-0"
                                :label="subscriptionNotifications ? 'On' : 'Off'"></v-switch>
                        </div>
                    </div>

                    <v-divider></v-divider>

                    <div class="profile-card--row">
                        <div class="name">Project notifications</div>
                        <div class="value justify-end">
                            <v-switch hide-details v-model="projectNotifications" class="ma-0"
                                :label="projectNotifications ? 'On' : 'Off'"></v-switch>
                        </div>
                    </div>

                    <v-divider></v-divider>

                    <div class="profile-card--row">
                        <div class="name">Email notifications</div>
                        <div class="value justify-end">
                            <v-switch hide-details v-model="emailNotifications" class="ma-0"
                                :label="emailNotifications ? 'On' : 'Off'"></v-switch>
                        </div>
                    </div>
                </div> -->
            </div>
        </div>
    </div>
</template>

<script>
import { mapState, mapGetters } from "vuex";

export default {
    name: "Profile",
    props: {
        fullName: { type: String, required: true },
        jobTitle: { type: String, required: false },
        email: { type: String, required: true },
        about: { type: String, required: false },
        //skills: { type: Array, required: true },
        avatar: { type: String, required: false },
        jhub_token: { type: String, required: false }
    },

    data() {
        return {
            itemsUpdate: true,
            subscriptionNotifications: true,
            projectNotifications: false,
            emailNotifications: false,
        };
    },
    computed: {
        ...mapGetters(["totalActiveNotifications"]),
        ...mapState(["notifications"]),
    },

    methods: {
        update(div) {
            if(div === "jupyter")
                this.$emit("jupyterClick", {
                    "jhub_token": this.jhub_token
                });
        }
    }
};
</script>

<style lang="scss" scoped>
.content {
    padding: 30px;
    display: flex;

    .avatar {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        box-shadow: 0 2px 10px 0 #dce2e8;
        object-fit: cover;
    }

    .profile-content {
        padding: 0 30px;

        .profile-card {
            border-radius: 4px;
            box-shadow: 0 13px 12px 0 #eaedf4;
            background-color: #ffffff;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 0 20px;
            margin-bottom: 30px;
            width: 768px;

            &--header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                color: #0a1448;
                padding: 20px 0;

                .title {
                    font-size: 20px;
                    font-weight: 500;
                    display: flex;
                    align-items: center;
                }

                .edit {
                    display: flex;
                    align-items: center;
                    cursor: pointer;
                    font-size: 14px;

                    .text {
                        font-weight: bold;
                    }
                }
            }

            &--row {
                display: flex;
                padding: 20px 0;
                font-size: 14px;

                .name {
                    color: #0a1448;
                    font-weight: bold;
                    min-width: 150px;
                }

                .value {
                    display: flex;
                    flex: 1;

                    .tag {
                        color: #38406a;
                        background-color: #f4f6fa;
                        padding: 6px;
                        border-radius: 5px;
                        margin-right: 10px;
                        text-transform: capitalize;
                    }
                }
            }
        }
    }
}
</style>
