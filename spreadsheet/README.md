# Spreadsheet leaderboards

This subdirectory contains the code and the instructions
to reproduce the leaderboard spreadsheets in Google Sheets.

## Links

### Spring 2023

[Live public Cranfield leaderboard Spring 2023][leaderboard-cranfield-2023] | [Edit leaderboard][leaderboard-cranfield-2023-sheets]

[leaderboard-cranfield-2023]: https://docs.google.com/spreadsheets/d/e/2PACX-1vSXuOTclZfHWYxh2rf7hfMeLvcCuE5UsJu7BzteyunhPw3z4YNZjCovjmMB6SnDdgjGyenOgdochaEq/pubhtml
[leaderboard-cranfield-2023-sheets]: https://docs.google.com/spreadsheets/d/1kDRTDUCPTOi0crgIO_WqctuvCazTmZ4V_EoVSvb6VQI/edit?usp=sharing

### Archive

#### Spring 2022

[Live public Cranfield leaderboard Spring 2022][leaderboard-cranfield-2022] | [Edit leaderboard][leaderboard-cranfield-2022-sheets]

[Live public TREC leaderboard Spring 2022][leaderboard-trec-2022] | [Edit leaderboard][leaderboard-trec-2022-sheets]

[Live public ARQMath leaderboard Spring 2022][leaderboard-arqmath-2022] | [Edit leaderboard][leaderboard-arqmath-2022-sheets]

[leaderboard-cranfield-2022]: https://docs.google.com/spreadsheets/d/e/2PACX-1vT0FoFzCptIYKDsbcv8LebhZDe_20GFeBAPmS-VyImlWbqET0T7I2iWy59p9SHbUe3LX1yJMhALPcCY/pubhtml
[leaderboard-cranfield-2022-sheets]: https://docs.google.com/spreadsheets/d/1TFE4RAx_kjaAkwhSRudel17kPunzD-C6BuNeZYzuzFk/edit?usp=sharing

[leaderboard-trec-2022]:https://docs.google.com/spreadsheets/d/e/2PACX-1vQPMjEwGPte34q6vT0CfT2NzmC6iDilpgG7s1cunr7eG5BY6T1OiHumbnwKrwrvQcj1e8-Pu96PiYc2/pubhtml
[leaderboard-trec-2022-sheets]: https://docs.google.com/spreadsheets/d/1QD-qS18fR0Q137dw_j8k73KwewsmeJsiB4SSzaXhbPs/edit?usp=sharing

[leaderboard-arqmath-2022]: https://docs.google.com/spreadsheets/d/e/2PACX-1vSF1I2TKhKqYc7kTxRfza__PTTQjrAtvezuQFm9I_lL3WsPSETE5yuxe8JyiN-7NvFjv4nZ8eCQ9aHg/pubhtml
[leaderboard-arqmath-2022-sheets]: https://docs.google.com/spreadsheets/d/1akHS9OSdN0_gu5xThJBSVAMKvUqAWg6sjO6vM6KCxfw/edit?usp=sharing

#### Spring 2021

[Live public Cranfield leaderboard Spring 2021][leaderboard-cranfield-2021] | [Edit leaderboard][leaderboard-cranfield-2021-sheets]

[Live public TREC leaderboard Spring 2021][leaderboard-trec-2021] | [Edit leaderboard][leaderboard-trec-2021-sheets]

[Live public ARQMath leaderboard Spring 2021][leaderboard-arqmath-2021] | [Edit leaderboard][leaderboard-arqmath-2021-sheets]

[leaderboard-cranfield-2021]: https://docs.google.com/spreadsheets/d/e/2PACX-1vRRR4eDkQIWx5FSU08Uj5DciWwxNfHJeLruNR1T0WW9xmSsYl457Zqv5SlA1jfvsYHpsaUw_8P3z1OF/pubhtml
[leaderboard-cranfield-2021-sheets]: https://docs.google.com/spreadsheets/d/1CNeZESOrPxBs3U0FeGtaDPLJQkb2Ubsr0aCvyNIwdtM/edit?usp=sharing

