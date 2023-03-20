<template>
    <div v-if="!isLoading">
        <Profile :fullName="fullName" :jobTitle="jobTitle" :email="email" :about="about" :skills="skills" :avatar="image" :jhub_token="jhub_token" @jupyterClick="jupyter_update"/>
    </div>
</template>

<script>
import Profile from '@/components/Profile';

import { API_URL, getUser, getUser_fake, updateUser } from "@/api_client.js";

export default {
    name: "ProfileView",
    data() {
        return {
            isLoading: true,

            fullName: null,
            jobTitle: null,
            email: null,
            about: null,
            skills: [],
            avatar: null,
            jhub_token: null
        }
    },
    components: {
        Profile,
    },

    mounted() {
        this.getData();
        this.getData_fake();
    },

    methods: {
        getData() {
            getUser().then(({ status, data }) => {
                if (status === 200) {
                    if(data.full_name !== null)
                        this.fullName = data.full_name;
                    else if(data.first_name !== "" || data.last_name !== "")
                        this.fullName = `${data.first_name} ${data.last_name}`
                    else if(data.username !== "")
                        this.fullName = data.username;

                    if(data.about !== null) 
                        this.about = data.about;

                    if(data.email !== null)
                            this.email = data.email;
                    
                    if(data.image !== null)
                        this.image = `${API_URL}${data.image}`;
                }

                this.isLoading = false;
            })
            .catch(() => {
                console.error("Invalid credential")
            });
        },

        getData_fake(){
            getUser_fake().then(({data}) => {
                let random = Math.floor(Math.random() * (data.length -1)) + 1;

                if(this.fullName === null)
                    this.fullName = data[random].name;
                
                if(this.jobTitle === null)
                    this.jobTitle = data[random].job_title;

                if(this.email === null)
                    this.email = data[random].email;

                if(this.about === null)
                    this.about = data[random].about;

                if(this.avatar === null)
                    this.avatar = `images/avatars/${data[random].avatar}.png`;

                if(this.skills.length === 0)
                    this.skills = data[random].skills;

                
                this.isLoading = false;
            })
            .catch(() => {
                console.error("File Not Exists")
            })
        },

        updateData(data){
            updateUser(data).then(({data}) => {
                console.log(data);
            }).catch(() => {
                console.error("Update Faild")
            })
        },
        
        //handle_clicks zone
        jupyter_update(data) {
            this.updateData(data)
        }
    }
}
</script>

<style scoped lang="scss">
</style>
