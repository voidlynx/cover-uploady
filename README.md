# cover-uploady

reminder to create a `env.py` file next to `main.py`, and in it define a `SECRET` string and a `PORT` int. it can be whatever you want, you need to send the SECRET along with your request to upload the image in the POST req as a `secret` parameter.

i'll probably write a better readme some day. if you use this in prod not for personal purposes -- you will be shot on sight.

also you probably would want to run this with a WSGI thing too. that's not within my realm of responsibilities.

this is prod-ready so check out the `main.py` file if you need to comment anything out

be-fucking-ware! discord permanently caches the images for given links in RPC sooo until i push out an update to randomly generate IDs -- shit's fucked! i'm personally stuck with the cover art for Dead Poet Society - FISSION.

oh yeah and i guess if you're structuring a request it should look something like this (using the `requests` library):

```py
data = requests.post(
    "https://cover.example.com/upload",
    data = { "secret": env.SECRET },
    files = { "image": requests.get(url).content }
).json()
if "message" not in data:
    raise Exception(data["error"])
```

where env.SECRET is the secret string and the image thing is an image as bytes. hopefully jpg.

TODO: image resizing and converting (256x256), random ID generation for links to bypass discord caching 