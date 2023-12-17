function flagRefStrInptField(){
  let el = refStrInpt;
  let msg = document.getElementById('refStrInptMsg');
  if (el.value) {
    el.parentElement.classList.add('has-success');
    el.parentElement.classList.remove('has-error');
    msg.style.display = 'none';
  } else {
    el.parentElement.classList.remove('has-success');
    el.parentElement.classList.add('has-error');
    msg.style.display = 'block';
  }
}

// Updating RefString Slider
function updateSliderValue(sliderID, valueID){
  let length = document.getElementById(sliderID).valueAsNumber;
  document.getElementById(valueID).innerHTML = '<b>' + length + '</b>';
}

// Test
function noEnter() {
  return !(window.event && window.event.keyCode == 13); 
}

function init(){
  updateSliderValue('refStrSize', 'refStrSizeValue');
  updateSliderValue('faultsFrameSize', 'FrameSizeValue');
  updateSliderValue('memoryFrameSize', 'memoryFrameSizeValue');
}

init();