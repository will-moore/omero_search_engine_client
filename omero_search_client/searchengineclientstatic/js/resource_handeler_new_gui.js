var querystarttime;
var queryendtime;
var resource;
let cancel_check = false;
var ajaxCall;
var task_id;
var set_query_form = false;
var bookmark;
var page=0;
var query;
var recieved_results=[];
var size=0;
var query;
var pages_data={};
var ag_grid;
var recieved_data=0;
var columnDefs=[];
var current_values={};
var cached_key_values={};
var extend_url;
var names_ids;
var main_attributes= ["Name (IDR number)"];
var query_details;
var raw_elasticsearch_query;
var no_cloned =0;
var original_external_int_div = document.getElementById('template'); //Div to Clone
var or_template = document.getElementById('ortemplate');
var or_parent=document.getElementById('conanewor');
var tree_nodes=[];
var is_new_query=true;



//save query json string to the local user storage, so he cal load it again
function save_query()
 {
    query=get_current_query(false);
    if (query==false)
        return;
    else
    {
        $("#confirm_message").modal("show");
            document.getElementById("queryfilename").focus();

        }
}

//Save query to user local storage
function download_query()
{
filename=document.getElementById("queryfilename").value;
query=JSON.stringify(get_current_query(false), null, 4);
if (filename) {
    filename=filename+'.txt'
    var file_container = document.createElement('a');
    file_container.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(query));
    file_container.setAttribute('download', filename);

    if (document.createEvent) {
        var event = document.createEvent('MouseEvents');
        event.initEvent('click', true, true);
        file_container.dispatchEvent(event);
    }
    else {
        file_container.click();
    }
    $("#confirm_message").modal("hide");
    document.getElementById("queryfilename").value="";
}
}

//
function reset_query(){
    query=get_current_query(false);
    if (query==false)
        return;
    if (confirm("All the conditions will be discarded, process?") == true) {
       reset_global_variables();
        const eGridDiv = document.querySelector('#myGrid_2');
        removeAllChildNodes(eGridDiv);
        document.getElementById("results").style.display='none';
        document.getElementById("reset_results_table_filter").style.display='none';
        $("#search_form").empty();
        $("#addAND").click();
        //location.reload();
        return false;
    }
}


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


function urlFormatter  (row, cell, value, columnDef, dataContext) {
    return "<a href=" + value + " target='_blank'>" + value + "</a>";
}

function valueFormatter(row, cell, value, columnDef, dataContext) {
try {
       return value.toString();

}
catch(err) {
    alert ("Error "+err+", for value: "+value);
}

}

function loadMoreResultsFunction()
{
    document.getElementById('loadMoreResults').disabled=true;
    submitQuery(false);
}


function reset_global_variables(data)
    {
        bookmark=null;
        raw_elasticsearch_query=null;
        page=0;
        pages_data={};
        recieved_results=[];
        size=0;
        query_details=null;
        recieved_data=0;
    }

function set_global_variables(data)
    {
    bookmark=data["bookmark"];
    raw_elasticsearch_query=data["raw_elasticsearch_query"];
    page=page+1;
    pages_data[page]=data;
    recieved_results=recieved_results.concat(data["values"]);
    size=data["size"];
    query_details=data["query_details"];
    recieved_data=recieved_data+data["values"].length;
    var resultsbutton = document.getElementById('loadMoreResults');
    if (recieved_data>=size){

    resultsbutton.disabled = true;
    }
    else
    resultsbutton.disabled= false;

}
function sizeToFit() {
  ag_grid.gridOptions.api.sizeColumnsToFit();
}

function resetResultsTabelFilters()
{
    ag_grid.gridOptions.api.setFilterModel(null);
    ag_grid.gridOptions.api.onFilterChanged();
}


function getBoolean(id) {
  //var field = document.querySelector('#' + id);
  return true;
}

function getParams() {
  return {
    allColumns: getBoolean('allColumns'),
    //columnSeparator: '\t'
  };
}

function exportToCSV() {
  ag_grid.gridOptions.api.exportDataAsCsv(getParams());
}



function autoSizeAll(skipHeader) {
  var allColumnIds = [];
  gridOptions.columnApi.getAllColumns().forEach(function (column) {
    allColumnIds.push(column.colId);
  });
  gridOptions.columnApi.autoSizeColumns(allColumnIds, skipHeader);
    }

