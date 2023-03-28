<template>
    <div class="mycontainer">
        <div class="mycontent">
            <div class="logo">
                <img src="@/assets/logo_no_background.png" />
            </div>

            <!-- <div class="links">
                link_1, link_2, link_3, link_4
            </div> -->

            <div class="buttons-container">
                <a href="#login-section" class="button">Login/Register</a>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: "Header",

};
</script>

<style lang="scss" scoped>
.mycontainer {
    width: 100%;
    height: 100%;
    background-color: white;

    .mycontent {
        width: 100%;
        height: 100%;
        padding: 0 50px;

        display: flex;
        flex-flow: row nowrap;
        justify-content: space-between;
        align-items: center;

        .logo {
            img {
                width: 60px;
            }
        }

        .buttons-container {
            .button {
                padding: 6px 10px;
                background: #384352;
                color: white;
                font-size: 14px;
                transition: all 300ms;

                &:hover {
                    opacity: 0.8;
                }
            }
        }
    }
}
</style>