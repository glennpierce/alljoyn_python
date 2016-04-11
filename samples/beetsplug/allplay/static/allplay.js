var app = angular.module('AllPlayApp', ['ngRoute',
					                              'checklist-model',
                                        'ngCookies',
                                        'rzModule', 
                                        'angularUtils.directives.dirPagination'], function($interpolateProvider) {

    // set custom delimiters for angular templates
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

app.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/showtracks', {
        templateUrl: '/showtracks.html',
        controller: 'MainController'
      }).
      when('/showqueue', {
        templateUrl: '/showqueue.html',
        controller: 'QueueController'
      }).
      when('/showmetadata', {
        templateUrl: '/showmetadata.html',
        controller: 'MetaDataController'
      }).
      otherwise({
        redirectTo: '/showtracks'
      });
}]);

app.directive("audiotrack", function() {
    return {
      restrict: 'E',
        templateUrl: '/track.html',
        replace: true,
        scope: {itemObject: "=",
                onQueueAdd: "&",
                onTrackPlay: "&",
                onMetadataEdit: "&"}
    }
});


app.directive("queuetrack", function() {
    return {
      restrict: 'E',
        templateUrl: '/queuetrack.html',
        replace: true,
        scope: {itemObject: "=",
                onTrackPlay: "&",
                onQueueRemove: "&"}
    }
});

app.service("QueueService", function() {
     var self = this;
     this.items = [];

     this.length = function() {
         return self.items.length;
     };

     this.add = function(item) {
         return self.items.push(item);
     };

     this.prepend = function(item) {
         return self.items.unshift(item);
     };
});


app.service("MetaDataService", function() {
     var self = this;
     this.item = {};

     this.updateMetaData = function($http) {
        var parameters = {'item': this.item};
        var json_data = JSON.stringify(parameters);
        return $http({cache: false, url: '/update', method: 'post', data: json_data});
     };

     this.setItem = function(item) {
         return self.item = item;
     };
});


app.controller('MainController', ['$rootScope', '$scope', '$http', '$timeout',
                                   '$interval', '$location', '$cookies',
                                   'QueueService', 'MetaDataService',
                                   function($rootScope, $scope, $http, $timeout, $interval,
                                            $location, $cookies , QueueService, MetaDataService) {

  $scope.currentView = 'showtracks';  
  $scope.currentPage = 1;
  $scope.selectedItem = {'title':'ddd'};
  $scope.pageSize = 10;
  $scope.devices = [];
  $scope.queueService = QueueService;

  $scope.devicesChanged = function() {
      var parameters = {'selected_devices': $scope.selected_devices};
      var json_data = JSON.stringify(parameters);
      $http({cache: false, url: '/create_zone', method: 'post', data: json_data});
      $cookies.putObject('selected_devices', $scope.selected_devices);
  };

  $scope.selected_devices = $cookies.getObject('selected_devices');

  if($scope.selected_devices == undefined) {
    $scope.selected_devices = [];
  }

  $scope.changeView = function(view){
  	$location.path(view); // path not hash

    $scope.selectedItem.title = "faris";
  }

  $http({ cache: true, url: '/get_devices', method: 'GET'}).success(

      function (data, status, headers, config) {
        var devices = data['devices'];

         for (i = 0; i < devices.length; i++) { 

          if(devices[i].state == 'playing') {
              $scope.selected_devices.push(devices[i].id);
          }

          $scope.devices.push({
            device_id: devices[i].id,
            state: devices[i].state,
            name: devices[i].name,
            minValue: 0,
            maxValue: 100,
            value: devices[i].volume,
            options: {
              id: devices[i].id,
              floor: 0,
              ceil: 100,
              vertical: false,
              showTicksValues: false,
              onChange: function(id, value) {
                  
                  var parameters = {'device_id': id,
                                                 'volume': value};

                  var json_data = JSON.stringify(parameters);

                  return $http({cache: false, url: '/adjust_volume', method: 'post', data: json_data});
              },
            }
          }
          );
        };
      }
  );

  $http({ cache: true, url: '/tracks', method: 'GET'}).success(

      function (data, status, headers, config) {
         $scope.items = data['items'];
      }
  );

  $scope.stop = function() {

   return $http({cache: false, url: '/stop', method: 'get'});
  };

  $scope.pause = function() {
     return $http({cache: false, url: '/pause', method: 'get'});
  };

  $scope.play = function() {
     var parameters = {'queue': $scope.queueService.items};
     var json_data = JSON.stringify(parameters);
     return $http({cache: false, url: '/play', method: 'post', data: json_data});
  };

   // $scope.track_select = function(item) {
   //    $scope.queueService.add(item);
   //    var parameters = {'id': item.id,
   //                      'queue': $scope.queueService.items,
   //                      'position': $scope.queueService.length-1};
   //    var json_data = JSON.stringify(parameters);
   //    return $http({cache: false, url: '/play', method: 'post', data: json_data});
   // };

   $scope.toggle_queue = function() {
       if($scope.currentView == 'showqueue') {
           $scope.currentView = 'showtracks';
           $scope.changeView('showtracks');
       }
       else {
           $scope.currentView = 'showqueue';
           $scope.changeView('showqueue');
       }
   };

   $scope.speakers = function() {
        $("#wrapper").toggleClass("toggled");
   };
   
   $scope.track_add_to_queue = function(track_id) {
    $scope.queueService.add(track_id);
   };

   $scope.track_edit_metadata = function(track_item) {
       MetaDataService.setItem(track_item);
       $scope.currentView = 'showmetadata';
       $scope.changeView('showmetadata');
   };

}]);


app.controller('QueueController', ['$rootScope', '$scope', '$http', '$timeout', '$interval', '$location', 'QueueService',
                                   function($rootScope, $scope, $http, $timeout, $interval, $location, QueueService) {

  $scope.currentPage = 1;
  $scope.queueService = QueueService;

  $scope.track_play = function(track_id) {
     var parameters = {'track_id': track_id};
     var json_data = JSON.stringify(parameters);
     return $http({cache: false, url: '/playtrack', method: 'post', data: json_data});
  };

  $scope.remove_from_queue = function(track_id) {
    alert("remove");
  };

}]);


app.controller('MetaDataController', ['$rootScope', '$scope', '$http', '$timeout', '$interval',
                                      '$location', 'QueueService', 'MetaDataService',
                                   function($rootScope, $scope, $http, $timeout, $interval,
                                            $location, QueueService, MetaDataService) {

  $scope.item = MetaDataService.item;
  
  $scope.cancel_metadata = function(item) {
       $scope.changeView('showtracks');
  };

  $scope.apply_metadata = function(item) {
       console.log($scope.item);
       MetaDataService.updateMetaData($http);
  };

}]);