function url_render(param){
    if (resource =="screen")
        return '<a href='+extend_url +' target="_blank" >'+param.value+'</a>'
    else
        return '<a href='+extend_url +param.value+' target="_blank" >'+param.value+'</a>'
    }

function onGridSizeChanged(params) {
        // get the current grids width
        var gridWidth = document.getElementById('grid-wrapper').offsetWidth;
        // keep track of which columns to hide/show
        var columnsToShow = [];
        var columnsToHide = [];
        // iterate over all columns (visible or not) and work out
        // now many columns can fit (based on their minWidth)
        var totalColsWidth = 0;
        var allColumns = params.columnApi.getAllColumns();
        for (var i = 0; i < allColumns.length; i++) {
        let column = allColumns[i];
        totalColsWidth += column.getMinWidth();
        if (totalColsWidth > gridWidth) {
                columnsToHide.push(column.colId);
            } else {
                columnsToShow.push(column.colId);
            }
        }

        // show/hide columns based on current grid width
        params.columnApi.setColumnsVisible(columnsToShow, true);
        params.columnApi.setColumnsVisible(columnsToHide, false);

        // fill out any available space to ensure there are no gaps
        params.api.sizeColumnsToFit();
}

function displayResults(data, new_data=true) {

if (is_new_query==true)
{
    is_new_query=false;
    reset_global_variables();
    $("#myGrid_2").empty();
}
   if (new_data)
        set_global_variables(data);
columnDefs =data["columns_def"]
extend_url=data["extend_url"];
names_ids=data["names_ids"];
for (i in data["columns_def"])
    {
    if(data["columns_def"][i]["field"]==="Id")// && resource==="image")
         data["columns_def"][i]['cellRenderer']=url_render;
     }

results = data["values"];

var gridOptions = {
  defaultColDef: {
    resizable: true,
  "filter": true,
  "animateRows":true,
  },
 enableCellTextSelection: true,
  columnDefs: columnDefs,
  rowData: null,

};

 // lookup the container we want the Grid to use
  const eGridDiv = document.querySelector('#myGrid_2');
  // create the grid passing in the div to use together with the columns & data we want to use
  if (page==1)
    ag_grid=new agGrid.Grid(eGridDiv, gridOptions);
  ag_grid.gridOptions.api.setRowData(recieved_results);
  var notice = data["notice"];

  server_query_time = data["server_query_time"];
  let no_image = results.length;

        var querytime = (queryendtime - querystarttime) / 1000;
        if (no_image!=size)
         {
            message = "No of "+data["resource"]+ ", "+ recieved_data +"/"+size + ", Search engine query time: " + server_query_time + " seconds.";
             document.getElementById('loadMoreResults').style.display = "block";
            }
        else
        {
            message = "No of "+data["resource"] +", "+ recieved_data+ ", Search engine query time: " + server_query_time + " seconds.";
             document.getElementById('loadMoreResults').style.display = "none";
            }


    var resultsDiv = document.getElementById('results');
//    document.getElementById('exportResults').style.display = "block";
    document.getElementById('reset_results_table_filter').style.display = "block";
    resultsDiv.style.display = "block";
    $('#no_images').text(message);
    var grid;
    var columns = data["columns"];
     for (var i = 0; i < columns.length; i++) {
        columns[i].formatter=valueFormatter;
    }
    var options = {
        enableCellNavigation: true,
        enableColumnReorder: false,
        multiColumnSort: true,
        forceFitColumns: true
    };
    $('#displaymessagemodal').modal('hide');

    window.location.hash = '#results';
    document.getElementById('load_results_buttons').style.display = "block";
    if (new_data)
    {
     return;
    var tr = document.getElementById('loads_results_table').tHead.children[0],
    th = document.createElement('th');
    tr.appendChild(th);
    var pagebutton = document.createElement("BUTTON");
    pagebutton.innerHTML = page;
    th.appendChild(pagebutton);
    th.appendChild(pagebutton);
    pagebutton.addEventListener("click", function() {
        alert(pagebutton.innerText);
        displayResults(data, false);
    });
    }
}

