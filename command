import requests

#send the small data to the graphs


<URL> Global



r = requests.post('<URL>/users/<USER>/update/', data={'instantAverage':<value>, 'overallAverage':<value>})
r = requests.post('<URL>/users/<USER>/', data={'driving': <BOOL>})




"FALSE" <<NOT IMPLIMENTED YET>>
r = requests.post()




ADD USER not neccessary
r = requests.post('<URL>', data={'firstname': '<NAME>', 'lastname' : '<NAME>', 'age' : <AGE>})

