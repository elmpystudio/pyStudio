<template>
    <div class="loader-container">
        <div class="loader"></div>
    </div>
</template>

<script>
export default {
    name: "CLoader"
}
</script>

<style lang="scss" scoped>
.loader-container {
    background: rgba(0, 0, 0, 0.5);
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1000;
}

.loader {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 150px;
    height: 150px;
    margin: -75px 0 0 -75px;
    border-radius: 50%;
    border: 4px solid transparent;
    border-top-color: #2869b2;
    -webkit-animation: spin 1.5s linear infinite;
    animation: spin 1.5s linear infinite;

    z-index: 1001;
}

.loader:before {
    content: "";
    position: absolute;
    top: 5px;
    left: 5px;
    right: 5px;
    bottom: 5px;
    border-radius: 50%;
    border: 4px solid transparent;
    border-top-color: #8d288f;

    -webkit-animation: spin 2.5s linear infinite;
    animation: spin 2.5s linear infinite;
}

.loader:after {
    content: "";
    position: absolute;
    top: 15px;
    left: 15px;
    right: 15px;
    bottom: 15px;
    border-radius: 50%;
    border: 4px solid transparent;
    border-top-color: #1c1351;

    -webkit-animation: spin 1s linear infinite;
    animation: spin 1s linear infinite;
}

@-webkit-keyframes spin {
    0% {
        -webkit-transform: rotate(0deg);
        -ms-transform: rotate(0deg);
        transform: rotate(0deg);
    }
    100% {
        -webkit-transform: rotate(360deg);
        -ms-transform: rotate(360deg);
        transform: rotate(360deg);
    }
}
@keyframes spin {
    0% {
        -webkit-transform: rotate(0deg);
        -ms-transform: rotate(0deg);
        transform: rotate(0deg);
    }
    100% {
        -webkit-transform: rotate(360deg);
        -ms-transform: rotate(360deg);
        transform: rotate(360deg);
    }
}
</style>