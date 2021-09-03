import _ from 'lodash';

function component() {
   var element = document.createElement('div')
   element.innerHTML = _.join(['Hello','world','!!'], ' ');

   return element;
}

document.body.appendChild(component());

/* ********************OL************************* */
//import 'ol/ol.css';
import {Map, View} from 'ol';
//import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import Feature from 'ol/Feature';
//import Map from 'ol/Map';
import Overlay from 'ol/Overlay';
import Point from 'ol/geom/Point';
import TileJSON from 'ol/source/TileJSON';
import VectorSource from 'ol/source/Vector';
//import View from 'ol/View';
import {Icon, Style, Circle as CircleStyle, Fill, Stroke,} from 'ol/style';
import {Tile as TileLayer, Vector as VectorLayer} from 'ol/layer';

import GPX from 'ol/format/GPX';

import {useGeographic} from 'ol/proj';

useGeographic();


////////////////////////////////////
var style = {
  'Point': new Style({
    image: new CircleStyle({
      fill: new Fill({
        color: 'rgba(255,255,0,0.4)',
      }),
      radius: 5,
      stroke: new Stroke({
        color: '#ff0',
        width: 1,
      }),
    }),
  }),
  'LineString': new Style({
    stroke: new Stroke({
      color: '#f00',
      width: 3,
    }),
  }),
  'MultiLineString': new Style({
    stroke: new Stroke({
      color: '#c008cc',
      width: 3,
    }),
  }),
};

var gpxLayer = new VectorLayer({
  source: new VectorSource({
    url: 'static/data/track_harz.gpx',
    format: new GPX(),
  }),
  style: function (feature) {
    return style[feature.getGeometry().getType()];
  },
});


////////////////////////////////////
var baselayer = new TileLayer({
    source: new OSM()
    });

var iconFeature = new Feature({
    geometry: new Point([0, 0]),
    name: 'Null Island',
    population: 4000,
    rainfall: 500,
    });
  var newIconFeature = new Feature({
    geometry: new Point([9, 51]),
    name: 'hesse Island',
    population: 4000,
    rainfall: 500,
    });

var vectorSource = new VectorSource({
    features: [iconFeature, newIconFeature],
    });

var vectorLayer = new VectorLayer({
    source: vectorSource,
    });

const map = new Map({
  target: 'map',
  layers: [
  baselayer, vectorLayer, gpxLayer
  ],
  view: new View({
    center: [9, 50],
    zoom: 5
  })
});

map.on('singleclick', function (evt) {
  console.log(evt.coordinate);
  var xy = evt.coordinate;
//  console.log(xy);
  $.getJSON({
    url: `/savePoint/${xy[0]}/${xy[1]}/${$("#pointName").val()}/`,
    success: data => {
        console.log(data);
        location.reload();
    }
  }).error(function(jqXHR, textStatus, errorThrown) {
      console.log("error " + textStatus);
      console.log("incoming Text " + jqXHR.responseText);
  });
});

//////////////////////////////////////////////////// 
/*
var dict = {typename : "test" , content:"irgendwas"};

    $.ajax({
        type: "POST", 
        url: "http://192.168.3.45:2100/saveMyJson", //localhost Flask
        data : JSON.stringify(dict),
        contentType: "application/json",
    });
*/