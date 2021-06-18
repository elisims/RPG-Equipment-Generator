Vue.config.devtools = true

Vue.component('c-card', {
  props: [
    'title',
    'text',
    'link',
    'image'
  ],
  data: function() {

  },
  methods: function() {

  },
  template:`
  <div>
    <b-link class="c-card-link" :href="link">
      <b-card align="center" class="c-card-class">
        <i :class="image"></i>
        <b-card-title>{{ title }}</b-card-title>
          <b-card-text>
            {{ text }}
          </b-card-text>
        <b-card-text class="small text-muted"></b-card-text>
      </b-card>
    </b-link>
  <div>
  `
})

Vue.component('login-prompt', {
  props: [],
  data: function() {

  },
  methods: {
    login() { // this should happen when the login button is pressed
      alert("Hello world!");
      if(!this.checkFilledIn()) {
        alert("Please enter both the username and password");
      } else {
        
      }
    },
  checkFilledIn() {
    if (document.getElementById("username").value() == null) {
      return false;
    } else if (document.getElementById("password").value() == null) {
      return false;
    }
    return true;
  }
  },
  template:`
  <form>
    <div>Username:<br/>
      <input type="text" placeholder="Enter Username" name="username" id="username"/>
    </div>
    <br/>
    <div>Password:<br/>
      <input type="password" placeholder="Enter Password" name="password" id="password"/>
    </div>
    <br/>
    <div>
      <input type="button" onclick="login()" value="Login"/>
    </div>
  </form>`
})

Vue.component('signup-prompt', {
  props: [],
  data: function () {

  },
  methods: {
    signup() { // this should happen when the signup button is pressed
      alert("Hello world!");
      if (!this.checkFilledIn()) {
        alert("Please enter information for all the boxes");
      } else {

      }
    },
    checkFilledIn() {
      if(document.getElementById("username").value() == null) {
        return false;
      } else if (document.getElementById("password").value() == null) {
        return false;
      } else if (document.getElementById("firstName").value() == null) {
        return false;
      } else if (document.getElementById("lastName").value() == null) {
        return false;
      } else if (document.getElementById("email").value() == null) {
        return false;
      }
      return true;
    }
  },
  template: `
  <form>
    <div>Username:<br/>
      <input type="text" placeholder="Enter Username" name="username" id="username"/>
    </div>
    <br/>
    <div>Password:<br/>
      <input type="password" placeholder="Enter Password" name="password" id="password"/>
    </div>
    <br/>
    <div>First Name:<br/>
      <input type="text" placeholder="Enter First Name" name="firstName" id="firstName"/>
    </div>
    <br/>
    <div>Last Name:<br/>
      <input type="text" placeholder="Enter Last Name" name="lastName" id="lastName"/>
    </div>
    <br/>
    <div>Email Address:<br/>
      <input type="text" placeholder="Enter Email" name="email" id="email"/>
    </div>
    <br/>
    <div>
      <input type="button" onclick="signup()" value="Sign Up"/>
    </div>
  </form>`
})

Vue.component('c-header', {
  props: [
    'title',
    'text'
  ],
  data: function() {

  },
  methods: {
  },
  template:`
  <span>
    <b-jumbotron 
      style="margin-bottom:0" 
      fluid 
      class="c-jumbo"
    >
      <template v-slot:header>{{ title }}</template>

      <template v-slot:lead>
        {{ text }}
      </template>
    </b-jumbotron>
  <span>
  `
})

Vue.component('c-navbar', {
  props: [],
  data: function() {

  },
  methods: function() {

  },
  template:`
  <span>

    <b-navbar class="c-nav">
      <b-navbar-nav>
        <b-nav-item href="/">Home</b-nav-item>
        <b-nav-item href="/unique_weapon">Generate</b-nav-item>
        <b-nav-item href="/loadouts">Loadouts</b-nav-item>
        <!-- Navbar dropdowns -->
        <b-nav-item-dropdown text="Components" right>
          <b-dropdown-item href="/damage_types">Damage Types</b-dropdown-item>
          <b-dropdown-item href="/weapons">Weapons</b-dropdown-item>
          <b-dropdown-item href="/cultures">Cultures</b-dropdown-item>
          <b-dropdown-item href="/owners">Owners</b-dropdown-item>
          <b-dropdown-item href="/element_types">Element Types</b-dropdown-item>
          <b-dropdown-item href="/status_effects">Status Effects</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
      <b-navbar-nav class="ml-auto">
        <b-nav-item href="/login" align="end">Login</b-nav-item>
        <b-nav-item href="/logout" align="end">Logout</b-nav-item>
        <b-nav-item href="/signup" align="end">Sign Up</b-nav-item>
      </b-navbar-nav>
      
    </b-navbar>

  <span>
  `
})

