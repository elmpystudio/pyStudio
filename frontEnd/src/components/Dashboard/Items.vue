<template>
    <div>
        <div class="filters-container pb-7">
            <div class="filters-column">
                <button @click="selectedStatus = 'private'" class="button select"
                    :class="selectedStatus === 'private' && 'active'">
                    Private
                </button>
                <button @click="selectedStatus = 'purchased'" class="button select"
                    :class="selectedStatus === 'purchased' && 'active'">
                    Purchased
                </button>
            </div>
            <div class="filters-column">
                <div class="search-container">
                    <SearchIcon class="search-icon" />
                    <input type="search" class="search" v-model="search" placeholder="Search for items" />
                </div>
                <button v-if="selectedStatus === 'private'" class="upload-button" @click="dialog = true">
                    <PlusIcon class="icon" /> Upload item
                </button>
            </div>
        </div>

        <!-- Private Table -->
        <template v-if="selectedStatus === 'private'">
            <!-- <v-data-table :headers="headers" :items="tablePrivateItems" item-value="value" item-text="label"
                class="elevation-1" :search="search" :loading="privateItems.isLoading"
                loading-text="Loading... Please wait" @click:row="handleOpenItem">
            </v-data-table> -->

            <v-data-table :headers="headers" :items="tablePrivateItems" class="elevation-1" :search="search"
                :loading="privateItems.isLoading" show-select v-model="selected" @click:row="handleOpenItem">
                <template v-slot:footer>
                    <div class="actions-container">
                        <button @click="delete_action">Delete</button>
                    </div>
                </template>
            </v-data-table>
        </template>

        <!-- Purchased Table -->
        <template v-if="selectedStatus === 'purchased'">
            <!-- <v-data-table :headers="headers" :items="tablePurchasedItems" item-value="value" item-text="label"
                class="elevation-1" :search="search" :loading="purchasedItems.isLoading"
                @click:row="handleOpenItem"></v-data-table> -->


            <v-data-table :headers="headers" :items="tablePurchasedItems" class="elevation-1" :search="search"
                :loading="tablePurchasedItems.isLoading" show-select v-model="selected" @click:row="handleOpenItem">
                <template v-slot:footer>
                    <div class="actions-container">
                        <button @click="delete_action">Delete</button>
                    </div>
                </template>
            </v-data-table>
        </template>

        <v-dialog v-model="dialog" max-width="600">
            <v-card>
                <v-card-title class="headline">
                    <span>Upload Dataset</span>
                </v-card-title>

                <v-divider></v-divider>

                <div v-if="uploadStep === 2">
                    <div class="file-preview">
                        <span>{{ file.name }}</span>
                        <DoneIcon class="file-icon" />
                    </div>
                    <v-divider></v-divider>
                </div>

                <v-card-text>
                    <template v-if="uploadStep === 1">
                        <input type="file" id="file" ref="file" @change="handleFileUpload" style="display: none;" />
                        <template v-if="isUploadingFile">
                            <div class="loader-container">
                                <v-progress-circular :size="50" color="primary" indeterminate></v-progress-circular>
                            </div>
                        </template>
                        <template v-else>
                            <div class="input-area" @click="$refs.file.click()">
                                Upload your file
                            </div>
                        </template>
                    </template>
                    <template v-if="uploadStep === 2">
                        <div class="upload-container">
                            <v-text-field v-model="datasetName" label="Dataset Name"></v-text-field>
                            <v-text-field class="pt-2" v-model="description" label="Dataset Description"
                                outlined></v-text-field>


                            <div class="upload-controls pt-3">
                                <v-progress-circular :size="30" color="primary" indeterminate v-if="isLoading">
                                </v-progress-circular>
                                <button class="button cancel" @click="handleClose">Cancel</button>
                                <button class="button submit" @click="handleSubmit"
                                    :disabled="!datasetName || isLoading">
                                    <span v-if="isLoading">Loading...</span>
                                    <span v-else>Submit</span>
                                </button>
                            </div>
                        </div>
                    </template>
                </v-card-text>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
import moment from 'moment';
import PlusIcon from '@/assets/icons/plus.svg';
import SearchIcon from '@/assets/icons/search.svg';
import DoneIcon from '@/assets/icons/done.svg';
import { createDataset, getDatasets, deleteDataset } from '@/api_client.js';

