<template>
    <div class="online_interactioncontainer-container" v-if="ml_model.columns && ml_model.columns.length > 0">
        <!-- Header -->
        <v-tabs v-model="tab" background-color="transparent" color="#2b468b" grow>
            <v-tab v-for="item in items" :key="item">
                {{ item }}
            </v-tab>
        </v-tabs>

        <!-- Content -->
        <v-tabs-items v-model="tab" class="custom-window">
            <v-tab-item v-for="item in items" :key="item">

                <div class="part1" v-if="item === 'Online Interaction'">
                    <div class="info-container">

                        <div class="scroll-container">
                            <div class="columns-container">
                                <div class="column-container" v-for="(
                                            column, index
                                        ) in filtered_columns(ml_model.columns)" :key="index">
                                    <div class="name">
                                        {{ column.name }}
                                    </div>

                                    <v-select v-if="column.hasOwnProperty('values')" :label="column.name"
                                        :item-color="'#2b468b'" :color="'#2b468b'" :items="Object.keys(
                                            column.values
                                        )
                                            " outlined dense v-model="column.value"></v-select>

                                    <input v-else type="text" v-model="column.value" placeholder="Number" />
                                </div>
                            </div>

                        </div>
                    </div>

                    <div class="actions-container">
                        <button class="btn btn-primary" @click="run1">
                            Send
                        </button>
                    </div>
                </div>

                <div class="part2" v-if="item === 'Bulk Execution'">
                    <div class="bulk-container">
                        <div class="name">
                            Set The Bulk File
                        </div>

                        <div class="file-input-container">
                            <input type="file" ref="file" @change="handleFileUpload">
                        </div>


                        <div class="actions-container">
                            <button class="btn btn-primary" @click="run2">
                                Send
                            </button>
                        </div>
                    </div>
                </div>
            </v-tab-item>
        </v-tabs-items>
    </div>
</template>

<script>
export default {
    name: "Online_Interaction",
    props: {
        ml_model: { type: Object, required: true },
    },
    data() {
        return {
            tab: null,
            items: [
                'Online Interaction', 'Bulk Execution'
            ],
            file: null
        }
    },
    methods: {
        handleFileUpload(event) {
            this.file = event.target.files[0];
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

        run1() {
            this.$emit("handle_run1");
        },

        run2() {
            this.$emit("handle_run2", this.file);
        }
    }
}
</script>

<style lang="scss" scoped>
.online_interactioncontainer-container {
    width: 100%;

    height: 600px;

    border: 2px solid #2b468b;
    border-radius: 5px;

    // change v-tabs body height
    .custom-window {
        height: 90%;
    }

    .part1 {
        padding: 20px;

        width: 100%;
        height: 100%;
        display: flex;
        flex-flow: column nowrap;
        justify-content: space-between;

        .info-container {
            height: 450px;
            position: relative;

            .scroll-container {
                padding: 10px;
                height: 400px;
                width: 100%;
                overflow-x: scroll;
                position: absolute;
                top: 0;
                left: 0;

                border: 2px solid #2b468b;
                border-radius: 10px;


                .columns-container {
                    display: flex;
                    flex-flow: row wrap;
                    gap: 20px;
                    align-items: center;
                    justify-content: center;

                    .column-container {
                        padding: 5px;
                        width: 280px;
                        height: 100px;

                        border-radius: 5px;
                        border: 1px solid #2b468b;

                        display: flex;
                        flex-flow: column nowrap;
                        gap: 10px;

                        align-items: center;
                        justify-content: center;


                        .name {
                            font-size: 18px;
                            text-align: start;
                            font-weight: bold;
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

                        .v-select {
                            background: white;
                        }

                    }

                }
            }
        }

        .actions-container {
            button {
                width: 300px;
            }
        }
    }

    .part2 {
        padding: 30px;
        width: 100%;
        height: 100%;

        .bulk-container {
            padding: 20px 10px;
            width: 100%;
            height: 100%;

            display: flex;
            flex-flow: column nowrap;
            justify-content: center;
            align-items: center;
            row-gap: 10px;

            border: 2px solid #2b468b;
            border-radius: 10px;

            .name {
                font-size: 30px;
            }

            .file-input-container {
                padding-left: 100px;

                .file-input {}
            }

            .actions-container {
                button {
                    width: 300px;
                }
            }
        }
    }
}
</style>


<style>
.online_interactioncontainer-container .part1 .info-container .scroll-container .columns-container .inrow .column-container[data-v-4789c200] {
    padding: 0;
}

.v-text-field {
    padding: 0;
    margin: 0;
}
</style>