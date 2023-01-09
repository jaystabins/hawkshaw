/* Project specific Javascript goes here. */

window.addEventListener('DOMContentLoaded',function() {
  const message = "{% translate 'Do you really want to remove the selected e-mail address?' %}";
  const actions = document.getElementsByName('action_remove');

  if (actions.length) {
    actions[0].addEventListener("click",function(e) {
      if (!confirm(message)) {
        e.preventDefault();
      }
    });
  }
  Array.from(document.getElementsByClassName('form-group')).forEach(x => x.classList.remove('row'));
});
