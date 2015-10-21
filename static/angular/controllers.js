'use strict';
crime_cast_app.controller('crime_cast_ctrl', function($scope) {

    var go_to_link = function(link) {
        //todo
    }

    var get_map = function() {
        try {
            var map = new GMaps({
                el: '.gmap',
                zoom: 12,
                lat: 30.280000,
                lng: -97.740000
            });
            map.addMarker({
                lat: 30.30000,
                lng: -97.730000,
                title: 'Quacks',
                click: function(e) {
                    alert('Alert: Burglary at Quacks Bakery.');
                }
            });

            map.addMarker({
                lat: 30.27000,
                lng: -97.7190000,
                title: '12th and Chicon',
                click: function(e) {
                    alert('Alert: Murder at 12th and Chicon.');
                }
            });

            map.addMarker({
                lat: 30.28500,
                lng: -97.7320000,
                title: 'GDC',
                click: function(e) {
                    alert('Alert: Graffiti on GDC.');
                }
            });
        }
        catch(err) {
                console.log(err.message);
            }
    }

    get_map();


    $scope.get_map = get_map();
    $scope.go_to_link = go_to_link;
});
