const accountSid = 'AC107dd89200d937d6c197b15e9ba2b840'
const authToken = '6a6eaf96aadae02d8c45bc364d88eccd'

const client = require('twilio')(accountSid, authToken);

client.messages.create({
  to: '+13032506161',
  from: '+17205752756',
  body: 'NAME has 3 strikes during this drive. Reply if you would like to send NAME a message.'
})
.then((message) => console.log(message.sid));
