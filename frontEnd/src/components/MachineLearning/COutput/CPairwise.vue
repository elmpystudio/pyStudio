<template>
    <div class="content">
        <div class="form-container">
            <div class="form-group">
                <label for="pairwise_first_column">Select First Column</label>
                <select class="bs-select form-control" id="pairwise_first_column">
                    <option value="-1">-- Select Column Please --</option>
                </select>
            </div>
            <div class="form-group">
                <label for="pairwise_second_column">Select Second Column</label>
                <select class="bs-select form-control" id="pairwise_second_column">
                    <option value="-1">-- Select Column Please --</option>
                </select>
            </div>
            <button id="view-pairwise-button" type="button" class="btn btn-default btn-primary">View</button>
        </div>
        <div id="pairwise-graph-div" class="modal-results-content"></div>
    </div>
</template>

<script>
export default {
    name: "CPairwise",
};
</script>

<style lang="scss" scoped>
.content {
    margin: 30px 150px;

    .form-container {
        border: 2px solid #364150;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;

        button {
            width: 300px;
        }
    }
}
</style>