Vue.component('create-modal', {
  props: [
    'caption',
    'dbTable',
    'api',
    'value_id'
  ],
  data: function() {
    return {
      items: [],
      fields: [],
      input_object: [{}],
      col_exceptions: {},
      api_values: {},
      dropdown_selected: {},
      create_modal_inputs: {},
      inputs_valid: {},
      formState: null
    }
  },
  methods: {
    resetModal() { // this happens on load and close
      this.import_col_exceptions();
      this.get_cols();
    },
    import_col_exceptions(){
      //  col_exceptions = JSON.parse("../json/col_exceptions.json");
      let api = 'api/col_exceptions';
      let ajax_options = {
        type: 'GET',
        url: api,
        accepts: 'application/json',
        dataType: 'json'
      };
      $.ajax(ajax_options)
        .done((data) => {
          // Do stuff
          this.col_exceptions = data;
        })
        .fail((error) => {
          console.log("FAIL", error)
        }).always((data) => {
          // Always do this after everything else
          // console.log("col_exceptions:",this.col_exceptions);
        })
    },
    handleOk(bvModalEvt) {
      // console.log("DEBUG: HandleOk run");
      // Prevent modal from closing
      bvModalEvt.preventDefault()
      // Trigger submit handler
      this.handleSubmit()
    },
    checkFormValidity: function() {
      const valid = this.$refs.form.checkValidity()
      console.log("Valid:",valid)
      this.formState = valid ? 'valid' : 'invalid'
      console.log("Returning valid, formState:", valid, this.formState);
      return valid;
    },
    param_state: function(param) {
      // console.log("DEBUG: param:",param);
      // console.log("DEBUG: inputs:",this.create_modal_inputs);
      if (this.create_modal_inputs[param]){
        if (this.get_col_type(param) == "INTEGER" || this.get_col_type(param) == "REAL")
          return this.create_modal_inputs[param] ? true : false;
      } else {
        return false;
      }
    },
    param_valid: function(param) {
      // console.log("DEBUG: param_valid run");
      let input = this.create_modal_inputs[param];
      let type = "";
      this.items.forEach(element => {
        if (element.col_name == param) 
          type = element.col_type;
      });
      if (type == "text") {
        return input ? input.length > 0 ? true : false : false
      } else if (type == "number") {
        // Check what the min (if any) and max (if any) are
        let min = Number(this.get_key(param, "min"));
        let max = Number(this.get_key(param, "max"));
        if (min && max) {
          if (input >= min && input <= max) {
            return true;
          } else {
            return false;
          }
        } else if (min && !max) {
          return input >= min ? true : false;
        } else if (!min && max) {
          return input <= max ? true : false;
        } else {
          return true;
        }
        // if the number is between min/max then it's valid
      } else {
        return true;
      }
    },
    handleSubmit() {
      // console.log("DEBUG: handleSubmit run");
      // Exit when the form isn't valid
      if (!this.checkFormValidity()) {
        return
      }

      // console.log("DEBUG: Submitted data: ", this.create_modal_inputs);

      // Axios call to submit create  
      const self = this;
      let ajax_options = {
        type: 'POST',
        url: 'api/' + this.api,
        accepts: 'application/json',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(this.create_modal_inputs)
      };
      $.ajax(ajax_options)
      .done(function(data) {
          // $event_pump.trigger('model_create_success', [data]);
        // console.log("DEBUG: Success:", data);
        self.$root.$emit('refresh_table', "data")
      })
      .fail(function(xhr, textStatus, errorThrown) {
          // $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
        console.log("ERROR:", errorThrown);
      })
      .always(function(data) {
      })

      // Hide the modal manually
      this.$nextTick(() => {
        this.$refs.modal.hide()
      })
    },
    get_col_type: function(key) {
      //Returns the type of the column
      // console.log("DEBUG:    Getting type...");
      for (let index = 0; index < this.items.length; index++) {
        const element = this.items[index];
        if (element.col_name == key) {
          // console.log("DEBUG:    FOUND TYPE:", element.col_name, element.col_type);
          return element.col_type;
        }
      }
      // console.log("DEBUG    No type found, defaulting to text", key);
      return "text";
    },
    get_cols: function() {
      // console.log("DEBUG: get_cols run");
      // Gets the columns from the api
      // console.log("Reading columns from api: ", this.api);
      let api = 'api/' + this.api + '/cols';
      let ajax_options = {
        type: 'GET',
        url: api,
        accepts: 'application/json',
        dataType: 'json'
      };
      $.ajax(ajax_options)
        .done((data) => {
          // Do stuff
          this.items = data
        })
        .fail((error) => {
          console.log("FAIL", error)
        }).always((data) => {
          // Always do this after everything else
          let re = "(_|^)(id)$"
          let vars = [];
          let news = this.items;
          let obj = {};
          news.forEach(function(element, index) {
            if (!element.col_name.match(re)) {
              vars.push(element.col_name);
              // console.log(element.col_type);
              // console.log(news[index].col_type);

              // Assigns the correct default value based on the variable type.
              // console.log("DEBUG: ", element.col_name, " is of type ", element.col_type);
              if (element.col_type == "INTEGER" || element.col_type == "REAL") {
                news[index].col_type = "number";
                obj[element.col_name] = 0;
              } else if (element.col_type == "TEXT") {
                news[index].col_type = "text";
                obj[element.col_name] = null;
              } else {
                news[index].col_type = "text";
                obj[element.col_name] = null;
              }
              // Do for every column name
            }
          });
          this.create_modal_inputs = obj;
          this.fields = vars
          this.items = news
          news = {}
          vars.forEach(element => {
            news[element] = null
          });
          this.inputs_valid = news;
        })
    },
    get_key: function(value, key) {
      // console.log("DEBUG: get_key run: value, key:", value, key);
    // Gets a given key from the given value in
    //  the col_exceptions.json file
      if (value in this.col_exceptions) {
        let val = this.col_exceptions[value];
        if (key in val) {
          // console.log(key, "found", val[key]);
          if (val[key] == "dropdown") {
            ref = this.get_key(value, "ref");
            // console.log("DEBUG: dropdown ref:", ref);
            // Get the dropdown values for each menu
            this.get_other_names(ref);
            // set the selected value to the first value in the
            // dropdown_selected.value to the first value in this.
            drop = this.dropdown_selected
            sel = this.api_values
            this.$set(drop, value, "")
            
          }
          return val[key]
        }
      }
      return null
    },
    get_other_names: function(ref_api) {
      // gets all values from a reference api (e.g. cultures)
      if (ref_api in this.api_values)
        return;

      // console.log("DEBUG: get_other_names run: refapi:", ref_api);
      // console.log("Getting",ref_api);
      let api = 'api/' + ref_api;
      let ajax_options = {
        type: 'GET',
        url: api,
        accepts: 'application/json',
        dataType: 'json'
      };
      // console.log("DEBUG: Running GET", api, "with options", ajax_options);
      $.ajax(ajax_options)
        .done((data) => {
          // Do stuff
          console.log("ref_api:",ref_api);
          console.log("api_values:",this.api_values)
          console.log("data:", data)
          // console.log("DEBUG:     Setting api_values to the following:",ref_api, this.get_names_from_objects(data));
          this.$set(this.api_values, ref_api, this.get_names_from_objects(data))
          // this.api_values = data;
        })
        .fail((error) => {
          console.log("FAIL", error)
        }).always((data) => {
          // Always do this after everything else
          // console.log("col_exceptions:",this.col_exceptions);
        })
    },
    create_dropdown_obj: function(data) {
      // Creates an array of objects formatted:
      //  [{ value: 0, text: 'Name' }]

      let arr = [];
      data.forEach((element) => {
        let tmp = {"value": element.id, "text": element.name}
        arr.push(tmp);
      });
      return arr; 
    },
    get_names_from_objects: function(data) {
      // console.log("DEBUG: get_names_from_objects run");
      dat = [];
      data.forEach(element => {
        dat.push({"value": element.id, "text": element.name});
      });
      return dat;
    },
    set_modal_inputs: function(element, val) {
      console.log("setting modal inputs:", element, val);
      this.$set(this.create_modal_inputs, element, val);
    }
  },
  filters: {
    makeReadable: function (value) {
      str = value.replace(/_/g, ' ');
      return str.charAt(0).toUpperCase() + str.slice(1);
    }
  },
  computed: {
    sortedArray: function() {
      function compare(a, b) {
        if (a == 'weapon_class')
          return -1;
        if (a == 'damage_type_primary' && b == 'damage_type_secondary')
          return -1;
        if (b == 'damage_type_primary' && a == 'damage_type_secondary')
          return 1;
        if(a > b && a != 'description')
          return -1;
        if (a < b || a == 'description')
          return 1;
        return 0;
      }
      return this.fields.sort(compare);
    }
  },
  template: `
  <div>
    <b-button variant="success" v-b-modal.create_modal>New</b-button>

    <b-modal
      id="create_modal"
      ref="modal"
      :title="caption"
      @show="resetModal"
      @ok="handleOk"
      size="xl"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit">
        <b-form-group
          invalid-feedback="Value is required"
          :state="formState"
        >            
          <b-table
            :fields="fields"
            :items = "input_object"
            :id="dbTable+'_create_table'"
            caption-top
            stacked
          >
            <template v-slot:table-caption>{{ caption }}</template>
            <template v-slot:cell()="data">
              <div v-if="get_key(data.field.key, 'type')=='dropdown'"> 
                
                <b-form-select
                  :options="api_values[get_key(data.field.key,'ref')]" 
                  v-model="create_modal_inputs[data.field.key]"

                  required
                  :state="param_valid(data.field.key)"
                  ></b-form-select>

              </div>
              <div v-else-if="get_key(data.field.key, 'type')=='range'">
                <b-form-input 
                  type="range" 
                  :min="get_key(data.field.key, 'min')" 
                  :max="get_key(data.field.key, 'max')" 
                  :step="get_key(data.field.key, 'step')"
                  v-model="create_modal_inputs[data.field.key]"
                  required
                  :state="param_valid(data.field.key)"
                  >
                </b-form-input>
                {{data.field.key | makeReadable}}: {{ create_modal_inputs[data.field.key] }}
              </div>
              <div v-else>
                <b-form-input 
                  :placeholder="data.field.key | makeReadable"
                  :id="data.field.key+'_create_input'"
                  :type="get_col_type(data.field.key)"
                  :min="get_key(data.field.key, 'min')" 
                  :max="get_key(data.field.key, 'max')"
                  v-model="create_modal_inputs[data.field.key]"
                  required
                  :state="param_valid(data.field.key)"
                  ></b-form-input>
              </div>
            
            
              </template>
          </b-table>
        </b-form-group>
      </form>
    </b-modal>
  </div>
  `
})