var filterParams = {
    suppressAndOrCondition: true,
    comparator: function (filterLocalDateAtMidnight, cellValue) {
    var dateAsString = cellValue;
    if (dateAsString == null)
        return -1;
    var dateParts = dateAsString.split('/');
    var cellDate = new Date(
    Number(dateParts[2]),
    Number(dateParts[1]) - 1,
    Number(dateParts[0])
    );

    if (filterLocalDateAtMidnight.getTime() === cellDate.getTime()) {
      return 0;
    }

    if (cellDate < filterLocalDateAtMidnight) {
      return -1;
    }

    if (cellDate > filterLocalDateAtMidnight) {
      return 1;
    }
    },
    browserDatePicker: true,
};

function get_returned_query_from_server()
        {
        resource = "image";//document.getElementById('resourcseFields').value;
        var query_ = {
            "resource": resource,
            "query_details": query_details,
            "raw_elasticsearch_query": raw_elasticsearch_query
        };
          query_["bookmark"]=bookmark;
          query_["columns_def"]=columnDefs;
          return query_;
    }

function get_current_query(include_addition_information,displaymessage=true)
    {
    and_conditions=[];
    or_conditions=[];
    //get and condition1

    queryandnodes = document.querySelectorAll('#search_form .and_clause');
    console.log(queryandnodes.length);
    for (let i=0; i<queryandnodes.length; i++) {

        query_dict={};

        let node = queryandnodes[i];
        // handle each OR...
        let ors = node.querySelectorAll(".form-row");

        let or_dicts = [...ors].map(orNode => {
            return {
                "name": orNode.querySelector(".keyFields").value,
                "value": orNode.querySelector(".valueFields").value,
                "operator": orNode.querySelector(".condition").value,
                "resource": get_resource( orNode.querySelector(".keyFields").value),
            }
        });
        if (or_dicts.length > 1) {
            or_conditions.push(or_dicts);
        } else {
            and_conditions.push(or_dicts[0]);
        }
    }

    query_details = {}
     var query = {
        "resource": "image",
        "query_details": query_details
    };

    query_details["and_filters"] = and_conditions;
    query_details["or_filters"] = or_conditions;
    query_details["case_sensitive"]=document.getElementById('case_sensitive').checked;
    query["mode"]=mode;
    return query;

}

function submitQuery(reset=true) {
   if (reset==true)
            reset_global_variables();
   if (query_details === undefined || size==0)
     {
        query=get_current_query(true);
            if (query==false)
                return;
        }
   else
        query=get_returned_query_from_server()

   send_the_request(query);

}

function send_the_request(query)
{
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
            displayResults(data);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("Status: " + textStatus);
            alert("Error: " + errorThrown);
        }
    });
}


function set_query_fields(container)
    {
            let selected_resource_ = container.querySelector('.resourcseFields');
            let keys_options_ = container.querySelector('.keyFields');
            let keyFields_= container.querySelector('.keyFields');
            let valueFields_= container.querySelector('.valueFields');

            keys_options_.onchange = function() {
                key_value = this.value;
                set_key_values(key_value,container);
            }

    valueFields_.addEventListener("focus", function() {

    setAutoCompleteValues();
        });

        valueFields_.addEventListener("change", function() {
        query = get_current_query()
        $("#queryJson").val(JSON.stringify(query, undefined, 4));

    });

      optionHtml = '';
      let condtion__ = container.querySelector('.condition');
       optionOpHtml = '';

       for (i in operator_choices)
           {
             optionOpHtml += '<option value ="' + operator_choices[i][0] + '">' + operator_choices[i][1]+ '</option>';
           }

       condtion__.innerHTML = optionOpHtml;

       set_resources("image",container);
}


