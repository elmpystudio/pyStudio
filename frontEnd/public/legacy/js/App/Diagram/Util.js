//static
function isItemInList(arrayToFetch, item) {

    var num = $.inArray(item, arrayToFetch);
    if (num !== -1) {
        return true;
    }
    return false;
}

//static
function isPanelHidden(panelId) {
    return $("#" + panelId).is(":hidden");
}

//static
function isStringNotNull(str) {
    if (str) {
        return true;
    } else {
        return false;
    }
}

//static
function isSelectElementFilled(elementId) {
    var optionsCount = $("#" + elementId + " option");
    if (optionsCount > 1) {
        return true;
    }
    return false;
}

//static
function appendToSelectColumns(elementId, val) {
    $('#' + elementId).append(`
            <li>
                <input type="checkbox" class="columnsCheckbox"><span class="lbl">`+ val + `</span>
            </li>
        `);
}

//static
function guid() {
    function s4() {
        return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
    }
    return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
        s4() + '-' + s4() + s4() + s4();
}

//static
function openCloseModal(modalName) {
    $("#" + modalName).modal("toggle");
}

//static
function showSuccessAlert(message) {
    App.alert({
        container: $('#alert_container').val(), // alerts parent container place: 'append', // append or prepent in container type: 'success', // alert's type message: 'Test alert', // alert's message
        type: 'success',
        message: message,
        close: true, // make alert closable reset: false, // close all previouse alerts first focus: true, // auto scroll to the alert after shown closeInSeconds: 10000, // auto close after defined seconds
        closeInSeconds: 5,
        focus: true,
        icon: 'fa fa-check' // put icon class before the message });
    });
}

//lostaticcal
function showErrorAlert(message) {
    App.alert({
        container: $('#alert_container').val(), // alerts parent container place: 'append', // append or prepent in container type: 'success', // alert's type message: 'Test alert', // alert's message
        type: 'danger',
        message: message,
        close: true, // make alert closable reset: false, // close all previouse alerts first focus: true, // auto scroll to the alert after shown closeInSeconds: 10000, // auto close after defined seconds
        closeInSeconds: 5,
        focus: true,
        icon: 'fa fa-warning' // put icon class before the message });
    });
}
///////////////////////////////////////////////////////
//jsplumbClient
function removeNumbersFromStr(str) {

    return str.replace(/[0-9]/g, '');
}

//jsplumbClient
function showPanel(panelId, bodyId, panelBody) {
    if (isPanelHidden(panelId)) {
        $("#" + bodyId).html(panelBody);
        $("#" + panelId).toggle("slide", { direction: "right" });
    }
}

//jsplumbClient
function hidePanel(panelId) {
    if (!isPanelHidden(panelId)) {
        $("#" + panelId).toggle("slide", { direction: "right" });
    }
}

//jsplumbClient
function getUrlParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

//jsplumbClient
function prepareSelect(elementId) {
    var firstOption = $("#" + elementId + " option")[0];
    $("#" + elementId).html(firstOption);
}

//jsplumbClient
function appendToSelect(elementId, val) {
    $('#' + elementId).append($('<option>', {
        value: val,
        text: val
    }));
}

//jsplumbClient
function removeNumberFromString(str) {
    return str.replace(/[0-9]/g, '');
}

//jsplumbClient | ApiClient
function roundNumberToTwoDigits(number) {
    try {
        return (Math.round(number * 100) / 100);
    } catch (e) {
        return number.toString;
    }
}

export {
    //jsplumbClient
    removeNumbersFromStr,
    showPanel,
    hidePanel,
    getUrlParameterByName,
    prepareSelect,
    appendToSelect,
    removeNumberFromString,

    //jsplumbClient | ApiClient
    roundNumberToTwoDigits
}