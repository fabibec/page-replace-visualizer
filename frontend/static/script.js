function updateSliderValue(sliderID, valueID){
  let length = document.getElementById(sliderID).valueAsNumber;
  document.getElementById(valueID).innerHTML = '<b>' + length + '</b>';
}

function toggleAllCheckboxes(source, destName) {
  for (i = 0; i < document.getElementsByName(destName).length; i++)
      document.getElementsByName(destName)[i].checked = source.checked;
}

function init(){
  updateSliderValue('refStrSize', 'refStrSizeValue');
  updateSliderValue('faultsFrameSize', 'FrameSizeValue');
  updateSliderValue('memoryFrameSize', 'memoryFrameSizeValue');
}

init();
