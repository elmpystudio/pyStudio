<template>
    <div class="content">
        <div class="table-container">
            <table
                id="outputDataSummaryTable"
                class="display nowrap active datasummary-table"
                width="100%"
            ></table>
        </div>
        <div id="outputModal-numberOfRecords">
            <b>Number of Records: X</b>
        </div>
    </div>
</template>

<script>
export default {
    name: "CDataSummary",
};
</script>

<style lang="scss" scoped>
.content {
    padding: 0 30px;
}

//overflow
::-webkit-scrollbar {
    height: 10px;
}

/* Track */
::-webkit-scrollbar-track {
    border-radius: 10px;
    background: white;
}

/* Handle */
::-webkit-scrollbar-thumb {
    background: #364150;
    border-radius: 10px;
}
</style>

<style lang="scss">
.table-container {
    overflow: auto;
    border-radius: 5px;
    padding-bottom: 1px;

    .datasummary-table {
        border-collapse: collapse;
        width: 900px;
        text-align: center;

        tr:nth-child(even) {
            background-color: rgba(0, 0, 0, 0.1);
        }

        tr:nth-child(odd) {
            background-color: rgba(0, 0, 0, 0.2);
        }

        th,
        td:first-child {
            background-color: #364150;
            color: white;
            font-size: 12px;
            text-transform: uppercase;
            padding: 2px 14px;
        }

        td {
            padding: 1px;
            font-size: 14px;
            color: #364150;
        }
    }
}

.ml-studio .dataTables_filter input {
    border-radius: 5px;
    background: white;
    border: 1px solid #364150;
    height: 30px;
}
</style>