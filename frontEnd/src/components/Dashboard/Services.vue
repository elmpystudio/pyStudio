<template>
    <div class="contant">
        <div class="search-container">
            <SearchIcon class="search-icon" />
            <input type="search" class="search" v-model="search" placeholder="Search for services" />
        </div>
        <v-data-table :headers="headers" :items="data" class="elevation-1" :search="search" :loading="isLoading"
            show-select v-model="selected" @click:row="handle_click">

            <template v-slot:footer>
                <div class="actions-container">
                    <button @click="delete_action">Delete</button>
                </div>
            </template>
        </v-data-table>


        <div class="body" v-if="isActive">
            <div class="header">
                <div class="back-icon" @click="isActive = false">
                    <i class="fa fa-arrow-left" aria-hidden="true"></i>
                </div>
            </div>

            <div class="content">
                <div class="main-row">
                    <!-- Api Information -->
                    <div class="main-row_col">
                        <div class="container">
                            <div class="title-container">
                                <div class="title">API Information</div>
                            </div>

                            <div class="api">
                                <div class="api_container" v-if="service.columns.length > 0">
                                    <div class="api_container_form">
                                        <div class="name">Name:</div>
                                        <div class="value">
                                            {{ service.name }}
                                        </div>
                                    </div>

                                    <div class="api_container_form">
                                        <div class="name">Model Name:</div>
                                        <div class="value">
                                            {{ service.model_name }}
                                        </div>
                                    </div>
                                    <div class="api_container_form full">
                                        <div class="name">Access URL</div>
                                        <div class="value">
                                            {{ `${access_url}/api/services/run` }}
                                        </div>
                                    </div>

                                    <div class="api_container_form">
                                        <div class="name">Version:</div>
                                        <div class="value">
                                            {{ service.version }}
                                        </div>
                                    </div>

                                    <div class="api_container_form full">
                                        <div class="name">Description:</div>
                                        <div class="value">
                                            {{ service.description }}
                                        </div>
                                    </div>

                                    <!-- eval_metrics -->
                                    <div class="api_container_form" v-for="(
                                            eval_metric, index
                                        ) in service.eval_metrics" :key="index">
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
                    </div>

                    <!-- Online Interaction -->
                    <div class="main-row_col">
                        <div class="container">
                            <div class="title-container">
                                <div class="title">Online Interaction</div>
                            </div>

                            <div class="columns">
                                <div class="columns_container scroll">
                                    <div class="columns_container_column" v-for="(
                                            column, index
                                        ) in filtered_columns(service.columns)" :key="index">
                                        <div v-if="
                                            column.hasOwnProperty('values')
                                        ">
                                            <div class="name">
                                                {{ column.name }}
                                            </div>

                                            <div class="value">
                                                <v-select :label="column.name" :item-color="'#2b468b'"
                                                    :color="'#2b468b'" :items="
                                                        Object.keys(
                                                            column.values
                                                        )
                                                    " outlined dense v-model="column.value"></v-select>
                                            </div>
                                        </div>

                                        <div v-else>
                                            <div class="name">
                                                {{ column.name }}
                                            </div>

                                            <input type="text" v-model="column.value" placeholder="Number" />
                                        </div>
                                    </div>
                                </div>

                                <div class="submit">
                                    <button class="btn btn-primary" id="deploy_post" @click="handle_submit">
                                        <v-progress-circular v-if="submit.isLoading" class="spin" indeterminate
                                            color="white"></v-progress-circular>
                                        Send
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <CModal :title="'response'" :active="modal_toggle" @close="modal_toggle = false">
            <template #default>
                <div class="modal-container">
                    <div class="status">
                        <i class="fa fa-check-circle" aria-hidden="true"></i>
                    </div>
                    <div class="content">
                        <div class="message-container">
                            <div class="message">{{ submit.response }}</div>
                        </div>
                    </div>
                </div>
            </template>
        </CModal>
    </div>
</template>

<script>
import CModal from "@/components/CModal.vue";
import SearchIcon from "@/assets/icons/search.svg";
import { get_services, post_service, delete_service, API_URL } from "@/api_client.js";

