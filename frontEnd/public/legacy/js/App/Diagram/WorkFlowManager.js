/*
    * In the diagramContainer_MouseDown-method we
        1- store the startPoint
        2- initialize the rubberband
        3- and show it!
*/

var startPoint = {};
var rubberbandDrawingActive = false;

//static
/*
    * this is local method
    * Finding items within the rubberband
        To be able to check, if an item is within the rubberband, we need to know the positions of the items and of the rubberband as well.
        Therefore, we create a little helper-functions, which returns us the distances to the left and to the top.
*/
function getTopLeftOffset(element) {
    var elementDimension = {};
    elementDimension.left = element.offset().left;
    elementDimension.top = element.offset().top;

    // Distance to the left is: left + width
    elementDimension.right = elementDimension.left + element.outerWidth();

    // Distance to the top is: top + height
    elementDimension.bottom = elementDimension.top + element.outerHeight();

    return elementDimension;
}

//static
/*
    * this is local method
    * The following method uses the above method getTopLeftOffset and checks, if an item is completly within the rubberband, by comparing the elementDimensions of the rubberband and item.
    * If so, it ads the css-class selected and adds the item to the dragSelection of jsPlumb by calling the method jsPlumb.addToDragSelection.
*/
function diagramContainer_FindSelectedItem() {
    if ($("#rubberband").is(":visible") !== true) { return; }

    var rubberbandOffset = getTopLeftOffset($("#rubberband"));

    $(".jtk-node").each(function () {
        var itemOffset = getTopLeftOffset($(this));
        if (itemOffset.top > rubberbandOffset.top &&
            itemOffset.left > rubberbandOffset.left &&
            itemOffset.right < rubberbandOffset.right &&
            itemOffset.bottom < rubberbandOffset.bottom) {
            $(this).addClass("selected");

            var elementid = $(this).attr('id');
            jsPlumb.addToDragSelection(elementid);
        }
    });
}

//jsplumbClient
/*
* mousemove
    In the method diagramContainer_MouseMove is the place, where the magic happens! Each time the mouse is moved, the rubberband is recalculated.
    The values we need to set on our rubberband (a div) are the top, left, width and height. We do this by simply updating the div‘s css values.
*/
function diagramContainer_MouseMove(event) {
    if ($("#rubberband").is(":visible") !== true) { return; }

    var t = (event.clientY > startPoint.y) ? startPoint.y : event.clientY;
    var l = (event.clientX >= startPoint.x) ? startPoint.x : event.clientX;
    // console.log("move: x " + l);

    let wcalc = event.clientX - startPoint.x;
    var w = (event.clientX > startPoint.x) ? wcalc : (wcalc * -1);

    let hcalc = event.clientY - startPoint.y;
    var h = (event.clientY > startPoint.y) ? hcalc : (hcalc * -1);

    $("#rubberband").css({ top: t, left: l, height: h, width: w, position: 'fixed' });
}

//jsplumbClient
/*
    * The implementation needs a little trick.
    *  As dragging is a click as well, we need to check, if the user is dragging or only clicking. We do this, by checking the mouseposition first.
*/
//handling clicks on diagram canvas empty area
function diagramContainer_Click(event) {
    if (startPoint.x === event.clientX && startPoint.y === event.clientY) {
        jsPlumb.clearDragSelection();
        $(".jtk-node").each(function () {
            $(this).removeClass("selected");
            $(this).children(".iconCircle").children("svg").children("circle").css("stroke", "#a5a5a5");
            $(this).children(".iconCircle").children("svg").children("circle").css("stroke-width", "1");
        });

        $("#propertiesBody").html('<h4 id="propertiesWindowHint">' + 'Task Properties and Description' + '</h4>');
    }
}

//jsplumbClient
/*
    * mouseup
        When the user finished dragging the rubberband, it must disappear. Thats what the method diagramContainer_MouseUp will do for us:
*/
/*function diagramContainer_MouseUp(event) {
    $("#rubberband").hide();
}*/

//jsplumbClient
/*
    * Finally we call the diagramContainer_FindSelectedItem-method within the mouseup-event.
*/
function diagramContainer_MouseUp(event) {
    diagramContainer_FindSelectedItem();
    $("#rubberband").hide();
}

function diagramContainer_MouseDown(event) {
    startPoint.x = event.clientX;
    startPoint.y = event.clientY;
    // console.log("down: x " + startPoint.x);

    $("#rubberband").css({ top: startPoint.y, left: startPoint.x, height: 1, width: 1, position: 'fixed' });
    $("#rubberband").show();
}

export {
    //jsplumbClient
    diagramContainer_MouseMove,
    diagramContainer_Click,
    diagramContainer_MouseUp,
    diagramContainer_MouseDown
}
