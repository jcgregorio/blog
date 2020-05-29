
function createXMLHttpRequest() {
    try { return new XMLHttpRequest(); } catch(e) {}
    try { return new ActiveXObject("Msxml2.XMLHTTP"); } catch (e) {}
    try { return new ActiveXObject("Microsoft.XMLHTTP"); } catch (e) {}
    return null;
}

// Utility function (gets around the problem of 'this' being a keyword).
function bindTo(o, f) {
    return function() {
        return f.apply(o, arguments)
    }
}

Collection = function(url) {
    this.url = url;
    this.xhReq = createXMLHttpRequest();
    this.xhReq.open("GET", this.url, false);
    this.xhReq.send(null);
    this.coll = eval('(' + this.xhReq.responseText + ')'); 
    this.members = this.coll['members'];
    // Index full_members by members.href to keep things independent 
    // (so things don't break when we add/remove elements.)
    this.full_members = new Array(); 
    this.status = document.getElementById('status');
}


Collection.prototype = {
    set_status: function(message) {
       this.status.innerHTML = message; 
       this.status.style.background = "#FF0"; 
       this.status.myfade = 0;
       status = this.status;
         
       function dofade() {
         arguments.callee.index += 1;
         color = arguments.callee.index;
         if (color < 16) {
             status.style.background = "#FF" + color.toString(16);
             setTimeout(dofade, 100);
         }
       }
       dofade.index = 0;
       setTimeout(dofade, 100);
    },
    
    refresh: function() {
        this.xhReq.open("GET", this.url, false);
        this.xhReq.send(null);
        this.coll = eval('(' + this.xhReq.responseText + ')'); 
        this.members = this.coll['members'];
    },

    cached_repr: function(n) {
        return this.full_members[this.members[n].href];
    },

    get: function(n, callback) {
         if (n < this.members.length) {
             href = this.members[n].href;
             if (this.full_members[href]) {
                 // Really need to do ETag checking at this point.
                 callback(this.full_members[href], true);
             } else {
                 this.set_status("Retrieving...");
                 xhReq = this.xhReq;
                 xhReq.open("GET", this.url + href, false);
                 xhReq.send(null);
                 repr = eval('(' + xhReq.responseText + ')'); 
                 success = xhReq.status <= 299;
                 callback(repr, success);
                 if (success) {
                    this.full_members[href] = repr;
                 }
                 this.set_status("Retrieved");
             }
         } else {
            callback(null, false);
         }
     },

     put: function(n, struct, callback) {
         repr = serializeJSON(json);
         xhReq = this.xhReq;
         xhReq.open("PUT", this.url + this.members[n].href, false);
         xhReq.send(repr);
         callback();
         delete this.full_members[this.members[n].href];
         this.set_status("Updated");
     },

     remove: function(n, callback) {
        if (this.members[n]) {
            this.xhReq.open("DELETE", 
               this.url + this.members[n].href, false);
            this.xhReq.send(null);
            this.refresh();
            this.set_status("Deleted");
            callback();
        }
     },

     create: function(struct, callback) {
         repr = serializeJSON(json);
         xhReq = this.xhReq;
         xhReq.open("POST", this.url, false);
         xhReq.send(repr);
         this.set_status("Created");
         this.refresh();
         callback();
     }
}

function Cookbook(url) {
    this.selected_index = -1;
    this.collection = new Collection(url);
    this.titles = new Array();
    this.instructions = document.getElementById('instructions');
    this.title = document.getElementById('title');
    this.update = document.getElementById('update');
    this.remove = document.getElementById('delete');
    this.create = document.getElementById('create');
}

Cookbook.prototype = {
    setup: function() {
        this.update.onclick = bindTo(this, this.update_on_click);
        this.create.onclick = bindTo(this, this.create_on_click);
        this.remove.onclick = bindTo(this, this.remove_on_click);
        for (var i=0; i<5; i++) {
            var title = document.getElementById('p' + i);
            title.onclick = bindTo(this, this.title_on_click(i));
            this.titles.push(title);
        }
    },

    title_on_click: function(index) {
        return function(event) {
            for (title in this.titles) {
                this.titles[title].style.background = "#FFF";
            }
            this.titles[index].style.background = "#DDD";
            this.selected_index = index;
            this.instructions.value = "...retrieving...";
            this.collection.get(index, 
              bindTo(this, 
                function(json, success) { 
                  if (success) {
                    this.instructions.value = json.instructions; 
                    this.title.value = json.title; 
                  } else {
                    this.instructions.value = " "; 
                    this.title.value = " "; 
                    this.titles[index].style.background = "#FFF";
                    this.titles[index].innerHTML = "&nbsp;";
                    this.collection.set_status("Failed to retrieve");
                  }
                }
              )
            );
            return false;
        }
    },

    update_on_click: function() {
        if (this.selected_index > -1) {
            json = this.collection.cached_repr(this.selected_index);
            json.instructions = this.instructions.value;
            json.title = this.title.value;
            self = this;
            this.collection.put(this.selected_index, json, function () {
                    self.populate_list(false);
                    });
        }
        return false;
    },

    create_on_click: function() {
       json = {};
       json.instructions = this.instructions.value;
       json.title = this.title.value;
       if (json.title.length > 0) {
          this.collection.create(json, bindTo(this, function () {
               this.instructions.value = "";                    
               this.title.value = "";
               this.titles[this.selected_index].style.ackground = "#FFF";
               this.selected_index = -1;
               this.populate_list(false);
               }));
       } else {
           alert("The Title must be non-empty");
       }
       return false;
    },

    remove_on_click: function() {
       if (this.selected_index > -1) {
           this.collection.remove(this.selected_index, 
             bindTo(this, 
               function () {
                 this.populate_list(false);
                 this.titles[this.selected_index].style.ackground = "#FFF";
                 this.instructions.value = "";                    
                 this.title.value = "";
                 this.selected_index = -1;
               }
             )
           );
       }
       return false;
    },

    populate_list: function(skip_title_text) {
        for (i=0; i<this.titles.length; i++) {
            if (!skip_title_text) {
                this.collection.get(i, 
                  bindTo(this, 
                    function(json, success) { 
                        if (success) { 
                            this.titles[i].innerHTML = json.title 
                        } else {
                            this.titles[i].innerHTML = "&nbsp;" 
                        }
                    }
                  )
                );
            }
            this.titles[i].style.ackground = "#FFF";
        }
    }
}

window.onload = function () {
    cookbook = new Cookbook("json/");
    cookbook.setup();
    cookbook.populate_list(true);
};
