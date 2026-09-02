# Pre-publication checklist

Delete this file once everything below is done.

## Blocking — do not publish until these are resolved

- [ ] Course coordinator has confirmed publishing our solutions is acceptable
- [ ] Co-author has agreed to publication and is credited by name in the root README
- [ ] Fill in the "my main individual contributions" line in the root README

## Cahn–Hilliard notebook

- [x] **Re-run the whole notebook top to bottom.** *(done — the submitted version runs
      clean end to end, no tracebacks, 19 figures including the Task 6 energy/mass
      results for the spinodal decomposition runs.)*
- [x] Fix the spelling: **Cahn**–Hilliard, not "Chan". 8 places:  *(done)*
      - cell 5 (×2, markdown), cell 7 (markdown), cell 35 (markdown)
      - cell 37 (comment), cell 42 (docstring + comment)
      - cell 38: rename the function `chan_hilliard_be_solver_sym` → `cahn_hilliard_be_solver_sym`
        and update its call site
- [x] cell 37: remove `# SJEKK MED MATHIASSSSSS`  *(done)*
- [x] fix remaining "linerar" -> "linear" typos  *(done)*

## Usadel notebook

- [x] cell 63: remove the `chat sier at:` block and write the comparison in your own words  *(done)*
- [x] cell 63: resolve `TO DO: write about: Boundaries at Position = 0 and 1...`  *(done)*
- [x] cell 57: resolve `OBS: comment on why DOS is 1 for all positions and epsilon here!`  *(done)*
- [x] cell 73: `comment on the difference from exercise 2l)` and  *(done)*
      `Mathias har analytisk bevis for siste ;)` — replace with the actual argument
      (it is written out properly in report 2, task 2m)
- [x] cell 78: `What do we observe?` is the final line of the notebook — replace with  *(done)*
      the conclusion about 2π-periodicity and the Josephson effect
- [x] cells 4 and 6: `GJORT I OVERLEAF` — replace with a pointer to `report.pdf`  *(done)*
- [x] cell 8: `# passende steglengde ??`  *(done)*
- [x] cell 15: `forklare hvorfor vi valgte 20???`  *(done)*
- [x] cell 16: `(SKAL VI PLOTTE AKSEPTERTE TIDSSTEG??)`  *(done)*
- [x] cell 26: `# because they are used in several functions ???`  *(done)*
- [x] cell 53: `hurray!` in a print statement — harmless, but tidy it up  *(done)*
- [ ] Remove the `time.time()` scaffolding cells, or keep them and label them as
      the benchmark they are

## Reports

- [ ] Report 3: replace `INSERT CURVE FIT` with the figure
- [ ] Report 3: replace `INSERT CODE FOR NCFL` and `AFTER NEW EOC 3.3`
- [ ] Report 3, task 5a: "if you keep going like that, which will not be prioritized
      this time" — either finish the derivation or cut the claim
- [ ] Report 2: subparts 1c–1h, 2d and 2i are empty. Either fill them in or restructure
      so the gaps are not visible
- [ ] Report 2, task 2m: the paragraph about the exercise sheet changing before the
      deadline is a submission-time note. Cut it for publication.

## General

- [x] Both notebooks are in English; keep it that way, including comments  *(done)*
- [x] Rename files: `TMA4320_Prosjekt_2.ipynb` → `usadel_josephson.ipynb`,  *(done)*
      `TMA4320_Prosjekt_3.ipynb` → `cahn_hilliard.ipynb`
- [ ] Check no personal data (student numbers, full addresses) in the report PDFs
- [x] Add a `LICENSE` file (MIT is the usual choice)  *(done)*
