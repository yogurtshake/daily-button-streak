# daily-button-streak

[webpage](https://lucas.su-keun.kim/daily-button-streak)

## What's Happening Here?

Stupid web app that is just a button. It tracks how many consecutive days you pressed the button. You only need to click the button once each day. 

*Context*: this is my satirical Duolingo alternative. As of the end of 2025, I have a ~1700 day streak on Duolingo. However, I stopped caring years ago about actually learning new languages. I just want to see my number go up each day. I essentially speedrun my Duolingo every day and have started to just do the simplest lesson (story) on a language I already speak. This will sound insane, but I have discovered a time-reducing technique that works on my mobile device: if you tab out and back in to the app, it skips the audio reading of the current line in the story and you can proceed faster. All in all, I've minimized my Duolingo lesson time to a record low of 21 seconds. Since this is probably the stupidest thing you've ever read, you can see why I created this dumb app as an alternative. End of context.

The webpage is accessible through the domain lucas.su-keun.kim (a sub-domain of su-keun.kim), which points to my server's internet-facing static IP.

I have Nginx on this server acting as a reverse proxy for a couple of domains - for traffic coming from lucas.su-keun.kim/daily-button-streak, it directs to the webpage which is an extremely simple python (Flask) webapp, "app.py".

Upon reaching the webpage, you are faced with a single field that asks you to enter a username. Since this app is supposed to be as simple as possible, there is no sophisticated login mechanism, no passwords, no authorization. There is literally nothing someone with bad intent can do if they enter with another person's username. What are they gonna do, press the button for you? I have no problem with people sharing a username to maximize their chances of keeping up a streak because it's not like they have any chance to beat me anyway. 

Once you enter a username, you now see the main page which has the button, shows your streak number, shows how much time is left today to press the button, and tells you whether or not you've clicked the button today. You also now have access to the rankings table which displays every active streak (rank, username, streak number). That is all.

When you click the button, you send the server an HTTP request which gets handled by Flask and results in your streak updating. If you have an active streak and had not clicked today, your streak is increased by 1. If you had already clicked today, your streak is unchanged. If you did not have an active streak, your streak is set to 1. Also, the first time you click each day, the message that says you haven't clicked today updates and says that you have clicked.

The frontend logic is handled by a javascript file called stuff.js. The Flask app and all routes are defined in the python file app.py. 

The last crucial part of this app is the reset_streaks.py script that sets all streaks that didn't click yesterday or today to 0. I set up a cron job on my server to run this script every day at midnight. The reason the script also checks if the user clicked today is because there is a possible (extremely unlikely) scenario where the user clicks after midnight and mere milliseconds before the script runs. If I didn't include the today check, then that user would get screwed over and have their streak reset to 0. Seems an unfair result for having been the highest possible level of proactive.


## Dependencies: 

### app functionality

python3, javascript, flask

### hosting functionality

nginx (for reverse proxy), gunicorn (HTTP server) 
