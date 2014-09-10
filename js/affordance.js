function on_check(name, value){
  if(value){
    
  var request = new ROSLIB.ServiceRequest({
    affordance : name,
    add : true
  });

  service1.callService(request, function(result) {
    console.log('Result for service call on '
      + service1.name
      + ': '
      + result.success);
      
    setup_ee_box(result.ids, result.end_effectors, result.num_points);
  });
  }
}

var buttons = {"start":"GO_TO_START", "left":"PLAY_BACKWARD", "rwnd":"STEP_BACKWARD", "right":"PLAY_FORWARD", "ffwd":"STEP_FORWARD", "pause":"PAUSE", "end": "GO_TO_END"};

function make_buttons()
{
    var path = "https://raw.githubusercontent.com/swhart115/affordance_templates/develop/rviz_affordance_template_panel/resources/"
    
    var s = "";
    for(b in buttons){
        s += "<img src=\"" + path + b + ".png\" width=\"50px\" onclick=\"button('" + buttons[b] + "')\" />\n";

    }
    document.getElementById("controls").innerHTML = s;
}

function populate_affordances(id, elements)
{
    document.getElementById(id).innerHTML = '';
    for(i in elements){
        var element = elements[i];
        // create the necessary elements
        var label= document.createElement("label");
        var description = document.createTextNode(element);
        var checkbox = document.createElement("input");

        checkbox.type = "checkbox";    // make the element a checkbox
        checkbox.name = element;       // give it a name we can check on the server side
        checkbox.value = element;      // make its value element
        checkbox.onclick=function() { on_check(this.name, this.checked); };

        label.appendChild(checkbox);   // add the box to the element
        label.appendChild(description);// add the description to the element

        // add the label element to your div
        document.getElementById(id).appendChild(label);
    }
}

var ees = [];

function button(s) {
    var steps = parseInt(document.getElementById('steps').value);
    var eop = document.getElementById('execute').checked;
    chosen_ees = [];
    
    for(i=0;i<ees.length;i++){
      if(document.getElementById('ee_opt_' + ees[i]).checked){
        chosen_ees.push(ees[i]);
      }
    }
     
    var request = new ROSLIB.ServiceRequest({
      affordances : ['Wheel'],
      ids : [0],
      type: s, 
      end_effectors: chosen_ees,
      steps: steps, 
      execute: eop
    });

    service2.callService(request, function(result) {
      console.log('Result for service call on '
        + service2.name
        + ': '
        + result.success);
      update_ee_box(result.ids, result.waypoints);  
      } 
      , function(err) { console.log('Err ' + err); });

}

function setup_ee_box(ids, end_effectors, num_points) {
    s = "<table><tr><th><th>name<th>@wp<th>#wps<th>cmd";
    for (i = 0; i < ids.length; i++) { 
        s += "<tr><td>" + ids[i] + "<td>" + end_effectors[i] + "<td id=\"ee_n_" + ids[i] + "\">X</td><td>" + num_points[i];
        s += "<td><input name=\"ee_opt_" + end_effectors[i] + "\" id=\"ee_opt_" + end_effectors[i] + "\" type=\"checkbox\" checked=\"checked\" />";
    }
    s += "</table>";
    ees = end_effectors;
    document.getElementById("ee_box").innerHTML = s;
}

function update_ee_box(ids, waypoints) {
    for(var i=0; i<ids.length; i++){
        var x = document.getElementById("ee_n_" + ids[i]);
        x.innerHTML = waypoints[i];
        
    }
}
