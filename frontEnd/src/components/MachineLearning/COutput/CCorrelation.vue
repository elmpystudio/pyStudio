<template>
    <div class="content">
        <div class="form-container">
            <label for="correlation_select_columns">Select Columns</label>
            <div class="form-group">
                <div class="col-md-12">
                    <select
                        id="correlation_select_columns"
                        class="multiselect-ui form-control"
                        multiple="multiple"
                    ></select>
                </div>
            </div>

            <br />
            <div class="input-group">
                <div class="form-group">
                    <label for="plotTypeRadio" class="control-label">Plot Type</label>
                    <div class="input-group">
                        <div id="radioBtn" class="btn-group">
                            <a
                                class="btn btn-primary btn-sm active"
                                data-toggle="plotTypeRadio"
                                data-title="heatmap"
                            >Heatmap</a>
                            <a
                                class="btn btn-primary btn-sm notActive"
                                data-toggle="plotTypeRadio"
                                data-title="matrix"
                            >Matrix</a>
                        </div>
                        <input
                            type="hidden"
                            name="plotTypeRadio"
                            id="plotTypeRadio"
                            value="heatmap"
                        />
                    </div>
                </div>
                <button
                    id="view-correlation-button"
                    type="button"
                    class="btn btn-default btn-primary"
                >View</button>
            </div>
        </div>
        <div
            id="correlation-graph-div"
            class="modal-results-content"
            style="width: 490px; overflow-x: auto; overflow: auto"
        ></div>
    </div>
</template>

<script>
export default {
    name: "CCorrelation",
};
</script>

<style lang="scss" scoped>
.content {
    padding: 30px 150px;

    .form-container {
        border: 2px solid #364150;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;

        .col-md-12 {
            padding: 0;
        }

        .form-group {
            margin: 0;
        }

        .input-group {
            flex-direction: column;
        }

        button {
            margin-top: 20px;
            width: 300px;
            align-self: center;
        }

        input {
            background: white;
        }
    }
}
</style>