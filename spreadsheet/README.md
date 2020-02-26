This subdirectory contains code to reproduce the leaderboard spreadsheet in
Google Sheets.

## Google Apps Script

The code is available in [dynamic-sorting.gs](./dynamic-sorting.gs).

Important:
* the range for sorting is manually set on [line 14](./dynamic-sorting.gs#L14)
* please leave a column right after this range blank, since the script uses it
  for temporary computations and deletes it automatically if it contains
  anything

#### How to import

Open the Google Sheets leaderboard > Tools > Script editor > {Create new
project | new .gs file}

## Trigger

Since API calls and their changes in the spreadsheet do not cause triggers to
run [[1][1]], we use time trigger to call the script every minute.

#### How to set up

Once in Script editor > Edit > Current project's triggers > New trigger > ..
time-driven trigger every minute

## Formulae in cells

#### Importing data from logs (submissions sheet) to the leaderboard sheet

Leaderboard sheet, cell C3, Czech localisation:
```
=IFERROR(SVYHLEDAT(C$2&$B3;SORT(submissions!$A:$F;4;NEPRAVDA;5;NEPRAVDA;6;NEPRAVDA);6;NEPRAVDA))
```

Submissions sheet, cell A1, Czech localisation:
```
=CONCAT(D1;E1)
```

#### Leader of the week

Leaderboard sheet, week n.1, Czech localisation:
```
=SORTN($B$3:$B$77;3;0;C3:C77;NEPRAVDA())
```

## Backup snapshots

Just for completeness:
* ODS (OpenDocument Spreadsheet) binary file
* FODS (Flat XML ODF Spreadsheet)


[1]: https://developers.google.com/apps-script/guides/triggers
