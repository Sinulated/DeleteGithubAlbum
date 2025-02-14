# DeleteGithubAlbum
Automate Deleting Github Albums

Since there seems to be no decent way to manage albums on Deviantart (at least when you have reached 40k uploads and everything breaks)

I created this stupid webdriver script to automate the tedious process.

On first launch, you will need to log in manually and press enter in the console to save the cookie.

Next it will ask you to specify the link to the album which you would like to delete. Just paste it into the console.

Now it will open the link and collect all the links of the specified album and save them to a text file.

Lastly, it will now process that list we just created and when it's done, it deletes the text file, ready for you to delete your next album.


## Note that, in this version of the app, i relied on detecting my own username Sinulated in the app.py, just edit it and put in your own deviantart username, there should be two occurances, i could have made this a variable but i really just made this for myself, and it's super janky and will probably break anyways as soon as deviantart updates anything.

I made this using GPT-4o and purely to accomplish a task, so it's by no means the best way to do this i'm sure, but the point is it works.
