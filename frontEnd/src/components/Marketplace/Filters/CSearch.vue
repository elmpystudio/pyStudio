<template>
    <div>
        <SearchIcon class="search-icon"/>
        <input type="search" class="search" v-model="search" placeholder="Search for items" @input="update"/>
    </div>
</template>

<script>
import SearchIcon from '@/assets/icons/search.svg';

export default {
    name: "CSearch",
    components: {
        SearchIcon
    },

    data() {
        return{
            search: ''
        }
    },

    methods: {
        //emits
        update(event){
            this.$emit("onUpdate", event.target.value);
        }
    }
}
</script>

<style scoped>
.search-icon {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    left: 25px;
}

.search {
    background-color: #ffffff;
    box-sizing: border-box;
    height: 42px;
    outline: none;
    padding: 18px 18px 18px 30px;
    border-radius: 10px;
    border: solid 1px #dee3ed;
    font-size: 16px;
    width: 100%;
}

.search:hover {
    border-color: #1976d2;
}
</style>