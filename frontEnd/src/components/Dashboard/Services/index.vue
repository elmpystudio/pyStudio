<template>
    <div class="contant">

        <!-- SEARCH -->
        <div class="search-container">
            <SearchIcon class="search-icon" />
            <input type="search" class="search" v-model="search" placeholder="Search for ml_models" />
        </div>

        <!-- Table -->
        <v-data-table :headers="headers" :items="data" class="elevation-1" :search="search" :loading="isLoading" show-select
            v-model="selected" @click:row="handle_click">
            <template v-slot:footer>
                <div class="actions-container">
                    <button @click="delete_action">Delete</button>
                </div>
            </template>
        </v-data-table>

        <!-- Details Page -->
        <DetailsPage :active="isActive" @close="isActive = false">
            <template #part1>
                <API_info :ml_model="ml_model" />
            </template>

            <template #part2>
                <Online_Interaction :ml_model="ml_model" @handle_run1="handle_run1" @handle_run2="handle_run2" />
            </template>
        </DetailsPage>

        <!-- run1 Modal -->
        <CModal :title="'response'" :active="run1.toggle" @close="run1.toggle = false">
            <template #default>
                <div class="modal-container">
                    <div class="status">
                        <i class="fa fa-check-circle" aria-hidden="true"></i>
                    </div>
                    <div class="message-content">
                        <div class="message-container">
                            <div class="message">{{ run1.response }}</div>
                        </div>
                    </div>
                </div>
            </template>
        </CModal>

        <!-- run2 Modal -->
        <CModal :title="'response'" :active="run2.toggle" @close="run2.toggle = false">
            <template #default>
                <div class="modal-container">
                    <div class="status">
                        <i class="fa fa-check-circle" aria-hidden="true"></i>
                    </div>
                    <div class="message-content">
                        <div class="message-container">
                            <div class="message">{{ run2.response }}</div>
                        </div>
                    </div>
                </div>
            </template>
        </CModal>
    </div>
</template>
  
<script>
import SearchIcon from "@/assets/icons/search.svg";
import CModal from "@/components/CModal.vue";
import DetailsPage from "./DetailsPage.vue";
import API_info from "./API_info.vue";
import Online_Interaction from "./Online_Interaction.vue";
import { get_mlModels, delete_mlModel, run_mlModels1, run_mlModels2 } from "@/api_client.js";

export default {
    name: "Services",
    components: {
        SearchIcon,
        CModal,
        DetailsPage,
        API_info,
        Online_Interaction,
    },
    data() {
        return {
            headers: [
                { text: "Name", value: "name" },
                { text: "Description", value: "description" },
            ],
            search: '',
            selected: [],
            isLoading: false,
            isActive: false,

            data: [],
            ml_model: {},

            run1: {
                response: "",
                isLoading: false,
                toggle: false
            },

            run2: {
                response: "",
                isLoading: false,
                toggle: false
            },
        };
    },

    mounted() {
        get_mlModels()
            .then(({ status, data }) => {
                if (status === 200) {
                    // convert [columns] string to json object
                    data.forEach((ml_model) => {
                        ml_model.columns = JSON.parse(ml_model.columns);

                        // eval_metrics
                        if (ml_model.eval_metrics !== null) {
                            let tmp = JSON.parse(ml_model.eval_metrics);
                            if (tmp.model_type === "classification")
                                ml_model.eval_metrics = [
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
                                ml_model.eval_metrics = [
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
                console.error("ml_model call");
            })
            .finally(() => {
                this.isLoading = false;
            });
    },

    methods: {
        handle_click(event) {
            this.data.forEach((ml_model) => {
                if (ml_model.name === event.name) this.ml_model = ml_model;
            });
            this.isActive = true;
        },

        delete_action() {
            this.selected.forEach(ml_model => {
                delete_mlModel(ml_model.id);
                // update data
                this.data = this.data.filter(this_ml_model => {

                    return this_ml_model.id != ml_model.id
                });
            });
        },

        get_key(column, value) {
            let found_key = null;
            Object.keys(column.values).forEach((key) => {
                if (column.values[key] == value)
                    found_key = key;
            });
            return found_key;
        },

        download(data, filename, mimeType) {
            const blob = new Blob([data], { type: mimeType });
            const url = URL.createObjectURL(blob);

            const link = document.createElement('a');
            link.href = url;
            link.download = filename;

            link.click();
        },

        handle_run1() {
            this.run1.isLoading = true;
            const payload = {
                model_name: this.ml_model.model_name,
                username: this.ml_model.username,
                columns: {},
            };
            let run_model = null;

            this.ml_model.columns.forEach((column) => {
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

            run_mlModels1(payload)
                .then(({ status, data }) => {
                    if (status === 200) {
                        data = JSON.parse(data);
                        if (data.hasOwnProperty("classification"))
                            this.run1.response = run_model.name + " = " + this.get_key(run_model, JSON.parse(data.classification)[0]);
                        else if (data.hasOwnProperty("result"))
                            this.run1.response = "Result = " + JSON.parse(data.result)[0];
                        else
                            this.run1.response = JSON.stringify(data);
                        this.run1.response = ""
                    }
                })
                .catch((error) => {
                    this.run1.response = error;
                })
                .finally(() => {
                    this.run1.toggle = true;
                    this.run1.isLoading = false;
                });
        },

        handle_run2(file) {
            this.run2.isLoading = true;

            let columns = [];
            this.ml_model.columns.forEach((column) => {
                if(!column.hasOwnProperty("values"))
                    columns.push(column.name);
            });

            run_mlModels2({
                model_name: this.ml_model.model_name,
                username: this.ml_model.username,
                file: file,
                columns: JSON.stringify(columns),
                isBulk: true
            })
                .then(({ status, data }) => {
                    if (status === 200){
                        this.download(data, 'data.csv', 'text/csv');
                        this.run2.response = ""
                    }
                })
                .catch(error => {
                    this.run2.response = error;
                })
                .finally(() => {
                    this.run2.toggle = true;
                    this.run2.isLoading = false;
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
            background-color: rgb(209, 83, 83);
            border-radius: 5px;
            transition: all 300ms;
            color: white;
            font-size: 15px;

            &:hover {
                opacity: 0.8;
            }
        }
    }
}

// Modal
.modal-container {
    padding: 20px 10px;
    height: 100%;
    width: 100%;
    display: flex;
    flex-flow: column nowrap;

    .status {
        >i {
            font-size: 60px;
            color: #2b468b9a;
        }
    }

    .message-content {
        flex-grow: 3;
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