[leaderboard-trec-2021]:https://docs.google.com/spreadsheets/d/e/2PACX-1vQ33YdFZtGH6g2bDbkD9aLozLdVVGNuP09sRh-F9d_EY9nWntOrLHSyNATFsXw4v9lw3UA3vOzl5l0s/pubhtml
[leaderboard-trec-2021-sheets]: https://docs.google.com/spreadsheets/d/1eiyase14FrSJs24_LjTSdPwOWOdqutDZhnl33ztBycc/edit?usp=sharing

[leaderboard-arqmath-2021]: https://docs.google.com/spreadsheets/d/e/2PACX-1vQb_L4ZL5vglRMJBMDn334JHL6xfGVXVz-D1YnZduXTZe4Pj_abKSpe_qnu2gkQEBV5jXEgFyge_Jtu/pubhtml
[leaderboard-arqmath-2021-sheets]: https://docs.google.com/spreadsheets/d/1XXR_3UsjUTxQApU5RRce1Zv4G_0uMJXoaEb0GejU868/edit?usp=sharing

#### Spring 2020

[Live public Cranfield leaderboard Spring 2020][leaderboard-cranfield-2020] | [Edit leaderboard][leaderboard-cranfield-2020-sheets]

[leaderboard-cranfield-2020]: https://docs.google.com/spreadsheets/d/e/2PACX-1vSGTg_Agc0SowDIsDDsaBN_UD-9r-F2eSpozyvVA8F51YHt3GmAle3niaCoj0ocazjDm01OJNgNEykZ/pubhtml
[leaderboard-cranfield-2020-sheets]: https://docs.google.com/spreadsheets/d/1f9P3bn17n2rHGCxBnn3GVr57PF5hMWJEILp06Uq7Jnk/edit?usp=sharing

## Google Apps Script

The code is available in [dynamic-sorting.gs](./dynamic-sorting.gs).

Important:
* the range for sorting is manually set on [line 12](./dynamic-sorting.gs#L12)
* please leave a column right after this range blank, since the script uses it
  for temporary computations and deletes it automatically if it contains
  anything

#### How to import

Open the Google Sheets leaderboard > Extensions > Apps Script > {Create new
project | new .gs file}

## Trigger

Since API calls and their changes in the spreadsheet do not cause triggers to
run [[1][1]], we use time trigger to call the script every five minutes.

#### How to set up

Once in the Google Apps Script editor > Triggers > Add trigger > select
time-driven trigger every minute

## Formulae in cells

#### Importing data from logs (submissions sheet) to the leaderboard sheet

Leaderboard sheet, cell C3, Czech / English localisation:
```
=IFERROR(SVYHLEDAT(C$2&$B3;SORT(submissions!$A:$F;4;NEPRAVDA;5;NEPRAVDA;3;NEPRAVDA);6;NEPRAVDA))
```
```
=IFERROR(VLOOKUP(C$2&$B3;SORT(submissions!$A:$F;4;FALSE;5;FALSE;3;FALSE);6;FALSE))
```

Expand the formula for every student and every week.

<!--
Submissions sheet, cell A1, Czech equals English localisation:
```
=CONCAT(D1;E1)
```
-->

#### Leader of the week

Leaderboard sheet, week n.1, Czech / English localisation:
```
=SORTN($B$3:$B$52;3;0;C3:C52;NEPRAVDA())
```
```
=SORTN($B$3:$B$52;3;0;C3:C52;FALSE())
```

Analogously for other weeks. Text colour is initially set to the
background color of the cell, so when there are some real submissions
for a given week, just reset text color and go live.


## Backup snapshots

Just for completeness:
* ODS (OpenDocument Spreadsheet) binary file
* FODS (Flat XML ODF Spreadsheet)


[1]: https://developers.google.com/apps-script/guides/triggers
