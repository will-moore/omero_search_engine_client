
// global variables declared elsewhere:
// SEARCH_ENGINE_URL
// resources_data
// query_mode

async function load_resources(mode) {
  let url;
  if (mode == "advanced") {
    url = SEARCH_ENGINE_URL + "resources/all/keys/";
  } else {
    url_ = SEARCH_ENGINE_URL + "resources/all/keys/";
    url = url_ + "?mode=" + encodeURIComponent(mode);
  }
  return await fetch(url).then((response) => response.json());
}

function get_resource(key) {
  // e.g. find if 'Antibody' key comes from 'image', 'project' etc
  for (resource in resources_data) {
    if (resources_data[resource].includes(key)) {
      return resource;
    }
  }
}

function get_current_query(form_id = "search_form") {
  console.log("get_current", form_id);
  let and_conditions = [];
  let or_conditions = [];
  //get and condition1

  let queryandnodes = document.querySelectorAll(`#${form_id} .and_clause`);
  console.log("queryandnodes", queryandnodes.length);
  for (let i = 0; i < queryandnodes.length; i++) {
    query_dict = {};

    let node = queryandnodes[i];
    // handle each OR...
    let ors = node.querySelectorAll(".search_or_row");

    let or_dicts = [...ors].map((orNode) => {
      console.log("orNode", orNode);
      return {
        name: orNode.querySelector(".keyFields").value,
        value: orNode.querySelector(".valueFields").value,
        operator: orNode.querySelector(".condition").value,
        resource: get_resource(orNode.querySelector(".keyFields").value),
      };
    });
    console.log("or_dicts", or_dicts);
    if (or_dicts.length > 1) {
      or_conditions.push(or_dicts);
    } else {
      and_conditions.push(or_dicts[0]);
    }
  }

  query_details = {};
  var query = {
    resource: "image",
    query_details: query_details,
  };

  query_details["and_filters"] = and_conditions;
  query_details["or_filters"] = or_conditions;
  query_details["case_sensitive"] =
    document.getElementById("case_sensitive").checked;
  query["mode"] = query_mode;
  return query;
}
