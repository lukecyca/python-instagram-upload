***Important: this library no longer works. The API calls we were using have been deprecated by Instagram. Sorry.***

# python-instagram-upload #

Upload and post photos to [Instagram](http://instagram.com) with Python!

This is inspired and roughly ported from the PHP implementation by
[Lance Newman](http://lancenewman.me/posting-a-photo-to-instagram-without-a-phone/).

Usage Example:

    filepath = "/tmp/square.jpg"
    print "Uploading " + filepath
    insta = InstagramSession()
    if insta.login(USERNAME, PASSWORD):
        media_id = insta.upload_photo("/tmp/small.jpg")
        print media_id
        if media_id is not None:
            insta.configure_photo(media_id, "")

Note that photos must be square to be uploaded. You can convert your
photo using ImageMagick with this command:

    convert -define jpeg:size=1280x1280 -resize 640x640^ \
        -extent 640x640 /tmp/original.jpg /tmp/square.jpg