function addConditionRow(key, value, condtion, resource, group) {
    let tableRef = document.getElementById(group + "_group");
    let newRow = tableRef.insertRow(-1);
    // Insert cells in the row
    let keyCell = newRow.insertCell(0);
    let operatorCell = newRow.insertCell(1);
    let valueCell = newRow.insertCell(2);
    let resourceCell = newRow.insertCell(3);
    let removeCell = newRow.insertCell(4);

    // Append a text node to the cells
    let keyText = document.createTextNode(key);
    keyCell.appendChild(keyText);

    let operatorText = document.createTextNode(condtion);
    operatorCell.appendChild(operatorText)

    let valueText = document.createTextNode(value);
    valueCell.appendChild(valueText);

    let resourceText = document.createTextNode(resource);
    resourceCell.appendChild(resourceText);

    var removebutton = document.createElement("BUTTON");
    removebutton.innerHTML = "X Remove";
    removebutton.setAttribute("class", "btn btn-danger btn-sm");
    removeCell.appendChild(removebutton);

    removebutton.addEventListener("click", function() {
        var row = removebutton.parentNode.parentNode;
        row.parentNode.removeChild(row);
    });
}

/*
set autocpmlete values for key using a function to filter the available values
It solves the issue of having many available values (sometimes tens of thousnads),
it was freezing the interface */
function setAutoCompleteValues(){
        container=document.activeElement.parentNode.parentNode;
        document.activeElement.addEventListener("keyup", function() {
        $(container.querySelector(".valueFields")) .autocomplete({
                   source:  setFieldValues(),
                   minLength:0
        });
    });


}


//As main attributes supports equals andnot equals only
//This function restrict the use to these two operators
function set_operator_options(key_value, container)
{
     condition = container.querySelector(".condition");
     condition.value=condition.options[0].text;

    for (i =0; i< condition.length; i++  )
    {
        if (main_attributes.includes(key_value))
            {
                 if (condition.options[i].text!= "equals" && condition.options[i].text!="not equals")
                    condition.options[i].style.display = "none";
              }
         else
            {
                condition.options[i].style.display = "block";
          }

        }
    }

function get_resource(attribute)
{
 for (resource in resources_data) {
                if (resources_data[resource].includes(attribute))
                {
                return resource;
                }
            }
}


function set_key_values(key_value, container) {

    container.querySelector(".valueFields").value='';
    resource=get_resource(key_value);
    set_operator_options(key_value, container);
    if (cached_key_values[key_value]===undefined)
    {
        //let selected_resource_ = document.getElementById('resourcseFields'+id);
        //resource = selected_resource_.value;
        url=getresourcesvalesforkey+ "/?key=" + encodeURIComponent(key_value)+"&&resource="+ encodeURIComponent(resource);
        fetch(url).then(function(response) {
          {
            response.json().then(function(data) {
                data.sort();
                cached_key_values[key_value]=data;

                    });
                }
        });
    }


}

function setFieldValues(){
    let value_fields = document.activeElement;//document.getElementById('valueFields'+id);
    container=document.activeElement.parentNode.parentNode;
    key_value=container.querySelector(".keyFields").value;
    current_value=cached_key_values[key_value];
    let val=value_fields.value;
    //for performance, when the length of the current values length is bigger than 1000, when the value is one letter, it will only return all the items which start with this letter
    //otherwise, it will return all the items which contains the value (even ther are  at the middle or at the end of the items)
    if (current_value.length>1000)
    {
    console.log("1: val: "+val);

      if (!val || val.length <2  )
        return [];
    else
        if (val.length ===2)
            return  current_value.filter(x => x.toLowerCase().startsWith(val.toLowerCase()))
    else
         return current_value.filter(x => x.toLowerCase().includes(val.toLowerCase()))
   }
    else
    {
         return current_value.filter(x => x.toLowerCase().includes(val.toLowerCase()))
        }


}

function set_resources(resource, container) {
    let __keys_options=container.querySelector(".keyFields");
    optionHtml = '';
    for (const [key, value] of Object.entries(resources_data)) {
       // if (key == resource) {
            if (value==null)
              {
              __keys_options.innerHTML = optionHtml;
            break;
              }
             //if (key=="image")
             //      //#value.unshift("Project name");
             //      value.push("Project name");
             value.sort();
            for (i in value) {
                optionHtml += '<option value ="' + value[i] + '">' + value[i] + '</option>'
            }
    }
        __keys_options.innerHTML = optionHtml;
        key_value = __keys_options.value;
        set_key_values(key_value, container);
}

