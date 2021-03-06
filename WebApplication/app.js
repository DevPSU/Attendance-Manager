//FORK & PULL 4/3/19 
var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var passport = require('passport');
var expressValidator = require('express-validator');
var bodyParser = require('body-parser');

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

//Passport - Authentication
app.use(passport.initialize());
app.use(passport.session());

auth = false;
firstNameLogin = null;
bearerToken =  null;
courses_count = null;
courses = null;
getCourse();


//Validator
app.use(expressValidator({
  errorFormatter: function(param,msg,value){
    var namespace = param.split('.')
    , root =namespace.shift()
    , formParam = root;

    while(namespace.length){
      formParam += '[' + namespace.shift()
    }
    return{
      param: formParam,
      msg: msg,
      value: value
    };
  }
}));

app.use(require('connect-flash')());
app.use(function (req, res, next) {
  res.locals.messages = require('express-messages')(req, res);
  next();
});

app.use('/', indexRouter);
app.use('/users', usersRouter);

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


function getCourse(){
  console.log('Start of Get Courses API');

  //Get courses
  var unirest = require('unirest');
  unirest.get('http://cantaloupe-dev.us-east-1.elasticbeanstalk.com/courses')
  .headers({'Content-Type': 'application/json', 'Authorization' : 'Bearer ' + bearerToken})
  .end(function (response) {

    global.courses_count = response.body.count;
    global.courses = response.body.courses;

    //console.log(courses_count);
   // console.log(courses);
    //res.render('dashboard', {title: 'Dashboard', user: auth, name: firstNameLogin, bearer: bearerToken, count: courses_count, course:courses});
    //res.end();
  });
}


module.exports = app;
