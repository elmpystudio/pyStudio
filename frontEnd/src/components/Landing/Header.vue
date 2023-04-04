<template>
    <div class="header-container">
        <div class="header-content">
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
.header-container {
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.2);

    .header-content {
        width: 100%;
        height: 100%;
        padding: 5px 70px;

        display: flex;
        flex-flow: row nowrap;
        justify-content: space-between;
        align-items: center;

        .logo {
            img {
                width: 70px;
            }
        }

        .buttons-container {
            .button {
                padding: 6px 10px;
                // background: #384352;
                color: white;
                font-size: 16px;
                transition: all 300ms;
                text-decoration: none;

                &:hover {
                    opacity: 0.8;
                }
            }
        }
    }
}
</style>