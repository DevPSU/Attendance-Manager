var express = require('express');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('respond with a resource');
});

router.get('/register', function(req, res, next) {
  res.render('register', {title:'Register'});
});

router.get('/login', function(req, res, next) {
  res.render('login',  {title:'Login'});
});


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

                 res.render('register',  {title:'Register', bool: false, booll: true, status: "Successful login." });

                 res.location('/login');
                 res.redirect('/login');
             }
             else{
              //Error code and response.
              console.log(response.statusCode);
              console.log(response.body);
              
              res.render('register',  {title:'Register', bool: true, booll:false, status: "Unsuccessful login." });

              }
         }
     );
  }
});

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
                 console.log(body);
                 console.log(body.bearer_token);
                 console.log(body.first_name);
                
                 //Look into express sessions/cookies
                 auth = true;
                 bearerToken = body.bearer_token;

                 //res.render('login',  {title:'Login', user: true, bool: false, booll:true, status: "Successful Login" });
                 res.render('index', {title: 'Members', user: auth, name: body.first_name, bearer: body.bearer_token});
                 //res.redirect('/')
             }
             else{

                auth = false;

                //Error code and response.
                console.log(response.statusCode);
                console.log(response.body);

                if(response.statusCode = 400)
                {
                  res.render('login',  {title:'Login', bool: true, booll:false, status: "400 BAD REQUEST Email or password are missing" });
                }
                else if(response.statusCode = 401){
                  res.render('login',  {title:'Login', bool: true, booll:false, status: "401 UNAUTHORIZED Email or password do not match" });
                }
                else if(response.statusCode = 422){
                  res.render('login',  {title:'Login', bool: true, booll:false, status: "422 UNPROCESSABLE ENTITY Email or password look invalid" });
                }
              }
         }
     );
  }
});

router.get('/logout',function(req, res){
  req.logout();
  res.redirect('/users/login');
});


//Create Course POST
router.post('/', function(req, res, next) {
  //var addCourseName = req.body.addCourseName;
  //var addOccurrence = req.body.addOccurrence;
  //var addStartDate = req.body.addStartDate;
  //var addEndDate = req.body.addEndDate;
  //var addStartTime = req.body.addStartTime;
  //var addEndTime = req.body.addEndTime;

  //console.log(addOccurrence);
  console.log(bearerToken);
  /*
  //For Validator
  req.checkBody('addCourseName', 'Course Name field is required').notEmpty();
  req.checkBody('addStartDate', 'Start Date field is required').notEmpty();
  req.checkBody('addEndDate', 'End Date is not valid').notEmpty();
  req.checkBody('addStartTime', 'Start Date field is required').notEmpty();
  req.checkBody('addEndTime', 'End Date field is required').notEmpty();

  //Check errors
  var errors = req.validationErrors();

  if(errors){
    res.render('/',{
      errors: errors
    });
  }
  else{
     var request = require('request');
     console.log(bearerToken);
    

    /*var b = b ;
     const options = {  
      url: 'http://cantaloupe-dev.us-east-1.elasticbeanstalk.com/courses/',
      method: 'POST',
      headers: {
          'Accept': 'application/json',
          'Accept-Charset': 'utf-8',
          'Authorization': 'Bearer' 
      }
  };
  
  request(options, function(err, res, body) {  
      let json = JSON.parse(body);
      console.log(json);
  });*/

     /*request.post(
      'http://cantaloupe-dev.us-east-1.elasticbeanstalk.com/courses/',
         { json: { name: addCourseName, days_of_week: addOccurrence, start_time: addStartDate , end_time: addEndDate, start_date: addStartTime , end_date: addEndTime } },
         function (error, response, body) {
             if (!error && response.statusCode == 200) {
                 console.log(body);
                 console.log(response.statusCode);

                 //res.render('register',  {title:'Register', bool: false, booll: true, status: "Successful login." });

                 //res.location('/login');
                 //res.redirect('/login');
             }
             else{
              //Error code and response.
              console.log(response.statusCode);
              console.log(response.body);
              
              //res.render('register',  {title:'Register', bool: true, booll:false, status: "Unsuccessful login." });

              }
         }
     );
}*/
});



module.exports = router;
