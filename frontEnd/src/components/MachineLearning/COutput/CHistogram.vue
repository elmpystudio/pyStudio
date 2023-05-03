<template>
    <div class="content">
        <div class="form-container">
            <div class="form-group">
                <label for="histogram_first_column">Select Column</label>
                <select class="bs-select form-control" id="histogram_first_column">
                    <option value="-1">-- Select Column --</option>
                </select>
            </div>

            <div class="input-group">
                <div class="col-md-6" style="padding-left: 0px">
                    <div class="input-group input-medium">
                        <label class="control-label" for="numberOfBins">Number of Bins</label>
                        <div class="input-group">
                            <input type="number" name="numberOfBins" id="numberOfBins" value="12" />
                        </div>
                    </div>
                </div>

                <div class="col-md-6">
                    <label for="normRadio" class="control-label">Norm</label>
                    <div class="input-group">
                        <div id="normRadioBtn" class="btn-group">
                            <a
                                class="btn btn-primary btn-sm active"
                                data-toggle="normRadio"
                                data-title="true"
                            >True</a>
                            <a
                                class="btn btn-primary btn-sm notActive"
                                data-toggle="normRadio"
                                data-title="false"
                            >False</a>
                        </div>
                        <input type="hidden" name="normRadio" id="normRadio" value="true" />
                    </div>
                </div>
            </div>

            <div class="form-group">
                <button
                    id="view-histogram-button"
                    type="button"
                    class="btn btn-default btn-primary"
                >View</button>
            </div>
        </div>

        <div id="histogram-graph-div" class="modal-results-content"></div>
    </div>
</template>

<script>
export default {
    name: "CHistogram",
};
</script>

<style lang="scss" scoped>
.content {
    padding: 30px 150px;

    .form-container {
        border: 2px solid #364150;
        border-radius: 10px;
        padding: 15px;
        padding-bottom: 0;
        margin-bottom: 20px;

        button {
            margin-top: 20px;
            width: 300px;
        }

        input {
            background: white;
        }
    }
}
</style>

<style lang="scss">
.input-group {
    justify-content: center;
}
</style>