<template>
    <div class="content">
        <div class="notebook" id="notebook">
            <!-- Loader -->
            <CLoader v-if="isLoading" id="loader" />
            <iframe v-else name="myFrame" :src="url + jhub_token"></iframe>
        </div>
    </div>
</template>

<script>
import { getUser } from "@/api_client.js";
import CLoader from "@/components/CLoader.vue";
// import $ from "jquery";

export default {
    name: "NotebookViwe",
    components: {
        CLoader,
    },

    data: () => ({
        isLoading: true,

        url: "http://localhost:8000/api/jupyterhub/start/?token=",
        jhub_token: "",
    }),

    mounted() {
        if (this.isLoading) this.getData();
    },

    methods: {
        getData() {
            getUser()
                .then(({ status, data }) => {
                    if (status === 200) {
                        if (data.jhub_token !== null)
                            this.jhub_token = data.jhub_token;
                        this.isLoading = false;
                    }
                })
                .catch(() => {
                    console.error("Invalid credential");
                });
        },
    },
};
</script>

<style scoped lang="scss">
.content {
    width: 100%;
    height: 100%;
    position: relative;

    .notebook {
        > #loader {
            background-color: rgb(242 242 242);
        }
    }

    iframe {
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        z-index: 1001;
    }
}
</style>