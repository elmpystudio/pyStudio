<template>
    <div class="modal fade" :id="id" role="dialog">
        <div class="modal-dialog">
            <div class="modal-content" :class="getClasses()">
                <div class="modal-header">
                    <h4 class="modal-title">
                        <slot name="title"></slot>
                    </h4>
                </div>

                <div class="modal-body">
                    <slot name="body"></slot>
                </div>
                <div class="modal-footer">
                    <button type="button" class="closebtn" data-dismiss="modal">
                        Close
                    </button>
                    <slot name="footer"></slot>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "CModal",

    props: {
        id: { type: String, required: true },
        size: { type: String, required: false },
        status: { type: String, required: false },
    },

    methods: {
        getClasses(){
            let classes = "";
            if(this.size === "small")
                classes += "small ";
            
            if(this.status === "error")
                classes += "error ";
            else if (this.status === "success")
                classes += "success";

            if(this.id === "deploy_modal")
                classes += "auto";

            return classes;
        }
    }
};
</script>

<style lang="scss" scoped>
.modal {
    width: 100%;
    position: fixed;
    top: 50%;
    left: 50%;

    transform: translate(-50%, -50%);
}

.modal-content {
    // width: 100%;
    // height: auto;
    min-width: 800px;
    max-height: 750px !important;
    border-radius: 20px;

    .modal-header {
        background: #364150;
        justify-content: center;
        border-radius: 15px 15px 0 0;
        border: 0;
        padding: 10px;

        .modal-title {
            color: #f2f2f2 !important;
            font-size: 22px;
        }
    }

    .modal-body {
        position: relative;
        overflow: auto;
        padding: 0;
    }

    .modal-footer {
        border-radius: 0 0 15px 15px;
        justify-content: space-between;
        flex-wrap: nowrap;
        background: #364150;
        padding: 6px;
        border: 0;

        .closebtn {
            background: #364150;
            text-transform: uppercase;
            width: 100%;
            height: 100%;
            font-size: 15px;
            color: #f2f2f2;
        }

        .closebtn:hover {
            color: red;
            opacity: 0.8;
        }
    }

    &.auto {
        margin-top: 100px !important;
        height: auto !important;
        max-height: auto !important;
    }
}

@media (min-width: 576px) {
    .modal-content {
        margin-top: 80px;
        margin-left: -150px;
        width: 800px;
        max-width: 800px;
        height: 800px;
        max-height: 800px;
    }
}

//small size
.small {
    height: 200px;
    width: 500px;
    margin-top: 300px;
    margin-left: 50px;
    min-width: 500px !important;

    .modal-header {
        padding: 2px;
    }
    .modal-footer {
        padding: 2px;
    }
}

.error {
    background: #dc3545;
}

.success {
    background: #058a00;
}

//overflow
::-webkit-scrollbar {
    width: 8px;
}

/* Track */
::-webkit-scrollbar-track {
    border-radius: 10px;
    background: #e3e3e3;
}

/* Handle */
::-webkit-scrollbar-thumb {
    background: #364150;
    border-radius: 3px;
}
</style>