/**
 * Created by markdaniel on 10/29/15.
 */
'use strict';

angular.module('crimeCastApp.services', [])
    .factory('services', function ($location) {
        return {
            getMap: getMap,
            addMarker: addMarker,
            goToPath: goToPath
        }
        function getMap() {
            try {
                var map = new GMaps({
                    el: '.gmap',
                    zoom: 12,
                    lat: 30.280000,
                    lng: -97.740000
                });

                return map;
            }
            catch(err) {
                console.log('map not available: ', err);
            }
        }

        function addMarker(lat, lng, address, map, crime_type) {
            map.addMarker({
                lat: lat,
                lng: lng,
                title: address,
                click: function (e) {
                    alert('Alert:' + crime_type + ' at ' + address);
                }
            });
        }

        function goToPath(path, id) {
            $location.path('/' + path + '/' + id);
        }

    })