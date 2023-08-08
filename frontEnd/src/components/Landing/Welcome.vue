<template>
    <div class="welcome-container">
        <div class="welcome-content">
            <div class="mytitle">
                <div class="welcome-text">Welcome to PyStudio</div>
                Get the max of your data with the easiest way to do machine learning without coding!
            </div>

            <div class="message">
                We provide most of the tools that data scientists need to carry out their tasks.
            </div>

            <div class="buttons-container">
                <a href="https://github.com/elmpystudio/pyStudio" target="_blank" class="button">
                    Vist us on <p class="headlink github">GitHub</p>
                </a>

                <a href="https://twitter.com/elmPyStudio" target="_blank" class="button">
                    Follow us on <p class="headlink x">X</p>
                </a>

                <a href="https://www.reddit.com/r/pyStudio" target="_blank" class="button">
                    Join us on <p class="headlink reddit">Reddit</p>
                </a>

                <a href="https://pystudio-workspace.slack.com/join/shared_invite/zt-1xi5r2uo4-aGSvV4gxxM68HM_FmWOVQg#/shared-invite/email" target="_blank" class="button">
                    Talk on <p class="headlink slack">Slack</p>
                </a>
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
.welcome-container {
    width: 100%;
    height: 100%;
    padding: 50px 150px;

    background-color: rgba(0, 0, 0, 0.2);


    .welcome-content {
        width: 100%;
        height: 100%;
        display: flex;
        flex-flow: column nowrap;
        justify-content: center;

        .mytitle {
            color: rgba(255, 255, 255, 0.8);
            font-size: 40px;
            text-align: center;

            @media screen and (max-width: 1280px) {
                font-size: 30px;
            }

            .welcome-text {
                color: white;
            }
        }

        .message {
            color: rgba(255, 255, 255, 0.8);
            font-size: 30px;
            text-align: center;
            margin-top: 20px;

            @media screen and (max-width: 1280px) {
                font-size: 20px;
            }
        }

        .buttons-container {
            padding-top: 10px;
            display: flex;
            flex-wrap: row nowrap;
            justify-content: space-around;

            .button {
                color: white;
                font-size: 20px;
                text-decoration: none;
                border-bottom: 2px solid white;
                transition: all 300ms;

                .headlink {
                    display: inline;
                    font-weight: bold;
                    
                    &.github {
                        color: #0D2636;
                    }

                    &.x {
                        color: black;
                    }

                    &.reddit {
                        color: #FF4500;
                    }

                    &.slack {
                        color: #ECB22E;
                    }
                }

                &:hover {
                    opacity: 0.8;
                    border-color: rgb(218, 218, 218);
                }
            }
        }
    }
}
</style>