export default {
    name: "",
    components: {
        CModal,
        SearchIcon,
    },
    data() {
        return {
            headers: [
                { text: "Name", value: "name" },
                { text: "Description", value: "description" },
            ],
            search: "",
            selected: [],
            isLoading: false,
            isActive: false,
            access_url: API_URL,

            data: [],
            service: {},
            modal_toggle: false,

            submit: {
                response: "",
                isLoading: false,
            },
        };
    },

    mounted() {
        this.fetch_services();
    },

    methods: {
        fetch_services() {
            get_services()
                .then(({ status, data }) => {
                    if (status === 200) {
                        // convert [columns] string to json object
                        data.forEach((service) => {
                            service.columns = JSON.parse(service.columns);
                            // service.eval_metrics = JSON.parse(service.eval_metrics)

                            // eval_metrics
                            if (service.eval_metrics !== null) {
                                let tmp = JSON.parse(service.eval_metrics);
                                if (tmp.model_type === "classification")
                                    service.eval_metrics = [
                                        {
                                            name: "Accuracy Score",
                                            value: tmp.accuracy_score,
                                        },
                                        {
                                            name: "Precision Score",
                                            value: tmp.precision_score,
                                        },
                                        {
                                            name: "Recall Score",
                                            value: tmp.recall_score[0],
                                        },
                                        {
                                            name: "F1 Score",
                                            value: tmp.f1_score[0],
                                        },
                                    ];
                                else if (tmp.model_type === "regression")
                                    service.eval_metrics = [
                                        {
                                            name: "Mean Absolute Error",
                                            value: tmp.mean_absolute_error,
                                        },
                                        {
                                            name: "Mean Squared",
                                            value: tmp.mean_squared_error,
                                        },
                                        {
                                            name: "R2 Score",
                                            value: tmp.r2_score,
                                        },
                                    ];
                            }
                        });
                        this.data = data;
                        this.isLoading = true;
                    }
                })
                .catch(() => {
                    console.error("service call");
                })
                .finally(() => {
                    this.isLoading = false;
                });
        },
        handle_click(event) {
            this.data.forEach((service) => {
                if (service.name === event.name) this.service = service;
            });
            this.isActive = true;
        },

        handle_submit() {
            this.submit.isLoading = true;
            const payload = {
                model_name: this.service.model_name,
                username: this.service.username,
                columns: {},
            };
            let run_model = null;

            this.service.columns.forEach((column) => {
                if (column.hasOwnProperty("run_model"))
                    run_model = column;
                else {
                    if (column.hasOwnProperty("values"))
                        payload.columns[column.name] = parseInt(
                            column.values[column.value]
                        );
                    else payload.columns[column.name] = parseInt(column.value);
                }
            });

            post_service(payload)
                .then(({ status, data }) => {
                    if (status === 200) {
                        data = JSON.parse(data);
                        if (data.hasOwnProperty("classification"))
                            this.submit.response = run_model.name + " = " + this.get_key(run_model, JSON.parse(data.classification)[0]);
                        else if (data.hasOwnProperty("result"))
                            this.submit.response = "Result = " + JSON.parse(data.result)[0];
                        else
                            this.submit.response = JSON.stringify(data);
                    }
                })
                .catch((error) => {
                    this.submit.response = error;
                })
                .finally(() => {
                    this.modal_toggle = true;
                    this.submit.isLoading = false;
                });
        },

        filtered_columns(columns) {
            const new_columns = [];
            for (let index = 0; index < columns.length; index++) {
                if (columns[index].hasOwnProperty("run_model"))
                    continue;
                new_columns.push(columns[index]);
            }

            return new_columns;
        },
        get_key(column, value) {
            let found_key = null;
            Object.keys(column.values).forEach((key) => {
                if (column.values[key] == value)
                    found_key = key;
            });
            return found_key;
        },

        delete_action() {
            this.selected.forEach(service => {
                delete_service(service.id);
                // update data
                this.data = this.data.filter(this_service => {
                    return this_service.id != service.id
                });
            });
        },
    },
};
</script>

