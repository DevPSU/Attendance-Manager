var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/',function(req, res, next) {
  res.render('index', {title: 'Members', user: auth, name: firstNameLogin, bearer: bearerToken});
  //res.render('index', {title: 'Members', user: auth});
});



module.exports = router;
