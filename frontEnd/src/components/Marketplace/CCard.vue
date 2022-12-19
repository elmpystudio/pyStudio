<template>
    <v-container class="d-flex justify-content-center">
        <v-card class="d-flex flex-column justify-content-between" height="100%" width="100%" max-width="250"
            min-height="350" elevation="3" :ripple="false">

            <!--Herader-->
            <div class="grey lighten-3">
                <v-card-text style="font-size: 20px">
                    {{ name }}
                </v-card-text>
            </div>

            <!--Body-->
            <div class="align-center flex-grow-1 py-2">
                <p class="description">
                    {{ description }}
                </p>
            </div>

            <!--Footer-->
            <div class="py-3 grey lighten-3">

                <div class="d-flex justify-content-around ">
                    <v-chip label outlined class="primary--text">{{ date }}</v-chip>
                    <v-chip label outlined>
                        <v-rating :value="rate" color="primary" dense half-increments readonly size="16">
                        </v-rating>
                    </v-chip>
                </div>

                <div class="pt-2">
                    <v-btn v-if="is_public" @click="onClick({ type: 'download', id })" color="primary"
                        style="width: 100px; height: 30px; font-size:12px" elevation="1">Download</v-btn>
                    <v-btn v-else @click="onClick({ type: 'request', id })" color="primary"
                        style="width: 120px; height: 30px; font-size:12px" elevation="1">Send Request</v-btn>
                </div>
            </div>
        </v-card>
    </v-container>
</template>

<script>
export default {
    name: "CCard",

    props: {
        id: { type: Number, required: true },
        // type: { type: String, required: true },
        name: { type: String, required: true },
        description: { type: String, required: true },
        // tags: { type: Array, required: true },
        date: { type: String, required: true },
        rate: { type: Number, required: true },
        is_public: { type: Boolean, default: false },
        to: { type: String, required: true },
    },

    methods: {
        onClick(data) {
            this.$emit('action', data)
        },
    }
}
</script>

<style scoped lang="scss">
a {
    text-decoration: none;

    transition: all 300ms;

    &:hover {
        opacity: 0.9;
    }
}

.type {
    position: absolute;
    text-align: center;
    font-size: 14px;
    top: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.description {
    font-size: 14px;
    padding: 0 12px;

    letter-spacing: 1px;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 4;
    line-clamp: 2;
    -webkit-box-orient: vertical;
}
</style>