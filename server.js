// Load required packages
var express = require('express');

// Create our Express application
var app = express();

// Add static middleware
app.use(express.static(__dirname + '/public'));

// Create our Express router
var router = express.Router();

// Initial dummy route for testing
router.get('/', function(req, res) {
  res.end('Sucess');
});

// Register all our routes
app.use(router);

// Start the server
app.listen(3000);