<style lang="scss" scoped>
.content {
    width: 100%;
    height: 100vh;

    position: relative;

    .search-container {
        display: flex;
        position: relative;

        margin-bottom: 10px;

        .search-icon {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            left: 10px;
        }

        .search {
            background-color: #ffffff;
            box-sizing: border-box;
            height: 42px;
            outline: none;
            padding: 18px 18px 18px 30px;
            border-radius: 4px;
            border: solid 1px #dee3ed;
            color: #858ba0;
            font-size: 14px;
            width: 100%;
        }
    }

    .body {
        width: 100%;
        height: 100%;
        position: absolute;
        top: 0;
        left: 0;

        background: #fff;

        .back-icon {
            width: 22px;
            height: 22px;
            position: absolute;
            z-index: 1;

            transition: all 300ms;

            &:hover {
                cursor: pointer;
                opacity: 0.8;
            }

            i {
                color: #2b468b;
                font-size: 22px;
            }
        }

        .content {
            width: 100%;
            height: 100%;

            padding: 30px;

            position: absolute;
            top: 0;
            left: 0;

            overflow: scroll;

            .main-row {
                width: 100%;
                height: 80vh;

                display: flex;
                flex-flow: row nowrap;
                column-gap: 10px;

                &_col {
                    flex: 1 1 100%;
                    margin-bottom: 6px;
                    padding: 10px;
                    display: flex;
                    flex-flow: column nowrap;

                    .container {
                        flex: 1 1 100%;

                        background: rgb(247 247 247);
                        border: 2px solid #2b468b;
                        border-radius: 5px;

                        position: relative;

                        .title-container {
                            position: absolute;
                            top: 0;
                            left: 0;

                            width: 150px;

                            background: #2b468b;

                            border-bottom-right-radius: 5px;

                            .title {
                                color: #fff;
                                padding: 0 5 px;
                                text-align: center;
                                font-size: 16px !important;
                            }
                        }
                    }
                }
            }

            .api {
                margin-top: 35px;
                padding: 0 10px;

                &_container {
                    height: 100%;
                    width: 100%;

                    display: flex;
                    flex-flow: row wrap;
                    gap: 20px;

                    &_form {
                        flex: 1 1 35%;

                        &.full {
                            flex: 1 1 100%;
                        }
                    }
                }

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

            .columns {
                height: 100%;
                width: 100%;

                position: relative;

                &_container {
                    width: 100%;
                    height: 100%;

                    display: flex;
                    flex-flow: row wrap;
                    justify-content: space-around;
                    gap: 5px;

                    &.scroll {
                        position: absolute;
                        top: 40px;
                        left: 0;
                        height: calc(100% - 100px);
                        width: 100%;
                        overflow-y: scroll;
                        overflow-x: hidden;
                        // background: #0000000a;
                        overflow-y: scroll;

                        /* width */
                        &::-webkit-scrollbar {
                            width: 10px;
                        }

                        /* Track */
                        &::-webkit-scrollbar-track {
                            // background: #0000000a;
                        }

                        /* Handle */
                        &::-webkit-scrollbar-thumb {
                            background: #2b468b;
                            border-radius: 5px;
                        }

                        /* Handle on hover */
                        &::-webkit-scrollbar-thumb:hover {
                            background: #2b468bb0;
                        }
                    }

                    &_column {
                        border: 2px solid #2b468b;
                        padding: 10px;
                        border-radius: 5px;
                        // max-width: 500px;
                        width: 45%;
                    }
                }

                .name {
                    font-size: 16px !important;
                    font-weight: bold;
                    text-align: center;
                    text-transform: uppercase;
                }

                .v-select {
                    background: white;
                }

                input {
                    width: 100%;
                    padding: 5px;
                    font-size: 17px;
                    box-sizing: border-box;
                    background: white;

                    border: 1px solid #2b468b;
                    border-radius: 3px;
                    text-align: center;
                    opacity: 0.8;

                    transition: all 300ms;

                    &:focus {
                        outline: none;
                        opacity: 1;
                    }
                }

                .submit {
                    position: absolute;
                    bottom: 5px;

                    width: 100%;
                    height: auto;
                    overflow: hidden;
                    padding: 0 50px;

                    .btn {
                        width: 100%;
                        height: 45px;
                        background: #2b468b;
                        position: relative;
                        border: 0;
                        transition: all 300ms;

                        &:hover {
                            opacity: 0.9;
                        }

                        .spin {
                            position: absolute;
                            top: 50%;
                            left: 10%;
                            transform: translate(-50%, -50%);

                            width: 100%;
                            height: 100%;
                        }
                    }
                }
            }
        }
    }

    .actions-container {
        width: 100%;
        height: 100%;
        padding-top: 20px;
        padding-left: 15px;

        display: flex;
        flex-flow: row nowrap;
        justify-content: flex-start;
        align-items: center;

        >button {
            width: 75px;
            height: 30px;
            background-color: red;
            border-radius: 5px;
            transition: all 300ms;
            color: white;
            font-size: 15px;

            &:hover {
                opacity: 0.8;
            }
        }
    }

    .modal-container {
        height: 100%;
        width: 100%;

        .status {
            flex: 1 1 10%;

            >i {
                font-size: 60px;
                color: green;
            }
        }

        .content {
            flex: 1 1 90%;
            position: relative;

            .message-container {
                position: absolute;
                top: 0;
                left: 0;
                height: 100%;
                width: 100%;
                overflow-y: scroll;
                overflow-x: hidden;

                // /* width */
                &::-webkit-scrollbar {
                    width: 8px;
                }

                /* Track */
                &::-webkit-scrollbar-track {
                    // background: #0000000a;
                }

                /* Handle */
                &::-webkit-scrollbar-thumb {
                    background: #2b468b;
                    border-radius: 5px;
                }

                /* Handle on hover */
                &::-webkit-scrollbar-thumb:hover {
                    background: #2b468bb0;
                }

                .message {
                    height: 100%;
                    width: 100%;

                    padding: 5px 20px;
                    font-size: 20px;
                    word-break: break-all;

                }
            }
        }
    }
}
</style>

<style>
.theme--light.v-data-table .v-data-footer {
    border-top: none;
}

/* v-select override */
.v-text-field.v-text-field--enclosed:not(.v-text-field--rounded)>.v-input__control>.v-input__slot,
.v-text-field.v-text-field--enclosed .v-text-field__details {
    margin: 0 !important;
}

.v-messages {
    min-height: 0 !important;
}

.v-text-field__details {
    min-height: 0 !important;
}
</style>