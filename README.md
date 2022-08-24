# nibe_mqtt

Communication service between the Nibe uplink and MQTT

# Nibe Uplink Communication Module

## Description

The module is an asyncio driven interface to nibe uplink public API. It is throttled to one http request every 4 seconds so
try to make the most of your requests by batching requests.

## Info

Thanks to Joakim for the Nibe Uplink API module: https://github.com/elupus/nibeuplink

And thanks to David for the very good background information / howto page about how to use the Nibe Uplink API: 
https://www.marshflattsfarm.org.uk/wordpress/?page_id=3480

## Installing this module

```
$ git clone https://github.com/wooni005/nibeuplink.git
$ cd nibeuplink
$ sudo pip3 install .
```

## Authorisation

Read this first: https://www.marshflattsfarm.org.uk/wordpress/?page_id=3480

### In short

**Step 1** - Register your application on: https://api.nibeuplink.com/
 You can use my VPS for callback URL: http://firm-ware.cz/oauth2callback/index.php

**Step 2** - Get an Authorization Code, fill in your Nibe Uplink API Identifier instead of **[Identifier]**
https://api.nibeuplink.com/oauth/authorize?response_type=code&client_id=9b1e683e2c904adfb52313b4a327b634&scope=READSYSTEM&redirect_uri=https://firm-ware.cz/oauth2callback/index.php&state=STATE

You will be redirected to something like http://firm-ware.cz/oauth2callback/index.php?code=<key>

This **redirect URL** will be used in the next step!

**Step 3** - Start the nibeuplink tool, which is already installed above

```
$ nibeuplink --client_id 'XXX' --client_secret 'YYY' --redirect_uri 'ZZZ'
https://api.nibeuplink.com/oauth/authorize?response_type=code&client_id=XXX&redirect_uri=https%3A%2F%2Ffirm-ware.cz%2Foauth2callback%2Findex.php&scope=READSYSTEM&state=38bd51b4aedb446c9090b80bbdbbcbf0
Enter full redirect url: 
```

* client_id:
  
  NIBE Uplink API: Identifier

* client_secret:
  
  NIBE Uplink API: Secret

* redirect_uri:
  
  NIBE Uplink API: Callback URL

When you get the prompt `Enter full redirect url:`

Enter here the **redirect URL** from step 2, but **WITHOUT** the last part `&state=STATE`

The authorisation keys will be stored in the "nibeuplink.json" in the current directory. This will be used for the next time if you start the nibeuplink tool or the next code example.

## Code example

Here is a working code example: https://github.com/wooni005/nibeuplink/blob/master/example.py

## Command line

The module contains a commandline tool to test and request data from Nibe Uplink called ``nibeuplink``, it will store token information in a file in the current directory called nibeuplink.json

## Nibeuplink tool examples

Help for utility

``` $ nibeuplink -h```

Request all systems

```$ nibeuplink --client_id 'XXX' --client_secret 'YYY' --redirect_uri 'ZZZ'```

Request data for specific system

```$ nibeuplink --client_id 'XXX' --client_secret 'YYY' --redirect_uri 'ZZZ' --system 12345```

Request data for outside temp

```$ nibeuplink --client_id 'XXX' --client_secret 'YYY' --redirect_uri 'ZZZ' --system 12345 --parameter 40004```

```
### Callback PHP script on my VPS

URL: firm-ware.cz/oauth2callback/index.php
```

<?php
// oauth2callback/index.php

echo "https://firm-ware.cz/oauth2callback/index.php";
echo "OAuth2 Callback Script<br>";

if ( isset( $_GET['code'] ) ) {
    echo "Parameter 'code' found, value is: ";
    $code = $_GET['code'];
    echo "$code<br>";
} else {
    echo "Parameter 'code' not found<br>";
}

if ( isset( $_GET['state'] ) ) {
    echo "Parameter 'state' found, value is: ";
    $state = $_GET['state'];
    echo "$state<br>";
}

if ( isset( $_GET['error'] ) ) {
    $error = $_GET['error'];
    echo $error;
}

?>

```

```