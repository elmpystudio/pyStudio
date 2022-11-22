<template>
    <v-container class="d-flex justify-content-center">
       <v-card class="d-flex flex-column justify-content-between" height="100%" width="100%" max-width="300" min-height="400" elevation="5" :to="to" :ripple="false">

             <!--Herader-->
            <div class="grey lighten-3">
                 <v-card-text class="type">
                    {{ type }}
                </v-card-text>

                <div class="pa-2 d-flex flex-column align-start">
                        <img src="@/assets/elm.png" alt="logo" width="50" class="rounded-pill"/>
                        <span class="pl-3 caption">ELM</span>
                </div>
            </div>

            <!--Body-1-->
            <div class="d-flex flex-column align-center flex-grow-1">
                <v-card-title>
                    {{ title }}
                </v-card-title>
                <p class="description">
                    {{ description }}
                </p>
            </div>

            <!--Body-2-->
            <div class="py-4 d-flex justify-content-around">
                <v-chip v-for="(tag, index) in tags" :key="index">
                    {{ tag.name }}
                </v-chip>
            </div>

            <!--Footer-->
            <div class="py-5 grey lighten-3 d-flex justify-content-around">
               <v-chip label outlined class="primary--text">{{ date }}</v-chip>
                <v-chip label outlined>
                    <v-rating
                    :value="rate"
                    color="primary"
                    dense
                    half-increments
                    readonly
                    size="16">
                    </v-rating>
                </v-chip>
           </div>
       </v-card>
    </v-container>
</template>

<script>
export default {
    name: "CCard",

    props: {
        type: { type: String, required: true },
        title: { type: String, required: true },
        description: { type: String, required: true },
        tags: { type: Array, required: true },
        date: { type: String, required: true },
        rate: { type: Number, required: true },
        to: { type: String, required: true }
    }
}
</script>

<style scoped>
a {
    text-decoration: none;
}

a:hover {
    filter: brightness(95%);
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