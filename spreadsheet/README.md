This subdirectory contains code to reproduce the leaderboard spreadsheet in
Google Sheets.

[Live public leaderboard Spring 2020][leaderboard-2020] | [Edit leaderboard][leaderboard-2020-sheets]

[Live public leaderboard Spring 2021][leaderboard-2021] | [Edit leaderboard][leaderboard-2021-sheets]


[leaderboard-2020]: https://docs.google.com/spreadsheets/d/e/2PACX-1vSGTg_Agc0SowDIsDDsaBN_UD-9r-F2eSpozyvVA8F51YHt3GmAle3niaCoj0ocazjDm01OJNgNEykZ/pubhtml
[leaderboard-2021]: https://docs.google.com/spreadsheets/d/e/2PACX-1vRRR4eDkQIWx5FSU08Uj5DciWwxNfHJeLruNR1T0WW9xmSsYl457Zqv5SlA1jfvsYHpsaUw_8P3z1OF/pubhtml
[leaderboard-2020-sheets]: https://docs.google.com/spreadsheets/d/1f9P3bn17n2rHGCxBnn3GVr57PF5hMWJEILp06Uq7Jnk/edit?usp=sharing
[leaderboard-2021-sheets]: https://docs.google.com/spreadsheets/d/1CNeZESOrPxBs3U0FeGtaDPLJQkb2Ubsr0aCvyNIwdtM/edit?usp=sharing

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
