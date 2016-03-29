var app = angular.module('AllPlayApp', ['checklist-model'], function($interpolateProvider) {

    // set custom delimiters for angular templates
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});


app.controller('MainController', ['$rootScope', '$scope', '$http', '$timeout', '$interval', 
                                   function($rootScope, $scope, $http, $timeout, $interval) {

  $http({ cache: true, url: '/get_devices', method: 'GET'}).success(

      function (data, status, headers, config) {
         $scope.devices = data;
      }
  );

  $scope.selected = []
  $scope.uri = 'http://192.168.1.149:8882/static/test.mp3'

  $scope.run = function() {

      var parameters = {'selected_devices': $scope.selected.devices,
                                    'uri': $scope.uri};

      var json_data = JSON.stringify(parameters);

      console.log(json_data);

      return $http({cache: false, url: '/run', method: 'post', data: json_data}).success(

        function (data, status, headers, config) {
           
        }
      );
   };

   $scope.stop = function() {

    return $http({cache: false, url: '/stop', method: 'get'}).success(

      function (data, status, headers, config) {
         
      }
    );
   };

   $scope.pause = function() {

    return $http({cache: false, url: '/pause', method: 'get'}).success(

      function (data, status, headers, config) {
         
      }
    );
   };

}]);
