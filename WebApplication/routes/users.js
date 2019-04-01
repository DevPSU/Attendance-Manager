var express = require('express');
var router = express.Router();
var session = require('express-session');
var bodyParser = require('body-parser');


/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('respond with a resource');
});

router.get('/register', function(req, res, next) {
  res.render('register', {title:'Register'});
});

router.get('/login', function(req, res, next) {
  res.render('login',  {title:'Login'});
  if(auth){
    res.redirect('/');
  }
});

router.get('/dashboard',function(req, res, next) {
  console.log('Start of Get Courses API');
  //Get courses
  var unirest = require('unirest');
  unirest.get('http://cantaloupe-dev.us-east-1.elasticbeanstalk.com/courses')
  .headers({'Content-Type': 'application/json', 'Authorization' : 'Bearer ' + bearerToken})
  .end(function (response) {

    courses_count = response.body.count;
    courses = response.body.courses;
    res.render('dashboard', {title: 'Dashboard', user: auth, name: firstNameLogin, bearer: bearerToken, count: courses_count, course: courses});
  });
});

//--------------------------------------------- API REQUESTS ----------------------------------------------------


//--------------------------------------------- REGISTER ----------------------------------------------------
//Register POST
router.post('/register', function(req, res, next) {
  var fname = req.body.fname;
  var lname = req.body.lname;
  var email = req.body.email;
  var password = req.body.password;

  //For Validator
  req.checkBody('fname', 'First name field is required').notEmpty();
  req.checkBody('lname', 'Last name field is required').notEmpty();
  req.checkBody('email', 'Email is not valid').isEmail();
  req.checkBody('password', 'Password field is required').notEmpty();

  //Check errors
  var errors = req.validationErrors();

  if(errors){
    res.render('register',{
      errors: errors
    });
  }
  else{
     var request = require('request');

     request.post(
      'http://cantaloupe-dev.us-east-1.elasticbeanstalk.com/auth/register',
         { json: { first_name: fname, last_name: lname, email: email ,password: password } },
         function (error, response, body) {
             if (!error && response.statusCode == 200) {
                 console.log(body);
                 console.log(response.statusCode);

                 res.render('register',  {title:'Register', bool: false, booll: true, status: "Successful Register." });

                 //res.redirect('/users/login');
                 //res.end();
             }
             else{
              //Error code and response.
              console.log(response.statusCode);
              console.log(response.body);
              
              res.render('register',  {title:'Register', bool: true, booll:false, status: "Unsuccessful Register." });

              }
         }
     );
  }
});

//--------------------------------------------- LOGIN ----------------------------------------------------

//Login POST
router.post('/login', function(req, res, next) {

  var email = req.body.email;
  var password = req.body.password;

  //For Validator
  req.checkBody('email', 'Email is not valid').isEmail();
  req.checkBody('password', 'Password field is required').notEmpty();

  //Check errors
  var errors = req.validationErrors();

  if(errors){
    res.render('login',{
      errors: errors
    });
  }
  else{
     var request = require('request');

     request.post(
      'http://cantaloupe-dev.us-east-1.elasticbeanstalk.com/auth/login',
         { json: { email: email ,password: password } },
         function (error, response, body){
             if (!error && response.statusCode == 200) {

                 //Look into express sessions/cookies
                 auth = true;
                 bearerToken = body.bearer_token;
                 firstNameLogin = body.first_name;
                 
                 res.redirect('/users/dashboard');
                 res.end();
                }
             else{

                auth = false;
                firstNameLogin = null;
                bearerToken =  null;

                //Error code and response.
                //console.log(response.statusCode);
                //console.log(response.body);

                if(response.statusCode = 400)
                {
                  res.render('login',  {title:'Login', bool: true, booll:false, status: "400 BAD REQUEST Email or password are missing" });
                }
                else if(response.statusCode = 401){
                  res.render('login',  {title:'Login', bool: true, booll:false, status: "401 UNAUTHORIZED Email or password do not match" });
                }
                else if(response.statusCode = 422){
                  res.render('login',  {title:'Login', bool: true, booll:false, status: "422 UNPROCESSABLE ENTITY Email or password look invalid"});
                }
              }
         }
     );
    
  }
});

function getCourse(){
router.get('/dashboard', function getCourse(){
  console.log('Start of Get Courses API');
  //Get courses
  var unirest = require('unirest');
  unirest.get('http://cantaloupe-dev.us-east-1.elasticbeanstalk.com/courses')
  .headers({'Content-Type': 'application/json', 'Authorization' : 'Bearer ' + bearerToken})
  .end(function (response) {

    global.courses_count = response.body.count;
    global.courses = response.body.courses;
  });
})
}



//--------------------------------------------- LOGOUT ----------------------------------------------------


router.get('/logout',function(req, res){
  auth = false;
  bearerToken = null;
  req.logout();
  res.redirect('/users/login');
});


//--------------------------------------------- CREATE COURSE ----------------------------------------------------

//Create Course POST
router.post('/dashboard', function(req, res, next) {
  var addCourseName = req.body.addCourseName;
  var addOccurrence = req.body.addOccurrence;
  var addStartDate = req.body.addStartDate;
  var addEndDate = req.body.addEndDate;
  var addStartTime = req.body.addStartTime + ':00';
  var addEndTime = req.body.addEndTime + ':00';

  //For Validator
  req.checkBody('addCourseName', 'Course Name field is required').notEmpty();
  req.checkBody('addStartDate', 'Start Date field is required').notEmpty();
  req.checkBody('addEndDate', 'End Date is not valid').notEmpty();
  req.checkBody('addStartTime', 'Start Date field is required').notEmpty();
  req.checkBody('addEndTime', 'End Date field is required').notEmpty();

  //Check errors
  var errors = req.validationErrors();

  if(errors){
    res.render('/users/dashboard',{
      errors: errors
    });
  }
  else{
     var request = require('request');
     var bearerTkn = bearerToken;

     var unirest = require('unirest');
     unirest.post('http://cantaloupe-dev.us-east-1.elasticbeanstalk.com/courses/')
     .headers({'Content-Type': 'application/json', 'Authorization' : 'Bearer ' + bearerToken})
     .type('json')
     .send({
       name: addCourseName,
       start_time: addStartTime,
       end_time: addEndTime,
       start_date: addStartDate,
       end_date: addEndDate,
       days_of_week: addOccurrence
     })
     .end(function (response) {

       console.log(response.body);
       console.log(response.body.name);
       console.log(courses_count);
       res.redirect('/users/dashboard');
       //res.render('dashboard', {title: 'Dashboard', user: auth, name: firstNameLogin, bearer: bearerToken, count: global.courses_count, course: response.body.name});
       res.end();
      });
  }
});



module.exports = router;
