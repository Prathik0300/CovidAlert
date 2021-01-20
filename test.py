import geocoder
g = geocoder.ip('me')
print(g.ip)
lat,lon = g.latlng[0], g.latlng[1]
