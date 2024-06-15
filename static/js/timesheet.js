function getCurrentTime() {
    return new Date();
  }

  function getCurrentDate() {
    return new Date().toLocaleDateString();
  }

  function formatTimeDiff(startTime, endTime) {
    var timeDiff = endTime - startTime;
    var hours = Math.floor(timeDiff / 3600000);
    var minutes = Math.floor((timeDiff % 3600000) / 60000);
    var seconds = Math.floor((timeDiff % 60000) / 1000);
    return hours + 'h ' + minutes + 'm ' + seconds + 's';
  }

  function checkIn() {
    var currentDateTime = getCurrentTime();
    var currentDate = getCurrentDate();
    var tableBody = document.getElementById('tableBody');
    var newRow = tableBody.insertRow();
    var dateCell = newRow.insertCell(0);
    var checkInCell = newRow.insertCell(1);
    var checkOutCell = newRow.insertCell(2);
    var totalTimeCell = newRow.insertCell(3); // Total Time cell
    dateCell.textContent = currentDate;
    checkInCell.textContent = currentDateTime.toLocaleTimeString();
    checkOutCell.textContent = '-';
    totalTimeCell.textContent = '-';
    newRow.dataset.checkInTime = currentDateTime.getTime(); // Store check-in time in dataset for later use

    // Save the table data to localStorage
    saveTableData();
  }

  function checkOut() {
    var currentDateTime = getCurrentTime();
    var tableBody = document.getElementById('tableBody');
    var lastRow = tableBody.lastElementChild;
    if (!lastRow) return; // No check-in record
    var checkOutCell = lastRow.cells[2];
    var checkInTime = parseInt(lastRow.dataset.checkInTime, 10); // Retrieve check-in time from dataset
    checkOutCell.textContent = currentDateTime.toLocaleTimeString();
    var totalTimeCell = lastRow.cells[3];
    var totalTime = formatTimeDiff(checkInTime, currentDateTime);
    totalTimeCell.textContent = totalTime;

    // Save the table data to localStorage
    saveTableData();
  }

  function saveTableData() {
    var tableData = [];
    var tableBody = document.getElementById('tableBody');
    for (var i = 0; i < tableBody.rows.length; i++) {
      var row = tableBody.rows[i];
      var rowData = {
        date: row.cells[0].textContent,
        checkInTime: row.cells[1].textContent,
        checkOutTime: row.cells[2].textContent,
        totalTime: row.cells[3].textContent
      };
      tableData.push(rowData);
    }
    localStorage.setItem('tableData', JSON.stringify(tableData));
  }

  // Load table data from localStorage when the page loads
  window.onload = function() {
    var savedData = localStorage.getItem('tableData');
    if (savedData) {
      var tableData = JSON.parse(savedData);
      var tableBody = document.getElementById('tableBody');
      tableData.forEach(function(rowData) {
        var newRow = tableBody.insertRow();
        var dateCell = newRow.insertCell(0);
        var checkInCell = newRow.insertCell(1);
        var checkOutCell = newRow.insertCell(2);
        var totalTimeCell = newRow.insertCell(3);
        dateCell.textContent = rowData.date;
        checkInCell.textContent = rowData.checkInTime;
        checkOutCell.textContent = rowData.checkOutTime;
        totalTimeCell.textContent = rowData.totalTime;
      });
    }
  };