# steam-transaction-total
Sums up all your steam transactions given the generated HTML of https://store.steampowered.com/account/history/

## Instructions
1. Go to https://store.steampowered.com/account/history/, log in if you need to.
2. Click on "Load more transactions" until your entire history is visible.
3. Type "console.log(document.documentElement.innerHTML)" into your browser's console and copy the output into a new file.
4. Run the script

Example:
  `  python steamhistparse.py "C:\Users\JohnDoe\Documents\mysteamhistory.html"`
