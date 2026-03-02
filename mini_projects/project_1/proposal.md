## My Project Proposal
### Project Title: Splitsy
**What I am building:**
I am building a web application called Splitsy that allows users to easily split bills and expenses among friends and family. The app will have features such as creating groups, adding expenses, and calculating how much each person owes or is owed.

I am building Splitsy a smart bill splitter app that calculates tax and tip and splits a bill equally or unevenly across multiple people.

**Why I chose this:**
I chose this project because I have personally experienced the hassle of splitting bills and expenses with friends and family, especially when it comes to group trips or shared living arrangements. I wanted to create a tool that simplifies this process and helps people avoid awkward conversations about money and makes it clrear who owes what. 

**Core Features:**
1. Accept bill subtotal and tax (percent or dollar amount)
2. Calculate tip (percent or dollar amount) and final total
3. Split the final total equally or by custom weights
4. Validate user input (numbers, positive values, menu choices)
5. Loop so the user can run multiple splits without restarting

**What I don't know yet:**
1. The cleanest way to structure input validation without repeating code
2. How to handle rounding so the split totals add up correctly
3. The best way to present results clearly (currency formatting and summaries)

**Peer Feedback**
Layla suggested that I should have tax rates for diffrent states. I should also have things like tax and tip as fixed items that are always split evenly among all members of the group. 

**User flow:**
1. User selects "Split a Bill" or "Split Trip Expenses"
-> If "Split a Bill": Evenly 
2. User inputs bill subtotal and number of people
3. User inputs state they are in (for tax calculation)
4. User inputs tip percentage or amount
5. App calculates and displays the final total, tax, tip, and individual shares for each person in the group in a short summary format
-> If "Split a Bill": Unevenly
2. User inputs bill subtotal and number of people
3. User inputs state they are in (for tax calculation)
4. User inputs tip percentage or amount
5. For each person: “Enter item price, or done”
6. For shared:“Enter shared item price, or done”
7. App calculates and displays the final total, tax, tip, and individual shares for each person in the group in a short summary format