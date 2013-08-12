Campfire Watcher
================
A simple script to watch a Campfire room for the appearance of strings.


Setup and Running
=================
Requires Camplight (http://mlafeldt.github.com/camplight)

```
pip install camplight
```

Rename ``settings_template.py`` to ``settings.py`` and update with your
personalized settings.

Once that's done you can run the watcher.

```
python watcher.py
```

This will sit in the background and every X seconds it will pull the most
recent messages from the room and notify you if one of your watch strings
appears. Notification is by way of a system alert (OS X only, I believe)
and print to screen.