function set_tree_nodes (mode=true)
{

tree_nodes=[];
tree_nodes.push({ "id" : "Resource", "parent" : "#", "text" : "Resource", "state": {"opened"    : true }});
for (resource in resources_data) {
                tree_nodes.push({ "id" : resource, "parent" : "Resource", "text" : resource, "state": {"opened"    : mode }});

                for (i in resources_data[resource].sort() )
                {
                if (resources_data[resource][i].trim().length>22)
                text= resources_data[resource][i].substr(0, 22) +  "...";
                else
                text= resources_data[resource][i];
                        tree_nodes.push(
                        {
                        "id" : resources_data[resource][i],
                         "parent" : resource,
                         "text" : text,//resources_data[resource][i]
                         "title":text
                         }
                      );

                        }

                }
                }

function create_tree(){

    $('#jstree_resource_div').jstree({ 'core' : {
        'data' :  tree_nodes
    } });
}

function set_tree_events_handller () {
$('#jstree_resource_div').on("changed.jstree", function (e, data) {
  console.log(data.selected);
});
$('#jstree_resource_div').on('hover_node.jstree',function(e,data){
    var node = $(event.target).closest("li");
    node.prop("title",node[0].id);
});
/*
Query the search engine using the resourse attribute, when the user double click the attribute node
*/
$('#jstree_resource_div').bind("dblclick.jstree", function (event) {
   var node = $(event.target).closest("li");
    var type = node.attr('rel');
    var key = node[0].id;
    $('body').addClass('wait');

    let resource=get_resource(key);
    url=searchresourcesvalesforkey+ "/?key=" + encodeURIComponent(key)+"&&resource="+ encodeURIComponent(resource);
    fetch(url).then(function(response) {
      {
        response.json().then(function(data) {
            display_value_search_results(data, resource);
                });
            }
    });


});
}

// This is called when the page is ready
$(document).ready(async function() {

    // wait while we load resources_data...
    await fetch(searchtermsurl).then(rsp => rsp.json()).then(data => {
        resources_data = data;
    });

    // now we can build tree etc...
    set_tree_nodes();

    create_tree();


    let _keys_options = document.getElementById('keyFields');
    optionHtml = ''
    for (key in resources_data) {
                optionHtml += '<option value ="' + key + '">' + key+ '</option>'
            }
       //resourcseFields.innerHTML = optionHtml;
       optionOpHtml = ''
       for (i in operator_choices)
       {
         optionOpHtml += '<option value ="' + operator_choices[i][0] + '">' + operator_choices[i][1]+ '</option>'
       }
       condtion.innerHTML = optionOpHtml;
        var resources_con = document.getElementById('resources');
        resources_con.style.display = "block";

        set_query_fields(_keys_options.parentNode.parentNode);

});
//Used to load query from local storage
// document.getElementById('load_file').onchange = function () {
// let file = document.querySelector("#load_file").files[0];
//   load_query_from_file(file);
// }


let $andClause;

$(function(){

    // clone empty form row before any changes
    // used for building form
    $andClause = $("#search_form .and_clause").clone();

    // Hide the X button if there's only 1 in the form
    function hideRemoveIfOnlyOneLeft() {
        let $btns = $("button.remove");
        if ($btns.length == 1) {
            $btns.css('visibility', 'hidden');
        } else {
            $btns.css('visibility', 'visible');
        }
    }

    // update JSON query
    function updateForm() {
        hideRemoveIfOnlyOneLeft();

        query = get_current_query()
        is_new_query=true;
        $("#queryJson").val(JSON.stringify(query, undefined, 4));
    }

    // OR buttons
    $("#search_form").on("click", ".addOR", function (event) {
        event.preventDefault();
        let $clause = $(this).parent();
        addOr($clause);
        updateForm();
    });

    // X buttons
    $("#search_form").on("click", ".remove", function (event) {
        let $row = $(this).closest(".form-row");
        let $clause = $row.parent();
        $row.remove();
        // If no rows left, remove clause...
        if ($(".form-row", $clause).length === 0) {
            let $and = $clause.prev();
            if ($and.length == 0) {
                // in case we're removing the first row
                $and = $clause.next();
            }
            $and.remove();
            $clause.remove();
        }
        updateForm();
    });

    // AND button
    $("#addAND").on("click", function(){
        addAnd();
        updateForm();
    });

    // handle any input/select changes to update textarea
    $("#search_form").on("change", "select", updateForm);
    $("#search_form").on("keyup", "input", updateForm);


    // initial update of JSON textarea
    updateForm()
    // update form in case case_sensitive changed
    $("#case_sensitive").on("click", function (event) {

    updateForm();

});

});

