'use strict';
crime_cast_app.controller('crime_cast_ctrl', function($scope) {

    var go_to_link = function(link) {
        //todo
    }

    var get_map = function() {
        try {
            console.log('getting map')
            var map = new GMaps({
                el: '.gmap',
                zoom: 11,
                lat: 30.250000,
                lng: -97.750000
            });
            console.log(map);
        }
        catch(err) {
                console.log(err.message);
            }
    }

    get_map();


    $scope.get_map = get_map();
    $scope.go_to_link = go_to_link;
});
