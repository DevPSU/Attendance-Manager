var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var indexRouter = require('./routes/index');
var professorRouter = require('./routes/professor');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/professor', professorRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

//Canvas API
var request = require('request');

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

module.exports = app;
