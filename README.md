# Gold News Sentiment vs Price Moves

This tests how well news sentiment about gold line up with later moves in the gold price (daily). It links a dataset of news headlines and sentiment labels to historical prices, then checks if “positive” or “negative” sentiment matches the following price move over a 3-day window. It looks stupid I did it 3 in the morning. I'll fix it don worry. 

1. **Load news data**

   - Read `gold-dataset.csv`.
   - Clean the `Dates` column and convert it to proper dates.
   - Clean the `Price Sentiment` column and map:
     - `positive` → `+1` (long)
     - `negative` → `-1` (short)

2. **Load gold price data**

   - Read `Gold_Prices.xlsx`.
   - Use the `Name` column as the date.
   - Use the `US dollar` column as the gold price.

3. **Build 3-day forward returns**

   - Compute `FutureClose` as the price 3 days ahead.
   - Compute `FutureReturn` as the 3-day percentage move in price.

4. **Match news to prices**

   - Merge news and price data on the date.
   - Drop rows where there is no 3-day forward price.
   - Set `PriceDirection` to:
     - `+1` if the 3-day return is positive
     - `-1` if the 3-day return is negative
   - Mark a signal as `Correct` if sentiment direction equals price direction.

5. **Report results**

   - Print the total number of articles.
   - Print overall accuracy and accuracy by sentiment (positive / negative).
   - Print average 3-day returns after positive and negative sentiment.

6. **Plot signals**

   - Plot the gold price over time.
   - Mark positive sentiment dates with green upward triangles (long).
   - Mark negative sentiment dates with red downward triangles (short).

## Requirements

- Python 3
- `pandas`
- `numpy`
- `matplotlib`

## Usage

1. Place `gold-dataset.csv`, `Gold_Prices.xlsx`, and the script in the same directory or smth.
2. Run the script
3. Profit

You will see:

- A printed summary of accuracy and average returns.
- A chart of the gold price with long/short markers based on news sentiment.
