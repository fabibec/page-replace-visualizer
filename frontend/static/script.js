function updateSliderValue(sliderID, valueID){
  let length = document.getElementById(sliderID).valueAsNumber;
  document.getElementById(valueID).innerHTML = '<b>' + length + '</b>';
}

function toggleAllCheckboxes(source, destName) {
  for (i = 0; i < document.getElementsByName(destName).length; i++)
      document.getElementsByName(destName)[i].checked = source.checked;
}

function onFaultCheckboxClick(destName) {
    onCheckboxClick('checkAllFaults', destName);
}
function onFaultRangeCheckboxClick(destName) {
    onCheckboxClick('checkAllFaultsRange', destName);
}
function onCheckboxClick(checkboxId, destName) {
    for (i = 0; i < document.getElementsByName(destName).length; i++) {
        if(!document.getElementsByName(destName)[i].checked){
          document.getElementById(checkboxId).checked = false;
          return;
        }
    }
    document.getElementById(checkboxId).checked = true;
}

function init(){
  updateSliderValue('refStrSize', 'refStrSizeValue');
  updateSliderValue('faultsFrameSize', 'FrameSizeValue');
  updateSliderValue('memoryFrameSize', 'memoryFrameSizeValue');
}

init();