Vue.component('edit-modal', {
  props: [
    'caption',
    'dbTable',
    'api',
    'value_id',
    'selected_values'
  ],
  data: function() {
    return {
      items: [],
      fields: [],
      input_object: [{}],
      col_exceptions: {},
      api_values: {},
      dropdown_selected: {},
      edit_modal_inputs: {},
      inputs_valid: {},
      formState: null
    }
  },
  methods: {
    resetModal() { // this happens on load and close
      this.import_col_exceptions();
      this.get_cols();
    },
    import_col_exceptions(){
      //  col_exceptions = JSON.parse("../json/col_exceptions.json");
      let api = 'api/col_exceptions';
      let ajax_options = {
        type: 'GET',
        url: api,
        accepts: 'application/json',
        dataType: 'json'
      };
      $.ajax(ajax_options)
        .done((data) => {
          // Do stuff
          this.col_exceptions = data;
        })
        .fail((error) => {
          console.log("FAIL", error)
        }).always((data) => {
          // Always do this after everything else
          // console.log("col_exceptions:",this.col_exceptions);
        })
    },
    handleOk(bvModalEvt) {
      // Prevent modal from closing
      bvModalEvt.preventDefault()
      // Trigger submit handler
      this.handleSubmit()
    },
    checkFormValidity: function() {
      const valid = this.$refs.form.checkValidity()
      console.log("Valid:",valid)
      this.formState = valid ? 'valid' : 'invalid'
      return valid
    },
    param_state: function(param) {
      console.log("param:",param);
      console.log("inputs:",this.edit_modal_inputs);
      if (this.edit_modal_inputs[param]){
        if (this.get_col_type(param) == "INTEGER" || this.get_col_type(param) == "REAL")
          return this.edit_modal_inputs[param] ? true : false;
      } else {
        return false;
      }
    },
    param_valid: function(param) {
      let input = this.edit_modal_inputs[param];
      let type = "";
      this.items.forEach(element => {
        if (element.col_name == param) 
          type = element.col_type;
      });
      if (type == "text") {
        return input ? input.length > 0 ? true : false : false
      } else if (type == "number") {
        // Check what the min (if any) and max (if any) are
        let min = Number(this.get_key(param, "min"));
        let max = Number(this.get_key(param, "max"));
        if (min && max) {
          if (input >= min && input <= max) {
            return true;
          } else {
            return false;
          }
        } else if (min && !max) {
          return input >= min ? true : false;
        } else if (!min && max) {
          return input <= max ? true : false;
        } else {
          return true;
        }
        // if the number is between min/max then it's valid
      } else {
        return true;
      }
    },
    handleSubmit() {
      // Exit when the form isn't valid
      if (!this.checkFormValidity()) {
        return
      }
      const self = this;
      // Axios call to submit create
      let ajax_options = {
        type: 'PUT',
        url: 'api/' + this.api + "/" + this.selected_values.id,
        accepts: 'application/json',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(this.edit_modal_inputs)
      };
      $.ajax(ajax_options)
      .done(function(data) {
        // Find a way to send a "refresh" signal to the table(s)
        self.$root.$emit('refresh_table', "data")
      })
      .fail(function(xhr, textStatus, errorThrown) {
          // $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
        console.log("ERROR:", errorThrown);
      })
      .always(function(data) {
        
      })

      // Hide the modal manually
      this.$nextTick(() => {
        this.$refs.edit_modal.hide()
      })
    },
    get_col_type: function(key) {
      //Returns the type of the column
      for (let index = 0; index < this.items.length; index++) {
        const element = this.items[index];
        if (element.col_name == key) {
          return element.col_type;
        }
      }
      return "text";
    },
    get_cols: function() {
      // Gets the columns from the api
      // console.log("Reading columns from api: ", this.api);
      console.log("selected_values:",this.selected_values);
      let api = 'api/' + this.api + '/cols';
      let ajax_options = {
        type: 'GET',
        url: api,
        accepts: 'application/json',
        dataType: 'json'
      };
      $.ajax(ajax_options)
        .done((data) => {
          // Do stuff
          this.items = data
        })
        .fail((error) => {
          console.log("FAIL", error)
        }).always((data) => {
          // Always do this after everything else
          let re = "(_|^)(id)$"
          let vars = [];
          let news = this.items;
          let obj = {};
          let sel = this.selected_values;
          news.forEach(function(element, index) {
            if (!element.col_name.match(re)) {
              vars.push(element.col_name);
              // console.log(element.col_type);
              // console.log(news[index].col_type);
              if (element.col_type == "INTEGER" || element.col_type == "REAL") {
                news[index].col_type = "number";
                // console.log("Looking for",element.col_name,"in",sel)
                if (sel[element.col_name]){
                  // console.log("Found", element.col_name,"in",sel);
                  obj[element.col_name] = sel[element.col_name];
                } else {
                  console.log("Not found",element.col_name,"setting default");
                  obj[element.col_name] = 0;
                }
                
              } else if (element.col_type == "TEXT") {
                news[index].col_type = "text";
                // console.log("Looking for",element.col_name,"in",sel)
                if (sel[element.col_name]){
                  // console.log("Found", element.col_name,"in",sel);
                  obj[element.col_name] = sel[element.col_name];
                } else {
                  console.log("Not found",element.col_name,"setting default");
                  obj[element.col_name] = null;
                }
              } else {
                news[index].col_type = "text";
                // console.log("Looking for",element.col_name,"in",sel)
                if (sel[element.col_name]){
                  // console.log("Found", element.col_name,"in",sel);
                  obj[element.col_name] = sel[element.col_name];
                } else {
                  console.log("Not found",element.col_name,"setting default");
                  obj[element.col_name] = null;
                }
              } 
              // Do for every column name
            }
          });
          this.edit_modal_inputs = obj;
          this.fields = vars
          this.items = news
          news = {}
          vars.forEach(element => {
            news[element] = null
          });
          this.inputs_valid = news;
        })
    },
    get_key: function(value, key) {
    // Gets a given key from the given value in
    //  the col_exceptions.json file
      if (value in this.col_exceptions) {
        let val = this.col_exceptions[value];
        if (key in val) {
          // console.log(key, "found", val[key]);
          if (val[key] == "dropdown") {
            ref = this.get_key(value, "ref");
            // Get the dropdown values for each menu
            this.get_other_names(ref);
            // set the selected value to the first value in the
            // dropdown_selected.value to the first value in this.
            drop = this.dropdown_selected
            sel = this.api_values
            this.$set(drop, value, "")
            
          }
          return val[key]
        }
      }
      return null
    },
    get_other_names: function(ref_api) {
      if (ref_api in this.api_values)
        return;
      // console.log("Getting",ref_api);
      let api = 'api/' + ref_api;
      let ajax_options = {
        type: 'GET',
        url: api,
        accepts: 'application/json',
        dataType: 'json'
      };
      $.ajax(ajax_options)
        .done((data) => {
          // Do stuff
          console.log("ref_api:",ref_api);
          console.log("api_values:",this.api_values)
          console.log("data:", data)
          this.$set(this.api_values, ref_api, this.get_names_from_objects(data))
          // this.api_values = data;
        })
        .fail((error) => {
          console.log("FAIL", error)
        }).always((data) => {
          // Always do this after everything else
          // console.log("col_exceptions:",this.col_exceptions);
        })
    },
    get_names_from_objects: function(data) {
      dat = [];
      data.forEach(element => {
        dat.push(element.name);
      });
      return dat;
    },
    set_modal_inputs: function(element, val) {
      this.$set(this.edit_modal_inputs, element, val)
    }
  },
  filters: {
    makeReadable: function (value) {
      str = value.replace(/_/g, ' ');
      return str.charAt(0).toUpperCase() + str.slice(1);
    }
  },
  computed: {
    sortedArray: function() {
      function compare(a, b) {
        if (a == 'weapon_class')
          return -1;
        if (a == 'damage_type_primary' && b == 'damage_type_secondary')
          return -1;
        if (b == 'damage_type_primary' && a == 'damage_type_secondary')
          return 1;
        if(a > b && a != 'description')
          return -1;
        if (a < b || a == 'description')
          return 1;
        return 0;
      }
      return this.fields.sort(compare);
    }
  },
  template: `
  <div>
    <b-button v-b-modal.edit_modal>Edit Selected</b-button>

    <b-modal
      id="edit_modal"
      ref="edit_modal"
      :title="caption"
      @show="resetModal"
      @ok="handleOk"
      size="xl"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit">
        <b-form-group
          invalid-feedback="Value is required"
          :state="formState"
        >
          <b-button @click="">Test Modal</b-button>
            
          <b-table
            :fields="fields"
            :items = "input_object"
            :id="dbTable+'_create_table'"
            caption-top
            stacked
          >
            <template v-slot:table-caption>{{ caption }}</template>
            <template v-slot:cell()="data">
              <div v-if="get_key(data.field.key, 'type')=='dropdown'"> 
                <b-form-select
                  :options="api_values[get_key(data.field.key,'ref')]" 
                  v-model="edit_modal_inputs[data.field.key]"
                  required
                  :state="param_valid(data.field.key)"
                  ></b-form-select>

              </div>
              <div v-else-if="get_key(data.field.key, 'type')=='range'">
                <b-form-input 
                  type="range" 
                  :min="get_key(data.field.key, 'min')" 
                  :max="get_key(data.field.key, 'max')" 
                  :step="get_key(data.field.key, 'step')"
                  v-model="edit_modal_inputs[data.field.key]"
                  required
                  :state="param_valid(data.field.key)"
                  >
                </b-form-input>
                {{data.field.key | makeReadable}}: {{ edit_modal_inputs[data.field.key] }}
              </div>
              <div v-else>
                <b-form-input 
                  :placeholder="data.field.key | makeReadable"
                  :id="data.field.key+'_create_input'"
                  :type="get_col_type(data.field.key)"
                  :min="get_key(data.field.key, 'min')" 
                  :max="get_key(data.field.key, 'max')"
                  v-model="edit_modal_inputs[data.field.key]"
                  required
                  :state="param_valid(data.field.key)"
                  ></b-form-input>
              </div>
            
            
              </template>
          </b-table>
        </b-form-group>
      </form>
    </b-modal>
  </div>
  `
})

