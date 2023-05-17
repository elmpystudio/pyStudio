<template>
    <div class="api_info-container">
        <div class="api_info-container__header">
            <div class="title-container">
                <div class="title">API Information</div>
            </div>
        </div>

        <div class="api_info-container__body">
            <div class="inrow">
                <div class="data-form">
                    <div class="name">Name:</div>
                    <div class="value">
                        {{ ml_model.name }}
                    </div>
                </div>
            </div>

            <div class="inrow">
                <div class="data-form">
                    <div class="name">Model Name:</div>
                    <div class="value">
                        {{ ml_model.model_name }}
                    </div>
                </div>
                <div class="data-form">
                    <div class="name">Version:</div>
                    <div class="value">
                        {{ ml_model.version }}
                    </div>
                </div>
            </div>

            <div class="inrow">
                <div class="data-form">
                    <div class="name">Access URL</div>
                    <div class="value">
                        {{ `${access_url}/api/ml_models/run` }}
                    </div>
                </div>
            </div>

            <div class="inrow">
                <div class="data-form">
                    <div class="name">Description:</div>
                    <div class="value">
                        {{ ml_model.description }}
                    </div>
                </div>
            </div>


            <!-- eval_metrics -->
            <div class="inrow">
                <div class="data-form" v-for="(eval_metric, index) in ml_model.eval_metrics" :key="index">
                    <div class="name">
                        {{ eval_metric.name }}:
                    </div>
                    <div class="value">
                        {{ eval_metric.value }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { API_URL } from "@/api_client.js";
export default {
    name: "API_info",
    props: {
        ml_model: { type: Object, required: true },
    },
    data() {
        return {
            access_url: API_URL,
        }
    }
}
</script>

<style lang="scss" scoped>
.api_info-container {
    width: 100%;
    height: 450px;

    border: 2px solid #2b468b;
    border-radius: 5px;

    display: flex;
    flex-flow: column nowrap;

    &__header {
        width: 100%;
        display: flex;
        flex-flow: row nowrap;
        justify-content: start;

        .title-container {
            background-color: #2b468b;
            width: 150px;
            border-radius: 0 0 10px 0;

            .title {
                color: white;
                padding: 0 5px;
                text-align: center;
                font-size: 16px !important;
            }
        }
    }

    &__body {
        padding: 20px;
        width: 100%;
        height: 100%;
        display: flex;
        flex-flow: column nowrap;
        row-gap: 20px;

        .inrow {
            width: 100%;
            display: flex;
            flex-flow: row nowrap;
            justify-content: space-around;
            column-gap: 20px;

            .data-form {
                width: 100%;

                .name {
                    font-size: 18px;
                    text-align: start;
                    font-weight: bold;
                }

                .value {
                    font-size: 18px;
                    text-align: start;
                    border-bottom: 2px solid #858ba0;
                    color: #2b468b;
                }
            }
        }
    }
}
</style>