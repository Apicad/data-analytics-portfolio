# Talking points: salary prediction

## The 60-second version

I took a small public dataset of salaries and years of experience and asked how much a year of
experience is worth. I fit an ordinary least squares regression in Python. The answer was about
$9,450 per year, and experience alone explained 96% of the variation in that data. For the capstone
I presented the model, the plot and the R². Afterwards I went further: I added confidence and
prediction intervals so the chart shows uncertainty, I checked the residuals to confirm a straight
line was the right shape, I ran leave-one-out cross-validation to get an honest accuracy number
(about $5,900 typical miss, five times better than guessing the average), and I pulled the model into
a tested Python module so the numbers on my slides are verified automatically.

## Questions I expect, and what I say

**Why linear regression?**
One numeric input, one numeric output, and the scatter plot looked like a line. Start with the
simplest model that could work, then check whether it does. The residual plot and Q-Q plot say it does
for this range.

**What does R² of 0.957 actually tell you?**
That 96% of the spread in salary in this dataset lines up with experience. It is not accuracy and it
is not causation. It is also measured on the training data, which is why I added cross-validation.

**What is the difference between the two bands on your chart?**
The confidence interval is about the line, where the average salary for that experience level sits.
The prediction interval is about a person, and it is much wider. If someone asks "what would I earn",
the prediction interval is the honest answer.

**How do you know the model is not overfitting?**
Two parameters on 30 points cannot overfit much, but I checked anyway: leave-one-out RMSE is $5,924
versus a residual standard deviation of $5,788 on the training fit. Almost no gap, so the line
generalises to people it has not seen, from the same population.

**What is wrong with the model?**
Thirty rows. One input. Role, industry, location and education are all missing. The slope would
change if any of them were added. And it is a straight line forever, but real pay growth flattens;
the data stops at 10.5 years so the model has never seen that.

**What would you do next?**
Get a real dataset with more columns, control for role and location, try a log or spline on
experience, and report the prediction interval rather than the point estimate.

**Tell me about a mistake you made.**
My first run had x and y swapped: I regressed experience on salary. The slope came out as a tiny
decimal and the summary table made no sense, which is how I caught it. Lesson: read the summary
table, not just the R².

## Technical details, if asked

- `statsmodels.OLS` with an added constant; `result.summary()` for the full table.
- Intervals from `get_prediction(...).summary_frame()`: `mean_ci_*` for the line, `obs_ci_*` for a person.
- Normality: Shapiro-Wilk on residuals, W = 0.952, p = 0.195.
- Cross-validation: 30 folds, model RMSE $5,924, mean-only baseline RMSE $27,883.
- Tests pin the slope to 9,449.96 and the intercept to 25,792.20, the figures on the capstone slides.