Vue.component('db-table', {
  props: [
    'caption',
    'dbTable',
    'api'
  ],
  data: function() {
    return {
      fields: [],
      items: [],
      selected: [],
      confirm: ""
    }
  },
  methods: {
    onRowSelected(items) {
      this.selected = items
    },
    show_confirm_box: function(text="Are you sure?") {
      this.confirm = '';
      this.$bvModal.msgBoxConfirm(text)
      .then(value => {
        this.confirm = value;
      })
      .catch(err => {
        console.log("Error", err);
      })
    },
    read_items: function () {
      this.items = [];
      // console.log("Reading from table");
      let api = 'api/' + this.api;
      let ajax_options = {
        type: 'GET',
        url: api,
        accepts: 'application/json',
        dataType: 'json'
      };
      // console.log(ajax_options);
      $.ajax(ajax_options)
        .done((data) => {
          for (var key in data) {
            console.log("DEBUG:",data);
            this.items.push(data[key])
            console.log("DEBUG:",this.items[key])
            // this.$set(this.items[key], newPsgId, newObj)
          }
        })
        .fail((error) => {
          console.log("FAIL", error)
        }).always((data) => {
          this.get_fields();
        })
      
    },
    get_fields: function() {
      let re = "(_|^)(id)$"
      for (key in this.items[0]) {
        if (!key.match(re))
        this.fields.push(key);
      }
    },  
    sort_fields: function() {
      //Sorts the fields array
    },
    delete_item: function() {
      if (this.selected.length == 0) {
        console.log("No delete selected");
        return;
      }
      let sel = this.selected[0];
      let id = sel.id;
      let text = "Are you sure you want to delete " + sel.name + "?";
      const self = this;
      this.confirm = '';
      this.$bvModal.msgBoxConfirm(text)
      .then(value => {
        // console.log("Value:",value);
        this.confirm = value;
        // this.show_confirm_box(text);
        if (this.confirm) {
          // console.log("Deleting");
          //Delete item with id
          let ajax_options = {
            type: 'DELETE',
            url: 'api/' + this.api + "/" + id,
            accepts: 'application/json',
            contentType: 'plain/text'
          };
          $.ajax(ajax_options)
          .done(function(data) {
              // $event_pump.trigger('model_delete_success', [data]);
              // console.log("Complete:",data);
              self.refresh_table();
          })
          .fail(function(xhr, textStatus, errorThrown) {
              // $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
              console.log("Error:", errorThrown);
          })
        } else {
          console.log("Cancelling request");
        }
      })
      .catch(err => {
        console.log("Error", err);
      })
      
    },
    refresh_table: function() {
      this.read_items();
      this.$root.$emit('bv::refresh::table', 'table')
    }
  },
  mounted: function() {
    this.$root.$on('refresh_table', (data) => {
      this.refresh_table();
    })
  },
  created: function() {
    this.read_items()
  },
  filters: {
    makeReadable: function (value) {
      str = value.replace(/_/g, ' ');
      return str.charAt(0).toUpperCase() + str.slice(1);
    }
  },
  computed: {
    sortedArray: function() {
      function compare(a, b) {
        if (a == 'weapon_class')
          return -1;
        if (a == 'damage_type_primary' && b == 'damage_type_secondary')
          return -1;
        if (b == 'damage_type_primary' && a == 'damage_type_secondary')
          return 1;
        if(a > b && a != 'description')
          return -1;
        if (a < b || a == 'description')
          return 1;
        return 0;
      }
      return this.fields.sort(compare);
    }
  },
  template: `
  <div class="c-table-container">
  <b-container class="c-button-container">
    <b-row class="justify-content-md-left">
      <b-col cols=4 md="auto">
          <create-modal 
            :caption="'Create'+ this.caption" 
            :api="this.api" 
            :dbTable="this.db_table">
          </create-modal>
      </b-col>
      <b-col cols=4 md="auto">
        <span v-if="selected.length > 0">
          <edit-modal 
            :caption="'Create'+ this.caption" 
            :api="this.api" 
            :dbTable="this.db_table" 
            :selected_values="this.selected[0]">
          </edit-modal>
        </span>
      </b-col>
      <b-col cols=4 md="auto">
        <span v-if="selected.length > 0">
          <b-button 
            @click="delete_item" 
            variant="danger">
          Delete Selected Item
          </b-button>
        </span>
      </b-col>
  </b-container>
    <b-table 
      :items="items" 
      :fields="fields" 
      :sort-compare="sortedArray" 
      :id="dbTable+'_table'" 
      class="c-table"
      ref="table"
      caption-top
      selectable
      select-mode='single' 
      @row-selected="onRowSelected"
      style="margin-top:16px"
      table-variant="secondary"
    >
      <template v-slot:table-caption>{{ caption }}</template>
      <template v-slot:cell()="data">

        <div v-show = "data.edit == false">
          <label @dblclick = "data.edit = true"> {{ data.value }} </label>
        </div>

        <input v-show = "data.edit == true" v-model = "data.value"
            v-on:blur= "data.edit=false; $emit('update')"
            @keyup.enter = "data.edit=false; $emit('update')">
        
        <b>{{ data.value }} </b>
     
      </template>
    </b-table>
    <i>Selected: {{selected.length > 0 ? selected[0].name : "" }}</i>
  </div>
  `
})

