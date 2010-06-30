     _  _                               _     _
  __| |(_) __ _ _ __   __ _  ___       | |__ | | ___   __ _  __ _  ___ _ __
 / _` || |/ _` | '_ \ / _` |/ _ \ _____| '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
| (_| || | (_| | | | | (_| | (_) |_____| |_) | | (_) | (_| | (_| |  __/ |
 \__,_|/ |\__,_|_| |_|\__, |\___/      |_.__/|_|\___/ \__, |\__, |\___|_|
     |__/             |___/                           |___/ |___/

A Google Blogger to Django linking app    Jaymz Campbell    http://jaymz.eu/


Overview
========

This application allows you to plug in an existing set of Blogger blogs to
your django application. It does not require authentication, it works off
pulling in the RSS feeds from blogger. You can enable this for your blogs
within the admin.

Installation
============

Add "blogger" to your installed app's and add in the following URL conf:

    (r'^blogs/', include('blogger.urls', namespace='blogger'))

To quickly import all blogs for a user add a new BloggerUser and paste in
the blogger id. You can find that in the URL for your profile. There is
an admin action to create new blogs for users. When you have created your
blogs there is another action to sync up the posts with blogs.

Please note that as this uses the RSS feed it does not download the entire
blog archive. The point for this app is to link in to a blog from a current
point.


