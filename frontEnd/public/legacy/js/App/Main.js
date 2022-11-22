import run from "./Diagram/JsplumbClient.js";

$(document).ready(function () {
    let user = {};
    user.userId = getUserIdFromTemplate();

    function getUserIdFromTemplate() {
        return document.getElementById("current-user-id").value;
    }

    //invoke JsPlumb
    run();

    function generatePDF(id) {
        const element = document.getElementById(id);

        var opt = {
            margin: 0.1,
            filename: `${id}.pdf`,
            image: { type: "jpeg", quality: 1 },
            html2canvas: { scale: 1 },
            jsPDF: { unit: "in", format: "a4", orientation: "portrait" },
        };
        html2pdf().set(opt).from(element).save();
    }

    $("#save_as_pdf_evaluationOutput").click(() => {
        generatePDF('evaluationOutput-content');
    });

    $("#save_as_pdf").click(() => {
        generatePDF('tab-content');
    });



    $(document).on("click", ".nav-link", function () {
        $(this).next().toggleClass("active"); //a->ul

        //arrow-icon
        var arrowIcon = $(this).children(".arrow-icon");
        if (arrowIcon.hasClass("fa-angle-double-down")) {
            arrowIcon.removeClass("fa-angle-double-down");
            arrowIcon.css("color", "rgb(164 187 209)");
        } else {
            arrowIcon.addClass("fa-angle-double-down");
            arrowIcon.css("color", "black");
        }
        arrowIcon.toggleClass("fa-angle-double-up");
    });

});
