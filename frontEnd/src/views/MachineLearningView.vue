<template>
    <div class="ml-studio">
        <input id="current-user-id" type="hidden" value="5" />
        <div class="ml-studio--content">
            <div class="page-content">
                <!-- Loader -->
                <CLoader id="loader" style="display: none" />

                <!-- MenuBar -->
                <CMenuBar />

                <div class="jtk-bootstrap jtk-bootstrap-wide">
                    <div class="jtk-page-container">
                        <!-- ToolBar -->
                        <CToolBar />

                        <!-- WorkSpace -->
                        <CWorkSpace />

                        <!-- PropertiesBar -->
                        <CPropertiesBar />
                    </div>
                </div>
            </div>
        </div>

        <!-- COutput -->
        <COutput />

        <!-- CEvaluationMetrix -->
        <CEvaluationMetrix />

        <!-- CError -->
        <CMessage
            :id="'ml_error'"
            :title="'Response'"
            :type="'error'"
        />
    </div>
</template>

<script>
import CToolBar from "@/components/MachineLearning/CToolBar.vue";
import CMenuBar from "@/components/MachineLearning/CMenuBar.vue";
import CPropertiesBar from "@/components/MachineLearning/CPropertiesBar.vue";
import CWorkSpace from "@/components/MachineLearning/CWorkSpace.vue";
import COutput from "@/components/MachineLearning/COutput";
import CEvaluationMetrix from "@/components/MachineLearning/CEvaluationMetrix.vue";
import CMessage from "@/components/MachineLearning/CMessage.vue";
import CLoader from "@/components/CLoader.vue";

export default {
    name: "MachineLearning",
    components: {
        CToolBar,
        CMenuBar,
        CPropertiesBar,
        CWorkSpace,
        COutput,
        CEvaluationMetrix,
        CMessage,
        CLoader,
    },
};
</script>

<style lang="scss">
@import "src/assets/styles/sweetalert";

.sweet-alert {
    display: none;
}

.ml-studio {
    display: flex;
    position: relative;

    &--content {
        display: flex;
        width: 100%;
        min-width: 800px;

        .page-content {
            height: 1000vh;
            background: #e3e3e3;
            position: relative;

            .loader-overlay {
                margin: 0px;
                display: none;
                padding: 0px;
                position: absolute;
                right: 0px;
                top: 0px;
                width: 100%;
                height: 100%;
                background-color: rgb(255, 255, 255);
                z-index: 30001;
                opacity: 0.8;

                .ml-loader {
                    position: absolute;
                    color: White;
                    top: 50%;
                    left: 45%;
                    height: 50px;
                    width: auto;
                }
            }
        }
    }
}
</style>
