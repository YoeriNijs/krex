# KRex - The German Shepherd for computer forensics
A Python tool to search on every machine - fast! 

## Table of Contents
- [Use KRex](#use-krex)
- [Customize path location](#customize-path-location)
- [Supported operating systems](#supported-browsers)
- [Supported browsers](#supported-browsers)

## Install
Just install Python 3.x and the dependencies in `requirements.txt` by using the Pip package manager.

## Use KRex
Using KRex is pretty straightforward. Just create your own config file to search for applications and to take browser screenshots.

Example:
```
{
  "os": "mac",
  "apps": [
    {
      "name": "Slack",
      "fileName": "Slack.app",
      "locations": [
        "/Applications"
      ]
    }
  ],
  "browsers": [
    {
      "name": "safari",
      "urls": [
        {
          "name": "Twitter",
          "link": "https://www.twitter.com",
          "delay_in_ms": 5000
        }
      ]
    }
  ]
}
```

With the above configuration, KRex does two things. Primarily, it search for a Slack application in the `/Applications` dir. Next, it takes
a screenshot of Twitter with the browser safari. Easy as that.

### Customize path location
KRex is flexible though. For example, you can add a wildcard to a path location. The pattern is provided to the
Python glob library under the hood:

```
  "apps": [
    {
      "name": "Slack",
      "fileName": "Slack.app",
      "locations": [
        "~/**"
      ]
    }
  ]
```

### Supported operating systems
The following `os` values are supported:
- mac
- windows
- linux

While running, KRex checks which operating system is currently used by the host. It skips config files that are not related
to the current os automatically.

### Supported browsers
For a list of supported webbrowsers, visit: https://docs.python.org/3/library/webbrowser.html

