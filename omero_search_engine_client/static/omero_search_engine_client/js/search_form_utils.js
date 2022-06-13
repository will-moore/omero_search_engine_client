const AND_CLAUSE_HTML = `
<div class="and_clause">
  <div class="search_or_row">
    <div class="or">OR</div>
    <div class="search_key">
        <label for="keyFields">Attribute</label>
        <select id="keyFields" class="form-control keyFields">
        </select>
    </div>
    <div class="search_condition">
        <label for="condition">Operator</label>
        <select id="condition" class="form-control condition">
          <option value="equals">equals</option>
          <option value="not_equals">not equals</option>
          <option value="contains">contains</option>
          <option value="not_contains">not contains</option>
        </select>
    </div>
    <div class="search_value" style="position: relative">
        <label for="valueFields">Value</label>
        <input type="text" class="form-control valueFields" id="valueFields" placeholder="type the attribute value">
    </div>
    <div class="or">
        <button class="remove_row btn btn-sm btn-outline-danger">
          X
        </button>
    </div>
  </div>
  <a class="addOR" href="#" title="Add OR condition to the group">
    add 'OR'...
  </a>
</div>`;

const FORM_FOOTER_HTML = `
<div>
<button id="addAND" type="button" class="no-border" title="Add an 'AND' clause to the query">
  add AND...
</button>
<label class="form-check-label" for="case_sensitive">
  Case sensitive:
  <input class="form-check-input" type="checkbox" value="" id="case_sensitive" />
</label>
<button id="doElasticSearch">Search</button>
</div>
`

class OmeroSearchForm {
  constructor(formId, SEARCH_ENGINE_URL) {
    this.SEARCH_ENGINE_URL = SEARCH_ENGINE_URL;
    this.resources_data = {};
    this.query_mode = "searchterms";
    this.cached_key_values = {};
    this.autoCompleteCache = {};

    // build form
    this.$form = $(`#${formId}`);
    this.$form.html(AND_CLAUSE_HTML);
    this.$form.append($(FORM_FOOTER_HTML));

    // auto-complete (for the first row in the form)
    this.initAutoComplete($(".and_clause"));
    // load Keys and add to keyField of first row
    this.loadResources("searchterms", $(".and_clause"));
  }

  async loadResources(mode = "searchterms", $updateElement) {
    let url;
    if (mode == "advanced") {
      url = this.SEARCH_ENGINE_URL + "resources/all/keys/";
    } else {
      url = this.SEARCH_ENGINE_URL + "resources/all/keys/";
      url = url + "?mode=" + encodeURIComponent(mode);
    }
    this.resources_data = await fetch(url).then((response) => response.json());
    if (this.resources_data.error != undefined) {
      alert(this.resources_data.error);
    }

    // option to update UI...
    if ($updateElement) {
      this.setKeyValues($updateElement);
    }

    return this.resources_data;
  }

  findResourceForKey(key) {
    // e.g. find if 'Antibody' key comes from 'image', 'project' etc
    for (let resource in this.resources_data) {
      if (this.resources_data[resource].includes(key)) {
        return resource;
      }
    }
  }

  getCurrentQuery(form_id = "search_form") {
    let and_conditions = [];
    let or_conditions = [];
    //get and condition1

    let queryandnodes = document.querySelectorAll(`#${form_id} .and_clause`);
    for (let i = 0; i < queryandnodes.length; i++) {
      let node = queryandnodes[i];
      // handle each OR...
      let ors = node.querySelectorAll(".search_or_row");

      let or_dicts = [...ors].map((orNode) => {
        return {
          name: orNode.querySelector(".keyFields").value,
          value: orNode.querySelector(".valueFields").value,
          operator: orNode.querySelector(".condition").value,
          resource: this.findResourceForKey(orNode.querySelector(".keyFields").value),
        };
      });
      if (or_dicts.length > 1) {
        or_conditions.push(or_dicts);
      } else {
        and_conditions.push(or_dicts[0]);
      }
    }

    let query_details = {};
    var query = {
      resource: "image",
      query_details: query_details,
    };

    query_details["and_filters"] = and_conditions;
    query_details["or_filters"] = or_conditions;
    query_details["case_sensitive"] =
      document.getElementById("case_sensitive").checked;
    query["mode"] = this.query_mode;
    return query;
  }

