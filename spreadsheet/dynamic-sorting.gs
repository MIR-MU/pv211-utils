 // LinkBack to this script:
 // http://webapps.stackexchange.com/questions/7211/how-can-i-make-some-data-on-a-google-spreadsheet-auto-sorting/43036#43036

 /**
 * Dynamically sorts the whole leaderboard descending
 * by the result of the latest submission.
 */
function onEdit(event){
  var sheetLeaderboard = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('leaderboard');

  // MANUAL INPUT NEEDED
  var tableRange = "B3:I52"; // What to sort.
  var range = sheetLeaderboard.getRange(tableRange);

  // Sort by a helper column with the latest submission score for a given row
  var columnToSortBy = addLatestColumn(sheetLeaderboard, range);
  Logger.log('Sort by the column ' +
    sheetLeaderboard.getRange(range.getRow(), columnToSortBy, range.getNumRows()).getA1Notation());

  // Extend the range by the helper column
  var extendedRange = range.offset(0,0,range.getNumRows(),range.getNumColumns()+1);

  Logger.log('Sorting...');
  extendedRange.sort( { column : columnToSortBy, ascending: false } );

  Logger.log('Cleaning...');
  deleteExtraColumn(sheetLeaderboard, range, columnToSortBy);

  Logger.log('Conditional formatting the podium...');
  applyConditionalFormattingPodium(sheetLeaderboard, range);

  // Reduced range without the first three places
  var reducedRange = range.offset(3,0,range.getNumRows()-3,range.getNumColumns());

  Logger.log('Conditional formatting...');
  applyConditionalFormatting(sheetLeaderboard, reducedRange);

  Logger.log('Done and dusted.');
}

/**
 * Delete extra column(s) with temporary scores
 * until a blank column is just after the range.
 */
function deleteExtraColumn(sheet, range, extraColumn) {
  var tmpColumn = sheet.getRange(1, extraColumn, range.getLastRow(), 1);
  do {
    sheet.deleteColumn(extraColumn);
  } while (!tmpColumn.isBlank());
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
* Extract the latest score for each row and
* insert new temporary column after the range with the latest score
*
* @return index of the temporary column
*/
function addLatestColumn(sheet,range){
  var rangeValues = range.getValues();// returns Javascript array, indexing [0][0]
  var startRow = range.getRow();
  var lastColumn = range.getLastColumn();

  // insert blank column
  sheet.insertColumnAfter(lastColumn);

  var numRows = range.getNumRows();
  var numCols = range.getNumColumns();

  for (let row = 0; row <= numRows-1; row++) {
    for (let col = numCols-1; col >= 1; col--) { // col 0 is the name column
      var cell = rangeValues[row][col];
      if (cell !== '') {
        sheet.getRange(startRow + row, lastColumn + 1).setValue(cell);
        break;
      }
    }
  }

  return lastColumn + 1;
}

/**
 * Apply conditional formatting for the first three rows
 * (the podium)
 */
function applyConditionalFormattingPodium(sheet, range) {
  range.setBackground("white");
  sheet.getRange(range.getRow(),1,1,range.getLastColumn()).setBackground("gold");
  sheet.getRange(range.getRow()+1,1,1,range.getLastColumn()).setBackground("silver");
  sheet.getRange(range.getRow()+2,1,1,range.getLastColumn()).setBackground("#ffd0a2");
}

/**
* Apply conditional formatting for the whole rows
* Condition 1: score is at least L18 (or 35 %)
* Condition 2: score is more than M18 (or 1.25 %) (kicking Mr Random)
* Scope: the range, or weeks 1--7 (columns C--I)
* Formatting 1: light green background
* Formatting 2: light yellow background
*/
function applyConditionalFormatting(sheet,range){
  var ruleThreshold = SpreadsheetApp.newConditionalFormatRule()
    .whenFormulaSatisfied("=OR($C6>=$L$18; $D6>=$L$18; $E6>=$L$18; $F6>=$L$18; $G6>=$L$18; $H6>=$L$18; $I6>=$L$18)")
    .setBackground("#CCFFCC")
    .setRanges([range])
    .build();

  var ruleMrRandom = SpreadsheetApp.newConditionalFormatRule()
    .whenFormulaSatisfied("=OR($C6>$M$18; $D6>$M$18; $E6>$M$18; $F6>$M$18; $G6>$M$18; $H6>$M$18; $I6>$M$18)")
    .setBackground("#FFFFAF")
    .setRanges([range])
    .build();

  var rules = sheet.getConditionalFormatRules();
  rules = [];// clear the rules
  rules.push(ruleThreshold);
  rules.push(ruleMrRandom);
  sheet.setConditionalFormatRules(rules);
}
