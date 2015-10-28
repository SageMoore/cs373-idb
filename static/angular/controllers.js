'use strict';
crimeCastApp.controller('crimeCastCtrl', function($scope, rest) {

    var getCrimes = function() {
        rest.getRequestGeneric('crimes').then(function(data) {
            console.log('data for crimes is: ', data)
        })
    }

    getCrimes();

    var goToLink = function(link) {
        //todo
    }

    var getMap = function() {
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

    var loadAllWidgets = function() {
        !function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");
    };

    var destroyAllWidgets = function() {
        var $ = function (id) { return document.getElementById(id); };
        var twitter = $('twitter-wjs');
        if (twitter != null)
            twitter.remove();
    };

    getMap();
    destroyAllWidgets();
    loadAllWidgets();

    $scope.getMap = getMap();
    $scope.goToLink = goToLink;

    $scope.sortType     = 'id'; // set the default sort type
    $scope.sortReverse  = false;  // set the default sort order
    $scope.crimetypes = [
        { id: 2, crime_type: 'Burglary', description: "Burglary is bad", "crimes" : [{"id":2},{"id":2},{"id":2}], worst_zipcode: "78705" },
        { id: 1, crime_type: 'Assault', description: "Assault is bad", "crimes" : [{"id":3}], worst_zipcode: "78704" },
        { id: 3, crime_type: 'Vandalism', description: "Vandalism is bad", "crimes" : [{"id":1}], worst_zipcode: "78706" }
    ];
    $scope.zipcodes = [
        { id: 1, zipcode: 78704, latitude: 32.123,longitude: 32.123, "crimes" : [{"id":1}]  },
        { id: 2, zipcode: 78705, latitude: 30.123,longitude: 30.123, "crimes" : [{"id":2}]  },
        { id: 3, zipcode: 78706, latitude: 35.123,longitude: 35.123, "crimes" : [{"id":3}]  }
    ];
    $scope.weeks = [
        { id: 1, start_date: "10/11/15", end_date: "10/17/15",popular_crime: "1", "crimes" : [{"id":1}]  },
        { id: 2, start_date: "10/18/15", end_date: "10/24/15",popular_crime: "2", "crimes" : [{"id":2}]  },
        { id: 3, start_date: "10/25/15", end_date: "10/31/15",popular_crime: "3", "crimes" : [{"id":3}]  },
    ];
    $scope.crimes = [
        { id: 1, description: "Graffiti of pig on building", time: "10-20-2015 19:12:00" ,address: "GDC", "crime_type" : 3  },
        { id: 2, description: "Burglary at Quacks Bakery", time: "10-20-2015 19:20:00" ,address: "Duval Rd", "crime_type" : 2  },
        { id: 3, description: "Murder on 12th and Chicon", time: "10-20-2015 22:20:00" ,address: "12th and Chicon", "crime_type" : 1  }
    ];
});
