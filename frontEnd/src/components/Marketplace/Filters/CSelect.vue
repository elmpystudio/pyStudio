<template>
    <v-select v-if="items.length !== 0" v-model="value" :items="items" :label="name" multiple @change="update" :disabled="isDisable">
        <template v-slot:selection="{ item, index }">
            <v-chip v-if="index === 0" style="height: 20px">
                <span style="font-size: 13px;">{{ item }}</span>
            </v-chip>
            <span v-if="index === 1" class="grey--text text-caption">
            (+{{ value.length - 1 }} others)
            </span>
        </template>
    </v-select>
</template>

<script>
export default {
    name: "CSelect",
    props: {
        name: { type: String, required: true },
        items: { type: Array, required: true },
        isDisable: { type: Boolean, default: false }
    },

    data() {
        return {
            value: []
        }
    },

    methods: {
        //emits
        update(value) {
            this.$emit("onUpdate", {
                name: this.name.replace(' ', '_').toLowerCase(),
                value: value.map(element => {
                    return element.toLowerCase();
                })
            });
        }
    }
}
</script>

<style scoped>
input {
    border: 1;
}
</style>