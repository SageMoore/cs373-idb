/**
 * Created by markdaniel on 10/29/15.
 */
'use strict';

angular.module('crimeCastApp.services', [])
    .factory('services', function () {
        return {
            getMap: getMap,
            addMarker: addMarker
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
                console.log(err.message);
            }
        }

        function addMarker(lat, lng, address, map) {
            map.addMarker({
                lat: lat,
                lng: lng,
                title: address,
                click: function (e) {
                    alert('Alert: Burglary at ' + address);
                }
            });
        }

    })