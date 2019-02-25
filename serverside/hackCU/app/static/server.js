const http = require('http');
const express = require('express');
var bodyParser = require('body-parser');
var unirest = require('unirest');
const MessagingResponse = require('twilio').twiml.MessagingResponse;

const app = express();
app.use(bodyParser.urlencoded({ extended: false }));

app.post('/sms', (req, res) => {
  const twiml = new MessagingResponse();

  twiml.message("Return..." + "\n" + "Phone: " + (req.body.From) + "\n" + "Message: " + (req.body.Body));

  res.writeHead(200, {'Content-Type': 'text/xml'});
  res.end(twiml.toString());

  unirest.post("https://twinword-emotion-analysis-v1.p.rapidapi.com/analyze/")
  .header("X-RapidAPI-Key", "878331264emsh6ad9c62465ed0dep17e346jsnf4718a718ab9")
  .header("Content-Type", "application/x-www-form-urlencoded")
  .send("text=" + req.body.Body + "")
  .end(function (result) {
    console.log(result.body.emotions_detected[0]);
  });
});

http.createServer(app).listen(1337, () => {
  console.log('Express server listening on port 1337');
});

