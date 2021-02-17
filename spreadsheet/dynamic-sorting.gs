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
  var tableRange = "B3:I84"; // What to sort.
  var range = sheet.getRange(tableRange);

  //var columnToSortBy = editedCell.getColumn();

  // Sort by a helper column with max value for a given row
  var columnToSortBy = addMaxColumn(sheet,range);
  Logger.log('Sort by column ' + columnToSortBy);

  // Extend the range by the helper column
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
  sheet.getRange("A3:I3").setBackground("gold");
  sheet.getRange("A4:I4").setBackground("silver");
  sheet.getRange("A5:I5").setBackground("#ffd0a2");

  // Reduced range without the first three places
  var reducedRange = range.offset(3,0,range.getNumRows()-3,range.getNumColumns());

  Logger.log('Conditional formatting (assignment condition >= 35% met)...');
  applyConditionalFormatting(sheet, reducedRange);

  Logger.log('Done and dusted.');
}

/**
* Compute max score for each row and
* insert new temporary column after the range with the max score
*
* @return index of the temporary column
*/
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

/**
* Apply conditional formatting for whole rows
* Condition 1: score is at least 35 %
* Condition 2: score is more than 0.92 % (kicking Mr Random)
* Scope: Weeks 1--7 (columns C--I)
* Formatting 1: light green background
* Formatting 2: light yellow background
*
* @todo remove hard-coded code
*/
function applyConditionalFormatting(sheet,range){
  var ruleThreshold = SpreadsheetApp.newConditionalFormatRule()
    .whenFormulaSatisfied("=OR($C6>=35%; $D6>=35%; $E6>=35%; $F6>=35%; $G6>=35%; $H6>=35%; $I6>=35%)")
    .setBackground("#CCFFCC")
    .setRanges([range])
    .build();

  var ruleMrRandom = SpreadsheetApp.newConditionalFormatRule()
    .whenFormulaSatisfied("=OR($C6>0,92%; $D6>0,92%; $E6>0,92%; $F6>0,92%; $G6>0,92%; $H6>0,92%; $I6>0,92%)")
    .setBackground("#FFFFAF")
    .setRanges([range])
    .build();

  var rules = sheet.getConditionalFormatRules();
  rules = [];// clear the rules
  rules.push(ruleThreshold);
  rules.push(ruleMrRandom);
  sheet.setConditionalFormatRules(rules);
}