new Vue({
  el: '#app',
  delimiters: ["[[", "]]"],
  data: {
    rand_item: {},
    caption: "Caption goes here",
    dbTable: "owners"
  },
  components: {

  },
  mounted: function () {
    
  },
  created: function() {
    var urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('caption')){
      console.log("Found caption in query string");
      this.caption = urlParams.get('caption');
    }
    if (urlParams.has('table')) {
      console.log("Found table in query string");
      this.dbTable = urlParams.get('table');
    }
  },
  methods: {
    get_random_item: function() {
      this.rand_item = "";
      // console.log("Reading from table");
      let api = 'api/get_random_item';
      let ajax_options = {
        type: 'GET',
        url: api,
        accepts: 'application/json',
        dataType: 'json'
      };
      // console.log(ajax_options);
      $.ajax(ajax_options)
        .done((data) => {
          this.rand_item = data
          }
        )
        .fail((error) => {
          console.log("FAIL", error)
        }).always((data) => {
        })
    },
    add_to_database: function() {
      // Create an object that can be passed to the database 
      // to make a unique item
      item_to_add = this.rand_item;
      let tp = this.rand_item.item_type;
      delete item_to_add.item_type;
      if (tp == 'weapon')
        tp = 'weapons';
      let api = 'api/unique_'+tp;
      console.log("api:",api);
      let ajax_options = {
        headers: { 
          'Accept': 'application/json',
          'Content-Type': 'application/json' 
       },
        type: 'POST',
        url: api,
        accepts: 'application/json',
        dataType: 'json',
        data: JSON.stringify(item_to_add,function(k, v) { return v === null ? null : v; })
      };
      console.log("DATA:", ajax_options);
      $.ajax(ajax_options)
      .done(function(data) {
          // $event_pump.trigger('model_create_success', [data]);
        // console.log("DEBUG: Success:", data);
        console.log("Added to backpack", data);
      })
      .fail(function(xhr, textStatus, errorThrown) {
          // $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
        console.log("ERROR:", errorThrown);
        
      })
      .always(function(data) {
      })
    }
  },
  filters: {
    makeReadable: function (value) {
      str = value.replace(/_/g, ' ');
      return str.charAt(0).toUpperCase() + str.slice(1);
    }
  },
  computed: {
    
  }
})