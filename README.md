# spectral_online_viewer
Web interactive visualiser for Specim IQ images, using Python and Flask

Uses Flask, as described in https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04 (archived in pdf in this repo)

The result is available at https://borec.fit.vutbr.cz/banany/?filenum=177&red_range=690.64%3B874.64&green_range=575.01%3B622.26&blue_range=397.32%3B452.25

Some features are:
1. remote retrieval of Specim RAW files
2. interactive setting of R, G, and B ranges
3. viewing multiple images
4. clicking a pixel in the image generates a graph of spectral responses at that location
5. scalable, fast, simple
6. shareable static URLs linking to a specific view of any image
