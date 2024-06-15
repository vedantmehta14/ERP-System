var events = []

$(document).ready(function() {
	$('#calendar').fullCalendar({
		header: {
			left: 'month, agendaWeek, agendaDay',
			center: 'title',
			right: 'prev, today, next'
		},
		buttonText: {
			today: 'Today',
			month: 'Month',
			week: 'Week',
			day: 'Day'
		},
		timezone: 'local',
		defaultView: 'month',
		allDayDefault: false,
		allDaySlot: false,
		slotEventOverlap: true,
		slotDuration: "00:30:00",
		slotLabelInterval: "00:30:00",
		snapDuration: "00:15:00",
		contentHeight: 600,
		scrollTime: "8:00:00",
		axisFormat: 'h:mm a',
		timeFormat: 'h:mm A()',
		minTime: "09:00:00",
		maxTime: "19:30:00",
		selectable: true,
		selectHelper: true,

		eventRender: function(event, element) {
			element.append(`<span class='I_delete'><i class="fa fa-remove fa-2x"></i></span>`);
			element.append(`<span class='I_edit'><i class="fa fa-edit fa-2x"></i></span>`);
			element.find(".I_delete").click(function() {
				$('#calendar-popup').hide();
				if (confirm('Are you sure want to delete event?')) {
					$('#calendar').fullCalendar('removeEvents', event._id);
					var index = events.map(function(x) {
						return x.id;
					}).indexOf(event.id);
					events.splice(index, 1);
					localStorage.setItem('events', JSON.stringify(events));

					events = parselocalstorage('events')

				}
			});
			element.find(".I_edit").click(function() {
				$('#calendar-popup').hide();

				$('#eventname').val(event.title)
				// $('#location').val(event.location)
				$('#eventdetails').val(event.details)
				$('input#eventstart').val(event.start._i)
				$('input#eventend').val(event.end._i)
				$('#simplemodal').show();


				//update events
				var that = event;
				$('#edit-form').on('submit', function(e) {
					e.preventDefault();
					$form = $(e.currentTarget);

					$title = $form.find('input#eventname');
					$details = $form.find('textarea#eventdetails');
					$start = $form.find('input#eventstart');
					$end = $form.find('input#eventend');
					that.title = $title.val();
					that.details = $details.val();
					that.start = $start.val();
					that.end = $end.val();

					$('#calendar').fullCalendar('updateEvent', that);
					$('#simplemodal').hide();
					$('#calendar-popup').hide();
				});
				$('#calendar').fullCalendar('updateEvent', event);
				// 		localStorage.setItem('events', JSON.stringify(events));
			});

			var modal = document.getElementById('simplemodal')

			window.addEventListener('click', clickOutside)
		},

		select: function() {
			// $('#simplemodal h2').text('Add Event');
			$('#simplemodal').show();
		}
	});

  // Simple modal hides when cancel is clicked
  $('.cancelButton').click(function(e) {
    e.preventDefault();
    $('#simplemodal').hide();
  });

});

// function showConfirmationDialog() {
//   document.getElementById('overlay').style.display = 'block';
//   document.getElementById('confirmationModal').style.display = 'block';
// }

// function confirmLogout() {
//   window.location.href = '/logout';
// }

// function cancelLogout() {
//   hideConfirmationDialog();
// }

// function hideConfirmationDialog() {
//   document.getElementById('overlay').style.display = 'none';
//   document.getElementById('confirmationModal').style.display = 'none';
// }
