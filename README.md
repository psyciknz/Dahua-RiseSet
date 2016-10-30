# Dahua-RiseSet

Sets the switch over from day time to night time bases on 15 mins (offset) from sunrise/sunset based on your location.

Sign up to OpenWeatherMap and generate an new API key: https://home.openweathermap.org/api_keys

Update the location, by taking the search terms then using the city ID in the url, eg for Wellington,NZ the iD is 2179537 (http://openweathermap.org/city/2179537)

Update the names of the cameras (or IPs) in the server list.  And if you have an NVR just put in a single IP, and update the channel numbers.

It can't currently have both and NVR and single cameras, or it might, but I've not tested what would happen if it tries to look at a single camera and tries to update more that one channel, it may just skip over the non existent channel.

Also at the moment all cameras must have a common username/password.



