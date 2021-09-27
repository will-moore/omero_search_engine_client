var querystarttime;
var queryendtime;
var resource;
let cancel_check = false;
var ajaxCall;
var task_id;
var set_query_form = false;


function cancell_ajaxcall() {
    ajaxCall.onreadystatechange = null;
    ajaxCall.abort();
    console.log("Canceled");
    ajaxCall = null;
    return;
}

//display message to the user
function displayMessage(header, body, btn_text) {
    messageHeader.innerText = header;
    messageBody.innerText = body;
    if (typeof(btn_text) !== "undefined" && btn_text !== null)
        moelButton.innerText = btn_text;
    $("#displaymessagemodal").modal("show");
    $("#moelButton").hide();
}

function cancelFunction() {
    cancel_check = true;
    cancell_ajaxcall();
    $("#moelButton").hide();
}

function urlFormatter(row, cell, value, columnDef, dataContext) {
    return "<a href=" + value + " target='_blank'>" + value + "</a>";
}

function valueFormatter(row, cell, value, columnDef, dataContext) {
    return value.toString();
}

function displayResults(data) {
    var notice = data["notice"];
    server_query_time = data["server_query_time"];
    results = data['Results'];
    let no_image = results.length;
    if (set_query_form == true) {
        var filters = data["filters"];
        var orFilter = filters["or_filters"];
        var andFilter = filters["and_filters"];
        var notFilter = filters["not_filters"];
        resource = data["resource"]

        for (i in orFilter)
            for (const [key, value] of Object.entries(orFilter[i])) {
                addConditionRow(key, value, "or");
            }
        for (i in andFilter)
            for (const [key, value] of Object.entries(andFilter[i])) {

                addConditionRow(key, value, "and");
            }
        for (i in notFilter)

            for (const [key, value] of Object.entries(notFilter[i])) {

                addConditionRow(key, value, "not");
            }
        message = "No of " + resource + "s: " + no_image + ", Search engine query time: " + server_query_time + " seconds.";

    } else {
        var querytime = (queryendtime - querystarttime) / 1000;
        message = "No of " + resource + "s: " + no_image + ", Query time: " + querytime + " Second" + ", Search engine query time: " + server_query_time + " seconds.";
    }

    var resultsDiv = document.getElementById('results');

    var conditions_con = document.getElementById('conditions');

    var resources_con = document.getElementById('resources');
    conditions_con.disabled = true;

    resources_con.style.display = "none";
    var query_cr = document.getElementById('conditions');

    resultsDiv.style.display = "block";

    if (notice != "None")
        message = message + "\n\n\r" + notice;
    $('#no_images').append(message);
    $('#query_id').append("Query id: " + task_id);

    var grid;
    var columns = [{
            id: "id",
            name: "Id",
            field: "id",
            sortable: true
        },
        {
            id: "name",
            name: "Name",
            field: "name",
            formatter: valueFormatter,
            sortable: true
        },
        {
            id: "url",
            name: "URL",
            field: "url",
            formatter: urlFormatter,
            sortable: true
        },
    ];
    var options = {
        enableCellNavigation: true,
        enableColumnReorder: false,
        multiColumnSort: true,
        forceFitColumns: true
    };
    $('#displaymessagemodal').modal('hide');
    var nodes = document.getElementById("conditions").getElementsByTagName('*');

    for (var i = 0; i < nodes.length; i++) {
        nodes[i].disabled = true;
    }
    grid = new Slick.Grid("#myGrid", results, columns, options);

    grid.onSort.subscribe(function(e, args) {
        var cols = args.sortCols;

        results.sort(function(dataRow1, dataRow2) {
            for (var i = 0, l = cols.length; i < l; i++) {
                var field = cols[i].sortCol.field;
                var sign = cols[i].sortAsc ? 1 : -1;
                var value1 = dataRow1[field],
                    value2 = dataRow2[field];
                var result = (value1 == value2 ? 0 : (value1 > value2 ? 1 : -1)) * sign;
                if (result != 0) {
                    return result;
                }
            }
            return 0;
        });
        grid.invalidate();
        grid.render();
    });
    window.location.hash = '#results';
}


function get_query_data(condition_table) {
    query_items = [];
    let andTable = document.getElementById(condition_table);
    for (var r = 1; r < andTable.rows.length; r++) {
        query_dict = {}
        query_items[r - 1] = query_dict;
        name_ = andTable.rows[r].cells[0].innerHTML;
        value_ = andTable.rows[r].cells[1].innerHTML;
        query_dict[name_] = value_
    }
    return query_items;
}

