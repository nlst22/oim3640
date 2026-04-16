## My Project Proposal

**What I'm building:**
I am building a Flask web application that allows users to enter a location or address and returns the nearest MBTA transit stop, including whether it is wheelchair accessible, with an optional map display.

**Why I chose this:**
I chose this project because navigating public transportation efficiently can be frustrating, especially when you are unfamiliar with an area. As someone who spends time in the Boston area, having a simple tool to quickly find the nearest T stop would be genuinely useful and practical.

**Core features:**

* Input field for users to enter a place name or address
* Integration with the Mapbox API to convert the input into coordinates
* Integration with the MBTA API to find the nearest transit stop
* Display of the nearest stop name and wheelchair accessibility
* (Optional) Map visualization showing the user’s location and the nearest stop

**What I don't know yet:**

* How to properly integrate and display a Mapbox map within an HTML template
* How the MBTA API structures its response for nearest stops and accessibility data
* Best practices for handling API errors and edge cases in a Flask app
* How to structure the Flask app cleanly with separate routes and helper functions
