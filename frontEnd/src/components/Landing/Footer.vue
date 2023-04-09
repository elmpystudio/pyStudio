<template>
    <div class="footer-container">
        <div class="fotter-content">
            <div class="message">
                This is a demo environment not an ELM production level application, please if you find any issues or you have suggestion feel free to add on GitHub <a target="_blank" href="https://github.com/elmpystudio/pyStudio/issues/new/choose">issues</a>.
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: "Footer",
};
</script>

<style lang="scss" scoped>
.footer-container {
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.2);

    .fotter-content {
        width: 100%;
        height: 100%;
        padding: 30px 100px;
        display: flex;
        flex-flow: column nowrap;
        justify-content: center;

        .message {
            color: rgba(255, 255, 255, 0.8);
            font-size: 20px;
            text-align: center;

            a {
                color: white;
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

