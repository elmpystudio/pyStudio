<template>
    <div class="content">
        <div class="notebook">
            <CLoader v-if="isLoading" id="loader" />
            <iframe v-else :src="url"></iframe>
        </div>
    </div>
</template>

<script>
import { jupyterhub_open, jupyterhub_sync } from "@/api_client.js";
import CLoader from "@/components/CLoader.vue";

export default {
    name: "NotebookViwe",
    components: {
        CLoader,
    },

    data: () => ({
        isLoading: true,
        url: "http://localhost:9000/hub/oauth_login?next=",
    }),

    mounted() {
        if (this.isLoading) this.open();
    },

    methods: {
        open() {
            jupyterhub_open()
                .then(({ status }) => {
                    if (status === 200) {
                        this.isLoading = false;
                        this.sync();
                    }
                })
        },
        sync() {
            jupyterhub_sync()
                .then(({ status }) => {
                    if (status !== 200)
                        setTimeout(() => {
                            this.sync();
                        }, 1000)
                })
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
        >#loader {
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