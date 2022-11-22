<template>
    <CModal :id="id" :size="'small'">
        <template v-slot:title>
            {{ title }}
        </template>
        
        <template v-slot:body>
            <div class="message-container">
                <div class="message">{{message}}</div>
            </div>
        </template>
    </CModal>
</template>

<script>
import CModal from "@/components/MachineLearning/CModal.vue";

export default {
    name: "CMessage",
    components: {
        CModal
    },

    props: {
        id: { type: String, required: true },
        type: { type: String, required: true },
        title: { type: String, required: true },
        message: { type: String, required: false }
    }
}
</script>

<style lang="scss" scoped>
.message-container {
    margin: 10px 20px;

    .message {
        padding-top: 25x;
        font-size: 25px;
    }
}
</style>