function addAnd(attribute, operator, value) {
    is_new_query=true;
    let $form = $("#search_form");
    if ($form.children().length > 0) {
        $form.append("<div>AND</div>");
    }
    let $newRow = $andClause.clone();

    $form.append($newRow);
    //set key values and auto complete
    set_query_fields($newRow.children()[0]);

    if (attribute) {
        $(".keyFields", $newRow).val(attribute);
    }
    if (operator) {
        $(".condition", $newRow).val(operator);
    }
    if (value) {
        $(".valueFields", $newRow).val(value);
    }
    return $newRow;
}

function addOr($and, attribute, operator, value) {
    is_new_query=true;
    let $row = $(".form-row", $and).last();
    let $newRow = $row.clone();

    $row.after($newRow);
    //set key values and auto complete
    set_query_fields($newRow[0]);
      if (attribute) {
        $(".keyFields", $newRow).val(attribute);
    }
    if (operator) {
        $(".condition", $newRow).val(operator);
    }
    if (value) {
        $(".valueFields", $newRow).val(value);
    }

}
function load_query() {
    // load JSON from textarea and build form...
    let text = $("#queryJson").val();
    let jsonData = {};
    try {
        jsonData = JSON.parse(text);
    } catch (error) {
        alert("Failed to parse JSON");
        return;
    }
    let query_details = jsonData.query_details;
    if (!query_details) {
        alert("No 'query_details' in JSON");
        return;
    }
    set_the_query(query_details);
    }

function set_the_query(query_details)
{
    let and_filters = query_details.and_filters;
    let or_filters = query_details.or_filters;
    if (!(and_filters || or_filters)) {
        alert("No 'and_filters' or 'or_filters' in 'query_details'");
        return;
    }

    // Start by clearing form...
    $("#search_form").empty();

    // handle ANDs...
    and_filters.forEach(filter => {
        let { name, operator, value } = filter;
        addAnd(name, operator, value);
    });

    // handle ORs...
    or_filters.forEach(or_filter => {
        let $and;
        or_filter.forEach(filter => {
            let { name, operator, value } = filter;
            if (!$and) {
                $and = addAnd(name, operator, value);
            } else {
                addOr($and, name, operator, value);
            }
        });
    });
}

function check_value(_keys_options, attribute)
 {

  _keys_options.value = attribute;
 if (_keys_options.selectedIndex===-1)
 {
 let values=resources_data["image"];
 values.push(attribute);
 }
}

function check_attribute(attribute)
{
//check if the attribute is in the default list, if not it will add it.
var elms = document.querySelectorAll("[id='keyFields']");
for(var i = 0; i < elms.length; i++)
{
check_value(elms[i], attribute);
}
        }


function onRowDoubleClicked(event) {
/* when the user double check a row inisde the grid
it will get he attribute and value pair and set the query builder for using them, then submit a query to get the results*/

  const  rowNode= event.api.getRowNode(event.node.rowIndex);
  let resource=get_resource(rowNode.data.Attribute);
  if (resource===undefined)
        resource='image';

  query["resource"]=resource;
  query_details={};
  query["query_details"]=query_details;
  check_attribute(rowNode.data.Attribute);
  query_details["and_filters"]= [{"name":rowNode.data.Attribute,"value":rowNode.data.Value,"operator":"equals","resource":"image"}];
  query_details["or_filters"]=[];
  set_the_query(query_details);
  query = get_current_query();
  var someTabTriggerEl = document.querySelector('#tabs  #querybuilder_nav a');
  var tab = new bootstrap.Tab(someTabTriggerEl);
  tab.show()
  reset_global_variables();
  $("#myGrid_2").empty();
  document.getElementById("results").style.display='none';
  document.getElementById("reset_results_table_filter").style.display='none';
  submitQuery();
}

function removeAllChildNodes(parentNode) {
    while (parentNode.firstChild) {
        parentNode.removeChild(parentNode.firstChild);
    }
}

