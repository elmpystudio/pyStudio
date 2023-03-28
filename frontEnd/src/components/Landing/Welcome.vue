<template>
    <div class="mycontainer">
        <div class="mycontent">
            <div class="mytitle">
                Get the max of your data with the easiest way to do machine learning without coding!
            </div>

            <div class="message">
                We provide most of the tools that data scientists need to carry out their tasks.
            </div>

            <div class="buttons-container">
                <a href="https://github.com/elmpystudio/pyStudio" target="_blank" class="button">Vist our project in Github</a>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: "Welcome",
};
</script>

<style lang="scss" scoped>
.mycontainer {
    width: 100%;
    height: 100%;
    background: rgb(56, 67, 82);
    background: linear-gradient(306deg, rgba(56, 67, 82, 1) 0%, rgba(106, 44, 145, 1) 50%, rgba(15, 108, 182, 1) 100%);

    .mycontent {
        width: 100%;
        height: 100%;
        padding: 0 100px;
        display: flex;
        flex-flow: column nowrap;
        justify-content: center;

        .mytitle {
            color: white;
            font-size: 50px;
            text-align: center;
        }

        .message {
            color: white;
            font-size: 30px;
            text-align: center;
        }

        .buttons-container {
            padding-top: 10px;
            .button {
                color: rgb(199, 199, 199);
                font-size: 20px;
                text-decoration: underline;
                transition: all 300ms;

                &:hover {
                    opacity: 0.8;
                }
            }
        }
    }
}
</style>