export default {
    name: "Items",
    components: {
        PlusIcon,
        SearchIcon,
        DoneIcon,
    },
    data() {
        return {
            search: '',
            selectedStatus: 'private',
            itemTypes: [
                { label: 'Dataset', value: 'Dataset' },
                { label: 'VA from tableau', value: 'VA from tableau' },
                { label: 'All', value: '' },
            ],
            headers: [
                { text: 'ID', value: 'id' },
                { text: 'Name', value: 'name' },
                { text: 'Type', value: 'type' },
                { text: 'Last Updated', value: 'last_updated' },
            ],
            privateItems: {
                data: [],
                isLoading: false,
            },
            purchasedItems: {
                data: [],
                isLoading: false,
            },
            dialog: false,
            dropzoneOptions: {
                url: 'https://httpbin.org/post',
                maxFilesize: 10,
                previewsContainer: false,
                manuallyAddFile: true,
            },
            file: null,
            fileId: null,
            isUploadingFile: false,
            uploadStep: 1,
            datasetName: '',
            description: '',
            isLoading: false,
            selected: []
        }
    },
    computed: {
        tablePrivateItems() {
            return this.privateItems.data.map((item) => ({
                id: item.id,
                name: item.name,
                type: 'Dataset',
                last_updated: moment(item.last_updated).format('DD.MM.YYYY'),
            }))
        },
        tablePurchasedItems() {
            return this.purchasedItems.data.map((item) => ({
                id: item.id,
                name: item.name,
                type: 'Dataset',
                last_updated: moment(item.last_updated).format('DD.MM.YYYY'),
            }))
        },
    },
    methods: {
        handleFileUpload(event) {
            this.isUploadingFile = true;
            this.file = event.target.files[0];
            this.uploadStep += 1;
            this.isUploadingFile = false;
        },
        handleSubmit() {
            this.isLoading = true;
            createDataset({
                file: this.file,
                name: this.datasetName,
                description: this.description
            })
                .then(({ data }) => {
                    this.isLoading = false;
                    this.$router.push({ name: 'dataset', params: { id: data.id } });
                })
                .catch(error => {
                    this.isLoading = false;
                    console.error('error', error);
                })
        },
        handleClose() {
            this.dialog = false;
            this.uploadStep = 1;
        },
        handleOpenItem(value) {
            if (value.type === 'Dataset') {
                this.$router.push({ name: 'dataset', params: { id: value.id } });
            }
            // if (value.type === 'Visual Analytics') {
            //     this.$router.push({ name: 'analytics-view', params: { name: value.name } });
            // }
        },

        // static method
        datasets_filter(datasets) {
            const filtered_data = {
                private: [],
                purchased: []
            }
            datasets.forEach(dataset => {
                if (dataset.purchased.length !== 0 && !dataset.is_public)
                    filtered_data.purchased.push(dataset);
                if (!dataset.is_public)
                    filtered_data.private.push(dataset);
            });
            return filtered_data;
        },

        delete_action() {
            this.selected.forEach((dataset) => {
                deleteDataset(dataset.id);
                // update privateItems
                this.privateItems.data = this.privateItems.data.filter(this_dataset => {
                    return this_dataset.id != dataset.id
                });
            });
        },
    },
    created() {
        this.privateItems.isLoading = true;

        getDatasets()
            .then(({ data }) => {
                data = this.datasets_filter(data);
                this.privateItems.data = data.private;
                this.privateItems.isLoading = false;
                this.purchasedItems.data = data.purchased;
                this.purchasedItems.isLoading = false;
            })
            .catch(error => {
                console.error(error)
            })
    }
}
</script>

<style scoped lang="scss">
.filters-container {
    display: flex;
    align-items: center;
    // background-color: #f4f6fa;

    .filters-column {
        display: flex;
        align-items: center;
        flex: 1;

        .upload-button {
            height: 42px;
            width: 162px;
            color: #ffffff;
            outline: none;
            border-radius: 4px;
            box-shadow: 0 5px 7px 0 rgba(94, 130, 245, 0.24);
            background-image: linear-gradient(to right, #2f6bff, #5e82f5);
            padding: 8px 16px;
            display: flex;
            font-weight: bold;
            font-size: 14px;
            align-items: center;

            .icon {
                margin-right: 14px;
            }
        }

        .button {
            height: 42px;
            width: 142px;
            color: #ffffff;
            outline: none;
            border-radius: 4px;

            &.select {
                background-color: #e4e4e4;
                margin: 0 10px 0 0;
                color: #868686;
                font-weight: bold;
                font-size: 14px;

                &.active {
                    background-image: linear-gradient(to right, #2f6bff, #5e82f5);
                    box-shadow: 0 5px 7px 0 rgba(94, 130, 245, 0.24);
                    color: #ffffff;
                }
            }
        }

        &:nth-child(2) {
            justify-content: flex-end;
        }

        .select-container {
            height: 42px;
            max-width: 142px;
            margin-left: 20px;

            &.items {
                margin: 0 20px 0 0;
                max-width: 200px;
            }
        }

        .search-container {
            display: flex;
            position: relative;
            height: 42px;
            margin-right: 20px;
            flex: 1;

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
    }
}

.input-area {
    border: 1px dashed #cecece;
    margin-top: 20px;
    border-radius: 5px;
    background-color: #f4f4f4;
    height: 140px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}

.upload-container {
    padding-top: 20px;
}

.upload-controls {
    display: flex;
    justify-content: flex-end;

    .button {
        border-radius: 5px;
        padding: 4px 10px;
        outline: none;

        &.submit {
            background: #000000;
            color: #ffffff;

            &:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
        }

        &.cancel {
            background: #f5f5f5;
            color: #000000;
            margin: 0 10px;
        }
    }
}

.close-icon {
    position: absolute;
    top: 10px;
    right: 10px;
    cursor: pointer;
}

.file-preview {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 24px;

    .file-icon {
        width: 30px;
        height: 30px;
    }
}

.loader-container {
    display: flex;
    min-height: 160px;
    justify-content: center;
    align-items: center;
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
</style>
