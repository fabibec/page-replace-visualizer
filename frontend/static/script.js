const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    console.log(entry);
    if (entry.isIntersecting) {
      entry.target.classList.add('scroll-show');
    } else {
      entry.target.classList.remove('scroll-show');
    }
  });
});
const hiddenElements = document.querySelectorAll('.scroll-hidden');
hiddenElements.forEach((el) => observer.observe(el));

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
