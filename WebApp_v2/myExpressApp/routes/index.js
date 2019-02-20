var express = require('express');
var router = express.Router();

//Canvas API
var request = require('request');

//https://canvas.instructure.com/api/v1/users/self?access_token=1050~Biow0L05eLcKJoU85ZGCpM8OQOP6NGAJSACxmdbMpGoo65DNXkmJp9XDRWz0L8Os

//Get User Information
request('https://canvas.instructure.com/api/v1/users/self?access_token=1050~Biow0L05eLcKJoU85ZGCpM8OQOP6NGAJSACxmdbMpGoo65DNXkmJp9XDRWz0L8Os', function (error, response, body) {
    console.log('error:', error); // Print the error if one occurred
    console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
  
    var json = body;
    var obj = JSON.parse(json);
    var userName = obj.short_name;
    var nameID = obj.id;
  });

//Daniel Key 1050~dCUSyFl3enAcT1n1NUjacpns9t5kZiGWnGo4Qa3UlqjzLrlQJtWTcIapyv2W5MLM

//Get Course Information
request('https://canvas.instructure.com/api/v1/courses?access_token=1050~Biow0L05eLcKJoU85ZGCpM8OQOP6NGAJSACxmdbMpGoo65DNXkmJp9XDRWz0L8Os', function (error, response, body) {
  console.log('error:', error); // Print the error if one occurred
  console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received

  var json = body;
  var obj = JSON.parse(json);
  courses = new Array();
  coursesID = new Array();

  for (i = 0; i < obj.length; i++) { 
    var str = "";
    str = obj[i].name;
    var arr = str.split(':');
    courses.push(arr[0]);
    coursesID.push(obj[i].id);
    console.log(courses[i]);
  }
});

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', {
     title: 'BluCantaloupe', 
     course: courses, 
     courseID: coursesID,
     name: "userName"
  });
});

module.exports = router;