function get_results() {
    let results = {}
    let status = "PENDING";

    ajaxCall = $.ajax({
        type: "POST",
        async: false,
        url: queryresultsurl + "?task_id=" + task_id + "&resource=" + resource,
        contentType: "application/json;charset=UTF-8",
        dataType: 'json',
        success: function(data) {
            status = data["Status"];
            results_ = data['Results'];
            //alert(typeof(results_));

            if (status !== 'PENDING') {

                //$('#results').html(data);

                //alert ("I got the  results ...and back///"+status+"////"+results);

                //var modal = document.getElementById("modal");
                //modal.style.display = "none";
                queryendtime = new Date().getTime();
                if (status == "FAILURE" || data['error'] != "None") {
                    $('#displaymessagemodal').modal('hide');
                    alert("Somthing went wrong, please try again later.");
                    return;
                }

                displayResults(data);
                return;
            } else {
                setTimeout(function() {
                    get_results();
                }, 600);
            }
        }
    });
}

function submitQuery() {
    resource = document.getElementById('resourcseFields').value;

    querystarttime = new Date().getTime();
    //alert("I am going to submit the query");
    query_details = {}
    var query = {
        "resource": resource,
        "query_details": query_details
    };
    var andQuery = get_query_data("and_condition");
    var orQuery = get_query_data("or_condition");
    var notQuery = get_query_data("not_condition");

    if (andQuery.length == 0 && orQuery.length == 0 && notQuery == 0) {
        alert("There is no query to submit, at least one condition should be selected");
        return;
    }
    query_details["and_filters"] = andQuery;
    query_details["or_filters"] = orQuery;
    query_details["not_filters"] = notQuery;

    $.ajax({
        type: "POST",
        url: submitqueryurl,
        contentType: "application/json;charset=UTF-8",
        dataType: 'json',
        data: JSON.stringify(query),
        success: function(data) {
            if (data["Error"] != "none") {
                alert(data["Error"]);
                return;
            }
            task_id = data['task_id'];
            header = "Awaiting results";
            body = "Query submited! Please wait, this may take some time \n\nQuery id is : " + task_id + " \n\nYou may review your results at a later time using this url: \n\n/getqueryresult/?task_id=" + task_id
            displayMessage(header, body);
            results = get_results();
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("Status: " + textStatus);
            alert("Error: " + errorThrown);
        }
    });
}


function AddConditionFunction() {
    let value_fields = document.getElementById('valueFields');
    let condtion = document.getElementById('condtion').value;

    let key = keys_options.value;
    let value = value_fields.value;

    if (!value || value.length === 0) {
        alert("Please select a value");
        return;
    }

    if (!key || key.length === 0) {
        alert("Please select an attribute");
        return;
    }
    addConditionRow(key, value, condtion);
}

function addConditionRow(key, value, condtion) {

    let tableRef = document.getElementById(condtion + "_condition");

    let newRow = tableRef.insertRow(-1);

    // Insert cells in the row
    let keyCell = newRow.insertCell(0);
    let valueCell = newRow.insertCell(1);
    let removeCell = newRow.insertCell(2);

    // Append a text node to the cells
    let keyText = document.createTextNode(key);
    keyCell.appendChild(keyText);

    let valueText = document.createTextNode(value);
    valueCell.appendChild(valueText);

    //let newText3 = document.createTextNode();
    var removebutton = document.createElement("BUTTON");
    removebutton.innerHTML = "Remove";

    removeCell.appendChild(removebutton);

    //alert(keys_options.value);
    removebutton.addEventListener("click", function() {
        //alert("I am going to remove");
        //var $row = $(this).closest("tr");
        var row = removebutton.parentNode.parentNode;
        row.parentNode.removeChild(row);
    });
}


function set_key_values(key_value) {
    resource = selected_resource.value;
    fetch('/' + resource + '/get_values/?key=' + key_value).then(function(response) {
        {
            response.json().then(function(data) {
                data.sort();

                optionHtml = ''
                for (i in data) {
                    optionHtml += '<option value ="' + data[i] + '">' + data[i] + '</option>'
                }
                let value_fields = document.getElementById('valueFields');
                value_fields.innerHTML = optionHtml;


            });

        }
    });
}

function set_resources(resource) {
    for (const [key, value] of Object.entries(resources_data)) {
        if (key == resource) {
            optionHtml = ''
            value.sort();
            for (i in value) {
                optionHtml += '<option value ="' + value[i] + '">' + value[i] + '</option>'
            }
            keys_options.innerHTML = optionHtml;
            break;
        }

    }
    key_value = keys_options.value;
    set_key_values(key_value);
}

let selected_resource = document.getElementById('resourcseFields');
let keys_options = document.getElementById('keyFields');
selected_resource.onchange = function() {
    resource = selected_resource.value;
    set_resources(resource);
}

keys_options.onchange = function() {
    key_value = keys_options.value;
    set_key_values(key_value);
}


$(document).ready(function() {

    if (query_id != "None") {
        set_query_form = true;
        task_id = query_id;
        header = "Retrieve results";
        body = "Please wait while retrieving the results for \n\rQuery no: " + task_id + ", this may take some time";
        displayMessage(header, body);
        setTimeout(function() {
            get_results();
        }, 600);

    } else {
        var resources_con = document.getElementById('resources');
        resources_con.style.display = "block";
        resource = selected_resource.value = 'image';
        set_resources('image');
    }

});