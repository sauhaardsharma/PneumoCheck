document.getElementById('subscribeButton').addEventListener('click', function(event) {
    var email = document.getElementById('email').value;
    setTimeout(function() {
  document.getElementById('successMessage').style.display = 'block';
  document.getElementById('email').value = '';
  }, 1000);
   event.preventDefault();
  });