function onSortChangedEvent(event)
{
/*
update row index after sorting
*/
  event.api.forEachNode((rowNode,index)=>{ rowNode.rowIndex = index; });
}

function display_value_search_results(results, resource)
   {
   /*
   Dipsly general search results using any value
   */
   if (results["Error"] != undefined )
   {
        alert (results["Error"]);
       $('body').removeClass('wait');
        return;
   }
           if (results["columnDefs"].length>0)
           {
           var searchGridOptions = {
              defaultColDef: {
              resizable: true,
              "filter": true,
              "animateRows":true,
          },
            enableCellTextSelection: true,
            columnDefs: results["columnDefs"],
            rowData: null,
            rowSelection: 'single',
          rowData: null,
          onCellDoubleClicked: onRowDoubleClicked,
          onSortChanged : onSortChangedEvent,


        };
            const searcheGridDiv = document.querySelector('#grid_key_values');
            var myobj = document.getElementById("demo");
            searcheGridDiv.innerHTML ='';
            let search_ag_grid=new agGrid.Grid(searcheGridDiv, searchGridOptions);
            search_ag_grid.gridOptions.api.setRowData(results["results"]);
            search_ag_grid.gridOptions.api.sizeColumnsToFit();
            document.getElementById("help_message").style.display='none';
           document.getElementById('exportsearchResults').style.display = "block";

            $("#exportsearchResults").on("click",  function (event) {

            search_ag_grid.gridOptions.api.exportDataAsCsv(getParams());
               });

              //results["total_number_of_images"], results["total_number_of_buckets"]
             if(results["total_number_of_buckets"]===results["no_buckets"] || results["total_number"]===results["total_number_of_images"] || results["total_number_of_images"] === undefined)
                $('#total_number_in_buckets').text("Number of buckets: "+results["no_buckets"]+", Total number of "+resource+"s: "+results["total_number"]);
            else
                $('#total_number_in_buckets').text("Number of buckets: "+results["no_buckets"]+ " / "+results["total_number_of_buckets"]+", Number of "+resource+"s: "+results["total_number"]+" / "+results["total_number_of_images"]);




    }
    else
    alert("No result is found");
    $('body').removeClass('wait');

   }


  $("#value_field_search_only").on("click",  function (event) {
  /*
  Search  using values provided by the user*/
        event.preventDefault();
        value=$("#value_field").val();
        if (value==null)
        {
        alert("No value is provided ..");
        return;
        }
        query= {"value": $("#value_field").val(), "resource": "image" };
$('body').addClass('wait');
        let resource="image";
        url=searchresourcesvales+ "/?value=" + encodeURIComponent(value)+"&&resource="+ encodeURIComponent(resource);
        fetch(url).then(function(response) {
          {
            response.json().then(function(data) {
                display_value_search_results(data, resource);
                    });
                }
        });

    });

set_tree_events_handller();

/**

**/
  $(function() {

    $('#commonattr').change(function() {


    if ($(this).prop('checked'))
    {
        mode= "searchterms"
        open=true;
    }
    else
    {
        mode="advanced";
        open=false  ;
    }

    url=getresourceskeysusingmode+ "/?mode=" + encodeURIComponent(mode);
    fetch(url).then(function(response) {
      {
        response.json().then(function(data) {
          resources_data=data;
          //$("#jstree_resource_div").jstree("init");
          set_tree_nodes(open);
          $('#jstree_resource_div').jstree("destroy").empty();

create_tree();
set_tree_events_handller ();
update_key_fields();
                });
            }
    });


    })
  })


function update_key_fields(){

const keyFields = document.querySelectorAll('#keyFields');

for (i in keyFields)
{
__keys_options=keyFields[i];
key=__keys_options.value;

 //et __keys_options=container.querySelector(".keyFields");
    optionHtml = '';
    for (const [key, value] of Object.entries(resources_data)) {
            if (value==null)
              {
                __keys_options.innerHTML = optionHtml;
                break;
              }
             value.sort();
            for (i in value) {
                optionHtml += '<option value ="' + value[i] + '">' + value[i] + '</option>'
            }
    }
        __keys_options.innerHTML = optionHtml;
        __keys_options.value=key;
        }
}

function searchforvalue()
{
}