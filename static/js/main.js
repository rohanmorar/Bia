// js code here
let begin_button = document.getElementById('begin_workout_button')
begin_button.addEventListener('click', async () => {
    let hand_selection = document.getElementById('hand_select').value;
    var data = {start: true, 'hand': hand_selection}

    try {
      const response = await fetch('https://bia-project-383604.uc.r.appspot.com/run-program', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
      const result = await response.json();
      console.log(result.status);
    } catch (error) {
      console.error(error);
    }
  });



