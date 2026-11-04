# Retail sales analysis ("Storytelling with Data")

**Status: originals being recovered.** The Excel workbook, the executive memo and the presentation
from this capstone lived in my Year Up Microsoft account and in Downloads. Neither copy survived. I
am re-downloading them from the Year Up OneDrive; until they land, this folder is a description, not
a reconstruction. Nothing below has been recreated from memory.

## The question

A retailer's transaction log for January through August 2024: what drove revenue, where did it come
from (region, product category, payment method), and what should the business do next?

## My contribution

Solo. I cleaned the transaction data in Excel, built the pivot tables and charts, wrote a one-page
executive memo, and presented a KPI deck with five recommendations in the course's "Storytelling
with Data" format (a short version for a 7-minute slot and a full version).

## Figures as reported on my resume

These are the numbers I quoted at the time. They have **not yet been reconciled** against the
workbook, which is the first thing that happens when it arrives.

| Figure | Value on resume |
|---|---|
| Period | January to August 2024 |
| Transactions | 240 |
| Revenue | about $3.4M |
| Breakdowns | region, product category, payment method |
| Deliverables | workbook, executive memo, KPI presentation with 5 recommendations |

## What this folder will contain once the files are recovered

| File | Label | Purpose |
|---|---|---|
| `original/<workbook>.xlsx` | Original | The capstone workbook, after a check for any customer-identifying columns |
| `original/<memo>.pdf`, `original/<deck>.pdf` | Original | Memo and deck, exported to PDF |
| `improvements/reconcile.py` | Portfolio improvement | Reads the workbook with pandas and recomputes transaction count, revenue and date range so the README numbers are verified, not quoted |
| `improvements/headline_chart.py` | Portfolio improvement | Re-creates the one chart the memo leans on, so the visual is reproducible |
| `docs/` | | The exported chart, and a trace from one recommendation back to the exact pivot figures that support it |

## One limitation (already known)

Eight months of one year is not enough to separate seasonality from trend. Any recommendation about
"growth" in the deck should be read as "growth within this window".

## If the files never turn up

This README stays as the honest record. I will not rebuild the workbook from the resume figures,
because a reconstructed dataset would look like evidence for recommendations it did not produce.