  setKeyValues($orClause) {
    // Adds <option> to '.keyFields' for each item in pre-cached resources_data
    let $field = $(".keyFields", $orClause);
    let anyOption = `<option value="Any">Any</option>`;
    let html = Object.entries(this.resources_data).map((keyValues) => {
      keyValues[1].sort();
      return keyValues[1].map(value => `<option value="${value}">${value}</option>`).join("\n");
    }).join("\n");
    $field.html(anyOption + html);
  }

  initAutoComplete($orClause) {
    let self = this;
    let $this = $(".valueFields", $orClause);
    // key is updated when user starts typing, also used to handle response and select
    let key;
    $this
      .autocomplete({
        autoFocus: false,
        delay: 1000,
        source: function (request, response) {
          // Need to know what Attribute is of adjacent <select>
          key = $(".keyFields", $orClause).val();
          console.log("key...", key);
          let url = `${SEARCH_ENGINE_URL}resources/image/getannotationvalueskey/?key=${encodeURI(
            key
          )}&resource=image`;

          // If possible values for current Key are cached...
          if (self.autoCompleteCache[key]) {
            let input = request.term.toLowerCase();
            let results = self.autoCompleteCache[key].filter((term) =>
              term.toLowerCase().includes(input)
            );
            response(results);
            return;
          }
          // ...otherwise we need AJAX call...
          // 'Any' uses different query
          if (key == "Any") {
            url = `${SEARCH_ENGINE_URL}resources/image/searchvalues/?value=${encodeURI(
              request.term
            )}&resource=image`;
          }
          // showSpinner();
          $.ajax({
            dataType: "json",
            type: "GET",
            url: url,
            success: function (data) {
              // hideSpinner();
              console.log(data);
              let results = [{ label: "No results found.", value: -1 }];
              if (key == "Any" && data.data.length > 0) {
                results = data.data.map((result) => {
                  return {
                    key: result.Key,
                    label: `<b>${result.Value}</b> (${result.Key}) <span style="color:#bbb">${result["Number of images"]}</span>`,
                    value: `${result.Value}`,
                  };
                });
              } else {
                // cache for future use
                self.autoCompleteCache[key] = data;
                // We need to filter by input text
                let input = request.term.toLowerCase();
                results = data.filter((term) =>
                  term.toLowerCase().includes(input)
                );
              }
              response(results);
            },
            error: function (data) {
              console.log("ERROR", data);
              // hideSpinner();
              response([{ label: "Failed to load", value: -1 }]);
            },
          });
        },
        minLength: 3,
        open: function () {},
        close: function () {
          // $(this).val('');
          return false;
        },
        focus: function (event, ui) {},
        select: function (event, ui) {
          console.log("select", ui.item, key == "Any");
          if (ui.item.value == -1) {
            // Ignore 'No results found'
            return false;
          }
          if (key == "Any") {
            // Use 'key' to update KeyField
            self.setKeyField($orClause, ui.item.key);
          }
          return true;
        },
      })
      .data("ui-autocomplete")._renderItem = function (ul, item) {
      return $("<li>")
        .append("<a style='font-size:14px; width:245px'>" + item.label + "</a>")
        .appendTo(ul);
    };
  }

  setKeyField($parent, key) {
    // Adds the Key as an <option> to the <select> if not there;
    let $select = $(".keyFields", $parent);
    if ($(`option[value='${key}']`, $select).length == 0) {
      $select.append($(`<option value="${key}">${key}</option>`));
    }
    $select.val(key);
  }
}
