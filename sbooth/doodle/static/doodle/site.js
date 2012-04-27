function handleDragEnd (e) {
  var t = parseInt($("#facehair").css('top').replace('px', ''));
  var l = parseInt($("#facehair").css('left').replace('px', ''));
  
  t = t + (e.y - start.y);
  l = l + (e.x - start.x);
  
  $("#facehair").css('top', t + 'px');
  $("#facehair").css('left', l + 'px');
  
  this.style.opacity = '1';
  l = l - 150;
  document.getElementById("id_coord").value = l + ',' + t;
}

var start;
function handleDragStart (e) {
  // Target (this) element is the source node.
  this.style.opacity = '0.4';

  dragSrcEl = this;

  e.dataTransfer.effectAllowed = 'move';
  
  start = e;
}

function load_webcam () {
    var video = document.getElementById('live');
    if (navigator.webkitGetUserMedia) {
        navigator.webkitGetUserMedia('video',
            function(stream) { video.src = webkitURL.createObjectURL(stream); },
            function(error) { alert('ERROR: ' + error.toString()); } );
            
        var facehair = document.getElementById("facehair");
        facehair.addEventListener('dragend', handleDragEnd, false);
        facehair.addEventListener('dragstart', handleDragStart, false);
        
    } else {
        $("#flag_alert").css('display', 'block');
        alert('webkitGetUserMedia not supported');
    }
}

function snap() {
  var live = document.getElementById("live");
  var snapshot = document.getElementById("snapshot");

  // Make the canvas the same size as the live video
  snapshot.width = live.clientWidth;
  snapshot.height = live.clientHeight;

  // Draw a frame of the live video onto the canvas
  c = snapshot.getContext("2d");
  c.drawImage(live, 0, 0, snapshot.width, snapshot.height);
  
  $('#snapshot').css('display', 'block');
  $('#postsnap').css('display', 'block');
  
  $('#live').css('display', 'none');
  $('#presnap').css('display', 'none');
}

function reset () {
  $('#snapshot').css('display', 'none');
  $('#postsnap').css('display', 'none');
  
  $('#live').css('display', 'block');
  $('#presnap').css('display', 'block');
  
  return false;
}

function upload () {
  var snapshot = document.getElementById("snapshot");
  var img_data = snapshot.toDataURL("image/png").split(',')[1];
  
  var name = document.getElementById("id_name").value;
  
  if (name == '') {
    alert('Please fill in a name of some sort!');
    return false;
  }
  
  document.getElementById("id_imgdata").value = img_data;
  document.getElementById("upload_form").submit();
  return false;
}
