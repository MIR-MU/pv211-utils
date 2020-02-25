 // LinkBack to this script:
 // http://webapps.stackexchange.com/questions/7211/how-can-i-make-some-data-on-a-google-spreadsheet-auto-sorting/43036#43036

 /**
 * Dynamically sorts the whole leaderboard descending
 * by the best result of each row (overall classification).
 */
function onEdit(event){
  // var sheet = event.source.getActiveSheet();
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('leaderboard');
  // var editedCell = sheet.getActiveCell();

  // MANUAL INPUT NEEDED
  var tableRange = "B3:N77"; // What to sort.
  var range = sheet.getRange(tableRange);
  
  //var columnToSortBy = editedCell.getColumn();
  
  // Sort by a helper column with max value for a given row
  var columnToSortBy = addMaxColumn(sheet,range);
  Logger.log('Sort by column ' + columnToSortBy);
  
  var extendedRange = range.offset(0,0,range.getNumRows(),range.getNumColumns()+1);

  Logger.log('Sorting...');
  extendedRange.sort( { column : columnToSortBy, ascending: false } );
  
  Logger.log('Cleaning...');
  var maxColumn = sheet.getRange(1, columnToSortBy, range.getLastRow(), 1);
  Logger.log(maxColumn.getA1Notation());
  do {
    Logger.log('Max Column has temporary values, deleting...');
    sheet.deleteColumn(columnToSortBy);
  } while (!maxColumn.isBlank());
  
  Logger.log('Formatting the first 3 places...');
  range.setBackground("white");
  sheet.getRange("A3:N3").setBackground("gold");
  sheet.getRange("A4:N4").setBackground("silver");
  sheet.getRange("A5:N5").setBackground("#ffd0a2");
  
  Logger.log('Done and dusted.');
}

function addMaxColumn(sheet,range){
  var rangeValues = range.getValues();// returns Javascript array, indexing [0][0]
  var startRow = range.getRow();
  var lastColumn = range.getLastColumn();
  
  // insert blank column
  sheet.insertColumnAfter(lastColumn);

  var i = 0;
  rangeValues.forEach(function(eachRow) {
    var maxInRow = Math.max.apply(null, eachRow.slice(1));// slice the first value which is the student's name
    Logger.log(maxInRow + ' max value of row ' + eachRow);
    sheet.getRange(startRow + i, lastColumn + 1).setValue(maxInRow);
    i++; //to get the next row
  });
  
  return lastColumn + 1;
}

