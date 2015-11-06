'use strict';
crimeCastApp.controller('crimeCastCtrl', function($scope, services, http_service) {

    services.getMap();

    $scope.sortType     = 'id'; // set the default sort type
    $scope.sortReverse  = false;  // set the default sort order

}).controller('crimesCtrl', function ($scope, http_service, services, $location) {

    var map = services.getMap();

    var loadAllWidgets = function() {
        !function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");
    };

    var destroyAllWidgets = function() {
        var $ = function (id) { return document.getElementById(id); };
        var twitter = $('twitter-wjs');
        if (twitter != null)
            twitter.remove();
    };

    destroyAllWidgets();
    loadAllWidgets();


    var getCrimes = function() {
        http_service.getRequestGeneric('crimes').then(function(data) {
            console.log('data for crimes is...: ', data);
            $scope.crimes = data;
            angular.forEach($scope.crimes, function(value, key) {
                services.addMarker(value.lat, value.lng, value.address, map, value.crime_type.crime_type_name);
            })
        })
    }

    $scope.crimes = getCrimes();

}).controller('crimeCtrl', function ($scope, http_service, $location, $stateParams, services) {

    var crimeId = $stateParams.crimeId;

    var map = services.getMap();

    var getCrime = function(crimeId) {
        http_service.getCrime(crimeId).then(function(data) {
            $scope.crime = data;
            services.addMarker(data.lat, data.lng, data.address, map, data.crime_type.crime_type_name);
        })
    }

    $scope.crime = getCrime(crimeId);

}).controller('crimeTypesCtrl', function ($scope, http_service, services, $location) {

    var map = services.getMap();

    var getCrimeTypes = function() {
        http_service.getRequestGeneric('crime_types').then(function(data) {
            $scope.crimeTypes = data;
            console.log('data for crimetypes is...: ', data);
        })
    };

    var goToCrimeType = function (crimeId) {
        $location.path('/crime_types/' + crimeId);
    };

    $scope.crimeTypes = getCrimeTypes();
    $scope.goToCrimeType = goToCrimeType;

}).controller('crimeTypeCtrl', function ($scope, http_service, $location, $stateParams, services) {

    var crime_type_id = $stateParams.crime_type_id;
    var map = services.getMap();

    var getCrimeType = function(crime_type_id) {
        http_service.getCrimeType(crime_type_id).then(function(data) {
            $scope.crime_type = data;
            console.log('data for crime type is ', data)
            angular.forEach($scope.crime_type.crimes, function(value, key) {
                services.addMarker(value.lat, value.lng, value.address, map, value.crime_type.crime_type_name);
            })
        })
    };

    $scope.crime_type = getCrimeType(crime_type_id);

}).controller('weeksCtrl', function ($scope, http_service, services, $location) {

    var map = services.getMap();

    var getWeeks = function() {
        http_service.getRequestGeneric('weeks').then(function(data) {
            $scope.weeks = data;
            console.log('data for weeks is...: ', data);
        })
    };

    var goToWeek = function (weekId) {
        $location.path('/weeks/' + weekId);
    };

    $scope.weeks = getWeeks();
    $scope.goToWeek = goToWeek;

}).controller('weekCtrl', function ($scope, http_service, $location, $stateParams, services) {

    var week_id = $stateParams.week_id;
    var map = services.getMap();

    var getWeek = function(week_id) {
        http_service.getWeek(week_id).then(function(data) {
            $scope.week = data;
            angular.forEach($scope.week.crimes, function(value, key) {
                services.addMarker(value.lat, value.lng, value.address, map, value.crime_type.crime_type_name);
            })
        })
    };

    $scope.week = getWeek(week_id);

}).controller('zipsCtrl', function ($scope, http_service, services, $location) {

    var map = services.getMap();

    var getZips = function() {
        http_service.getRequestGeneric('zips').then(function(data) {
            $scope.zips = data;
            console.log('data for zips is...: ', data);
        })
    };

    var goToZip = function (zipId) {
        $location.path('/zips/' + zipId);
    };

    getZips();
    $scope.goToZip = goToZip;

}).controller('zipCtrl', function ($scope, http_service, $location, $stateParams, services) {

    var zip_id = $stateParams.zip_id;
    var map = services.getMap();

    var getZip = function(zip_id) {
        http_service.getZip(zip_id).then(function(data) {
            $scope.zip = data;
            angular.forEach($scope.zip.crimes, function(value, key) {
                services.addMarker(value.lat, value.lng, value.address, map, value.crime_type.crime_type_name);
            })
        })
    };

    $scope.zip = getZip(zip_id);

}).controller('aboutCtrl', function ($scope, http_service, $location, $stateParams) {
    $scope.results = "No test results yet..."

    $scope.runTests = function() {
        http_service.getRequestGeneric('tests').then(function(data) {
            alert("Running tests...")
            $scope.results = data.results;
        })
    };
});