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

// Use the session middleware
/*router.use(session({ secret: 'mySecret_FruitSession', cookie: { maxAge: (1000*60)*30 }}))

// Access the session as req.session
router.get('/dashboard', function(req, res, next) {
  if (req.session.views) {
    req.session.views++
    res.setHeader('Content-Type', 'text/html')
    res.write('<p>views: ' + req.session.views + '</p>')
    res.write('<p>expires in: ' + (req.session.cookie.maxAge / 1000) + 's</p>')
    res.end()
    console.log(res.session.view);
  } else {
    req.session.views = 1
    res.end('welcome to the session demo. refresh!')
  }
})*/


router.get('/dashboard',function(req, res, next) {
  res.render('dashboard', {title: 'Dashboard', user: auth, name: firstNameLogin, bearer: bearerToken});
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
         function (error, response, body) {
             if (!error && response.statusCode == 200) {
                 //console.log(body);
                 //console.log(body.bearer_token);
                 //console.log(body.first_name);
                
                 //Look into express sessions/cookies
                 auth = true;
                 bearerToken = body.bearer_token;
                 firstNameLogin = body.first_name;

                 res.redirect('/users/dashboard');

                 console.log('Start of Get Courses API');

                  //Get courses

                  /*var request = require("request");

                  var options = { method: 'GET',
                    url: 'http://cantaloupe-dev.us-east-1.elasticbeanstalk.com/courses',
                    headers: {'Authorization': bearerToken }};
                  
                  request(options, function (error, response, body) {
                    if (error) throw new Error(error);
            
                    console.log(body);
                    console.log(bearerToken);
                  });*/

                  var unirest = require('unirest');
                  unirest.get('http://cantaloupe-dev.us-east-1.elasticbeanstalk.com/courses')
                  .headers({'Content-Type': 'application/json', 'Authorization': bearerToken})
                  .end(function (response) {
                    console.log(response.body);
                  });

                  /*request.get({url:'http://cantaloupe-dev.us-east-1.elasticbeanstalk.com/courses',
                  headers:{'Authorization': 'Bearer ' + bearerToken}
                },      
                  function (error, response, body) {
                    if (!error && response.statusCode == 200) {
                      console.log(body);
                      console.log(response.statusCode);
                      res.end();
                    }
                    else{
                      console.log(body);
                      //console.log(response);
                      res.end();
                    }
                  });*/

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
  var addStartTime = req.body.addStartTime;
  var addEndTime = req.body.addEndTime;

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

    request.post(
      'http://cantaloupe-dev.us-east-1.elasticbeanstalk.com/courses/',
      { json: 
        {
          name: addCourseName,
          days_of_week: addOccurrence, 
          start_time: addStartDate, 
          end_time: addEndDate,
          start_date: addStartTime, 
          end_date: addEndTime 
        },
        'auth':
        {
          'Bearer': bearerTkn
        }
      },
      function (error, response, body) {
        if (!error && response.statusCode == 200) {
          console.log(body);
          console.log(response.statusCode);
          res.end();
        }
        else{
          console.log(body);
          console.log(error);
          res.end();
        }
      }
     );
  }
});



module.exports = router;
