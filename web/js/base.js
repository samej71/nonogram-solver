function display_grid(size) {
    /* This function updates the grid layout when the user selects a new size. */

    let grid = "<form id='grid_form' name='grid_form'>";

    grid += "<table id='grid_table' name='grid_table'>";
    grid += "<tr id='entry_row'><td />";

    for (let col = 0; col < size; col++) {
        // Fill out the colunn entry boxes.
        grid += "<td class='entry_col'><input id='grid_col_entry_" + col
             +  "' class='grid_col_entry' type='text' /></td>";
    }

    grid += "</tr>";
    
    for (row = 0; row < size; row++) {
        // Fill out the row entry boxes.
        grid += "<tr id='grid_row_'" + row + "'>";
        grid += "<td><input id='grid_row_entry_" + row + "' type='text' /></td>";

        for (let col = 0; col < size; col++) {
            // Fill out the cells.
            grid += "<td class='grid_cell' id='grid_cell_" + row + "_" + col
                 +  "' onClick='toggle_cell(this);'> </td>";
        }

        grid += "</tr>";
    }

    grid += "</form></table>";

    // Display the grid.
    document.getElementById("nonogram_grid").innerHTML = grid;
    document.getElementById("solve_button").style.visibility = "visible";
}

function toggle_cell(cell) {
    /* This function toggles a cell between filled out and blank when it is clicked on. */

    if (window.getComputedStyle(cell, "").backgroundColor == "rgb(255, 255, 255)") {
        // The cell is currently white, set it to black.
        cell.style.backgroundColor = "#000000";
    }
    else {
        // The cell is currently black, set it to white.
        cell.style.backgroundColor = "#FFFFFF";
    }
}

function submit_puzzle() {
    /* This function submits the filled out puzzle to the back-end to be solved. */

    // Initialize the tables.
    let horizontal = [];
    let vertical = [];

    // TODO: Ensure that the entered numbers are not larger than the grid size.
    // TODO: Check that the value is not negative.
    // TODO: Check that the values are all numbers.

    // Get the size of the grid.
    const size = document.getElementById("size_entry").value;

    // Initialize the error condition.
    let error = false;

    for (let row = 0; row < size; row++) {
        // Get the user-entered values for the row.
        let row_val = document.getElementById("grid_row_entry_" + row).value;

        // Initialize the row data.
        horizontal[row] = [];

        if (row_val) {
            if (verify(size, row_val)) {
                // If the value is bad, flag it.
                error = true;
            }
            else {
                // If the row was entered, set the table data to the values.
                row_val.split(",").forEach(val => horizontal[row].push(parseInt(val)));
            }
        }
        else {
            // If the row was not entered, set the table data to an array of the value 0.
            horizontal[row] = [0]
        }
    }

    for (let col = 0; col < size; col++) {
        let col_val = document.getElementById("grid_col_entry_" + col).value;

        // Initialize the column data.
        vertical[col] = [];

        let col_size = 0;

        if (col_val) {
            if (verify(size, col_val)) {
                // If the value is bad, flag it.
                error = true;
            }
            else {
                // If the column was entered, set the table data to the values.
                col_val.split(",").forEach(val => vertical[col].push(parseInt(val)));
            }
        }
        else {
            // If the column was not entered, set the table data to an array of the value 0.
            vertical[col] = [0]
        }
    }

    /* Currently, passing in a partially solved puzzle is not supported.  The way nonograms are
       setup, it should never be required to have a partially solved puzzle to beging with unlike,
       for instance, sudokos.
    */

    if (!error) {
        pywebview.api.solve(parseInt(size), horizontal, vertical).then(solved_callback);
    }
    else {
        alert("Please ensure that the entered values are all numeric and that they are not" +
              "larger than the grid size (including padding between the digits).");
    }
}

function verify(size, value) {
    /* This function verifies that the values that the user entered are valid for the puzzle size.
       1. The numbers (including padding) do not exceed the size of the grid.
       2. The numbers are positive (0 is already accounted for).
       3. Only numbers and commas are in the string.

       Check 2 is handled by check 3 since a negative sign would not be a digit or a comma.
    */

    // Initialize the size to test against to 0.
    let test_size = 0;

    // This regex will test for values other than digits and commas.
    const not_number = /^[^0-9,]*$/;

    if (not_number.test(value)) {
        // The user-entered list contains a non-numeric value.

        return(true);
    }

    // Add the values from the list including the padding.
    value.split(",").forEach(val => test_size += parseInt(val) + 1);

    // Subtract one since last value does not need to be padded.
    test_size -= 1;

    if (test_size > size) {
        // The value is too large for the grid.
        return(true);
    }

    // All of the tests passed.
    return(false);
}

function solved_callback(response) {
    /* This function is the callback from the web server and fills out the grid with the
       solution returned from the back-end.
    */

    // Store the returned values in scalars.
    solved = response[0];
    empty = response[1];

    for (let row = 0; row < solved.length; row++) {
        for (let col = 0; col < solved.length; col++) {
            // Get the current cell element.
            let cell = document.getElementById("grid_cell_" + row + "_" + col);

            if (solved[row][col] == 1) {
                // If the cell is part of the solution, fill it in with black.
                cell.style.backgroundColor = "#000000";
            }
            else {
                // If the cell is not part of the solution, clear it with white.
                cell.style.backgroundColor = "#FFFFFF";
            }
        }
    }
}
